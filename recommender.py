from model import *
from random import sample

init_app()

def get_new_restaurant_recs(user):
	"""Finds restaurants based on restaurants similar to what user has rated 4 or above."""


	# get restaurants from user's ratings where user's rating is 4 or above
	user_favorites = [r.restaurants for r in user.ratings if r.user_rating >= 4]
	
	sim_restaurants = []
	
	# get similar restaurants for each restaurant in top_rated; append as (match score, r)
	for restaurant in user_favorites:
		sim_restaurants += restaurant.find_sim_restaurants()
	
	# all restaurants rated by user
	user_rated = [r.restaurants for r in user.ratings]

	new_restaurants = []

	# filters out restaurants user has already rated and duplicates
	for s in sim_restaurants:
		if s[1] not in user_rated:
			new_restaurants.append(s[1])

	return list(set(new_restaurants))

def show_top_picks(user):
	"""Uses restaurant and user similarity recommendations to create a top 5 picks list."""

	top_picks = []

	top_picks += user.get_user_recs()
	top_picks += get_new_restaurant_recs(user)

	return sample(top_picks, 5)