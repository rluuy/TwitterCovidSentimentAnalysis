import tweepy
import time
import datetime
import json
import passwords

# Twitter API keys. I stored them in a seperate file for security reasons
consumer_key = passwords.consumer_key
consumer_secret = passwords.consumer_secret
access_token = passwords.access_token
access_token_secret = passwords.access_token_secret

# Setting up the tweepy_api based on twitter keys
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Constants used to modify what data is grabbed and stored
# currentdate grabs the current time that the script is ran. Used in helping sort when data is grabbed by
# appending that information to the filename.
phrase_to_search = 'Corona'
MAX_TWEETS = 100
currentDT = datetime.datetime.now()
currentdate = str(currentDT.month) + "-" + str(currentDT.day) + "-" + str(currentDT.year)

# Geocode Location of cities we want to look at.
# Format is Latitude, Longitude, Radius in either mi or km. 2nd Tuple information is used simply for file naming
# Also since the twitter api is dumb, don't put spaces between geolocation string information (1st item in Tuple)
tucson_geocode = ("32.22174,-110.92648,50mi", 'Tucson')
los_angles_geocode = ("34.052235,-118.243683,50mi", 'Los Angeles')
new_york_geocode = ("40.712776,-74.005974,50mi", 'New York')
miami_geocode = ("25.761681,-80.191788,50mi", 'Miami')
chicago_geocode = ("41.881832,-87.623177,50mi", 'Chicago')
seattle_geocode = ("47.608013,-122.335167,50mi", 'Seattle')

cities = (tucson_geocode, los_angles_geocode, new_york_geocode, miami_geocode, chicago_geocode, seattle_geocode)


# Calls the API to search 
try:
    for city in cities:
        tweet_string = ""
        for tweet in api.search(q=phrase_to_search, count=MAX_TWEETS, geocode=city[0], tweet_mode='extended'):
            tweet_string += str(tweet.full_text)

        # Format the json string for the google natural language api to process
        data = {
            "document":{
                "type":"PLAIN_TEXT",
                    "content": tweet_string
                },
            "encodingType": "UTF8"
            }

        # Every filename will be different depending on city
        filename = str(city[1]) + currentdate +  ".json"
        # Writes out the tweet list to a json file with the relevant city and the current date grabbed       
        with open(filename, 'w') as filehandle:
            json.dump(data, filehandle, ensure_ascii=False)

except BaseException as e:
    print("Failed with exception: " + str(e))
    time.sleep(3)


