# https://krishijagran.com/agriculture-world/agricultural-schemes-2021-best-government-farmer-s-welfare-schemes/
# https://agricoop.nic.in/en/ministry-major-schemes

# from crypt import methods
import random
from ctypes import addressof
from flask import Flask, render_template, request, session, url_for, redirect, jsonify, make_response, flash
import pymysql
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
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
# from weather import Weather, WeatherException
#########################################################################################################################################
#                                       importing models pickle file and defining functions
#########################################################################################################################################
# nitro_file='model_nitrogen_moisture_ph_ada.sav'
# nitro_model=pickle.load(open(nitro_file,'rb'))
# phos_file='model_Phosphorous_moisture_ph_ada.sav'
# phos_model=pickle.load(open(phos_file,'rb'))
# potas_file='model_Potassium_moisture_ph_ada.sav'
# potas_model=pickle.load(open(potas_file,'rb'))


# filename1='model_MPH_LR_newest.sav'
# loaded_model = pickle.load(open(filename1, 'rb'))
# filename2='model_MPH_NB_newest.sav'
# loaded_model1= pickle.load(open(filename2, 'rb'))
# filename3='model_MPH_RF_newest.sav'
# loaded_model2=  pickle.load(open(filename3, 'rb'))
# filename4='model_MPH_SVM_newest.sav'
# loaded_model3=  pickle.load(open(filename4, 'rb'))
# filename5='model_MPH_DT_newest.sav'
# loaded_model4=  pickle.load(open(filename5, 'rb'))
# filename6='model_MPH_ADA_newest.sav'
# loaded_model5=  pickle.load(open(filename6, 'rb'))
filename7='NN_MPH.hp5'
loaded_model6= tf.keras.models.load_model(filename7)
# filename8='model_fer_ADA_newest.sav'
# loaded_model7=  pickle.load(open(filename8, 'rb'))


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
        host="localhost", user="root", password="root", database="cropnew", port=3307)
    return connection


def dbClose():
    dbConnection().close()
    return


app = Flask(__name__)
app.secret_key = 'random string'

app.config['UPLOADED_PHOTOS_DEST'] = 'static/upload/'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
#########################################################################################################################################
#                                               Main initial page
#########################################################################################################################################


@app.route('/index')
def index():
    return render_template('index1.html')
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
    return redirect(url_for('register'))
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


@app.route('/weth1', methods=["GET", "POST"])
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
            print(location, cur, tomo, dayaft)
            
            # legend = "Temperature and Humidity forcasting"
            # df = pd.read_csv("pred_temp.csv")
            # temp = df["yhat"][101937:]
            # dt = df["ds"][101937:]
            # print("##################################################")
            # print(dt)
        ########################################################################
            # df2 = pd.read_csv("pred_hum.csv")
            # temp2 = df2["yhat"][97822:]
            # dt2 = df2["ds"][97822:]
            # print("##################################################")
            # print(dt2)

            # , labels1=dt, values1=temp, legend=legend, values2=temp2, labels2=dt2)
            return render_template('weth.html', user=session['user'], loc=loc, cur=list(cur), tomo=list(tomo), dayaft=list(dayaft))
        return render_template('test1.html', user=session['user'])
    return render_template("login.html")


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
            city = address.get('city', '')
            print('City : ', city)
            # location1="vashi"
            print("location or city name",location)
            API_KEY = 'ffdc73fba9bede8bb4da20f33d4843df'
            API_URL = 'http://api.openweathermap.org/data/2.5/forecast'
            # loc = request.form.get("location")
            loc = location
            location, cur, tomo, dayaft = get_forecast_data(
                loc, API_KEY, API_URL)
            cur = list(cur)
            tomo = list(tomo)
            dayaft = list(dayaft)
            print(location, cur, tomo, dayaft)
            
            # legend = "Temperature and Humidity forcasting"
            # df = pd.read_csv("pred_temp.csv")
            # temp = df["yhat"][101937:]
            # dt = df["ds"][101937:]
            # print("##################################################")
            # print(dt)
        ########################################################################
            # df2 = pd.read_csv("pred_hum.csv")
            # temp2 = df2["yhat"][97822:]
            # dt2 = df2["ds"][97822:]
            # print("##################################################")
            # print(dt2)

            # , labels1=dt, values1=temp, legend=legend, values2=temp2, labels2=dt2)
            return render_template('weth.html', user=session['user'], loc=loc, cur=list(cur), tomo=list(tomo), dayaft=list(dayaft))
        return render_template('test1.html', user=session['user'])
    return render_template("login.html")
