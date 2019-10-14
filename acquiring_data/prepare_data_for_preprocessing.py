from web_scraping_tools import text_cleaning
import pickle
import pandas as pd

if __name__ == '__main__':
	#remove comas
	df_no_comas = pd.read_csv('../data/data_df.csv')
	df_no_comas.text = [text_cleaning(text) for text in df_no_comas.text.values]
	df_no_comas.thread_name = [text_cleaning(text) for text in df_no_comas.thread_name.values]
	df_no_comas.forum_name = [text_cleaning(text) for text in df_no_comas.forum_name.values]
	df_no_comas.to_csv("../data/df-no-comas.csv")

	df_hand = df_no_comas[df_no_comas['hand_labeled']==True]
	df_hand.to_csv('../data/df_hand.csv')

	data_df_prod = df_no_comas[df_no_comas['product_oriented']==True]
	data_df_prod_has_likes = data_df_prod[data_df_prod['thread_total_likes'] != 0]
	data_df_prod_has_likes.to_csv("../data/data_df_prod_has_likes.csv",index=False)

	data_df_prod_no_likes = data_df_prod[data_df_prod['thread_total_likes'] == 0]
	data_df_prod_no_likes.to_csv("../data/data_df_prod_no_likes.csv",index=False)

