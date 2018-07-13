import os
from dotenv import load_dotenv, find_dotenv
import pylast as pl
import discogs_client as dgs_c

load_dotenv(find_dotenv())

network = pl.LastFMNetwork(api_key=os.getenv('LASTFM_API_KEY'), \
                           api_secret=os.getenv('LASTFM_API_SECRET'), \
                           username=os.getenv('LASTFM_USERNAME'), \
                           password_hash=pl.md5(os.getenv('LASTFM_PASSWD')))

dgs = dgs_c.Client('AYearInMusic', user_token=os.getenv('DISCOGS_USER_TOKEN'))
'''
#Search an Artist
results = dgs.search('queens of the stone age', type='artist')  #release, master, artist, label
artist = results[0] #That's the artist you're looking for, next ones will be considered as "Similar Artists"
print(artist.name) #Correct name of the artist
print(artist.id) #Returns Artist's ID
print(artist.profile) #Returns brief descritption
print(artist.members[0].name) #Returns the first member (alfabetically) and tells you if is still active
print(artist.releases[0].title) #Returns the name of the first release

#Search an Album
results = dgs.search('Its album time', type='master')
album = results[0]
for el in album.styles:
    print(el)
for el in album.genres:
    print(el)
print(album.title) #returns album name
print(album.main_release) #returns Release Object
print(album.id) #returns album ID
#print(album.lowest_price) #returns lowest_price

for el in album.tracklist:
    print('#' + str(el.position) + ': ' + str(el.title) + ', ' + str(el.duration))
'''
def stringsComparison(realName, idealName):
    listI = idealName.split()
    listR = realName.split()
    x = 0.0
    if len(listI) != len(listR):
        print("Error, different length!")
    else:
        numSplits = len(listI)
        i = errors = 0
        for el in listR:
            if el != listI[i]:
                errors += 1
            i += 1
        x = float(((numSplits - errors)*100)/numSplits)
    return x
        


#Search a song
results = dgs.search(artist='Todd Terje', title='its album time', track='Swing Star (Part 1)')
#results = dgs.search('its album time', type='release')
cosa = results[0]
print(cosa.title)

songNameOLD = 'Swing Star (Part 1)'
results = dgs.search(title='its album time', type='release', format='album')
albumDgs = results[0]
albumName = str(albumDgs.title).partition(' - ')[2]
print(albumName)


realName = songNameOLD.lower()
j = 0
tracklistPercentages = []
maxIndex = -1
maxX = -1
for track_el in albumDgs.tracklist:
    tracklistPercentages.append(stringsComparison(realName, str(track_el.title).lower()))
    if tracklistPercentages[j] > maxX:
        maxX = tracklistPercentages[j]
        maxIndex = j
    j += 1
print(tracklistPercentages)
songName = albumDgs.tracklist[maxIndex].title
print('A fronte di \'' + songNameOLD + '\' è stato scelto il brano: \'' + songName + '\'')



    

'''
for track_el in album.tracklist:
    if str(track_el.title).lowercase() == songName
'''
