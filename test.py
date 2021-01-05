import requests
import json

with open('doctors.json') as json_file:
    data = json.load(json_file)

n_data = data['Doctor']

for x in n_data:
    if (x == "pediatrician"):
        d = n_data[x]

for y in d:
    if(y['Zip Code']==60165):
        doctor = y
# print(n_data)

print(n_data['pediatrician'][len(n_data['pediatrician'])-1])

# print(doctor)
