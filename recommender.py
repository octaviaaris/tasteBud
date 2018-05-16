from model import *
from random import sample

init_app()

def get_new_restaurant_recs(user):
	"""Finds restaurants based on restaurants similar to what user has rated 4 or above."""

	# get restaurants from user's ratings where user's rating is 4 or above
	top_rated = [r.restaurants for r in user.ratings if r.user_rating >= 4]
	sim_restaurants = []
	rated_restaurants = [r.restaurants for r in user.ratings]
	new_restaurants = []
	

	# get similar restaurants for each restaurant in top_rated
	for t in top_rated:
		sim_restaurants += t.find_sim_restaurants()

	# filters out restaurants user has already rated and duplicates
	for s in sim_restaurants:
		if s[1].ratings not in rated_restaurants and s[1] not in new_restaurants:
			new_restaurants.append(s[1])

	return new_restaurants

def show_top_picks(user):
	"""Uses restaurant and user similarity recommendations to create a top 5 picks list."""

	top_picks = []

	user_recs = user.get_user_recs()
	rest_sim = get_new_restaurant_recs(user)

	if user_recs and rest_sim:
		top_picks += sample(user_recs, 1)
		top_picks += sample(rest_sim, 4)
	
	return top_picks