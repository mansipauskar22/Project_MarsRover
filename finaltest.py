from pymongo import MongoClient
import requests
import json
import pprint
import matplotlib.pyplot as plt

client = MongoClient()
db=client.nasa
Y = []
X = []

rov = input('Choose the rover out of the three:\n Curiosity \n Opportunity \n Spirit \n')
print(rov)

if rov == 'Curiosity':
    cam = input('Choose the camera out of the 7 given below:\n FHAZ \n RHAZ \n MAST \n MAST \n CHEMCAM \n MAHLI \n MARDI \n NAVCAM \n')
    print(cam)
    print('Choose a sol range between 0 to 1660:')
    SS = input('Start Sol :')
    ES = input('End Sol :') 
elif rov == 'Opportunity':
    cam = input('Choose the camera out of the 5 given below:\n FHAZ \n RHAZ \n MAST \n PANCAM \n MINITES \n')
    print(cam)
    print('Choose a sol range between 1 to 4650:')
    SS = input('Start Sol :')
    ES = input('End Sol :') 
elif rov == 'Spirit':
    cam = input('Choose the camera out of the 5 given below:\n FHAZ \n RHAZ \n MAST \n PANCAM \n MINITES \n')
    print(cam)
    print('Choose a sol range between 1 to 2208:')
    SS = input('Start Sol :')
    ES = input('End Sol :') 
else:
    print('Invalid Entry')

SS=int(SS)
ES=int(ES)+1

for i in range(SS , ES):
    check = db.MARS.count({"rover.name":rov , "sol" : i})
    print(check)
    if check == 0:
        url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/{}/photos?sol={}&api_key=a9SQ4PQJPy1YoYFg5Ow9slZprx6DaKbcju0bOjq7'.format(rov,i)
        print(url)
        response = requests.get(url)
        data = response.json()
        l=len(data['photos'])
        print(l)

        if l != 0:
            db.MARS.insert_many(data['photos'])
            tmp=db.MARS.find()
            print(tmp.count(with_limit_and_skip=False))
        else:
            db.MARS.insert({"rover":{"name":rov},"sol":i})
        number = db.MARS.count({"rover.name": rov , "camera.name": cam , "sol": i})
        print(number)
        Y.append(number)
        X.append(i)
    else:
        number = db.MARS.count({"rover.name": rov , "camera.name": cam , "sol": i})
        print(number)
        Y.append(number)
        X.append(i)

print(Y)
print(X)

plt.plot(X, Y)
plt.show()

del Y[:]
del X[:]


    