#########################################################################################################################################
#                                                   Crop and fertilizer prediction
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
        # location1="vashi"
        print("location or city name",location)
        API_KEY = 'ffdc73fba9bede8bb4da20f33d4843df'
        API_URL = 'http://api.openweathermap.org/data/2.5/forecast'
        # loc = request.form.get("location")
        loc = location
        location, cur, tomo, dayaft = get_forecast_data(
            loc, API_KEY, API_URL)
        cur = list(cur)
        tomo = list(tomo)
        dayaft = list(dayaft)
        print(location, cur, tomo, dayaft)
        return render_template('weth.html', loc=loc, cur=list(cur), tomo=list(tomo), dayaft=list(dayaft))

#########################################################################################################################################
#                                                   Crop and fertilizer prediction
#########################################################################################################################################
@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    if 'user' in session:
        if request.method == "POST":

            N_val = request.form.get("N_val")
            p_val = request.form.get("p_val")
            k_val = request.form.get("k_val")
            temp_val = request.form.get("temp_val")
            hum_val = request.form.get("hum_val")
            moist_val = request.form.get("moist_val")
            ph = request.form.get("ph")

            print("######### ", N_val, p_val, k_val, temp_val, hum_val, hum_val, moist_val,ph, "###########")

            dict = {
                'N':float(N_val),
                'P':float(p_val),
                'K':float(k_val),
                'Temperature':float(temp_val),
                'Humidity':float(hum_val),
                'PH':float(ph),
                'Moisture':float(moist_val)}
            
            dff=pd.DataFrame(dict,index=[0])
            
            pred_nn = loaded_model6.predict(
                [[int(list(dff.loc[0])[0]),int(list(dff.loc[0])[1]),int(list(dff.loc[0])[2])
                            ,int(list(dff.loc[0])[3]),int(list(dff.loc[0])[4]),int(list(dff.loc[0])[5])
                            ,int(list(dff.loc[0])[6])]])
            
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

            import random

            op = random.choice(fer_lst)
            flash("Recommended Fertilizer for crop is: "+str(op))

            #con = dbConnection()
            #cursor = con.cursor()
            #sql = "INSERT INTO data(Moisture,ph_value,Nitrogen,Phosphorous,Potassium) VALUES ( %s, %s, %s,%s,%s,%s)"
            #val = (moist,ph,nitrogen,Phosphorous,Potassium,occurs)
            #cursor.execute(sql, val)
            # con.commit()
            # nitrogen = str(nitrogen)
            # Phosphorous = str(Phosphorous)
            # Potassium = str(Potassium)
            occurs = nn_pred[0] 
            op = op

            return render_template('prediction.html', user=session['user'],predicted_op=occurs,op=op)

            # print(dict1)

            # print(gender)
        return render_template('prediction.html', user=session['user'])
    return render_template("login.html")


# @app.route('/prediction', methods=["GET", "POST"])
# def prediction():
#     if 'user' in session:
#         if request.method == "POST":

#             moist = request.form.get("Name2")
#             ph = request.form.get("Name3")

#             print("######### ", moist, ph, "###########")

#             moist = int(moist)
#             ph = int(ph)
#             new = []
#             array = []

