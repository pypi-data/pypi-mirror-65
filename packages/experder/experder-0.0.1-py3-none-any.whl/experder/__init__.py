import itertools
__all__ = ['caesar_lshift', 'caesar_rshift','caesar_bruteforce','tenkey_lshift','tenkey_rshift']
__author__ = 'Matthew Lam'
__version__ = '0.0.1'
__email__ = 'lcpmatthew@gmail.com'
# Usually when you encode the message you shift right
def caesar_rshift(message, key=13):
	final = ''
	for char in message:
		if (char.isupper() and ord(char)+ key >90) or (char.islower() and ord(char) + key > 122):
			final += chr(ord(char)+key - 26)
		elif char.isalpha():
			final += chr(ord(char)+ key)
		else:
			final += char
	return final

# Usually when you decode the message you left shift
def caesar_lshift(message, key=13):
	final = ''
	for char in message:
		if (char.isupper() and ord(char) - key < 65) or (char.islower() and ord(char) - key < 97):
			final += chr(ord(char) - key + 26)
		elif char.isalpha():
			final += chr(ord(char) - key)
		else:
			final += char
	return final

# tests every possible combination for given string
def caesar_bruteforce(message):
	for i in range(26):
		print('{key:2}|{dec}'.format(dec=caesar_lshift(message, i), key=i ))

def tenkey_rshift(message, key, skip_spaces = True):
	final = ''
	key = str(key)
	if skip_spaces:
		counter = 0
		for char in message:
			if char.isalpha():
				final += caesar_rshift(char, int(key[counter%len(key)]))
				counter += 1
			else:
				final += char
	else:
		for count, k in enumerate(itertools.cycle(key)):
			try:
				final += caesar_rshift(message[count],int(k))
			except IndexError:
				break
	return final

def tenkey_lshift(message, key, skip_spaces= True):
	final = ''
	key = str(key)
	if skip_spaces:
		counter = 0
		for char in message:
			if char.isalpha():
				final += caesar_lshift(char,int(key[counter%len(key)]))
				counter += 1
			else:
				final += char
	else:
		for count, k in enumerate(itertools.cycle(key)):
			try:
				final += caesar_lshift(message[count], int(k))
			except IndexError:
				break
	return final