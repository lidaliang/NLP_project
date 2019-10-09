import re
import sys
from utils import write_status
from nltk.stem.porter import *


def preprocess_word(word):
    # Remove punctuation
    word = word.strip('\'"?!,.():;')
    # Convert more than 2 letter repetitions to 2 letter
    # funnnnny --> funny
    word = re.sub(r'(.)\1+', r'\1\1', word)
    # Remove - & '
    word = re.sub(r'(-|\')', '', word)
    return word


def is_valid_word(word):
    # Check if word begins with an alphabet
    return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)


def handle_emojis(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
    return tweet


def preprocess_tweet(tweet):
    use_stemmer = True
    stemmer = PorterStemmer()
    
    processed_tweet = []
    # Convert to lower case
    tweet = tweet.lower()
    # Replaces URLs with the word URL
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', tweet)
    # Replace @handle with the word USER_MENTION
    tweet = re.sub(r'@[\S]+', 'USER_MENTION', tweet)
    # Replaces #hashtag with hashtag
    tweet = re.sub(r'#(\S+)', r' \1 ', tweet)
    # Remove RT (retweet)
    tweet = re.sub(r'\brt\b', '', tweet)
    # Replace 2+ dots with space
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    # Strip space, " and ' from tweet
    tweet = tweet.strip(' "\'')
    # Replace emojis with either EMO_POS or EMO_NEG
    tweet = handle_emojis(tweet)
    # Replace multiple spaces with a single space
    tweet = re.sub(r'\s+', ' ', tweet)
    words = tweet.split()

    for word in words:
        word = preprocess_word(word)
        if is_valid_word(word):
            if use_stemmer:
                word = str(stemmer.stem(word))
            processed_tweet.append(word)

    return ' '.join(processed_tweet)


def preprocess_df(structured_file_name):
    overall_file_name = sys.argv[1][:-4] + '-overall.csv'
    room_file_name = sys.argv[1][:-4] + '-room.csv'
    cleanliness_file_name = sys.argv[1][:-4] + '-cleanliness.csv'
    service_file_name = sys.argv[1][:-4] + '-service-linear.csv'
    
    save_to_file = open(service_file_name, 'w')

    with open(structured_file_name, 'r',encoding='utf-8') as csv:
        lines = csv.readlines()
        total = len(lines)
        for i, line in enumerate(lines):
            if i==0: continue
            line = line.split(',')
            post_id, content, n_likes, sentiment_hand, relevance, nltk_senti = line[0],line[1],line[2],line[3],line[4], line[5]
            sentiment_hand = int(sentiment_hand)
            if sentiment_hand > 3: sentiment = 1
            else: sentiment = 0
            processed_content = preprocess_tweet(content)
            save_to_file.write('%s,%s,%s\n' % (post_id,sentiment,processed_content))
            
            write_status(i + 1, total)
            
    save_to_file.close()
    return


if __name__ == '__main__':
    structured_file_name = sys.argv[1]
    preprocess_df(structured_file_name)
