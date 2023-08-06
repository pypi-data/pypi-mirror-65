from nltk.tokenize import TweetTokenizer
tokenizer = TweetTokenizer()


def tokenize(text):
	return tokenizer.tokenize(text=text)
