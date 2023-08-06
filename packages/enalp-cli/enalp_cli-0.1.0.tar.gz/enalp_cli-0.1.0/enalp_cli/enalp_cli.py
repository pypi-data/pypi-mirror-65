# Leet
# Reverse
# MixUp

# Core Pkgs
import click
from pyfiglet import Figlet
from click_help_colors import HelpColorsGroup, HelpColorsCommand

# Misc Pkgs
import json
import time
import random

# NLP Pkgs
from textblob import TextBlob
#!python -m textblob.download_corpora


POS_dict = {'CC':'coordinating conjunction','CD':'cardinal digit','DT':'determiner',
'EX':'existential there (like: “there is” … think of it like “there exists”)',
'FW':'foreign word','IN':'preposition/subordinating conjunction','JJ':"adjective ‘big’",
'JJR':"adjective, comparative ‘bigger’",'JJS':"adjective, superlative, ‘biggest’",
'LS':'list marker 1)','MD':'modal could, will','NN':"noun, singular, ‘desk’",
'NNS':"noun plural ‘desks’",'NNP':"proper noun, singular ‘Harrison’",
'NNPS':"proper noun, plural ‘Americans’",'PDT':"predeterminer ‘all the kids’",
'POS':"possessive ending parent‘s",'PRP':"personal pronoun I, he, she",
'PRP$':"possessive pronoun my, his, hers",'RB':"adverb very, silently",
'RBR':"adverb, comparative better",'RBS':'adverb, superlative best','RP':'particle give up',
'TO':"to go ‘to‘ the store",'UH':'interjection errrrrrrrm','VB':"verb, base form take",
'VBD':'verb, past tense took','VBG':'verb, gerund/present participle taking',
'VBN':'verb, past participle taken','VBP':'verb, sing. present, non-3d take',
'VBZ':'verb, 3rd person sing. present takes','WDT':'wh-determiner which',
'WP':'wh-pronoun who, what','WP$':'possessive wh-pronoun whose','WRB':'wh-abverb where, when'
}

@click.group(cls=HelpColorsGroup,help_headers_color='yellow',help_options_color='cyan')
@click.version_option(version='0.1.0', prog_name='ENALP CLI')
def main():
	""" ENALP CLI """
	pass

# Tokenization
@main.command()
@click.argument('text')
@click.option('--tokentype','-t',help="Specify Type of Tokenization [word(def)|sentence]",default='word')
@click.option('--save','-s',default=False)
def tokens(text,tokentype,save):
	"""Word and Sentence Tokenization (saving option)

	 --usage: enalp_cli tokens 'your text'

	"""
	final_result = TextBlob(text)
	if tokentype == 'word' and save == 'True':
		click.secho("Word Tokenization",fg='black',bg='white')
		click.secho("Original Text: {}".format(text),fg='yellow')
		click.secho("Word Tokens: {}".format(final_result.words),fg='green')
		save_to_json(str(final_result.words))
	elif tokentype == 'sentence' and save == 'True':
		click.secho("Sentence Tokenization",fg='black',bg='white')
		click.secho("Original Text: {}".format(text),fg='yellow')
		click.secho("Sentence Tokens: {}".format(final_result.sentences),fg='green')
		save_to_json(str(final_result.sentences))
	else:
		if tokentype == 'word':
			click.secho("Word Tokenization",fg='black',bg='white')
			click.secho("Original Text: {}".format(text),fg='yellow')
			click.secho("Word Tokens: {}".format(final_result.words),fg='green')
		elif tokentype == 'sentence':	
			click.secho("Sentence Tokenization",fg='black',bg='white')
			click.secho("Original Text: {}".format(text),fg='yellow')
			click.secho("Sentence Tokens: {}".format(final_result.sentences),fg='green')
		else:
			click.secho("Please Specify 'word' or 'sentence after tokentype",fg='red')


# Sentiment
@main.command()
@click.argument('text')
def sentiment(text):
	"""Sentiment Analysis with Polarity and Subjectivity

	 --usage: enalp_cli sentiment 'your text'

	"""
	raw_text = TextBlob(text)
	final_result = raw_text.sentiment
	click.secho("Sentiment Analysis",fg='black',bg='white')
	click.secho("Original Text: {}".format(text),fg='yellow')
	click.secho("Sentiment: {}".format(final_result),fg='green')


