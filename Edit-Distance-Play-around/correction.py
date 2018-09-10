import sys
from operator import itemgetter
import re

def tokenizer(sentence):
	"""
	tokenizer() takes a sentence (string) and tokenizes it according to the
	algorithm for tokenization provided by Jurafsky and Martin in
	'Speech and Language Processing' (2nd) on page 71.
	@params: senetence to be tokenized.
	@return: tokenized sentence.
	"""
	clitic = "'|:|-|'S|'D|'M|'LL|'RE|'VE|N'T|'s|'d|'m|'ll|'re|'ve|n't"
	abbr = {'Co.' : 1, 'Dr.' : 1, 'Jan.' : 1, 'Feb.' : 1, 'Mr.' : 1,
	        'Ms.' : 1, 'Mrs.' : 1, 'Inc.' : 1, 'Mar.' : 1, 'Apr.' : 1,
	        'Aug.' : 1, 'Sept.' : 1, 'Oct.' : 1, 'Nov.' : 1, 'Dec.' : 1}

	tokenized_sent = sentence

	# Put whitespace around separators.
	tokenized_sent = re.sub('([\\?!()\";/|`:])', r' \1 ', tokenized_sent)

	# Put whitespace around commas that are not inside numbers.
	tokenized_sent = re.sub('([^0-9]),', r'\1 , ', tokenized_sent)
	tokenized_sent = re.sub(',([^0-9])', r' , \1', tokenized_sent)

	# Distinguish singlequotes from apostrophes by segmenting off single
	# quotes not preceded by a letter.
	tokenized_sent = re.sub("^\'", r"' ", tokenized_sent)
	tokenized_sent = re.sub("([^A-Za-z0-9])\'", r"\1 '", tokenized_sent)

	# Segment off punctuation from clitics.
	reg = '(' + clitic + ')([^A-Za-z0-9])'
	tokenized_sent = re.sub(reg, r'\1 \2', tokenized_sent)

	# Now periods.
	words = tokenized_sent.split()
	count = -1
	words_new = []
	# Loops over each word and checks if it ends in a period. If it does end
	# with a period we check if it is an abbreviation or a sequence of letters
	# and periods (U.S.)
	for word in words:
		count += 1
		if word[-1] == '.':
			if word in abbr:
				# it is an abbreviation
				words_new.append(word)
			else:
				# not an abbreviation
				if '.' in word[:-1]:
					words_new.append(word)
				else:
					words_new.append(word[:-1])
					words_new.append('.')
		else:
			words_new.append(word)

	tokenized_sent = ' '.join(words_new)

	return tokenized_sent

def deletion():
	"""
	deletion() finds hte cost of deleting a character.
	@params: n/a.
	@return: The cost of a deletion (1).
	"""
	return 1

def insertion():
	"""
	insertion() finds the cost of inserting a character.
	@params: n/a.
	@return: The cost of an insertion (1).
	"""
	return 1

def substitution(j, i):
	"""
	substitution() takes two characters and finds the cost of substituting one
	for the other. If the characters are the same the cost is 0, while if they
	are within reasonable distance of each other the cost is 1, otherwise the
	cost is 2.
	@params: Two single characters.
	@return: The cost of a substition (integer: 0,1,2).
	"""
	# If the letters are the same there is no cost of substituting them.
	if j == i:
		return 0
	elif j.lower() == i.lower():
		return 0


	# List used to find out whether a character was a 'likely' typo or not.
	# a-z, 0-9, comma, full stop, semi-colon, square bracket ([) and dash
	# are included in the list and maps to a string with all keys that
	# surround it. Surrounding keys are taken to be 'likely' typos and given
	# a lesser weight of 1. 
	surrounding = {'1': 'q', '2': 'qw', '3': 'we', '4': 'er', 
				   '5': 'rt', '6': 'ty', '7': 'yu', '8': 'ui', 
				   '9': 'io', '0': 'op', '-': 'p', 'q': 'wsa', 
				   'w': 'qeasd', 'e': 'wrsdf', 'r': 'etdfg', 
				   't': 'ryfgh', 'y': 'tughj', 'u': 'yihjk', 
				   'i': 'uojkl', 'o': 'ipkl', 'p': 'ol', '[': 'p', 
				   'a': 'qwszx', 's': 'qweadzx', 'd': 'wersfxc', 
				   'f': 'ertdgcv', 'g': 'rtyfhvb', 'h': 'tyugjbn', 
				   'j': 'yuihknm', 'k': 'uiojlm', 'l': 'iopk', 
				   ';': 'olp', 'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 
				   'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk', 
				   '.': 'klm', ',': 'l'}

	if j.lower() in surrounding:
		if i.lower() in surrounding[j.lower()]:
			return 1
	return 2

