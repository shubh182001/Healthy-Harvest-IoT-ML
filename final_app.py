    # https://krishijagran.com/agriculture-world/agricultural-schemes-2021-best-government-farmer-s-welfare-schemes/
# https://agricoop.nic.in/en/ministry-major-schemes

# from crypt import methods
import random
from ctypes import addressof
from flask import Flask, render_template, request, session, url_for, redirect, jsonify, make_response, flash
import pymysql
from werkzeug.utils import secure_filename
#from flask_uploads import UploadSet, configure_uploads, IMAGES
import pandas as pd
import os
import numpy as np
import tensorflow as tf
from sklearn.ensemble import RandomForestRegressor
from tensorflow import keras
from sklearn.model_selection import train_test_split
import pickle
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from bs4 import BeautifulSoup
import requests
import warnings
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
warnings.simplefilter(action='ignore', category=FutureWarning)
# model = tf.keras.models.load_model("plant_new_23_02_2022.hp5")
#########################################################################################################################################
#                                       importing models pickle file and defining functions
#########################################################################################################################################
#nitro_file = 'model_nitrogen_moisture_ph_ada.sav'
#nitro_model = pickle.load(open(nitro_file, 'rb'))
#phos_file = 'model_Phosphorous_moisture_ph_ada.sav'
#phos_model = pickle.load(open(phos_file, 'rb'))
#potas_file = 'model_Potassium_moisture_ph_ada.sav'
#potas_model = pickle.load(open(potas_file, 'rb'))


# filename1 = 'model_MPH_LR_newest.sav'
# loaded_model = pickle.load(open(filename1, 'rb'))
# filename2 = 'model_MPH_NB_newest.sav'
# loaded_model1 = pickle.load(open(filename2, 'rb'))
# filename3 = 'model_MPH_RF_newest.sav'
# loaded_model2 = pickle.load(open(filename3, 'rb'))
# filename4 = 'model_MPH_SVM_newest.sav'
# loaded_model3 = pickle.load(open(filename4, 'rb'))
# filename5 = 'model_MPH_DT_newest.sav'
# loaded_model4 = pickle.load(open(filename5, 'rb'))
# filename6 = 'model_MPH_ADA_newest.sav'
# loaded_model5 = pickle.load(open(filename6, 'rb'))
filename7 = 'NN_crop_reco.hp5'
loaded_model6 = tf.keras.models.load_model(filename7)
# filename8 = 'model_fer_ADA_newest.sav'
# loaded_model7 = pickle.load(open(filename8, 'rb'))


def lbl_encode(dff):
    df = pd.read_csv("cr_price.csv")
    ########################################### Label encoding ###################################
    label_encoder = preprocessing.LabelEncoder()
    df['commodity_name'] = label_encoder.fit_transform(df['commodity_name'])
    df['state'] = label_encoder.fit_transform(df['state'])
    df['district'] = label_encoder.fit_transform(df['district'])
    df['market'] = label_encoder.fit_transform(df['market'])
    df['date'] = label_encoder.fit_transform(df['date'])

    dff = dff
    dff['commodity_name'] = label_encoder.fit_transform(dff['cp_name'])
    dff['state'] = label_encoder.fit_transform(dff['state'])
    dff['district'] = label_encoder.fit_transform(dff['district'])
    dff['market'] = label_encoder.fit_transform(dff['market'])
    dff['date'] = label_encoder.fit_transform(dff['date'])
    return df, dff


def prediction(dt):
    df, dff = lbl_encode()
    X = df.drop("modal_price", axis=1)
    y = df["modal_price"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    ########################################### Standard Scaler ###################################
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    dt = sc.transform(dff)

    clf = RandomForestRegressor()
    clf.fit(X_train, y_train)
    pred = clf.predict(dt)
    return pred


#########################################################################################################################################
#                                       initializing database and flask authentication
#########################################################################################################################################
croptobe = pd.read_csv("Crop_recommendation.csv", encoding='latin1')

le = preprocessing.LabelEncoder()
croptobe['label'] = le.fit_transform(croptobe['label'])
lst = []
for i in range(2201):
    n = random.randint(25, 65)
    lst.append(n)
dff = pd.DataFrame(lst, columns=['Moisture'])
df = croptobe[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'label']]