# Parts of Speech
@main.command()
@click.argument('text')
def pos(text):
	"""Parts of Speech Tagging

	 --usage: enalp_cli pos 'your text'

	"""
	raw_text = TextBlob(text)
	final_result = raw_text.pos_tags
	click.secho("Parts of Speech Tagging",fg='black',bg='white')
	click.secho("Original Text: {}".format(text),fg='yellow')
	click.secho("POS: {}".format(final_result),fg='green')
	click.echo("-----> 'posdictionary' to print all POS TAGS Definitions.")


# POS TAGS Definitions
@main.command()
def posdictionary():
	"""POS TAGS Definitions

	 --usage: enalp_cli posdictionary

	"""
	click.secho("POS TAGS Definitions",fg='black',bg='white')
	for tag in POS_dict:
		print(tag+'\t', POS_dict[tag])



# Sentence Correction
@main.command()
@click.argument('text')
def correction(text):
	"""Sentence Correction

	 --usage: enalp_cli correct 'your text'

	"""
	input_text = TextBlob(text)
	click.secho("Sentence Correction",fg='black',bg='white')
	click.secho("Original Text: {}".format(text),fg='yellow')
	click.secho("Corrected Text: {}".format(input_text.correct()),fg='green')


# Words Definition
@main.command()
@click.argument('text')
def definition(text):
	"""Words Definition

	 --usage: enalp_cli definition 'your words'

	"""
	raw_text = TextBlob(text)
	final_words = raw_text.words
	click.secho("Words Definition",fg='black',bg='white')
	for w in final_words:
		click.secho("Original Word: {}".format(w),fg='yellow')
		click.secho("Word Definition: {}".format(w.definitions),fg='green')


# Words Plural
@main.command()
@click.argument('text')
def plural(text):
	"""Words Plural

	 --usage: enalp_cli plural 'your words'

	"""
	raw_text = TextBlob(text)
	final_words = raw_text.words
	click.secho("Words Plural",fg='black',bg='white')
	click.secho("Original Text: {}".format(text),fg='yellow')
	click.secho("Plural: {}".format(final_words.pluralize()),fg='green')


# Spell Check
@main.command()
@click.argument('text')
def spell_check(text):
	"""Spell Check

	 --usage: enalp_cli spell-check 'your words'

	"""
	raw_text = TextBlob(text)
	final_words = raw_text.words
	click.secho("Spell Check",fg='black',bg='white')
	for w in final_words:
		click.secho("Original Word: {}".format(w),fg='yellow')
		click.secho("Word Spelling with Probability: {}".format(w.spellcheck()),fg='green')


# Word Count
@main.command()
@click.argument('text')
@click.option('--word_to_search',prompt=True)
def word_count(text,word_to_search):
	"""Word Count

	 --usage: enalp_cli word-count 'your text'

	"""
	input_text = TextBlob(text)
	click.secho("Word Count",fg='black',bg='white')
	click.secho("Original Text: {}".format(text),fg='yellow')
	click.secho("The Text cointains {} time(s) the word {}".format(input_text.word_counts[word_to_search.lower()],word_to_search),fg='green')


# Translation to English
@main.command()
@click.argument('text')
def translation(text):
	"""Text Translation (to English)

	 --usage: enalp_cli translation 'your text'

	"""
	input_text = TextBlob(text)
	click.secho("Text Translation",fg='black',bg='white')
	click.secho("Original Text: {}".format(text),fg='yellow')
	click.secho("Translated Text {}".format(input_text.translate(to='en')),fg='green')


# Language Detection
@main.command()
@click.argument('text')
def ldetect(text):
	"""Language Detection

	 --usage: enalp_cli ldetect 'your text'

	"""
	input_text = TextBlob(text)
	click.secho("Language Detection",fg='black',bg='white')
	click.secho("Original Text: {}".format(text),fg='yellow')
	click.secho("The language in the Text is {}".format(input_text.detect_language()),fg='green')


# Lemmatization
@main.command()
@click.argument('text')
def lemmatize(text):
	"""Text Lemmatization
	
	 --usage: enalp_cli lemmatize 'your text'

	"""
	raw_text = TextBlob(text)
	poss = raw_text.pos_tags
	click.secho("Lemmatization",fg='black',bg='white')
	words_to_lemma = [pos[0] for pos in poss]
	pos = [pos[1] for pos in poss]

	for i in range(len(pos)):
		if pos[i] in ['VB','VBD','VBG','VBN','VBP','VBZ']:
			pos[i]='v'

	click.secho("Original Text: {}".format(text),fg='yellow')

	lemmas = []
	for j in range(len(pos)):
		if pos[j]=='v':
			lemmas.append(words_to_lemma[j].lemmatize("v"))
		else:
			lemmas.append(words_to_lemma[j].lemmatize())

	click.secho("Lemmas: {}".format(lemmas),fg='green')


