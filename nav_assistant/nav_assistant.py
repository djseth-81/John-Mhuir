import os
import re
import pprint
import googlemaps
from datetime import datetime
from googlemaps import timezone
from googlemaps import directions
from googlemaps import geolocation
from googlemaps import distance_matrix

print ("### DEV NOTES ###")
print("BETA UNIT 2")
print("ACTIVE UNIT")
print("More casual input style")
print("Added travel ammenities and places locator")
print("Place information and Identification ranges from formal/formatted address to coordinates to unique ID. Maybe that needs to be one method")

api_key = "you_key_here" #--> GET YOUR OWN
gmaps = googlemaps.Client(key = api_key)

#Establishing user's geolocation
current_location = gmaps.geolocate()
origin = current_location['location']
accuracy = current_location['accuracy']
where_am_i = gmaps.reverse_geocode(origin)[0]['formatted_address']

#Establishing timezone for units (for some reason)
timespec = None
units = None
if timespec != None:
    time = timespec
else:
    time = datetime.now()
my_timezone = gmaps.timezone(origin,time)
timezone_id = my_timezone['timeZoneId']
if re.search("America",timezone_id) != None:
    units = 'imperial'

else:
    units = 'metric'

print('\nFound you\n')
#find out where the user wants to go
test = 'talk.txt'
optimize_wapoints = False
waypoints = None
places = []
transit_mode = None
car = True
waypoints = None
arrival = None
avoidables = ['tolls']

"""
### LIBRARIAN 2: ELECTRIC BOOGALOO
"""

#find out where the user wants to go
with open(test, 'a+') as file:
    daddy = True
    print("What's your destination? Type done, end, or back to finish.\n")
    while daddy == True:
        string = input("")
        if string == "end" or string == "back" or string == "done": #Terminator keys
            daddy = False
        else:
            file.write(string + '\n')
    #Now we analyze
    file.seek(0,0)
    for line in file:
        line = line.lower().strip('\n')
        line = re.split(' to | then | and | finally ', line)
        for thwap in line:
            if re.search('take me|directions |going |trip ', thwap):
                directions_api = True
            elif re.search('where | is |locate |find ', thwap):
                locator = True
            elif re.search('how far away |how long ', thwap):
                distance_matrix = True
            elif re.search('walk|walking', thwap):
                mode = 'walking'
            elif re.search('subway|tube|underground', thwap):
                mode = 'transit'
                transit_mode = 'subway'
            elif re.search('rail', thwap):
                mode = 'transit'
                transit_mode = 'rail'
            elif re.search('train', thwap):
                mode = 'transit'
                transit_mode = 'train'
            elif re.search('bus', thwap):
                mode = 'transit'
                transit_mode = 'bus'
            else:
                places.append(thwap)
            if re.search('from', thwap):
                thwap = thwap.split()
                index = thwap.index('from')+1
                origin = []
                while index < len(thwap):
                    origin.append(thwap[index])
                    index += 1
                origin = ' '.join(origin)
                print('origin is now {}'.format(origin))

os.remove('talk.txt')
print("Places requested\n{}".format(places))
#Using partials to come up with results; useful for missing locations/data in personal database
for place in places:
    discovery = gmaps.find_place(place,'textquery') #--> Modify to analyze for both phone numbers (input_type = 'phonenumber') and strings (input_tyoe = 'textquery')
    # pprint.pprint(discovery)
    if 'ZERO_RESULTS' in discovery['status']:
        places.remove(place)
pprint.pprint(places)
if len(places) != 0:
    for item in places:
        address = gmaps.geocode(item)[0]['formatted_address'] #Returns user-friendly name
        print("Found {}.".format(address))
        places.remove(item)
        places.append(address)
    if len(places) > 1:
        optimize_wapoints = True
        waypoints = places
        destination = places[-1]
        places.pop(-1)
    else:
        destination = places[0]
        
if directions_api:
    directions_result = gmaps.directions(origin,
                                        destination,
                                        mode='driving',
                                        transit_mode = transit_mode,
                                        units = units,
                                        avoid = avoidables,
                                        waypoints = waypoints,
                                        departure_time = time,
                                        arrival_time=arrival
                                        )

    if len(directions_result) != 0:
        pprint.pprint(directions_result)
    else:
        print('Mode of transportation unavaliable')

if distance_matrix:
    travel_duration = gmaps.distance_matrix(origin, 
                                            destination,
                                            mode = 'driving', 
                                            transit_mode = transit_mode,
                                            units = units,
                                            )

    travel_distance = travel_duration['rows'][0]['elements'][0]['distance']['text']
    travel_time = travel_duration['rows'][0]['elements'][0]['duration']['text']
    print('Distance from {}, to {} is approximately {}'.format(where_am_i,destination,travel_distance))
    print('Travel time is approximately {}'.format(travel_time))