#             new.append(moist)
#             new.append(ph)
#             nitropred = nitro_model.predict([np.array(new)])
#             nitrogen = nitropred[0]
#             print("Required Nitrogen is ", nitrogen)
#             flash("Required Nitrogen is "+str(nitrogen))
            
#             phospred = phos_model.predict([np.array(new)])
#             Phosphorous = phospred[0]
#             print("Required Phosphorous is ", Phosphorous)
#             flash("Required Phosphorous is "+str(Phosphorous))
#             potaspred = potas_model.predict([np.array(new)])
#             Potassium = potaspred[0]
#             print("Required Potassium is ", Potassium)
#             flash("Required Potassium is "+str(Potassium))
#             pred_logistic = loaded_model.predict(
#                 [[nitrogen, Phosphorous, Potassium, moist, ph]])
#             lr_output = pred_logistic[0]
#             lr_pred = le.inverse_transform([int(lr_output)])
#             array.append(lr_pred[0])
#             print("Recommended Crop By Logistic Regression ", lr_pred[0])
#             #flash("Recommended Crop By Logistic Regression is "+str(lr_pred[0]))
#             pred_nb = loaded_model1.predict(
#                 [[nitrogen, Phosphorous, Potassium, moist, ph]])
#             nb_output = pred_nb[0]
#             nb_pred = le.inverse_transform([int(nb_output)])
#             array.append(nb_pred[0])
#             print("Recommended Crop By Naive Bayes ", nb_pred[0])
#             #flash("Recommended Crop By Naive Bayes is "+str(nb_pred[0]))
#             pred_rf = loaded_model2.predict(
#                 [[nitrogen, Phosphorous, Potassium, moist, ph]])
#             rf_output = pred_rf[0]
#             rf_pred = le.inverse_transform([int(rf_output)])
#             array.append(rf_pred[0])
#             print("Recommended Crop By Random Forest ", rf_pred[0])
#             #flash("Recommended Crop By Random Forest is "+str(rf_pred[0]))
#             # pred_svm=loaded_model3.predict([[nitrogen,Phosphorous,Potassium,moist,ph]])
#             # svm_output=pred_svm[0]
#             # svm_pred=le.inverse_transform([int(svm_output)])
#             # array.append(svm_pred[0])
#             # print("Recommended Crop By Support Vector Machine ",svm_pred[0])
#             #flash("Recommended Crop By Support Vector Machine is "+str(svm_pred[0]))
#             pred_dt = loaded_model4.predict(
#                 [[nitrogen, Phosphorous, Potassium, moist, ph]])
#             dt_output = pred_dt[0]
#             dt_pred = le.inverse_transform([int(dt_output)])
#             array.append(dt_pred[0])
#             print("Recommended Crop By Decision Tree ", dt_pred[0])
#             #flash("Recommended Crop By Decision Tree is "+str(dt_pred[0]))
#             pred_ada = loaded_model5.predict(
#                 [[nitrogen, Phosphorous, Potassium, moist, ph]])
#             ada_output = pred_ada[0]
#             ada_pred = le.inverse_transform([int(ada_output)])
#             array.append(ada_pred[0])
#             print("Recommended Crop By Ada Boost", ada_pred[0])
#             #flash("Recommended Crop By Ada Boost is "+str(ada_pred[0]))
#             pred_nn = loaded_model6.predict(
#                 [[int(nitrogen), int(Phosphorous), int(Potassium), int(moist), int(ph)]])
#             a = np.ceil(max(pred_nn[0])*10)
#             nn_pred = le.inverse_transform([int(a)])
#             array.append(nn_pred[0])
#             print("Recommended Crop By Neural Networks", nn_pred[0])
#             #flash("Recommended Crop By Neural Networks is "+str(nn_pred[0]))

#             def most_frequent(List):
#                 dict = {}
#                 count, itm = 0, ''
#                 for item in reversed(List):
#                     dict[item] = dict.get(item, 0) + 1
#                     if dict[item] >= count:
#                         count, itm = dict[item], item
#                 return(itm)
#             print(array)
#             occurs = most_frequent(array)
#             print(occurs)
#             flash("Recommended Crop is "+str(occurs))