# Reading a file
@main.command()
@click.argument('text',type=click.File('rb'))
@click.option('--analysis', '-a',help="Specify Kind of Analysis [tokens(def)|sentiment|pos]",default='tokens')
def readfile(text,analysis):
	"""Read a File and Analyze

	 --usage: enalp_cli readfile 'file name'

	"""
	mytext = text.read().decode('utf-8')
	file_text = TextBlob(mytext)
	if analysis == 'pos':
		click.secho("Parts of Speech Tagging",fg='black',bg='white')
		click.secho("Original Text: {}".format(mytext),fg='yellow')
		click.secho("POS: {}".format(file_text.pos_tags),fg='green')
		click.echo("-----> 'posdictionary' to print all POS TAGS Definitions.")
	elif analysis == 'sentiment':
		click.secho("Sentiment Analysis",fg='black',bg='white')
		click.secho("Original Text: {}".format(mytext),fg='yellow')
		click.secho("Sentiment: {}".format(file_text.sentiment),fg='green')
	elif analysis == 'tokens':
		click.secho("Word Tokenization",fg='black',bg='white')
		click.secho("Original Text: {}".format(mytext),fg='yellow')
		click.secho("Word Tokens: {}".format(file_text.words),fg='green')
	else:
		click.secho("Please Specify 'tokens', 'pos' or 'sentiment' after file name",fg='red')		


@main.command()
def about():
	"""Info About ENALP CLI Tool

	 --usage: enalp_cli about

	"""
	click.echo('\n')
	f = Figlet(font='slant')
	print(f.renderText('ENALP CLI'))
	click.secho("ENALP CLI: Easy NAtural Language Processing CLI",fg='cyan')
	click.secho("By: Rosario Moscato",fg='white')
	click.secho("mailto: rosario.moscato@outlook.com",fg='cyan')
	click.secho("https://www.linkedin.com/in/rosariomoscato/",fg='white')
	click.echo('\n')


@main.command()
@click.argument('text')
@click.option('--save','-s',default=False)
def leet(text,save):
	"""Leet a Text

	 --usage: enalp_cli leet 'your text'

	"""
	chars = {'a':'4','b':'l3','c':'[','d':'|)','e':'3','f':'|=','g':'&','h':'#','i':'1','j':',_|','k':'>|','l':'1',
	'm':'(V)','n':'^/','o':'0','p':'|*','q':'(_,)','r':'l2','s':'5','t':'7','u':'(_)','v':'|/','w':"'//",'x':'><','y':'j','z':'2'}
	getchar = lambda c: chars[c.lower()] if c.lower() in chars else c
	result = ''.join(getchar(c) for c in text)

	click.secho("Leet a Text",fg='black',bg='white')
	click.secho("Original Text: {}".format(text),fg='yellow')
	click.secho("Leet Version: {}".format(result),fg='green')

	if save == 'True':
		save_to_json(result)



@main.command()
@click.argument('text')
@click.option('--save','-s',default=False)
def reverse(text,save):
	"""Reverse a Text

	 --usage: enalp_cli reverse 'your text'

	"""
	result = text[::-1]
	click.secho("Reverse a Text",fg='black',bg='white')
	click.secho("Original Text: {}".format(text),fg='yellow')
	click.secho("Reverse Version: {}".format(result),fg='green')

	if save == 'True':
		save_to_json(result)




@main.command()
@click.argument('text')
@click.option('--save','-s',default=False)
def mixup(text,save):
	"""MixUp a Text

	 --usage: enalp_cli mixup 'your text'

	"""
	result = ''.join(random.sample(text,len(text)))
	click.secho("mixup a Text",fg='black',bg='white')
	click.secho("Original Text: {}".format(text),fg='yellow')
	click.secho("MixUp Version: {}".format(result),fg='green')

	if save == 'True':
		save_to_json(result)



def save_to_json(x):
	timestr = time.strftime("%Y%m%d-%H%M%S")
	filename = 'result' + timestr + '.txt'
	with click.open_file(filename,'w') as f:
		json.dump(x,f,indent=4,sort_keys=True)

if __name__ == '__main__':
	main()


