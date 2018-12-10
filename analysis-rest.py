# -*- coding: utf-8 -*-
from pymongo import MongoClient
from geopy.geocoders import Nominatim
import numpy as np
import pandas as pd


class AnalyzeRestaurantItem(object):

	db_name = 'restaurantinfo'
	fields = ['rest_name', 'lat', 'lon', 'rest_street', 'rest_city', \
				'rest_country', 'rest_rating', 'review_excellent_count', \
				'review_good_count', 'review_avg_count', 'review_poor_count', \
				'review_terrible_count', 'positive_review_count', 'negative_review_count', \
				'rest_total_reviews', 'rest_price', 'rest_cuisines', 'rest_features', 'rest_meals']
	df = None

	def __init__(self):

		#Setup Client for MongoDB
		self.client = MongoClient('mongodb://localhost:27017/restaurantinfo')
		self.db = self.client[self.db_name]


	def convert_addr_to_coord(self, addr):
		
		geolocator = Nominatim()
		location = geolocator.geocode(addr, timeout=3)
		if location:
			return location.latitude, location.longitude
		else:
			return 0,0

	def load_mongodb_to_pandas(self):

		rest_info = []
		for doc in self.db.restaurantreviews.find():
			street = doc['rest_street']
			city = doc['rest_city']
			country = doc['rest_country']
			lat, lon = self.convert_addr_to_coord(street + ", " + city + ", " + country)	
			if (lat != 0 and lon != 0):
				positive_review_count = int(doc['review_excellent_count']) + int(doc['review_good_count'])
				negative_review_count = int(doc['review_avg_count']) + int(doc['review_poor_count']) + int(doc['review_terrible_count'])

				rest_info.append([doc['rest_name'], float(lat), float(lon), doc['rest_street'], \
								doc['rest_city'], doc['rest_country'], doc['rest_rating'], \
								doc['review_excellent_count'], doc['review_good_count'], doc['review_avg_count'], \
								doc['review_poor_count'], doc['review_terrible_count'], \
								positive_review_count, negative_review_count, doc['rest_total_reviews'], \
								doc['rest_price'], doc['rest_cuisines'], doc['rest_features'], doc['rest_meals']])
		self.df = pd.DataFrame(rest_info, columns=self.fields)
		print(self.df)	

if __name__ == '__main__':
	analyze = AnalyzeRestaurantItem()
	analyze.load_mongodb_to_pandas()
	