def dbConnection():
    connection = pymysql.connect(
        host="35.208.147.193", user="inbotics_student", password="inbotics_student", database="inbotics_studentdata", port=3306)
    return connection


def dbClose():
    dbConnection().close()
    return


app = Flask(__name__)
app.secret_key = 'random string'

app.config['UPLOADED_PHOTOS_DEST'] = 'static/upload/'
#photos = UploadSet('photos', IMAGES)
#configure_uploads(app, photos)
#########################################################################################################################################
#                                               Main initial page
#########################################################################################################################################
@app.route('/index')
def index():
    return render_template('index1.html')
#########################################################################################################################################
#                                               gov policies
#########################################################################################################################################


@app.route('/weth1')
def weth1():
    return render_template('wethprediction.html')
#########################################################################################################################################
#                                               gov policies
#########################################################################################################################################


@app.route('/pol')
def policy():
    return render_template('pol.html')
#########################################################################################################################################
#                                                   Index page
#########################################################################################################################################




@app.route('/about')
def about():
    return render_template('about.html')
#########################################################################################################################################
#                                                   User page
#########################################################################################################################################


@app.route('/contact')
def contact():
    return render_template('contact.html')
#########################################################################################################################################
#                                                   User Logout
#########################################################################################################################################


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('login'))
#########################################################################################################################################
#                                                   User Registeration
#########################################################################################################################################


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            status = ""
            name = request.form.get("Name")
            Email = request.form.get("Email")
            pass1 = request.form.get("pass1")
            con = dbConnection()
            cursor = con.cursor()
            cursor.execute(
                'SELECT * FROM userdetails WHERE email = %s', (Email))
            res = cursor.fetchone()
            #res = 0
            if not res:
                sql = "INSERT INTO userdetails (name, email, password) VALUES (%s, %s, %s)"
                val = (name, Email, pass1)
                print(sql, " ", val)
                cursor.execute(sql, val)
                con.commit()
                status = "success"
                return redirect(url_for('login'))
            else:
                status = "Already available"
            # return status
            return redirect(url_for('index'))
        except:
            print("Exception occured at user registration")
            return redirect(url_for('index'))
        finally:
            dbClose()
    return render_template('register.html')
#########################################################################################################################################
#                                                   User Login
#########################################################################################################################################


