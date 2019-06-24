import requests
import math

LOCATION = (52.518593, 13.375217)
URL = "https://emmy.frontend.fleetbird.eu/api/prod/v1.06/map/cars/"
# number of scooters that should be displayed
N = 10
G_MAPS = "https://www.google.com/maps/search/?api=1&query={lat},{lon}"


def distance(lat1, lon1, lat2, lon2):
    if (lat1 == lat2) and (lon1 == lon2):
        return 0

    else:
        radlat1 = math.pi * lat1/180
        radlat2 = math.pi * lat2/180
        theta = lon1-lon2
        radtheta = math.pi * theta/180

        dist = math.sin(radlat1) * math.sin(radlat2) + math.cos(radlat1) * math.cos(radlat2) * math.cos(radtheta)
        if dist > 1:
            dist = 1

        dist = math.acos(dist)
        dist = dist * 180/math.pi
        dist = dist * 60 * 1.1515
        dist = dist * 1.609344

        return dist


# sorting function
def sort_by_dist(o):
    """sort by distance to the specified global location LOCATION"""
    return distance(o.get("lat"), o.get("lon"), *LOCATION)


# get all emmy scooters
scooters = requests.get(URL).json()

# sort scooters by distance
closest_scooters = sorted(scooters, key=sort_by_dist)

# print the N closest scooters if available
for i, closest_scooter in enumerate(closest_scooters):
    if i < N:
        print(closest_scooter.get("licencePlate"), ":", closest_scooter.get("address"),
              G_MAPS.format(lat=closest_scooter.get("lat"), lon=closest_scooter.get("lon")))
    else:
        break
