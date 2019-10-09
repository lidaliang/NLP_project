import re
import sys
from nltk.stem.porter import *
from nltk.corpus import stopwords


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

def is_stop_word(word):
    return word in {'once', 'is', 'until', 'itself', "you'll", 'than', 'did', 'him', 'now', 'the',\
     'all', 'are', 'on', 'her', 'mightn', 'yourself', 'further', 'his',\
      'a', 'was', 'its', 'between', 'more', 'at','would','think', 'wouldn', 'hers', 'not', 'below',\
       "wasn't", "mustn't", "weren't", 'can', "mightn't", 'up', 'you',\
        'do', 'herself', 'under', 'very', 'what', 'why', 'there', 't', 'before',\
         'this', 'same', 'does', 'should', 've', 'here', 'ourselves', 'such',\
          "you've", 'who', 'any', "hadn't", 'each', 'with', 'too', 'how', 'aren',\
           "didn't", 'theirs', 'our', 'she', 'them', 'had', "won't", "you're", 'needn',\
            "don't", 'themselves', "isn't", 'an', 'just', 'don', 'ain', 'again',\
             'll', 'didn', "it's", 'in', 'while', "she's", 'after', 'myself', 'when', 'hasn',\
              'himself', 'he', 'your', 'yourselves', 'having', 'and', 'into', 'have', "shouldn't",\
               'to', 'about', 'won', "wouldn't", 'it', 'few', 'my', 'weren', 'am', "you'd", 'their',\
                'which', 'been', 'above', 'during', 'other', 'y', 'out', "doesn't", 's', 'being', 'mustn',\
                 'or', "aren't", 'as', 'off', 'where', 're', "needn't", 'own', 'doesn', 'hadn', 'has', 'most', 'down',\
                  'will', 'both', 'shan', "that'll", 'doing', 'of', 'd', 'yours', 'we', 'by', 'me', 'through', 'from',\
                   'm', 'isn', 'so', 'those', 'because', 'only', "hasn't", 'no', 'then', 'but', 'ma', 'some', 'haven',\
                    'they', 'be', 'o', 'over', 'if', 'were', 'wasn', 'that', 'ours', "should've", "shan't", 'whom', 'these',\
                     'for', 'shouldn', 'i', "haven't", 'havent','hadnt','shes','youd','ill','youve','wont','s','ll'}


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


def preprocess_tweet(tweet, use_stemmer=True):
    stemmer = PorterStemmer()
    
    processed_tweet = []
    # Convert to lower case
    #tweet = tweet.lower()
    # Replaces URLs with the word URL
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', tweet)
    #Replace @handle with the word USER_MENTION
    tweet = re.sub(r'@[\S]+', 'USER_MENTION', tweet)
    #Replaces # with space
    tweet = re.sub('#',' ', tweet)
    #Replace emojis with either EMO_POS or EMO_NEG
    tweet = handle_emojis(tweet)
    #Focal ratios
    tweet = re.sub('f/\d*',lambda x:x.group(0).replace('/',''),tweet)
    #replace / \ with space
    tweet = re.sub('/',' ',tweet)
    tweet = tweet.replace("\\", "")
    tweet = re.sub('=',' = ',tweet)
    tweet = tweet.replace("[", " ").replace('😆',' EMO_POS ').replace('^',' ').replace('`',' ').replace('`',' ')
    tweet = tweet.replace("]", " ").replace('”',' ').replace('+',' + ').replace('$',' $ ').replace('‘',' ')
    tweet = tweet.replace("(", " ").replace('<',' < ').replace('>',' > ').replace('-',' - ').replace(":"," ")
    tweet = tweet.replace(")", " ").replace('!',' ').replace('â€™',' ').replace('_',' ').replace('’',' ')
    tweet = tweet.replace(":", " ").replace('…',' ').replace('„',' ').replace('“',' ').replace('?',' ')
    tweet = re.sub('~',' ~ ',tweet)
    tweet = re.sub('%',' % ',tweet)
    tweet = re.sub('\d+',' NUM ',tweet)
    #tweet = handle_emojis(tweet)
    # Remove RT (retweet)
    #tweet = re.sub(r'\brt\b', '', tweet)
    # Replace dots with space
    tweet = re.sub('\.',' ',tweet)
    #Replace ' and " with space
    tweet = re.sub('\'',' ',tweet)
    tweet = re.sub('\"',' ',tweet)
    #Replace "*" with space
    tweet = re.sub("\*","",tweet)
    # Strip space, " and ' from tweet
    tweet = tweet.strip(' "\'')
    # Replace multiple spaces with a single space
    tweet = re.sub(r'\s+', ' ', tweet)
    words = tweet.split()

    for word in words:
        word = preprocess_word(word)
        if is_stop_word(word): continue
        if is_valid_word(word):
            if use_stemmer:
                word = str(stemmer.stem(word))
        processed_tweet.append(word)

    return ' '.join(processed_tweet)

#if __name__ == '__main__':
#    print(set(stopwords.words('english')))