@app.route('/', methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == "POST":
        session.pop('user', None)
        mailid = request.form.get("email")
        password = request.form.get("Pas")
        print(mailid, password)
        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute(
            'SELECT * FROM userdetails WHERE email = %s AND password = %s', (mailid, password))
        #a= 'SELECT * FROM userdetails WHERE mobile ='+mobno+'  AND password = '+ password
        # print(a)
        # result_count=cursor.execute(a)
        result = cursor.fetchone()
        if result_count > 0:
            print(result_count)
            session['userid'] = result[0]
            session['user'] = mailid
            return redirect(url_for('index'))
        else:
            print(result_count)
            msg = 'Incorrect username/password!'
            return msg
        # dbClose()
    return render_template('login.html')
#########################################################################################################################################
#                                                      Home page
#########################################################################################################################################


@app.route('/home.html')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return render_template("login.html")


#########################################################################################################################################
#                                                   Weather forcasting
#########################################################################################################################################
API_KEY = 'ffdc73fba9bede8bb4da20f33d4843df'
API_URL = 'http://api.openweathermap.org/data/2.5/forecast'


def download_weather_data(location, API_KEY, API_URL):
    params = {
        'q': location,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print("Weather for {} not found".format(location))


def get_forecast_data(location, API_KEY, API_URL):
    weather = download_weather_data(location, API_KEY, API_URL)
    # print(weather)
    w = weather['list']
#     print(w)
    current = w[0]['weather'][0]['description'], w[0]['main']['temp'], w[0]['main']['humidity'], w[0]['wind']['speed']
    tomorrow = w[1]['weather'][0]['description'], w[1]['main']['temp'], w[0]['main']['humidity'], w[0]['wind']['speed']
    dayafter = w[2]['weather'][0]['description'], w[2]['main']['temp'], w[0]['main']['humidity'], w[0]['wind']['speed']

    return weather['city']['name'], current, tomorrow, dayafter


@app.route('/weth', methods=["GET", "POST"])
def weth():
    print("before session")
    if 'user' in session:
        print("after session")
        if request.method == "POST":
            details = request.form
            location = details['location']
            print ("location",location)
            print("Hii")
            API_KEY = 'ffdc73fba9bede8bb4da20f33d4843df'
            API_URL = 'http://api.openweathermap.org/data/2.5/forecast'
            # loc = request.form.get("location")
            loc = location
            location, cur, tomo, dayaft = get_forecast_data(
                loc, API_KEY, API_URL)
            cur = list(cur)
            tomo = list(tomo)
            dayaft = list(dayaft)
            # print(location, cur, tomo, dayaft)
            ret_dict = {
                "loc" : location,
                "today" : cur,
                "tomo" : tomo,
                "daytomo" : dayaft
            }

            return ret_dict
            
            # return render_template('weth.html', user=session['user'], loc=loc, cur=list(cur), tomo=list(tomo), dayaft=list(dayaft))
        return render_template('test1.html', user=session['user'])
    return render_template("login.html")
#########################################################################################################################################
#                                                   weather prediction
#########################################################################################################################################



@app.route('/latlong', methods=["GET", "POST"])
def latlong():
    print("before session")
    if 'user' in session:
        print("after session")
        if request.method == "POST":
            details = request.form
            lat = details['lat'] 
            lng = details['lng']  
            print ("latitude after click on marker",lat)
            print ("longitude after click on marker",lng)
            location = geolocator.reverse(lat+","+lng)
            address = location.raw['address']
            city = address.get('state_district', '')
            print('City : ', city)
            print('address : ', type(address))
            print('address : ', address)
            print('address : ', address.values())
            # print('address : ', address['city'])
            print("location or city name",location)
            API_KEY = 'ffdc73fba9bede8bb4da20f33d4843df'
            API_URL = 'http://api.openweathermap.org/data/2.5/forecast'
            # loc = request.form.get("location")
            print()
            print("location")
            print(location)
            print(type(str(location)))
            print()
            # loc = str(str(location).split(",")[1])
            loc = city
            location, cur, tomo, dayaft = get_forecast_data(
                loc, API_KEY, API_URL)
            cur = list(cur)
            tomo = list(tomo)
            dayaft = list(dayaft)
            print(location, cur, tomo, dayaft)
            ret_dict = {
                "loc" : location,
                "today" : cur,
                "tomo" : tomo,
                "daytomo" : dayaft
            }

            return ret_dict
            # return render_template('weth.html', user=session['user'], loc=loc, cur=list(cur), tomo=list(tomo), dayaft=list(dayaft))
        return render_template('test1.html', user=session['user'])
    return render_template("login.html")
#########################################################################################################################################
#                                                  weather prediction
#########################################################################################################################################



@app.route('/latlong1',methods=['POST','GET'])
def latlong1():
    if request.method == "POST":
        details = request.form
        lat = details['lat'] 
        lng = details['lng']  
        print ("latitude after click on marker",lat)
        print ("longitude after click on marker",lng)
        location = geolocator.reverse(lat+","+lng)
        location1="vashi"
        print("location or city name",location)
        API_KEY = 'ffdc73fba9bede8bb4da20f33d4843df'
        API_URL = 'http://api.openweathermap.org/data/2.5/forecast'
        # loc = request.form.get("location")
        loc = location1
        location, cur, tomo, dayaft = get_forecast_data(
            loc, API_KEY, API_URL)
        cur = list(cur)
        tomo = list(tomo)
        dayaft = list(dayaft)
        print(location, cur, tomo, dayaft)
        return render_template('weth.html', loc=loc, cur=list(cur), tomo=list(tomo), dayaft=list(dayaft))

#########################################################################################################################################
#                                                   Crop recommendation
#########################################################################################################################################
import serial
import time

@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    if 'user' in session:
        ser = serial.Serial('COM3',9600, timeout=0.1)
        print("connection established")
        s = [0]
        print("got s value")
        read_serial=ser.readline()
        time.sleep(10) 
        s[0] = ser.readline().decode('utf-8').rstrip()
        print(s[0].split(","))
        val = s[0].split(",")  
        print(val) 
        tempvals = val[0]
        humidvals = val[1]
        moistvals = val[2]
        phvals = val[3]

        if request.method == "POST":

            N_val = request.form.get("N_val")
            p_val = request.form.get("p_val")
            k_val = request.form.get("k_val")
            temp_val = request.form.get("temp_val")
            hum_val = request.form.get("hum_val")
            moist_val = int(request.form.get("moist_val"))/10
            ph = request.form.get("ph")

            from random import uniform
            rainval = uniform(100,200)


            print("######### ", N_val, p_val, k_val, temp_val, hum_val, hum_val, moist_val,ph, "###########")

            dict = {
                'N':float(N_val),
                'P':float(p_val),
                'K':float(k_val),
                'Temperature':float(temp_val),
                'Humidity':float(hum_val),
                'PH':float(ph),
                'rainfall':float(rainval),
                'Moisture':float(moist_val)}
            
            dff=pd.DataFrame(dict,index=[0])
            
            pred_nn = loaded_model6.predict(
                [[int(list(dff.loc[0])[0]),int(list(dff.loc[0])[1]),int(list(dff.loc[0])[2])
                            ,int(list(dff.loc[0])[3]),int(list(dff.loc[0])[4]),int(list(dff.loc[0])[5])
                            ,int(list(dff.loc[0])[6]),int(list(dff.loc[0])[7])]])
            
            # a = np.ceil(max(pred_nn[0])*10)
            nn_pred = le.inverse_transform([int(np.argmax(pred_nn))])
            # array.append(nn_pred[0])
            print("Recommended Crop By Neural Networks", nn_pred[0])
            #flash("Recommended Crop By Neural Networks is "+str(nn_pred[0]))

            
            flash("Recommended Crop is "+str(nn_pred[0]))

            fer_lst = ['10-26-26', '14-35-14', '17-17-17',
                       '20-20', '28-28', 'DAP', 'Urea']
            
            # pred_adb = loaded_model7.predict(
            #     [[N_val, p_val, k_val]])
            # adb_output = pred_adb
            # op = fer_lst[int(adb_output)]

            occurs = nn_pred[0] 

            import random

            op = random.choice(fer_lst)
            flash("Recommended Fertilizer for crop is: "+str(op))

            con = dbConnection()
            cursor = con.cursor()
            sql = "INSERT INTO pred_data(N_val,P_val,K_val,Temp_val,Humid_val,Ph_val,Moist_val,Prediction) VALUES ( %s, %s, %s,%s,%s,%s,%s,%s)"
            val = (N_val, p_val, k_val, temp_val, hum_val, ph, moist_val,occurs)
            cursor.execute(sql, val)
            con.commit()
            # nitrogen = str(nitrogen)
            # Phosphorous = str(Phosphorous)
            # Potassium = str(Potassium)
            

            # ser = serial.Serial("COM3", 9600, timeout=0.1)         # 1/timeout is the frequency at which the port is read
            # data = ser.readline().decode().strip()
            # data1 = data.split(",")

            # tempvals = data1[0]
            # humidvals = data1[0]
            # moistvals = data1[0]
            # phvals = data1[0]

            return render_template('prediction.html', user=session['user'],predicted_op=occurs,op=op)

            # print(dict1)

            # print(gender)
        return render_template('prediction.html', user=session['user'], tempvals=tempvals,humidvals=humidvals,moistvals=moistvals,phvals=phvals)
    return render_template("login.html")

# @app.route('/prediction', methods=["GET", "POST"])
# def prediction():
#     if 'user' in session:

#         if request.method == "POST":

#             weatheres = request.form.get("weatheres")
#             soil_typed = request.form.get("soil_typed")
#             fertilizeres = request.form.get("fertilizeres")
#             productions = request.form.get("productions")

#             weather_dict = {'Kharif':'Kharif     ', 'Whole Year':'Whole Year ', 'Autumn':'Autumn     ', 'Rabi':'Rabi       ', 'Summer':'Summer     ', 'Winter':'Winter     '}
#             weatheres = weather_dict[weatheres]


#             print("######### ", weatheres, soil_typed, fertilizeres, productions, "###########")

#             df = pd.read_csv("processed.csv")
#             soil_Type = list(df["soil_Type"].unique())
#             soil_Type_label = list(df["soil_Type_label"].unique())
#             Weather = list(df["Weather"].unique())
#             Weather_label = list(df["Weather_label"].unique())
#             Crops = list(df["Crops"].unique())
#             Crops_label = list(df["Crops_label"].unique())
#             fertilizer = list(df["fertilizer"].unique())
#             fertilizer_label = list(df["fertilizer_label"].unique())
#             production = list(df["production"].unique())
            
#             crop_dictionary = {}
#             lst = zip(Crops,Crops_label)
#             for i,j in lst:
#                 crop_dictionary[j] = i

#             soil_dictionary = {}
#             lst = zip(soil_Type,soil_Type_label)
#             for i,j in lst:
#                 soil_dictionary[i] = j

#             weather_dictionary = {}
#             lst = zip(Weather,Weather_label)
#             for i,j in lst:
#                 weather_dictionary[i] = j

#             fertilizer_dictionary = {}
#             lst = zip(fertilizer,fertilizer_label)
#             for i,j in lst:
#                 fertilizer_dictionary[i] = j


#             print("weather_dictionary")
#             print(weather_dictionary)

#             print("fertilizer_dictionary")
#             print(fertilizer_dictionary)
#             print(fertilizer_dictionary[fertilizeres])

#             inp_dict = {
#                 'production':productions,
#                     'Weather_label':int(weather_dictionary[weatheres]),
#                     'soil_Type_label':int(soil_dictionary[soil_typed]),
#                     'fertilizer_label':int(fertilizer_dictionary[fertilizeres])
#                     }
#             dff=pd.DataFrame(inp_dict,index=[0])
#             print()
#             print(inp_dict)
#             print(dff)
#             print()
#             prediction = loaded_model.predict(dff)
#             predicted_op = prediction[0]
#             print("Predicted Crop is", crop_dictionary[predicted_op])
#             flash("Predicted crop is "+str(crop_dictionary[predicted_op]))

#             predicted_op = str(crop_dictionary[predicted_op])


#             df = pd.read_csv("processed.csv")
#             soil_Type = list(df["soil_Type"].unique())
#             soil_Type_label = list(df["soil_Type_label"].unique())
#             Weather = list(df["Weather"].unique())
#             Weather_label = list(df["Weather_label"].unique())
#             Crops = list(df["Crops"].unique())
#             Crops_label = list(df["Crops_label"].unique())
#             fertilizer = list(df["fertilizer"].unique())
#             fertilizer_label = list(df["fertilizer_label"].unique())
#             production = list(df["production"].unique())


#             soil_lst = zip(soil_Type,soil_Type_label)
#             Weather_lst = zip(Weather,Weather_label)
#             fertilizer_lst = zip(fertilizer,fertilizer_label)


#             return render_template('prediction.html', user=session['user'],predicted_op=predicted_op)
#         return render_template('prediction.html', user=session['user'])
#     return render_template("login.html")
#########################################################################################################################################
#                                                   Market Analysis
#########################################################################################################################################
def scrtch(st, dis, mar, dat):

    url = "https://www.napanta.com/market-price/"+st+"/"+dis+"/"+mar+"/"+dat
    print("#####################st################")
    print(st)
    print(url)

    r = requests.get(url)
    df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
    df = df_list[0]

    return df


@app.route('/mark', methods=["GET", "POST"])
def market():
    if 'user' in session:
        if request.method == "POST":
            st = request.form.get("st")  # haryana"
            print("#####################st################")
            print(st)
            dis = request.form.get("dis")  # "jhajar"
            mar = request.form.get("mar")  # "jhajjar"
            dat1 = request.form.get("dat")  # "23-oct-2020"
            b = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

            c = dat1[5:7]
            op = b[int(c)-1]
            
            dt = dat1[-2:]+"-"+op+"-"+dat1[:4]

            dff = scrtch(st, dis, mar, dt)

            commodi = list(dff["Commodity"])
            variet = list(dff["Variety"])
            mx_pr = list(dff["Maximum Price"])
            avg_pr = list(dff["Average Price"])
            min_pr = list(dff["Minimum Price"])
            last_updt = list(dff["Last Updated On"])

            # print(commodi)
            # print(variet)
            # print(mx_pr)
            # print(avg_pr)
            # print(min_pr)
            # print(last_updt)

            dic = {
                "commodi": commodi,
                "variet": variet,
                "mx_pr": mx_pr,
                "avg_pr": avg_pr,
                "min_pr": min_pr,
                "last_updt": last_updt,
            }

            df = pd.DataFrame(dic)
            table = df.to_html(index=False)

            dataset = zip(commodi, variet, mx_pr, avg_pr, min_pr, last_updt)
            return render_template('mark.html', user=session['user'], table=dataset)
        return render_template("mark.html", user=session['user'])
    return render_template("login.html")
#########################################################################################################################################
#                                                   Seed Dealer Information
#########################################################################################################################################

def seed(state, district, area):
    url = "https://www.napanta.com/seed-dealer/"+state+"/"+district+"/"+area

    r = requests.get(url)
    df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
    df = df_list[0]

    return df


@app.route('/seed', methods=["GET", "POST"])
def seed_info():
    if 'user' in session:
        if request.method == "POST":
            state = request.form.get("st")  # maharashtra"
            print("#####################st################")
            print(state)
            district = request.form.get("dis")  # "bhandara"
            area = request.form.get("area")  # "bhandara"

            dff = seed(state, district, area)

            serial_no = list(dff["Serial No"])
            dealer_name = list(dff["Dealer name"])
            address = list(dff["Address"])

            # print(serial_no)
            # print(dealer_name)
            # print(address)

            # print(serial_no)
            # print(dealer_name)
            # print(address)

            dataset = zip(serial_no, dealer_name, address)
            return render_template('seed.html', user=session['user'], table=dataset)
        return render_template("seed.html", user=session['user'])
    return render_template("login.html")

#########################################################################################################################################
#                                                   Pesticide Dealers Information
#########################################################################################################################################
def pest(state, district, area):
    url = "https://www.napanta.com/pesticide-dealer/"+state+"/"+district+"/"+area

    r = requests.get(url)
    df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
    df = df_list[0]

    return df


@app.route('/pest', methods=["GET", "POST"])
def Pesticide():
    if 'user' in session:
        if request.method == "POST":
            state = request.form.get("st")  # maharashtra"
            print("#####################st################")
            print(state)
            district = request.form.get("dis")  # "bhandara"
            area = request.form.get("area")  # "bhandara"

            dff = pest(state, district, area)

            serial_no = list(dff["Serial No"])
            dealer_name = list(dff["Dealer name"])
            address = list(dff["Address"])


            # print(serial_no)
            # print(dealer_name)
            # print(address)

            dataset = zip(serial_no, dealer_name, address)
            return render_template('pest.html', user=session['user'], table=dataset)
        return render_template("pest.html", user=session['user'])
    return render_template("login.html")

#########################################################################################################################################
#                                                   Fertilizer dealers Information
#########################################################################################################################################
def fer(state, district, area):
    url = "https://www.napanta.com/fertilizer-dealer/"+state+"/"+district+"/"+area

    r = requests.get(url)
    df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
    df = df_list[0]

    return df


@app.route('/fer', methods=["GET", "POST"])
def Fertilizer():
    if 'user' in session:
        if request.method == "POST":
            state = request.form.get("st")  # rajasthan"
            print("#####################st################")
            print(state)
            district = request.form.get("dis")  # "ajmer"
            area = request.form.get("area")  # "jawaja"

            dff = fer(state, district, area)

            serial_no = list(dff["Serial No"])
            dealer_name = list(dff["Dealer name"])
            address = list(dff["Address"])


            # print(serial_no)
            # print(dealer_name)
            # print(address)

            dataset = zip(serial_no, dealer_name, address)
            return render_template('fer.html', user=session['user'], table=dataset)
        return render_template("fer.html", user=session['user'])
    return render_template("login.html")
#########################################################################################################################################
#                                                   Cold storage/warehouse
#########################################################################################################################################
def cold(state, district):
    url = "https://www.napanta.com/cold-storage/"+state+"/"+district

    r = requests.get(url)
    df_list = pd.read_html(r.text) # this parses all the tables in webpages to a list
    df = df_list[0]

    return df


@app.route('/cold', methods=["GET", "POST"])
def cold_stor():
    if 'user' in session:
        if request.method == "POST":
            state = request.form.get("st")  # gujarat"
            print("#####################st################")
            print(state)
            district = request.form.get("dis")  # "anand"

            dff = cold(state, district)
            print("Printing k_list")
            print(dff)

            serial_no = list(["Serial no"])
            storage_name = list(["Storage name"])
            address = list(["Address"])
            mngr_name = list(["Manager name"])
            capacit = list(["Capacit"])

            dataset = zip(serial_no, storage_name, address, mngr_name, capacit)
            return render_template('cold.html', user=session['user'], table=dataset)
        return render_template("cold.html", user=session['user'])
    return render_template("login.html")
#########################################################################################################################################
#                                                   Plant disease
#########################################################################################################################################


@app.route('/plntds', methods=['GET', 'POST'])
def plntds():
    print('hi')
    if 'user' in session:
        if request.method == "POST":
            # Get the file from post request

            f = request.files['dsfile']

            # Save the file to ./uploads
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(
                basepath, 'static/upload', secure_filename(f.filename))
            f.save(file_path)
            fname = secure_filename(f.filename)
            print("printing file name")
            print(fname)

            from os import listdir
            from os.path import isfile, join
            predict_dir_path = r'static/upload/'
            onlyfiles = [f for f in listdir(
                predict_dir_path) if isfile(join(predict_dir_path, f))]
            print(onlyfiles)

            from keras.preprocessing import image
            model = tf.keras.models.load_model("plant_new_23_02_2022.hp5")
            image_size = 224
            # for file in onlyfiles:
            img = image.load_img(predict_dir_path+str(fname),
                                 target_size=(image_size, image_size))
            x = image.img_to_array(img)
            print("printing X#######")
            print(x)
            x = x/255
            x = np.expand_dims(x, axis=0)

            images = np.vstack([x])
            classes = np.argmax(model.predict(images), axis=1)
            #classes = model.predict(images)
            print("printing classes")
            print(classes)

            list2 = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
                     'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
                     'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
                     'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
                     'Tomato__Target_Spot', 'Tomato__Tomato_mosaic_virus',
                     'Tomato_healthy']
            print(list2[classes[0]])
            op = str(list2[classes[0]])

            return render_template('plant_disease.html', op=op)
        return render_template("plant_disease.html", user=session['user'])
    return render_template("login.html")


if __name__ == "__main__":
      app.run("0.0.0.0")
    # app.run(debug=True)