def minimumEditDistance(target, source):
	"""
	minimumEditDistance() two strings and find the minimum cost of transforming
	one into the other through substituting two characters and inserting or
	deleting a character. This algorithm is implemented dynamically (table).
	@params: Two strings (target, source).
	@return: Distance from target to source (integer).
	"""
	n = len(target) # vertical
	m = len(source) # horizontal

	# Set up table and fill in appropriate initial numbers.
	distance = [[0 for i in range(m + 1)] for j in range(n + 1)]
	distance[0][0] = 0

	for i in range(1, n + 1):
		distance[i][0] = distance[i - 1][0] + insertion()
	
	for j in range(1, m + 1):
		distance[0][j] = distance[0][j - 1] + deletion()

	# Complete the table by finding hte lowest value of insertion/deletion/
	# substitution. Final minimum edit distance will be in the top-right
	# corner (distance[n][m]).
	for i in range(1, n + 1):
		for j in range(1, m + 1):
			distance[i][j] = min(distance[i - 1][j] + insertion(),
								 distance[i][j - 1] + deletion(),
								 distance[i - 1][j - 1] + 
								   substitution(source[j - 1], target[i - 1]))

	return distance[n][m]

def getDictionary():
	"""
	getDictionary() gets all the words in the dictionary and sorts them 
	according to size (words of equal size are put into separate lists). 
	Returns this list.
	@params: n/a.
	@return: List of lists, where a list at index i contains all the strings
			 in the dictionary of length i.
	"""
	words = []

	# Open up the dictionary file and add all the words to a list where they
	# are sorted by length of the words. Example: A word of length 5 is
	# added to the list of words at index 5 of words.
	for word in open('/usr/share/dict/words', 'r'):
		word = word.strip()
		# If the list of lists is large enough, simply add the new word to
		# the appropriate list.
		# [[0], [1], [2]] -> [[0], [1, 1], [2]]
		if len(word) < len(words):
			words[len(word)].append(word)
		# If the list of lists is just not long enough, append to the end.
		# [[0], [1], [2]] -> [[0], [1], [2], [3]]
		if len(word) == (len(words)):
			words.append([word])
		# If the list of lists is not long enough by more than one, add
		# the appropriate number of lists to make the desirable length.
		else:
			# [[0], [1], [2]] -> [[0], [1], [2], [3], [4], [5], [6], [7]]
			for i in range(len(words), len(word) + 1):
				words.append([])
			words[len(word)].append(word)

	# Add a buffer at the end so that we can always search for words of one
	# character longer length (although the max will be empty list).
	words.append([])

	return words

def findPlausibleWords(word, valid_words):
	"""
	findPlausibleWords() takes a word and a list of valid words and checks
	whether the word is valid or not. If it is not valid the minimum edit
	distance is calculated for a series of valid words and the ones with the
	lowest edit distance are returned.
	@params: A string (word) and a list of lists, where a list at index i
			 contains all the valid strings of length i.
	@return: A list of tuples containing the words with the lowest minimum
			 edit distance to the word provided along with the edit distance.
			 At most 5 tuples are returned.
	"""
	word_list = valid_words

	if len(word) >= 2:
		max_word_length = len(word) + 1
		min_word_length = len(word) - 1
	else:
		max_word_length = len(word) + 1
		min_word_length = 1

	plausible_words = {}

	# Typos are more common than missing a character, as a user can usually
	# tell whether a word is too short or too long. Therefore we start by
	# checking other words of similar length.


	# BEGINNINGS and ENDINGS are the most important -- users usually get
	# those correct (see top of file efficiency section for more detail).
	# Loops over words of the same length and tries to find matches.
	sorted_list = []
	if len(word) > 2:
		for w in word_list[len(word)]:
			if (w[:2] == word[:2]) or (w[-2:] == word[-2:]):
				min_dist = minimumEditDistance(word, w.lower())
				if len(word) > 8:
					if min_dist <= 4:
						plausible_words[w.lower()] = min_dist
				elif len(word) > 3:
					if min_dist <= 2:
						plausible_words[w.lower()] = min_dist
				else:
					if min_dist == 1:
						plausible_words[w.lower()] = min_dist

		# If 5 decent alternatives have already been found, be are satisfied
		# and return those. We do this because a substitution is more likely
		# than an extra or missing letter, due to the user probably having a
		# feel for whether the word is too short or too long.
		for wd in sorted(plausible_words.items(), key=itemgetter(1)):
			if len(sorted_list) < 5:
				sorted_list.append(wd)
				if len(sorted_list) == 5:
					if sorted_list[-1][1] <= 1.0:
						return sorted_list
		
		# Users can typically tell whether something they have typed is too
		# long or short, meaning that the number of errors in terms of length
		# is fairly limited. Therefore we choose not to look at words that are
		# more than a single character shorter or longer than the word the
		# user actually typed.
		for i in range(min_word_length, max_word_length + 1):
			if i != len(word):
				for w in word_list[i]:
					if (w[:2] == word[:2]) or (w[-2:] == word[-2:]):
						min_dist = minimumEditDistance(word, w.lower())
						if min_dist == 0: 
							return []
						if len(word) > 8:
							if min_dist <= 4:
								plausible_words[w.lower()] = min_dist
						elif len(word) > 3:
							if min_dist <= 2:
								plausible_words[w.lower()] = min_dist
						else:
							if min_dist == 1:
								plausible_words[w.lower()] = min_dist
	# length < 3 aka 1 or 2.
	elif len(word) == 2:
		for i in range(1, max_word_length + 1):
			for w in word_list[i]:
				if (w[0] == word[0]) or (w[-1] == word[-1]):
					min_dist = minimumEditDistance(word, w.lower())
					if min_dist == 1:
						plausible_words[w.lower()] = min_dist

	# Finds the best 5 words (those with the smallest edit distance)
	# and returns those.
	for wd in sorted(plausible_words.items(), key=itemgetter(1)):
		if len(sorted_list) < 5:
			sorted_list.append(wd)
			if len(sorted_list) == 5:
				return sorted_list

	return sorted_list

