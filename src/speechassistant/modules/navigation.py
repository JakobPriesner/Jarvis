import re
import googlemaps

SECURE = True

# Beschreibung
"""
Dieses Modul fragt die Distanz und Fahrzeit zwischen zwei Orten von Google Maps ab.
"""


# Python Client Library: https://github.com/googlemaps/google-maps-services-python
# Requirements: pip install -U googlemaps
# API Doc: https://developers.google.com/maps/documentation/distance-matrix/intro
# HTTP-Request: https://maps.googleapis.com/maps/api/distancematrix/json?origins=<>&destinations=<>&language=de&key=<>


def isValid(text):
    text = text.lower()
    if ("wie weit" in text or "wie lang" in text) and (
        "von" in text and ("bis" in text or "nach" in text)
    ):
        return True
    else:
        return False


def handle(text, core, skills):
    text = text.lower()
    length = len(text)

    gmaps = googlemaps.Client(key="AIzaSyB_zhlP1qX-Nfhgigp6C2TPpUlDfdXW_vA")

    # get locations
    matchLocations = re.search("von", text)
    if matchLocations != None:
        startLocations = matchLocations.end() + 1
        locations = text[startLocations:length]

        matchMiddle = re.search("(bis|nach)", text)
        if matchMiddle != None:
            startMiddle = matchMiddle.start() - 1
            endMiddle = matchMiddle.end() + 1

    origin = text[startLocations:startMiddle]
    destination = text[endMiddle:length]

    # get distance and duration
    directions_result = gmaps.distance_matrix(origin, destination, language="de")

    durationTxt = directions_result["rows"][0]["elements"][0]["duration"]["text"]
    distanceTxt = directions_result["rows"][0]["elements"][0]["distance"]["text"]

    match = re.search("km", distanceTxt)
    if match != None:
        endNumber = match.start() - 1
        distanceTxt = distanceTxt[0:endNumber]

        distance = float(re.sub(",", ".", distanceTxt))

    core.say(
        "Von "
        + origin
        + " nach "
        + destination
        + " sind es "
        + distanceTxt
        + " Kilometer. Die Fahrt dauert "
        + durationTxt
    )


class Core:
    def __init__(self):
        pass

    def say(self, text):
        print(text)


if __name__ == "__main__":
    core = Core()
    while True:
        handle(input(), core, None)
