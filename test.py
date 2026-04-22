# # import module
# from geopy.geocoders import Nominatim

# # initialize Nominatim API
# geolocator = Nominatim(user_agent="geoapiExercises")


# # Latitude & Longitude input
# Latitude = "25.594095"
# Longitude = "85.137566"

# location = geolocator.reverse(Latitude+","+Longitude)

# address = location.raw['address']

# # traverse the data
# city = address.get('city', '')
# state = address.get('state', '')
# country = address.get('country', '')
# code = address.get('country_code')
# zipcode = address.get('postcode')
# print('City : ', city)
# print('State : ', state)
# print('Country : ', country)
# print('Zip Code : ', zipcode)


# import serial


# def readserial(comport, baudrate):

#     ser = serial.Serial(comport, baudrate, timeout=0.1)         # 1/timeout is the frequency at which the port is read

#     while True:
#         data = ser.readline().decode().strip()
#         if data:
#             print(data)


# if __name__ == '__main__':

#     readserial('COM3', 9600)

import serial
import time
ser = serial.Serial('COM3',9600, timeout=0.1)
print("connection established")
s = [0]
print("got s value")
read_serial=ser.readline()
time.sleep(5) 
s[0] = ser.readline().decode('utf-8').rstrip()
print(s[0].split(","))
val = s[0].split(",")   
tempval = val[0]
humval = val[1]
moistval = val[2]