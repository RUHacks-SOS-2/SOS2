#My goal: match a student-senior pair using information from database
#This match will be hard-coded
import math
import requests
import json
from google.cloud import firestore

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()


##_____________ PART ONE INPUTTNG USER INFO INTO FIRESTORE DATABASE
newSeniorFile = open("newSenior.txt", 'r')

#YOU WILL NEED TO ADD ANOTHER DATASET TO HAVE BOTH SENIOR AND STUDENT LOCATIONS...RN THEYRE BOTH AT THE SAME ADDRESS
data = {
    u'nameFirst' : newSeniorFile.readline() ,
    u'nameLast' : newSeniorFile.readline(),
    u'age' : newSeniorFile.readline(),
    u'addressStreetName' : newSeniorFile.readline(),
    u'postalCode'
    u'need1' : newSeniorFile.readline()

}
db.collection(u'seniors').document(u'sSenor').set(data)
print("Document successfully uploaded to the database.")


##_________________PARTTWO

URL = "https://maps.googleapis.com/maps/api/directions/json"
API_KEY = "AIzaSyAyZXTl4SzfMi8nHwxghSbotXtKO2hafX0"
#parameters = {"origin":"u'addressStreetName", "destination":"u'addressStreetName", "key":API_KEY, "region": "toronto"}
parameters = {"origin": "130 Victoria St Toronto", "destination": "325 Victoria Street Toronto", "key":API_KEY, "region": "Ontario", "mode": "walking"}

##for latitude/longitude
def latLongVolun():
    response = requests.get(url=URL, params=parameters)
    res = response.json()
    print("")
    print("\t travel duration: " + res["routes"][0]["legs"][0]["duration"]["text"])
    latStud = res["routes"][0]["legs"][0]["start_location"]["lat"]
    longStud = res["routes"][0]["legs"][0]["start_location"]["lng"]
    return latStud,longStud

def latLongSenior():
    response = requests.get(url=URL, params=parameters)
    res = response.json()
    print("")
    print("\t time of arrival: " + res["routes"][0]["legs"][0]["duration"]["text"])
    latSen = res["routes"][0]["legs"][0]["end_location"]["lat"]
    longSen = res["routes"][0]["legs"][0]["end_location"]["lng"]
    return latSen,longSen

def haversineFunction(lat1, lat2, lon1, lon2):
    radius = 6378.137  # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180;
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(lat1 * math.pi / 180) * math.cos(
        lat2 * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
    distance = radius * c * 1000
    return distance

#actual use of lat/long functions
[latStud,longStud]=latLongVolun()
[latSen,longSen]=latLongSenior()

dist = haversineFunction(latSen,latStud,longSen,longStud) #haversine distance

#saving obtained lats and longs
db.collection(u'seniors').document(u'sSenor').set({
    u'latitude' : latSen,
    u'longitude' : longSen
}, merge=True)

#range finder
availabilityRange = 1000
if availabilityRange > dist:
    print("(output to user)\nThis is a suitable Match!\nYou have been matched with Johnny Kid.")


#THE ENDDDDDDDDDDDD


"""
function measure(lat1, lon1, lat2, lon2){  // generally used geo measurement function
    var  = 6378.137;
    var dLat = lat2 * Math.PI / 180 - lat1 * Math.PI / 180;
    var dLon = lon2 * Math.PI / 180 - lon1 * Math.PI / 180;
    var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon/2) * Math.sin(dLon/2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c;
    return d * 1000; // meters
"""""
#Haversine formula for calculating distance

"""
data = {
    u'nameFirst' : u'Adam',
    u'nameLast' : u'Grant',
    u'age' : 75,
    u'addressStreetNumber' : 14,
    u'addressStreetName' : "Henry Street",
    u'need1' : 'groceries',
    u'need2' : 'laundry' ,
    u'latitude' : 43.656767,
    u'longitude' : -79.393780
}

senior_ref = db.collection(u'seniors').document(u'jSmith')

senior_ref.set({
    u'nameFirst' : u'James',
    u'nameLast' : u'Smith',
    u'age' : 87,
    u'addressStreetNumber' : 350,
    u'addressStreetName' : "Victoria Street",
    u'need1' : 'groceries',
    u'need2' : 'Dog Walking' ,
})
#    u'latitude' : 43.657549,
#    u'longitude' : -79.393780

student_ref = db.collection(u'students').document(u'jKid')

student_ref.set({
    u'nameFirst': u'Johnny',
    u'nameLast': u'Kid',
    u'age': 14,
    u'addressStreetNumber': 320,
    u'addressStreetName': "Victoria Street",
    u'availabilityRange' : 15 #UNITS = KM. UNSURE OF HOW THIS WOULD TRANSLATE INTO THE MAPS.API
})
"""


# Add a new doc in collection 'cities' with ID 'LA'
#db.collection(u'seniors').document(u'aGrant').set(data)

#users_ref = db.collection(u'seniors')
#docs = users_ref.stream()

#for doc in docs:
#    print(u'{} => {}'.format(doc.id, doc.to_dict()))