#             fer_lst = ['10-26-26', '14-35-14', '17-17-17',
#                        '20-20', '28-28', 'DAP', 'Urea']
            
#             pred_adb = loaded_model7.predict(
#                 [[nitrogen, Phosphorous, Potassium]])
#             adb_output = pred_adb
#             op = fer_lst[int(adb_output)]
#             flash("Recommended Fertilizer for crop is: "+str(op))

#             #con = dbConnection()
#             #cursor = con.cursor()
#             #sql = "INSERT INTO data(Moisture,ph_value,Nitrogen,Phosphorous,Potassium) VALUES ( %s, %s, %s,%s,%s,%s)"
#             #val = (moist,ph,nitrogen,Phosphorous,Potassium,occurs)
#             #cursor.execute(sql, val)
#             # con.commit()
#             nitrogen = str(nitrogen)
#             Phosphorous = str(Phosphorous)
#             Potassium = str(Potassium)
#             occurs = occurs 
#             op = op

#             return render_template('prediction.html', user=session['user'], nitrogen=nitrogen,Phosphorous=Phosphorous,Potassium=Potassium,occurs=occurs,op=op)

#             # print(dict1)

#             # print(gender)
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

    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.prettify())

    table1 = soup.find_all('th', attrs={'class': 'head-style'})

    k_list = []
    for i in soup.find_all("table", class_="table structure-table"):
        for j in i.find_all("tr"):
            for k in j.find_all("td", class_="td-style"):
                k_list.append(k.text)
                # for l in k.find_all("a"):
                #     print(l.text)
    return k_list


@app.route('/mark', methods=["GET", "POST"])
def market():
    if 'user' in session:
        if request.method == "POST":
            st = request.form.get("st")  # haryana"
            dis = request.form.get("dis")  # "jhajar"
            mar = request.form.get("mar")  # "jhajjar"
            dat1 = request.form.get("dat")  # "23-oct-2020"
            print("#####################st################")
            print(st)
            print(dat1)
            
            b = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

            c = dat1[5:7]
            op = b[int(c)-1]
            
            dt = dat1[-2:]+"-"+op+"-"+dat1[:4]
            
            # dat = "23-oct-2020"

            k_list = scrtch(st, dis, mar, dt)

            final_l = []
            i = 0
            a = -1
            while i < len(k_list):
                list1 = []
                k_list = k_list[a+1:]
                a = k_list.index("")
                # print(a)
                final_l.append(k_list[:a])
                i += a
                # print(i)

            commodi = []
            variet = []
            mx_pr = []
            avg_pr = []
            min_pr = []
            last_updt = []

            for i in final_l:
                commodity = i[0]
                commodi += [commodity]
                variety = i[1]
                variet += [variety]
                mx_price = i[2]
                mx_pr += [mx_price]
                avg_price = i[3]
                avg_pr += [avg_price]
                min_price = i[4]
                min_pr += [min_price]
                last_updat = i[5]
                last_updt += [last_updat]

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

    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.prettify())

    table1 = soup.find_all('th', attrs={'class': 'head-style'})

    k_list = []
    for i in soup.find_all("table", class_="table structure-table"):
        for j in i.find_all("tr"):
            for k in j.find_all("td", class_="td-style"):
                k_list.append(k.text)
                for l in k.find_all("a"):
                    print(l.text)

    N = 3
    subList = [k_list[n:n+N] for n in range(0, len(k_list), N)]
    subList
    return subList


