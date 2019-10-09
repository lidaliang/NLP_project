import sys
from utils import write_status
from word_processing_lib import preprocess_tweet


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
            post_id, content, n_likes, sentiment_hand, relevance = line[0],line[10],line[5],line[9],line[8]
            sentiment_hand = int(float(sentiment_hand))
            if sentiment_hand > 3: sentiment = 1
            else: sentiment = 0
            processed_content = preprocess_tweet(content)
            save_to_file.write('%s,%s,%s\n' % (post_id,int(int(n_likes)>0),processed_content))
            
            write_status(i + 1, total)
            
    save_to_file.close()
    return


if __name__ == '__main__':
    structured_file_name = sys.argv[1]
    preprocess_df(structured_file_name)
