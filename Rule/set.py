

def get_file(filename):
	file_list = []
	with open(filename) as f:
		for line in f:
			line = line.strip()
			if line=="" or line==" " or line=="\n":
				print(filename,line)
			elif "-" in line:
				pass
			else:
				file_list.append(line)
	return file_list

def get_dictionary():
	return get_file("Sets/dictionary.txt")

def get_animals():
	return get_file("Sets/animals.txt")

def get_nouns():
	return get_file("Sets/nouns.txt")

def get_verbs():
	return get_file("Sets/verbs.txt")

def get_adjectives():
	return get_file("Sets/adjectives.txt")

def get_countries():
	return get_file("Sets/countries.txt")

def get_states():
	return get_file("Sets/states.txt")

def get_heathrows():
	return get_file("Sets/heathrows.txt")

def get_python_reserved():
	return get_file("Sets/python_reserved.txt")

def get_uppercase():
	return get_file("Sets/uppercase.txt")

def get_lowercase():
	return get_file("Sets/lowercase.txt")

def get_vowels():
	return get_file("Sets/vowels.txt")

def get_consonants():
	return get_file("Sets/consonants.txt")

given_sets = {
	"Dictionary": get_dictionary(),
	"Animals": get_animals(),
	"Nouns": get_nouns(),
	"Verbs": get_verbs(),
	"Adjectives": get_adjectives(),
	"Countries": get_countries(),
	"States": get_states(),
	"Heathrows": get_heathrows(),
	"Python Reserved Words": get_python_reserved(),
	"Uppercase": get_uppercase(),
	"Lowercase": get_lowercase(),
	"Vowel": get_vowels(),
	"Consonant": get_consonants(),
}

