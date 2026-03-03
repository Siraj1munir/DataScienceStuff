import selenium
from selenium import webdriver
import time
import requests
import os
from PIL import Image
import io
import hashlib
import ipaddress
import socket
from urllib.parse import urlparse

# All in same directory
DRIVER_PATH = 'chromedriver.exe'

_ALLOWED_URL_SCHEMES = {"http", "https"}
_ALLOWED_PORTS = {80, 443}
_MAX_DOWNLOAD_BYTES = 10 * 1024 * 1024  # 10 MiB


def _is_public_host(hostname: str) -> bool:
    try:
        infos = socket.getaddrinfo(hostname, None)
    except OSError:
        return False

    for family, *_rest, sockaddr in infos:
        ip_str = sockaddr[0]
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            return False
        if not ip.is_global:
            return False
    return True


def _validate_and_normalize_public_http_url(raw_url: str) -> str:
    parsed = urlparse(raw_url)
    if parsed.scheme.lower() not in _ALLOWED_URL_SCHEMES:
        raise ValueError("Only http/https URLs are allowed")
    if not parsed.hostname:
        raise ValueError("URL must include a hostname")
    port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)
    if port not in _ALLOWED_PORTS:
        raise ValueError("Only ports 80/443 are allowed")
    if not _is_public_host(parsed.hostname):
        raise ValueError("Refusing to fetch from non-public host")
    return parsed.geturl()


def _download_limited(raw_url: str) -> bytes:
    safe_url = _validate_and_normalize_public_http_url(raw_url)
    headers = {"User-Agent": "DataScienceStuff-image-scraper/1.0"}
    with requests.get(
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


def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)        
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    error_clicks = 0
    while (image_count < max_links_to_fetch) & (error_clicks < 30): # error clicks to stop when there are no more results to show by Google Images. You can tune the number
        scroll_to_end(wd)

        print('Starting search for Images')

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        for img in thumbnail_results[results_start:max_links_to_fetch]:
            # try to click every thumbnail such that we can get the real image behind it
            print("Total Errors till now:", error_clicks)
            try:
                print('Trying to Click the Image')
                img.click()
                time.sleep(sleep_between_interactions)
                print('Image Click Successful!')
            except Exception:
                error_clicks = error_clicks + 1
                print('ERROR: Unable to Click the Image')
                if(results_start < number_results):
                	continue
                else:
                	break
                	
            results_start = results_start + 1

            # extract image urls    
            print('Extracting of Image URLs')
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            print('Current Total Image Count:', image_count)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
            else:
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")
            	        
        results_start = len(thumbnail_results)

    return image_urls

def persist_image(folder_path:str,file_name:str,url:str):
    try:
        image_content = _download_limited(url)

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")
        return

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path,file_name)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path,hashlib.sha256(image_content).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path,hashlib.sha256(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

if __name__ == '__main__':
    wd = webdriver.Chrome(executable_path=DRIVER_PATH)
    queries = ["Karachi City"]  #change your set of queries here
    for query in queries:
        wd.get('https://google.com')
        search_box = wd.find_element_by_css_selector('input.gLFyf')
        search_box.send_keys(query)
        links = fetch_image_urls(query,100,wd) # 200 denotes no. of images you want to download
        images_path = 'dataset/'
        for i in links:
            persist_image(images_path,query,i)
    wd.quit()
