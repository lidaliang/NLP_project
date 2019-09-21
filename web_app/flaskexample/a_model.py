from flaskexample.thread_loader import thread_loader
from flaskexample.suggest_post import suggest_post
from flaskexample.sentiment import star_rating

def ModelIt(fromUser  = 'Default',n_post_displayed=5):
	n_posts=25
	thread_pd = thread_loader(fromUser)
	thread_selected_list = suggest_post(thread_pd,n_posts=n_posts)
	posts = []
	star_overall = 0
	for line in thread_selected_list:
		star_rating_current = star_rating(line[0])
		posts.append({'star':star_rating_current, 'text':line[0]})
		star_overall += star_rating_current
	star_overall/=n_posts
	return star_overall,posts[:n_post_displayed]