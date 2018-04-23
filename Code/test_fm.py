import pylast as pl
import os

print(str(os.getcwd()))

api_file = open('config.ini', 'r')

APIS = api_file.read().split("\n")
api_file.close()

#print(APIS)

API_KEY = APIS[0]
API_SECRET = APIS[1]

USERNAME = APIS[2]
PASSWORD_HASH = pl.md5(APIS[3])
network = pl.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=USERNAME, password_hash=PASSWORD_HASH)

selected_artist = input("Insert artist: ")

artist = network.get_artist(selected_artist)
artist_tags = artist.get_top_tags(limit=5)
related_artists = artist.get_similar(limit=20)

j = 0
for rel in iter(artist_tags):
    print("Tag #" + str(j+1) + " for \'" + str(artist.get_name()) + "\': " + str(rel.item))
    j = j+1
print("\n")

j = 0
for rel in iter(related_artists):
    print("Here the #" + str(j+1) + " related artist: " + str(rel.item))
    j = j+1