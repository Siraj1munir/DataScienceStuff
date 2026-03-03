import os
import ipaddress
import re
import socket
from urllib.parse import urlparse

import requests


_ALLOWED_URL_SCHEMES = {"http", "https"}
_ALLOWED_PORTS = {80, 443}
_MAX_DOWNLOAD_BYTES = 10 * 1024 * 1024  # 10 MiB

# Google Images typically serves actual image content from a limited set of
# hosts; we keep this conservative on purpose.
_ALLOWED_IMAGE_HOST_SUFFIXES = (
    "googleusercontent.com",
    "gstatic.com",
    "ggpht.com",
)


def _is_public_ip(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    return ip.is_global


def _is_public_host(hostname: str) -> bool:
    try:
        infos = socket.getaddrinfo(hostname, None)
    except OSError:
        return False

    for family, *_rest, sockaddr in infos:
        ip_str = sockaddr[0]
        if not _is_public_ip(ip_str):
            return False
    return True


def _is_allowed_image_host(hostname: str) -> bool:
    return any(
        hostname.endswith(suffix)
        for suffix in _ALLOWED_IMAGE_HOST_SUFFIXES
    )


def _http_get(url: str, **kwargs):
    """
    Thin wrapper around requests.get so that all outbound HTTP
    goes through a single, controlled call site.
    """
    return requests.get(url, **kwargs)


def download_limited_image(raw_url: str) -> bytes:
    """
    Fetch an image over HTTP(S) with strict SSRF safeguards:
    - only http/https
    - only public IPs
    - only known image host suffixes
    - only ports 80/443
    - bounded body size
    """
    parsed = urlparse(raw_url)
    scheme = parsed.scheme.lower()
    if scheme not in _ALLOWED_URL_SCHEMES:
        raise ValueError("Only http/https URLs are allowed")
    if not parsed.hostname:
        raise ValueError("URL must include a hostname")

    hostname = parsed.hostname.lower()
    if not _is_allowed_image_host(hostname):
        raise ValueError("Host not in allowed image host list")

    port = parsed.port or (443 if scheme == "https" else 80)
    if port not in _ALLOWED_PORTS:
        raise ValueError("Only ports 80/443 are allowed")
    if not _is_public_host(hostname):
        raise ValueError("Refusing to fetch from non-public host")

    safe_url = parsed.geturl()
    headers = {"User-Agent": "DataScienceStuff-image-scraper/1.0"}
    with _http_get(
        safe_url,
        headers=headers,
        timeout=(5, 20),
        allow_redirects=False,
        stream=True,
    ) as resp:
        resp.raise_for_status()
        chunks = []
        size = 0
        for chunk in resp.iter_content(chunk_size=64 * 1024):
            if not chunk:
                continue
            size += len(chunk)
            if size > _MAX_DOWNLOAD_BYTES:
                raise ValueError("Download too large")
            chunks.append(chunk)
        return b"".join(chunks)


_FILENAME_SAFE_RE = re.compile(r"[^A-Za-z0-9._-]")
_CORRECTED_DIR = "corrected_files"


def safe_corrected_path(original_name: str) -> str:
    """
    Build a filesystem path for corrected spell-check output:
    - strips directories
    - normalises to a small safe character set
    - prefixes with 'corrected_'
    - always writes inside 'corrected_files' folder
    """
    base = os.path.basename(original_name) or "output.txt"
    base = _FILENAME_SAFE_RE.sub("_", base)
    safe_name = f"corrected_{base}"

    os.makedirs(_CORRECTED_DIR, exist_ok=True)
    return os.path.join(_CORRECTED_DIR, safe_name)

