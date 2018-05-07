import json
import model

with open("rest_data.txt") as f:
	for line in f:
		line = json.loads(line)
		# print type(line)
		rest_id = line['id']
		name = line['name']
		url = line['url']
		address1 = line["location"]['address1']
		address2 = line["location"]['address2']
		address3 = line["location"]['address3']
		city = line["location"]['city']
		state = line["location"]['state']
		zipcode = line["location"]['zip_code']
		latitude = line['coordinates']['latitude']
		longitude = line['coordinates']['longitude']

		print """
			  rest_id: {rest_id}
			  name: {name}
			  url: {url}
			  address1: {a1}
			  address2: {a2}
			  address3: {a3}
			  city: {city}
			  state: {state}
			  zipcode: {zipcode}
			  latitude: {latitude}
			  longitude: {longitude}""".format(rest_id=rest_id,
			  								   name=name,
			  								   url=url,
			  								   a1=address1,
			  								   a2=address2,
			  								   a3=address3,
			  								   city=city,
			  								   state=state,
			  								   zipcode=zipcode,
			  								   latitude=latitude,
			  								   longitude=longitude)