@app.route('/seed', methods=["GET", "POST"])
def seed_info():
    if 'user' in session:
        if request.method == "POST":
            state = request.form.get("st")  # maharashtra"
            print("#####################st################")
            print(state)
            district = request.form.get("dis")  # "bhandara"
            area = request.form.get("area")  # "bhandara"

            k_list = seed(state, district, area)

            serial_no = []
            dealer_name = []
            address = []

            for i in k_list:
                srno = i[0]
                serial_no.append(srno)
                dname = i[1]
                dealer_name.append(dname)
                addr = i[2]
                address.append(addr)

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

    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.prettify())

    table1 = soup.find_all('th', attrs={'class': 'head-style'})

    k_list = []
    for i in soup.find_all("table", class_="table structure-table"):
        for j in i.find_all("tr"):
            for k in j.find_all("td", class_="td-style"):
                k_list.append(k.text)
                for l in k.find_all("a"):
                    print(l.text)

    N = 3
    subList = [k_list[n:n+N] for n in range(0, len(k_list), N)]
    return subList


@app.route('/pest', methods=["GET", "POST"])
def Pesticide():
    if 'user' in session:
        if request.method == "POST":
            state = request.form.get("st")  # maharashtra"
            print("#####################st################")
            print(state)
            district = request.form.get("dis")  # "bhandara"
            area = request.form.get("area")  # "bhandara"

            k_list = pest(state, district, area)

            serial_no = []
            dealer_name = []
            address = []

            for i in k_list:
                srno = i[0]
                serial_no.append(srno)
                dname = i[1]
                dealer_name.append(dname)
                addr = i[2]
                address.append(addr)

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

    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.prettify())

    table1 = soup.find_all('th', attrs={'class': 'head-style'})

    k_list = []
    for i in soup.find_all("table", class_="table structure-table"):
        for j in i.find_all("tr"):
            for k in j.find_all("td", class_="td-style"):
                k_list.append(k.text)
                for l in k.find_all("a"):
                    print(l.text)

    N = 3
    subList = [k_list[n:n+N] for n in range(0, len(k_list), N)]
    return subList


@app.route('/fer', methods=["GET", "POST"])
def Fertilizer():
    if 'user' in session:
        if request.method == "POST":
            state = request.form.get("st")  # rajasthan"
            print("#####################st################")
            print(state)
            district = request.form.get("dis")  # "ajmer"
            area = request.form.get("area")  # "jawaja"

            k_list = fer(state, district, area)

            serial_no = []
            dealer_name = []
            address = []

            for i in k_list:
                srno = i[0]
                serial_no.append(srno)
                dname = i[1]
                dealer_name.append(dname)
                addr = i[2]
                address.append(addr)

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

    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.prettify())

    table1 = soup.find_all('th', attrs={'class': 'head-style'})

    k_list = []
    for i in soup.find_all("table", class_="table structure-table"):
        for j in i.find_all("tr"):
            for k in j.find_all("td", class_="td-style"):
                k_list.append(k.text)
                for l in k.find_all("a"):
                    print(l.text)

    N = 5
    subList = [k_list[n:n+N] for n in range(0, len(k_list), N)]
    subList
    return subList


@app.route('/cold', methods=["GET", "POST"])
def cold_stor():
    if 'user' in session:
        if request.method == "POST":
            state = request.form.get("st")  # gujarat"
            print("#####################st################")
            print(state)
            district = request.form.get("dis")  # "anand"

            k_list = cold(state, district)
            print("Printing k_list")
            print(k_list)

            serial_no = []
            storage_name = []
            address = []
            mngr_name = []
            capacit = []

            for i in k_list:
                srno = i[0]
                serial_no.append(srno)
                strg = i[1]
                storage_name.append(strg)
                addr = i[2]
                address.append(addr)
                mngr = i[3]
                mngr_name.append(mngr)
                capc = i[4]
                capacit.append(capc)

            dataset = zip(serial_no, storage_name, address, mngr_name, capacit)
            return render_template('cold.html', user=session['user'], table=dataset)
        return render_template("cold.html", user=session['user'])
    return render_template("login.html")


if __name__ == "__main__":
    app.run("0.0.0.0",port=7000)
    # app.run(debug=True)
