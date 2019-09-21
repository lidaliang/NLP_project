from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk_sentiment = SentimentIntensityAnalyzer()

def star_rating(string,model='nltk_vader',verbose=False):
	if model == 'nltk_vader':
		senti = nltk_sentiment.polarity_scores(string)['compound']
		if senti<-0.5: return 1
		elif senti < 0.1: return 2
		elif senti < 0.4: return 3
		elif senti < 0.95: return 4
		else: return 5

if __name__ == '__main__':
	print(star_rating("lol"))