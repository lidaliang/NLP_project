import pandas as pd

def ranking_score(post_info):
	#test for nan
	if post_info[0]!=post_info[0]: return post_info[1]
	else: return post_info[1]+len(post_info[0])/1000

def suggest_post(thread_pd,n_posts=5):
    #input pd frame
    #output list
	thread_list=thread_pd.values.tolist()
	return	sorted(thread_list,key=ranking_score,reverse=True)[:n_posts]