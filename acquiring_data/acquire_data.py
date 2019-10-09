#We scrape cloudynights.com, it may take a few hours
import web_scraping_tools
import pickle
import pandas as pd

if __name__ == '__main__':
	#The front page of the 6 different forums on cloudynights.com for equipment discussions.
	forum_page_urls = ["https://www.cloudynights.com/forum/67-refractors/?prune_day=100&sort_by=Z-A&sort_key=posts&topicfilter=all",
                   "https://www.cloudynights.com/forum/71-eyepieces/?prune_day=100&sort_by=Z-A&sort_key=posts&topicfilter=all",
                   "https://www.cloudynights.com/forum/64-binoculars/?prune_day=100&sort_by=Z-A&sort_key=posts&topicfilter=all",
                   "https://www.cloudynights.com/forum/69-cats-casses/?prune_day=100&sort_by=Z-A&sort_key=posts&topicfilter=all",
                   "https://www.cloudynights.com/forum/66-mounts/?prune_day=100&sort_by=Z-A&sort_key=posts&topicfilter=all",
                   "https://www.cloudynights.com/forum/68-reflectors/?prune_day=100&sort_by=Z-A&sort_key=posts&topicfilter=all",
                   "https://www.cloudynights.com/forum/65-binoviewers/?prune_day=100&sort_by=Z-A&sort_key=posts&topicfilter=all"
                  ]
    #The filters to remove threads that are not product oriented.
    world_filters = ["-you","-we-","money","collection","guidelines","important","mod","how-to","to-improve","info",
                 "improvements","question","auction",
                 "apos-better",
                 "what-is-your","whats-in-your","show-us-your","have-you-found",
                 "post-a-pic","links-of-interest","policy","do-you-own","show-off","no-use","billp","myths-and-misconceptions",
                 "paracorr-settings","eyepiece-buyers-guide","identifying-eyepiece-aberrations","filters-buyers-guide",
                "clarifications","overlooking-the-obvious","most-beautiful","gems-best-of","vintage-and-classic","tinkering",
                 "home-built","collimated","complementary","resolving","birding","not-popular","scams","classical-cassegrain",
                 "focal-reducer","classic-cassegrain","new-scam","best-threads","duplicate","cables","is-soft","corrector",
                 "thermal-issues","collima","coma","make-a-reflector","best-25mm",
                ]
    #Generate URLs to product discussion threads:
    forum_level_soup = [soup_a_forum(forum_url,n_pages=5) for forum_url in forum_page_urls]
    url_lists = [np.concatenate([from_a_soup_to_url(page) for page in forum]) for forum in forum_level_soup]
    filtered_url_lists = [remove_from_list_if_contains_any_substring(url_list,world_filters) for url_list in url_lists]
    with open('filtered_url_lists', 'wb') as fp:
    	pickle.dump(filtered_url_lists, fp)
    title_lists = [[extract_title_from_thread_url(url) for url in url_list] for url_list in filtered_url_lists]

	all_soups_s = []
    for i,filtered_url_list_short in enumerate(filtered_url_lists_short):
	    print("souping url list",i)
		all_soups_s.append([soup_a_thread(thread,n_pages = 50,wait_time = 0.8) for thread in filtered_url_list_short])

	with open('all_soups_s', 'wb') as fp:
		pickle.dump(all_soups_s, fp)
    
	filtered_url_lists_short = [url_list[:25] for url_list in filtered_url_lists]

	#Scrape all the posts, this takes a few hours
	info_all_threads_all_forums = []
	for i,soups in enumerate(all_soups_s):
	    print("processing forum:",i)
	    info_all_threads_all_forums.append([all_info_from_a_souped_thread(soup) for soup in soups])

	#data_df now contains much more info including hand labels. Directly read data_df.csv to load these data.
	#Saving the results as a pandas dataframe
	data_df=pd.DataFrame(columns=['forum_name','thread_name','text', 'n_likes', 'n_images'])
	for forum_index in range(len(info_all_threads_all_forums)):
    	for thread_index in range(len(info_all_threads_all_forums[forum_index])):
        	df = pd.DataFrame(info_all_threads_all_forums[forum_index][thread_index], 
            	              columns =['text', 'n_likes', 'n_images']) 
        	thread_name = extract_title_from_thread_url(filtered_url_lists[forum_index][thread_index])
        	df['forum_name']=[extract_title_from_thread_url(forum_page_urls[forum_index])]*len(df)
        	df['thread_name']=[thread_name]*len(df)
        	df['thread_total_likes']=[int(np.sum(df['n_likes'].values))]*len(df)
        	df['product_oriented']=[not thread_name in none_product_oriented_threads]*len(df)
        	df['forum_index']=[forum_index]*len(df)
        	df['thread_index']=[thread_index]*len(df)
        	df['post_index']=np.arange(len(df))
        	df['post_id'] = [str(forum_index)+"_"+str(thread_index)+"_"+str(i) for i in range(len(df))]
        	df["sentiment"] = [-1]*len(df)
        	df["relevance"] = [-1]*len(df)
        	df["hand_labeled"] = [False]*len(df)
        	data_df = data_df.append(df)
	del df

	data_df = data_df.set_index('post_id')


	for index, row in data_df.iterrows():
    	q_res = data1_extra[data1_extra['post_id']==index]
    	if len(q_res)>0:
        	data_df.at[index, 'hand_labeled'] = True
        	data_df.at[index, 'sentiment'] = q_res.iloc[0]['sentiment']
        	data_df.at[index, 'relevance'] = q_res.iloc[0]['relevance']

	data_df.to_csv("data_df.csv")