def spellChecker(f):
	"""
	spellChecker() takes a file and checks whether the words in the file are
	spelled correctly according to the dictionary. Suggests corrections to
	words that are incorrectly spelled and makes adjustments depending on
	whether the user decides to correct the spelling or not.
	@params: Name of file.
	@return: n/a.
	"""
	# Open /usr/share/dict/words/ and read the words into a two dimentional
	# list, sorted by length of words. This will make it easy to later
	# restrict the number of words we have to check later.
	words = getDictionary()

	try:
		f = open(f)
		f_new = ''

		count = 0
		line = input()
		line = tokenizer(line)
		line_start = 0
			# Loops over each word in the tokenized line.
		for word in line.split():
			if line_start == 0:
				line_start = 1
			else:
				line_start = 2

				new = word
				# Check whether word is spelled correctly by looking it up in
				# the dictionary. If it is not spelled correctly we want to
				# find plausible other words it could be.
				if len(word) <= len(words) - 2:
					if ((word not in words[len(word)]) and
					   (word.lower() not in words[len(word)])):
						plausible = findPlausibleWords(word, words)
						if len(plausible) > 0:
							print('Attention!')
							print('\'' + word + '\' might be spelled',
							      'incorrectly.')
							print('Line Number: ' + str(count))
							print('Line: \'' + line + '\'')
							print('Did you mean:')
							for i in range(len(plausible)):
								print('Index: %s, Word: %s, Min dist: %f' % 
									(i, plausible[i][0], plausible[i][1]))
							print('Index: ' + str(len(plausible)) + ',',
								  'Ignore misspelling')
							print('Please enter below the index of the',
								  'correct word:')

							# Wait for the user to decide which of the words 
							# they want the word to be corrected to. Replace
							# the existing word with the correct one in the
							# new corrected_* file.
							user_input = None
							while user_input == None:
								user_input = input()
								if user_input.isdigit():
									user_int = int(user_input)
									if user_int == len(plausible):
										new = word
									elif ((user_int < len(plausible)) and 
										  (user_int >= 0)):
										new = plausible[user_int][0]
									else:
										# user did not enter an int in the 
										# range 0-5.
										user_input = None
										print('Invalid index entered.',
											  'Please try again.')
								else:
									# user did not enter an int in the range
									# 0-5.
									user_input = None
									print('Invalid index entered.',
										  'Please try again.')
							# Prints empty lines around the resuming message,
							# as this highlights it more.
							print()
							print('Resuming. Please be patient.')
							print()
				
				# Check if the word was the first word in the line and add
				# spaces accordingly.
				if line_start == 1:
					f_new = f_new + new
				else:
					f_new = f_new + ' ' + new

			# Makes sure we start a new line at the correct places.
			f_new = f_new + '\n'
		f.close()
	except:
		print("Error: Could be an invalid filename.")
		sys.exit()

	f_new = f_new.strip()

	# Create a new file and write the corrected version of the text to that
	# file.
	fixed_file = open('corrected_' + f.name, 'w')
	fixed_file.write(f_new)
	fixed_file.close()

	print('Corrected file saved as \'corrected_' + sys.argv[1] + '\'.')
	print('Done!')

def main():
	if len(sys.argv) != 2:
		print('Error. Please provide a filename.')
		print('Usage: $ python3 corrector.py <filename>')
		sys.exit()
	print('Please be patient.')
	print('Enter Sentence for correction.')
	spellChecker(sys.argv[1])


if __name__ == '__main__':
	main()
