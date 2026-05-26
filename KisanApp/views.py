from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import redirect
from datetime import date
import pymysql
import os
import io
import base64
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, r2_score
import pymysql
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout, Flatten
import cv2
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
import pickle
from keras.models import model_from_json
import requests
import json
from datetime import date
from googletrans import Translator
from django.views.decorators.csrf import csrf_exempt

global username
global rf_crop, rf_yield, rf_fertilizer

accuracy = []
fertilizers = []
plants = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___healthy",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___healthy",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Potato___Early_blight",
    "Potato___healthy",
    "Potato___Late_blight",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___healthy",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
]

with open("model/messages.txt", "r") as file:
    for line in file:
        line = line.strip("\n")
        line = line.strip()
        fertilizers.append(line)
file.close()


def trainFertilizer(dataset_path):
    global accuracy
    dataset = pd.read_csv(dataset_path)
    names = np.unique(dataset["Fertilizer Name"])
    label_encoder = []
    columns = dataset.columns
    types = dataset.dtypes.values
    for j in range(len(types)):
        name = types[j]
        if name == "object":  # finding column with object type
            le = LabelEncoder()
            dataset[columns[j]] = pd.Series(
                le.fit_transform(dataset[columns[j]].astype(str))
            )  # encode all str columns to numeric
            label_encoder.append([columns[j], le])
    dataset.fillna(dataset.mean(), inplace=True)  # missing values imputation
    Y = dataset["Fertilizer Name"].ravel()
    dataset.drop(["Fertilizer Name"], axis=1, inplace=True)
    X = dataset.values
    scaler = MinMaxScaler((0, 1))
    X = scaler.fit_transform(X)
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    X = X[indices]
    Y = Y[indices]
    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2
    )  # split dataset into train and test
    if os.path.exists("model/fertilizer.pckl"):
        f = open("model/fertilizer.pckl", "rb")
        rf_fertilizer = pickle.load(f)
        f.close()
    else:
        rf_fertilizer = RandomForestClassifier(n_estimators=50,max_depth=10,random_state=42)
        rf_fertilizer.fit(X_train, y_train)
        f = open("model/fertilizer.pckl", "wb")
        pickle.dump(rf_fertilizer, f)
        f.close()
    predict = rf_fertilizer.predict(X_test)
    acc = accuracy_score(y_test, predict)
    print(acc)
    accuracy.append(acc)
    return dataset, label_encoder, names, scaler, rf_fertilizer


def trainYield(dataset_path):
    global accuracy
    dataset = pd.read_csv(dataset_path)
    names = np.unique(dataset["Crops"])
    le = LabelEncoder()
    dataset["Crops"] = pd.Series(
        le.fit_transform(dataset["Crops"].astype(str))
    )  # encode all str columns to numeric
    dataset.fillna(dataset.mean(), inplace=True)
    Y = dataset["yield"].ravel()
    dataset.drop(["yield"], axis=1, inplace=True)
    X = dataset.values
    scaler = MinMaxScaler((0, 1))
    X = scaler.fit_transform(X)
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    X = X[indices]
    Y = Y[indices]
    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2
    )  # split dataset into train and test
    data = np.load("model/yield.npy", allow_pickle=True)
    X_train, X_test, y_train, y_test = data
    rf = RandomForestRegressor()
    rf.fit(X_train, y_train)
    predict = rf.predict(X_test)
    acc = r2_score(y_test, predict)
    accuracy.append(round(acc, 2))
    return dataset, le, names, scaler, rf


def getModel():
    with open("model/model.json", "r") as json_file:
        loaded_model_json = json_file.read()
        cnn_model = model_from_json(loaded_model_json)
    json_file.close()
    cnn_model.load_weights("model/model_weights.h5")
    return cnn_model


dataset_yield, le_yield, names_yield, scaler_yield, rf_yield = trainYield(
    "Dataset/Crop_yield.csv"
)
(
    dataset_fertilizer,
    label_encoder,
    names_fertilizer,
    scaler_fertilizer,
    rf_fertilizer,
) = trainFertilizer("Dataset/FertilizerPrediction.csv")


def getFertilizer(name):
    details = "Fertilizer Details Not Available"
    for i in range(len(fertilizers)):
        arr = fertilizers[i].split(":")
        arr[0] = arr[0].strip()
        arr[1] = arr[1].strip()
        if arr[0] == name:
            details = arr[1]
            break
    return details

# def DiseaseAction(request):
#     if request.method == "POST":
#         global plants, phone_no
#         model = getModel()
#         myfile = request.FILES["t1"].read()
#         fname = request.FILES["t1"].name
#         if os.path.exists("KisanApp/static/" + fname):
#             os.remove("KisanApp/static/" + fname)
#         with open("KisanApp/static/" + fname, "wb") as file:
#             file.write(myfile)
#         file.close()
#         img = cv2.imread("KisanApp/static/" + fname)
#         img = cv2.resize(img, (64, 64))
#         im2arr = np.array(img)
#         im2arr = im2arr.reshape(1, 64, 64, 3)
#         test = np.asarray(im2arr)
#         test = test.astype("float32")
#         test = test / 255
#         preds = model.predict(test)
#         predict = np.argmax(preds)
#         img = cv2.imread("KisanApp/static/" + fname)
#         img = cv2.resize(img, (800, 400))
#         details = getFertilizer(plants[predict])
#         output = (
#             "Disease : "
#             + plants[predict]
#             + "<br/><font size=4 color=red>Fertilizer Details : </font>"
#             + details
#         )
#         cv2.putText(
#             img,
#             "Disease : " + plants[predict],
#             (10, 25),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.7,
#             (0, 255, 255),
#             2,
#         )
#         plt.imshow(img)
#         buf = io.BytesIO()
#         plt.savefig(buf, format="png", bbox_inches="tight")
#         img_b64 = base64.b64encode(buf.getvalue()).decode()
#         plt.clf()
#         plt.cla()
#         context = {"data": output, "img": img_b64}
#         return render(request, "AISuggestion.html", context)


def Disease(request):

    if 'farmer' not in request.session:
        return redirect("FarmerLogin")

    context = {}

    if request.method == "POST":

        if 't1' not in request.FILES:
            context["data"] = "Please upload an image."
            return render(request, "Disease.html", context)

        try:
            model = getModel()

            myfile = request.FILES["t1"].read()
            fname = request.FILES["t1"].name

            path = os.path.join("KisanApp/static/", fname)

            if os.path.exists(path):
                os.remove(path)

            with open(path, "wb") as file:
                file.write(myfile)

            img = cv2.imread(path)
            img = cv2.resize(img, (64, 64))

            im2arr = np.array(img).reshape(1, 64, 64, 3)
            test = im2arr.astype("float32") / 255

            preds = model.predict(test)
            predict = np.argmax(preds)

            img = cv2.imread(path)
            img = cv2.resize(img, (800, 400))

            details = getFertilizer(plants[predict])

            output = (
                "Disease : "
                + plants[predict]
                + "<br/><font size=4 color=red>Fertilizer Details : </font>"
                + details
            )

            cv2.putText(
                img,
                "Disease : " + plants[predict],
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
            )

            plt.imshow(img)
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight")
            img_b64 = base64.b64encode(buf.getvalue()).decode()
            plt.clf()
            plt.cla()

            context["data"] = output
            context["img"] = img_b64

        except Exception as e:
            context["data"] = "Error during prediction: " + str(e)

    return render(request, "Disease.html", context)

def Back(request):
    if request.method == "GET":
        return render(request, "FarmerScreen.html", {})

# def YieldAction(request):
#     if request.method == "POST":
#         global dataset_yield, le_yield, names_yield, scaler_yield, rf_yield
#         crop = request.POST.get("t1", False)
#         area = request.POST.get("t2", False)
#         rainfall = request.POST.get("t3", False)
#         temperature = request.POST.get("t4", False)
#         data = []
#         data.append([int(area), float(rainfall), float(temperature), crop])
#         data = pd.DataFrame(data, columns=["Area", "Rainfall", "Temperature", "Crops"])
#         data["Crops"] = pd.Series(le_yield.transform(data["Crops"].astype(str)))
#         data = scaler_yield.transform(data.values)
#         predict = rf_yield.predict(data)[0]
#         output = (
#             "<font size=4 color=blue>Predicted Yield for given Crop "
#             + crop
#             + "  ====> "
#             + str(predict)
#             + "</font>"
#         )
#         context = {"data": output}
#         return render(request, "AISuggestion.html", context)

def Yield(request):
    global dataset_yield, le_yield, names_yield, scaler_yield, rf_yield

    context = {
        "crop_list": names_yield
    }

    if request.method == "POST":
        try:
            crop = request.POST.get("t1")
            area = float(request.POST.get("t2"))
            rainfall = float(request.POST.get("t3"))
            temperature = float(request.POST.get("t4"))

            data = [[area, rainfall, temperature, crop]]

            data = pd.DataFrame(
                data,
                columns=["Area", "Rainfall", "Temperature", "Crops"]
            )

            # Encode crop
            data["Crops"] = le_yield.transform(data["Crops"].astype(str))

            # Scale
            data = scaler_yield.transform(data.values)

            # Predict
            predict = rf_yield.predict(data)[0]

            output = f"Predicted Yield for {crop} : {round(predict, 2)} Tons"

            context["data"] = output

        except Exception as e:
            context["data"] = "Error in prediction"

    return render(request, "Yield.html", context)

# def FertilizerAction(request):
#     if request.method == "POST":
#         (
#             dataset_fertilizer,
#             label_encoder,
#             names_fertilizer,
#             scaler_fertilizer,
#             rf_fertilizer,
#         )
#         temperature = request.POST.get("t1", False)
#         humidity = request.POST.get("t2", False)
#         moisture = request.POST.get("t3", False)
#         soil = request.POST.get("t4", False)
#         crop = request.POST.get("t5", False)
#         n = request.POST.get("t6", False)
#         p = request.POST.get("t7", False)
#         k = request.POST.get("t8", False)
#         data = []
#         data.append(
#             [
#                 int(temperature),
#                 int(humidity),
#                 int(moisture),
#                 soil,
#                 crop,
#                 int(n),
#                 int(p),
#                 int(k),
#             ]
#         )
#         data = pd.DataFrame(
#             data,
#             columns=[
#                 "Temparature",
#                 "Humidity",
#                 "Moisture",
#                 "Soil Type",
#                 "Crop Type",
#                 "Nitrogen",
#                 "Potassium",
#                 "Phosphorous",
#             ],
#         )
#         for i in range(
#             len(label_encoder) - 1
#         ):  # label encoding from non-numeric to numeric
#             le = label_encoder[i]
#             data[le[0]] = pd.Series(
#                 le[1].transform(data[le[0]].astype(str))
#             )  # encode all str columns to numeric
#         data = scaler_fertilizer.transform(data.values)
#         predict = rf_fertilizer.predict(data)
#         predict = names_fertilizer[predict]
#         output = (
#             "<font size=4 color=blue>Predicted Fertilizer Based on Soil & Crop  ====> "
#             + predict
#             + "</font>"
#         )
#         context = {"data": output}
#         return render(request, "AISuggestion.html", context)

def Fertilizer(request):

    # Load dropdown values
    data_csv = pd.read_csv(
        "Dataset/FertilizerPrediction.csv",
        usecols=["Soil Type", "Crop Type"],
    )

    soil_list = np.unique(data_csv["Soil Type"])
    crop_list = np.unique(data_csv["Crop Type"])

    context = {
        "soil_list": soil_list,
        "crop_list": crop_list,
    }

    # If form submitted
    if request.method == "POST":
        try:
            temperature = int(request.POST.get("t1"))
            humidity = int(request.POST.get("t2"))
            moisture = int(request.POST.get("t3"))
            soil = request.POST.get("t4")
            crop = request.POST.get("t5")
            n = int(request.POST.get("t6"))
            p = int(request.POST.get("t7"))
            k = int(request.POST.get("t8"))

            # Prepare data
            data = [[temperature, humidity, moisture, soil, crop, n, p, k]]

            data = pd.DataFrame(
                data,
                columns=[
                    "Temparature",
                    "Humidity",
                    "Moisture",
                    "Soil Type",
                    "Crop Type",
                    "Nitrogen",
                    "Potassium",
                    "Phosphorous",
                ],
            )

            # 🔹 Your existing model encoding logic here
            for i in range(len(label_encoder) - 1):
                le = label_encoder[i]
                data[le[0]] = le[1].transform(data[le[0]].astype(str))

            data = scaler_fertilizer.transform(data.values)
            predict = rf_fertilizer.predict(data)
            predict = names_fertilizer[predict]

            context["data"] = predict

        except Exception as e:
            context["data"] = "Error in prediction"

    return render(request, "Fertilizer.html", context)

def ExpertRegister(request):
    if request.method == "GET":
        return render(request, "ExpertRegister.html", {})

def ExpertRegisterAction(request):

    if request.method == "POST":

        username = request.POST.get("t1")
        password = request.POST.get("t2")
        contact = request.POST.get("t3")
        email = request.POST.get("t4")
        address = request.POST.get("t5")
        qualification = request.POST.get("t6")
        desc = request.POST.get("t7")

        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )

        with con:
            cur = con.cursor()

            # ✅ Check duplicate username
            cur.execute("SELECT username FROM experts WHERE username=%s", (username,))
            row = cur.fetchone()

            if row:
                output = username + " Username already exists"

            else:
                cur.execute(
                    """INSERT INTO experts
                       (username, password, contact, email, address, qualification, description, approve)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,'Pending')""",
                    (username, password, contact, email, address, qualification, desc),
                )
                con.commit()

                output = "Signup completed. Login to continue"

        return render(request, "ExpertRegister.html", {"data": output})

def FarmerRegister(request):
    if request.method == "GET":
        return render(request, "FarmerRegister.html", {})


def FarmerRegisterAction(request):
    if request.method == "POST":
        global username
        username = request.POST.get("t1", False)
        password = request.POST.get("t2", False)
        contact = request.POST.get("t3", False)
        email = request.POST.get("t4", False)
        address = request.POST.get("t5", False)
        crops = request.POST.get("t6", False)

        output = "none"
        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )
        with con:
            cur = con.cursor()
            cur.execute("select username FROM farmers")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username + " Username already exists"
                    break
        if output == "none":
            db_connection = pymysql.connect(
                host="127.0.0.1",
                port=3308,
                user="root",
                password="root",
                database="kisansathi",
                charset="utf8",
            )
            db_cursor = db_connection.cursor()
            student_sql_query = (
                "INSERT INTO farmers VALUES('"
                + username
                + "','"
                + password
                + "','"
                + contact
                + "','"
                + email
                + "','"
                + address
                + "','"
                + crops
                + "','Pending')"
            )
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = "<font size=3 color=blue>Signup process completed. Login to perform KisanSathi Activities</font>"
        context = {"data": output}
        return render(request, "FarmerRegister.html", context)


# def ExpertLoginAction(request):
#     global username
#     if request.method == 'POST':
#         global username, otp, phone_no
#         status = "none"
#         users = request.POST.get('t1', False)
#         password = request.POST.get('t2', False)
#         con = pymysql.connect(host='127.0.0.1',port = 3308,user = 'root', password = 'root', database = 'kisansathi',charset='utf8')
#         with con:
#             cur = con.cursor()
#             cur.execute("select username,password FROM experts where approve='Approved'")
#             rows = cur.fetchall()
#             for row in rows:
#                 if row[0] == users and row[1] == password:
#                     username = users
#                     status = "success"
#                     break
#         if status == 'success':
#             context= {'data':"<font size=3 color=blue>Welcome "+username}
#             return render(request, 'ExpertScreen.html', context)
#         else:
#             context= {'data':'Invalid username or account not yet approved by admin'}
#             return render(request, 'ExpertLogin.html', context)


# def ExpertLoginAction(request):
#     global username

#     # 🚫 Prevent direct GET access
#     if request.method != "POST":
#         return render(request, "ExpertLogin.html", {"data": "Invalid Access"})

#     status = "none"
#     users = request.POST.get("t1")
#     password = request.POST.get("t2")

#     con = pymysql.connect(
#         host="127.0.0.1",
#         port=3308,
#         user="root",
#         password="root",
#         database="kisansathi",
#         charset="utf8",
#     )

#     with con:
#         cur = con.cursor()

#         # 🔎 Check Login
#         cur.execute("SELECT username,password FROM experts WHERE approve='Approved'")
#         rows = cur.fetchall()

#         for row in rows:
#             if row[0] == users and row[1] == password:
#                 username = users
#                 status = "success"
#                 break

#         # ❌ If login failed
#         if status != "success":
#             return render(
#                 request,
#                 "ExpertLogin.html",
#                 {"data": "Invalid username or account not approved"},
#             )

#         # ✅ If login success → Fetch Dashboard Data

#         # Approved Farmers Count
#         cur.execute("SELECT COUNT(*) FROM farmers WHERE approve='Approved'")
#         farmers_count = cur.fetchone()[0]

#         # Total Guides
#         cur.execute("SELECT COUNT(*) FROM guides")
#         guides_count = cur.fetchone()[0]

#         # Pending Queries
#         cur.execute("SELECT COUNT(*) FROM query WHERE response IS NULL OR response=''")
#         pending_queries = cur.fetchone()[0]

#     context = {
#         "expert_name": username,
#         "farmers_count": farmers_count,
#         "guides_count": guides_count,
#         "pending_queries": pending_queries,
#     }
#     request.session["expert"] = username
#     return redirect("ExpertDashboard")

def ExpertLoginAction(request):

    if request.method != "POST":
        return redirect("ExpertLogin")

    users = request.POST.get("t1")
    password = request.POST.get("t2")

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    status = "none"

    with con:
        cur = con.cursor()
        cur.execute("SELECT username,password FROM experts WHERE approve='Approved'")
        rows = cur.fetchall()

        for row in rows:
            if row[0] == users and row[1] == password:
                status = "success"
                break
    print("Login Status:", status)
    if status == "success":
        request.session["expert"] = users
        return redirect("ExpertDashboard")
    else:
        return render(
            request,
            "ExpertLogin.html",
            {"data": "Invalid username or account not approved"},
        )

def ExpertDashboard(request):
    print("Session value:", request.session.get("expert"))
    if 'expert' not in request.session:
        return redirect('ExpertLogin')
    username = request.session['expert']

    con = pymysql.connect(
        host='127.0.0.1',
        port=3308,
        user='root',
        password='root',
        database='kisansathi',
        charset='utf8'
    )
    with con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM farmers WHERE approve='Approved'")
        farmers_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM guides")
        guides_count = cur.fetchone()[0]

        cur.execute("""SELECT COUNT(*) FROM query WHERE response='Pending' OR response IS NULL""")
        pending_queries = cur.fetchone()[0]

    context = {
        'expert_name': username,
        'farmers_count': farmers_count,
        'guides_count': guides_count,
        'pending_queries': pending_queries
    }

    return render(request, 'ExpertScreen.html', context)

def AdminLogin(request):
    if request.method == "GET":
        return render(request, "AdminLogin.html", {})

def AdminLoginAction(request):
    if request.method == "POST":

        users = request.POST.get("t1")
        password = request.POST.get("t2")

        if users == "admin" and password == "admin":

            # ✅ SET SESSION HERE
            request.session['admin'] = users
            return redirect("AdminDashboard")
   # use redirect, not render
        else:
            context = {"data": "Invalid username or password"}
            return render(request, "AdminLogin.html", context)

def AdminDashboard(request):

    # 🔐 Check admin session
    if 'admin' not in request.session:
        return redirect("AdminLogin")

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    with con:
        cur = con.cursor()

        # ✅ Total Experts (Approved only)
        cur.execute("SELECT COUNT(*) FROM experts WHERE approve='Approved'")
        total_experts = cur.fetchone()[0]

        # ✅ Pending Approvals (Farmers + Experts)
        cur.execute("SELECT COUNT(*) FROM farmers WHERE approve='Pending'")
        pending_farmers = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM experts WHERE approve='Pending'")
        pending_experts = cur.fetchone()[0]

        pending_approvals = pending_farmers + pending_experts

        # ✅ Total Queries
        cur.execute("SELECT COUNT(*) FROM query")
        total_queries = cur.fetchone()[0]

        # ✅ Total AI Verifications
        cur.execute("SELECT COUNT(*) FROM ai_verification")
        total_verifications = cur.fetchone()[0]

    context = {
        "total_experts": total_experts,
        "pending_approvals": pending_approvals,
        "total_queries": total_queries,
        "total_verifications": total_verifications
    }

    return render(request, "AdminScreen.html", context)

def ExpertLogin(request):
    if request.method == "GET":
        return render(request, "ExpertLogin.html", {})


def FarmerLoginAction(request):
    global username
    if request.method == "POST":
        global username, otp, phone_no
        status = "none"
        users = request.POST.get("t1", False)
        password = request.POST.get("t2", False)
        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )
        with con:
            cur = con.cursor()
            cur.execute(
                "select username,password FROM farmers where approve='Approved'"
            )
            rows = cur.fetchall()
            for row in rows:
                if row[0] == users and row[1] == password:
                    username = users
                    status = "success"
                    break
        if status == "success":
            request.session["farmer"] = username
            return redirect("FarmerDashboard")
        else:
            context = {"data": "Invalid username or account not yet approved by admin"}
            return render(request, "FarmerLogin.html", context)

def FarmerDashboard(request):
    if 'farmer' not in request.session:
        return redirect("FarmerLogin")

    username = request.session['farmer']

    return render(request, "FarmerScreen.html", {
        "username": username
    })

def FarmerLogin(request):
    if request.method == "GET":
        return render(request, "FarmerLogin.html", {})


def index(request):
    if request.method == "GET":
        return render(request, "index.html", {})


def Contactus(request):
    if request.method == "GET":
        return render(request, "Contactus.html", {})


def Aboutus(request):
    if request.method == "GET":
        return render(request, "Aboutus.html", {})


def help(request):
    if request.method == "GET":
        return render(request, "help.html", {})


def login(request):
    if request.method == "GET":
        return render(request, "login.html", {})


def register(request):
    if request.method == "GET":
        return render(request, "register.html", {})

def ApproveAccountAction(request):
    if request.method == "GET":

        user = request.GET.get("rid")
        table = request.GET.get("table")

        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )

        with con:
            cur = con.cursor()
            cur.execute(
                f"UPDATE {table} SET approve='Approved' WHERE username=%s",
                (user,)
            )
            con.commit()

        return redirect("ApproveAccount")

def ApproveAccount(request):

    if 'admin' not in request.session:
        return redirect("AdminLogin")

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    pending_accounts = []

    with con:
        cur = con.cursor()

        # Pending Farmers
        cur.execute("SELECT username, contact, email, address FROM farmers WHERE approve='Pending'")
        farmers = cur.fetchall()

        for row in farmers:
            pending_accounts.append({
                "username": row[0],
                "contact": row[1],
                "email": row[2],
                "address": row[3],
                "type": "Farmer"
            })

        # Pending Experts
        cur.execute("SELECT username, contact, email, address FROM experts WHERE approve='Pending'")
        experts = cur.fetchall()

        for row in experts:
            pending_accounts.append({
                "username": row[0],
                "contact": row[1],
                "email": row[2],
                "address": row[3],
                "type": "Expert"
            })

    return render(request, "ApproveAccounts.html", {
        "accounts": pending_accounts
    })

def UpdatePrices(request):

    # 🔹 Load crop dropdown from CSV
    data = pd.read_csv("Dataset/FertilizerPrediction.csv", usecols=["Crop Type"])
    crop = np.unique(data["Crop Type"])

    output = '<select name="t1">'
    for i in range(len(crop)):
        output += '<option value="' + crop[i] + '">' + crop[i] + "</option>"
    output += "</select>"

    # 🔹 Fetch all updated crop prices
    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    prices = []

    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT crop_name, price, price_date
            FROM cropprices
            ORDER BY price_date DESC
        """)
        rows = cur.fetchall()

        for row in rows:
            prices.append({
                "crop": row[0],
                "price": row[1],
                "date": row[2]
            })

    context = {
        "data1": output,
        "prices": prices
    }

    return render(request, "UpdatePrices.html", context)

# def UpdatePricesAction(request):
#     if request.method == "POST":
#         global username
#         crop = request.POST.get("t1", False)
#         price = request.POST.get("t2", False)
#         dd = str(date.today())
#         output = (
#             "INSERT INTO cropprices VALUES('" + crop + "','" + price + "','" + dd + "')"
#         )
#         con = pymysql.connect(
#             host="127.0.0.1",
#             port=3308,
#             user="root",
#             password="root",
#             database="kisansathi",
#             charset="utf8",
#         )
#         with con:
#             cur = con.cursor()
#             cur.execute(
#                 "select crop_name FROM cropprices where crop_name='" + crop + "'"
#             )
#             rows = cur.fetchall()
#             for row in rows:
#                 if row[0] == crop:
#                     output = (
#                         "update cropprices set price='"
#                         + price
#                         + "', price_date='"
#                         + dd
#                         + "' where crop_name='"
#                         + crop
#                         + "'"
#                     )
#                     break
#         db_connection = pymysql.connect(
#             host="127.0.0.1",
#             port=3308,
#             user="root",
#             password="root",
#             database="kisansathi",
#             charset="utf8",
#         )
#         db_cursor = db_connection.cursor()
#         db_cursor.execute(output)
#         db_connection.commit()
#         output = "<font size=3 color=blue>Crop price successfully updated</font>"
#         context = {"data": output}
#         return render(request, "UpdatePrices.html", context)

def UpdatePricesAction(request):
    if request.method == "POST":
        crop = request.POST.get("t1")
        price = request.POST.get("t2")
        today = str(date.today())
        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )
        with con:
            cur = con.cursor()
            # Check if crop already exists
            cur.execute("SELECT crop_name FROM cropprices WHERE crop_name=%s", (crop,))
            row = cur.fetchone()

            if row:
                # Update
                cur.execute(
                    "UPDATE cropprices SET price=%s, price_date=%s WHERE crop_name=%s",
                    (price, today, crop)
                )
            else:
                # Insert
                cur.execute(
                    "INSERT INTO cropprices (crop_name, price, price_date) VALUES (%s, %s, %s)",
                    (crop, price, today)
                )

            con.commit()
        messages.success(request, "Crop price successfully updated!")
        return redirect("UpdatePrices")

def PostPolicies(request):

    success_message = request.GET.get("success")

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    policies = []

    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT policy_name, info_type, info_date
            FROM schemes
            ORDER BY info_date DESC
            LIMIT 5
        """)
        rows = cur.fetchall()

        for row in rows:
            policies.append({
                "name": row[0],
                "type": row[1],
                "date": row[2],
            })

    return render(request, "PostPolicies.html", {
        "policies": policies,
        "data": success_message
    })

def PostPoliciesAction(request):
    if request.method == "POST":

        # ✅ Get correct form field names
        name = request.POST.get("policyName")
        desc = request.POST.get("policyDescription")
        policy_type = request.POST.get("policyType")
        today = str(date.today())

        # ✅ Basic validation
        if not name or not desc or not policy_type:
            return render(request, "PostPolicies.html", {
                "data": "All fields are required."
            })

        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )

        with con:
            cur = con.cursor()

            # ✅ Column names match your DB exactly
            cur.execute(
                """
                INSERT INTO schemes (policy_name, policy_desc, info_type, info_date)
                VALUES (%s, %s, %s, %s)
                """,
                (name, desc, policy_type, today)
            )

            con.commit()

        return redirect(reverse("PostPolicies") + "?success=Policy published successfully!")

def ViewQueryResult(request):

    if 'admin' not in request.session:
        return redirect("AdminLogin")

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM query")
        rows = cur.fetchall()

    return render(request, "ViewQueryResult.html", {
        "rows": rows
    })

def UploadGuide(request):
    if request.method == "GET":
        return render(request, "UploadGuide.html", {})


def UploadGuideAction(request):
    if request.method == "POST":

        # ✅ Check login
        if 'expert' not in request.session:
            return redirect("ExpertLogin")

        username = request.session['expert']   # ✅ FIX HERE

        desc = request.POST.get("t1")

        if "t2" not in request.FILES:
            return render(request, "UploadGuide.html", {
                "data": "<font color='red'>Please upload a file</font>"
            })

        myfile = request.FILES["t2"]
        fname = myfile.name

        file_path = "KisanApp/static/guide/" + fname

        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, "wb") as file:
            for chunk in myfile.chunks():
                file.write(chunk)

        # ✅ Use parameterized query (VERY IMPORTANT)
        db_connection = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )

        with db_connection:
            cursor = db_connection.cursor()
            cursor.execute(
                "INSERT INTO guides (expert_name, guide_description, filename) VALUES (%s, %s, %s)",
                (username, desc, fname)
            )
            db_connection.commit()

        output = "<font size=3 color=green>Guide uploaded successfully ✅</font>"

        return render(request, "UploadGuide.html", {"data": output})

def VerifySuggestionAction(request):
    if request.method == "POST":

        if 'expert' not in request.session:
            return redirect("ExpertLogin")

        username = request.session['expert']
        model = getModel()

        if "t1" not in request.FILES:
            return render(request, "VerifySuggestion.html", {
                "data": "<font color='red'>Please upload image</font>"
            })

        myfile = request.FILES["t1"]
        fname = myfile.name
        file_path = "KisanApp/static/" + fname

        # Save file
        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, "wb") as f:
            for chunk in myfile.chunks():
                f.write(chunk)

        # -------------------------
        # IMAGE PROCESSING
        # -------------------------

        img = cv2.imread(file_path)
        img = cv2.resize(img, (64, 64))

        im2arr = np.array(img).reshape(1, 64, 64, 3)
        test = im2arr.astype("float32") / 255

        preds = model.predict(test)
        predict = np.argmax(preds)

        disease = plants[predict]
        details = getFertilizer(disease)

        # -------------------------
        # CONVERT IMAGE TO BASE64
        # -------------------------

        img_display = cv2.imread(file_path)
        img_display = cv2.resize(img_display, (600, 400))

        _, buffer = cv2.imencode('.jpg', img_display)
        img_b64 = base64.b64encode(buffer).decode('utf-8')

        # -------------------------
        # CONTEXT
        # -------------------------

        context = {
            "disease": disease,
            "fertilizer_details": details,
            "img": img_b64,
            "verified": False
        }

        return render(request, "VerifySuggestion.html", context)


def VerifySuggestion(request):
    if request.method == "GET":
        return render(request, "VerifySuggestion.html", {})
    
def SaveVerification(request):
    if request.method == "POST":

        if 'expert' not in request.session:
            return redirect("ExpertLogin")

        expert = request.session['expert']
        disease = request.POST.get("disease")
        status = request.POST.get("status")
        correction = request.POST.get("correction", "")

        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )

        with con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO ai_verification 
                (expert_name, disease, status, correction)
                VALUES (%s, %s, %s, %s)
            """, (expert, disease, status, correction))
            con.commit()

        return render(request, "VerifySuggestion.html", {
            "success": "Verification saved successfully!",
            "verified": True
        })
        
def ExpertProfile(request):

    if 'expert' not in request.session:
        return redirect("ExpertLogin")

    username = request.session['expert']

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    with con:
        cur = con.cursor()

        # ✅ 1. Fetch Expert Details
        cur.execute("""
            SELECT username, email, contact, qualification, description, address
            FROM experts
            WHERE username=%s
        """, (username,))
        row = cur.fetchone()

        if row:
            expert_details = {
                "username": row[0],
                "email": row[1],
                "contact": row[2],
                "qualification": row[3],
                "description": row[4],
                "address": row[5],
            }
        else:
            expert_details = {}

        # ✅ 2. Fetch Responded Queries
        cur.execute("""
            SELECT farmer_name, query, response, query_date
            FROM query
            WHERE expert_name=%s
            ORDER BY id DESC
        """, (username,))
        query_rows = cur.fetchall()

        responded_queries = []
        for q in query_rows:
            responded_queries.append({
                "farmer_name": q[0],
                "query": q[1],
                "response": q[2],
                "query_date": q[3],
            })

        # ✅ 3. Fetch Uploaded Guides
        cur.execute("""
            SELECT guide_description, filename
            FROM guides
            WHERE expert_name=%s
        """, (username,))
        guide_rows = cur.fetchall()

        uploaded_guides = []
        for g in guide_rows:
            uploaded_guides.append({
                "description": g[0],
                "filename": g[1],
            })

        # ✅ 4. Fetch AI Verifications
        cur.execute("""
            SELECT disease, status, correction, verify_date
            FROM ai_verification
            WHERE expert_name=%s
            ORDER BY verify_date DESC
        """, (username,))
        verification_rows = cur.fetchall()

        verified_ai = []
        for v in verification_rows:
            verified_ai.append({
                "disease": v[0],
                "status": v[1],
                "correction": v[2],
                "verify_date": v[3],
            })

    context = {
        "expert_details": expert_details,
        "responded_queries": responded_queries,
        "uploaded_guides": uploaded_guides,
        "verified_ai": verified_ai,
    }

    return render(request, "ExpertProfile.html", context)

def FarmerProfile(request):

    # ===============================
    # Check Session
    # ===============================
    if 'farmer' not in request.session:
        return redirect("FarmerLogin")

    username = request.session['farmer']

    # ===============================
    # Database Connection
    # ===============================
    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
        autocommit=True
    )

    cur = con.cursor()
    cur.execute("SELECT * FROM farmers WHERE username=%s", (username,))
    row = cur.fetchone()

    if not row:
        con.close()
        return redirect("FarmerLogin")

    # ===============================
    # Farmer Data
    # ===============================
    farmer = {
        "username": row[0],
        "password": row[1],
        "contact": row[2],
        "email": row[3],
        "address": row[4],
        "intrested_crops": row[5],
        "approve": row[6],
    }

    # ===============================
    # Split Crops Safely
    # ===============================
    crops = []
    if farmer["intrested_crops"]:
        crops = [
            c.strip()
            for c in farmer["intrested_crops"].split(",")
            if c.strip()
        ]

    context = {
        "farmer": farmer,
        "crops": crops,
    }

    # ===============================
    # Handle Password Change
    # ===============================
    if request.method == "POST":

        current = request.POST.get("current_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")

        # Validation
        if not current or not new or not confirm:
            context["message"] = "All fields are required"
            context["message_type"] = "error"

        elif current != farmer["password"]:
            context["message"] = "Current password incorrect"
            context["message_type"] = "error"

        elif new != confirm:
            context["message"] = "Passwords do not match"
            context["message_type"] = "error"

        elif len(new) < 6:
            context["message"] = "Password must be at least 6 characters"
            context["message_type"] = "error"

        else:
            cur.execute(
                "UPDATE farmers SET password=%s WHERE username=%s",
                (new, username),
            )

            context["message"] = "Password updated successfully"
            context["message_type"] = "success"

            # Update local copy
            farmer["password"] = new

    con.close()

    return render(request, "FarmerProfile.html", context)


def ChangeExpertPassword(request):

    if request.method == "POST":

        if 'expert' not in request.session:
            return redirect("ExpertLogin")

        username = request.session['expert']
        current = request.POST.get("current_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")

        if new != confirm:
            return render(request, "ExpertProfile.html", {
                "message": "New passwords do not match"
            })

        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )

        with con:
            cur = con.cursor()

            # Check current password
            cur.execute("SELECT password FROM experts WHERE username=%s", (username,))
            db_pass = cur.fetchone()[0]

            if db_pass != current:
                return render(request, "ExpertProfile.html", {
                    "message": "Current password incorrect"
                })

            # Update password
            cur.execute("UPDATE experts SET password=%s WHERE username=%s",
                        (new, username))
            con.commit()

        return redirect("ExpertProfile")

def QueryResponse(request):
    if request.method == "GET":

        query_id = request.GET.get("id")

        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )

        with con:
            cur = con.cursor()
            cur.execute("SELECT farmer_name, query FROM query WHERE id=%s", (query_id,))
            row = cur.fetchone()

        if row:
            farmer = row[0]
            query_text = row[1]
        else:
            return redirect("ResponseQuery")

        context = {
            "query_id": query_id,
            "farmer": farmer,
            "query_text": query_text,
            "data1": f"<p><b>Farmer:</b> {farmer}</p><p><b>Query:</b> {query_text}</p>"
        }

        return render(request, "QueryResponse.html", context)

def ResponseQueryAction(request):

    if request.method == "POST":

        if 'expert' not in request.session:
            return redirect("ExpertLogin")

        expert = request.session['expert']
        query_id = request.POST.get("query_id")
        response = request.POST.get("t2")

        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )

        with con:
            cur = con.cursor()
            cur.execute("""
                UPDATE query 
                SET response=%s, expert_name=%s
                WHERE id=%s
            """, (response, expert, query_id))
            con.commit()
            
        messages.success(request, "Response submitted successfully ✅")
        # ✅ Redirect instead of manually rendering
        return redirect("ResponseQuery")

def ResponseQuery(request):
    if request.method == "GET":

        columns = ["Farmer Name", "Query", "Query Date", "Give Your Response"]
        output = "<table border=1 align=center>"
        font = '<font size="" color="black">'

        # Table Header
        for col in columns:
            output += "<th>" + font + col + "</th>"
        output += "</tr>"

        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )

        with con:
            cur = con.cursor()

            # 👇 IMPORTANT CHANGE — also show NULL responses
            cur.execute("SELECT * FROM query WHERE response='Pending' OR response IS NULL")
            rows = cur.fetchall()

            for row in rows:
                query_id = row[0]        # id
                farmer_name = row[1]
                query_text = row[2]
                query_date = row[4]

                output += "<tr>"
                output += "<td>" + font + str(farmer_name) + "</td>"
                output += "<td>" + font + str(query_text) + "</td>"
                output += "<td>" + font + str(query_date) + "</td>"

                # 👇 VERY IMPORTANT — send id only
                output += (
                    "<td><a href='QueryResponse?id="
                    + str(query_id)
                    + "'><font size=3 color=black>Click to Send Response</font></a></td>"
                )

                output += "</tr>"

        output += "</table><br/><br/><br/><br/>"

        context = {"data": output}
        return render(request, "ExpertScreen.html", context)

def ResponseQuery(request):

    if 'expert' not in request.session:
        return redirect('ExpertLogin')

    success_message = None

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    # 🔹 Handle Response Submit
    if request.method == "POST":
        query_id = request.POST.get("query_id")
        response = request.POST.get("t2")

        with con:
            cur = con.cursor()
            cur.execute(
                "UPDATE query SET response=%s WHERE id=%s",
                (response, query_id)
            )
            con.commit()

        success_message = "Response submitted successfully ✅"

    # 🔹 Always reload pending queries
    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT id, farmer_name, query, query_date
            FROM query
            WHERE response='Pending' OR response IS NULL
        """)
        rows = cur.fetchall()

    context = {
        "queries": rows,
        "success_message": success_message
    }

    return render(request, "QueryResponse.html", context)

def ResponseQuery(request):

    if 'expert' not in request.session:
        return redirect("ExpertLogin")

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT id, farmer_name, query, query_date
            FROM query
            WHERE response='Pending' OR response IS NULL
        """)
        rows = cur.fetchall()

    context = {
        "queries": rows
    }

    return render(request, "QueryResponse.html", context)

def ViewFarmers(request):

    if 'admin' not in request.session:
        return redirect("AdminLogin")

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT username, contact, email, address, intrested_crops
            FROM farmers
            WHERE approve='Approved'
        """)
        rows = cur.fetchall()

    farmers_list = []
    for row in rows:
        crops_list = row[4].split(",") if row[4] else []

        farmers_list.append({
            "username": row[0],
            "contact": row[1],
            "email": row[2],
            "address": row[3],
            "crops": crops_list,
        })

    return render(request, "ViewFarmers.html", {
        "farmers": farmers_list
    })

def ViewApprovedExperts(request):

    if 'admin' not in request.session:
        return redirect("AdminLogin")

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT username, contact, email, qualification, address, description
            FROM experts
            WHERE approve='Approved'
        """)
        rows = cur.fetchall()

    experts_list = []
    for row in rows:
        experts_list.append({
            "username": row[0],
            "contact": row[1],
            "email": row[2],
            "qualification": row[3],
            "address": row[4],
            "description": row[5],
        })

    return render(request, "ViewApprovedExperts.html", {
        "experts": experts_list
    })

def AccessSchemes(request):

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    schemes_list = []

    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT policy_name, policy_desc, info_date
            FROM schemes
            ORDER BY info_date DESC
        """)
        rows = cur.fetchall()

        for row in rows:
            schemes_list.append({
                "policy_name": row[0],
                "policy_desc": row[1],
                "info_date": row[2],
            })

    return render(request, "AccessSchemes.html", {
        "schemes": schemes_list
    })

def AISuggestion(request):
    if request.method == "GET":
        return render(request, "AISuggestion.html", {})


def SearchNetwork(request):

    # 🔐 Check if farmer is logged in
    if 'farmer' not in request.session:
        return redirect("FarmerLogin")

    username = request.session['farmer']

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    farmers_list = []
    user_crops = []

    with con:
        cur = con.cursor()

        # 🔹 1. Get current farmer crops
        cur.execute(
            "SELECT intrested_crops FROM farmers WHERE username=%s",
            (username,)
        )
        row = cur.fetchone()

        if row and row[0]:
            user_crops = [crop.strip() for crop in row[0].split(",")]

        # 🔹 2. Get other approved farmers
        cur.execute("""
            SELECT username, intrested_crops, contact
            FROM farmers
            WHERE username != %s AND approve='Approved'
        """, (username,))
        rows = cur.fetchall()

        # 🔹 3. Compare crops
        for row in rows:
            other_username = row[0]
            other_crops_raw = row[1]
            contact = row[2]

            if other_crops_raw:
                other_crops = [crop.strip() for crop in other_crops_raw.split(",")]

                common_crops = list(set(user_crops) & set(other_crops))

                if common_crops:
                    farmers_list.append({
                        "username": other_username,
                        "crops": other_crops,
                        "common_crops": common_crops,
                        "contact": contact,
                    })

    context = {
        "farmers": farmers_list,
        "your_crops": user_crops,
        "total_matches": len(farmers_list)
    }

    return render(request, "SearchNetwork.html", context)


def QueryResponses(request):

    if 'farmer' not in request.session:
        return redirect("FarmerLogin")

    username = request.session['farmer']

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    queries_list = []

    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT farmer_name, query, response, query_date
            FROM query
            WHERE farmer_name=%s
        """, (username,))
        rows = cur.fetchall()

        for row in rows:
            queries_list.append({
                "farmer_name": row[0],
                "query": row[1],
                "response": row[2],
                "query_date": row[3]
            })

    return render(request, "QueryResponses.html", {
        "queries": queries_list
    })

def PostQuery(request):
    if 'farmer' not in request.session:
        return redirect("FarmerLogin")
    return render(request, "PostQuery.html")

def PostQueryAction(request):

    if 'farmer' not in request.session:
        return redirect("FarmerLogin")

    if request.method == "POST":

        username = request.session['farmer']   # ✅ GET FROM SESSION
        query = request.POST.get("t1")
        dd = str(date.today())

        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )

        with con:
            cur = con.cursor()

            cur.execute("""
                INSERT INTO query (farmer_name, query, response, query_date)
                VALUES (%s, %s, %s, %s)
            """, (username, query, "Pending", dd))

            con.commit()

        context = {
            "data": "Your query successfully submitted to our experts"
        }

        return render(request, "PostQuery.html", context)

def ViewGuide(request):

    if 'farmer' not in request.session:
        return redirect("FarmerLogin")

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    guides_list = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT expert_name, guide_description, filename FROM guides")
        rows = cur.fetchall()

        for row in rows:
            guides_list.append({
                "expert_name": row[0],
                "description": row[1],
                "filename": row[2]
            })

    return render(request, "ViewGuide.html", {
        "guides": guides_list
    })



def Download(request):
    if request.method == "GET":
        name = request.GET.get("rid", False)
        with open("KisanApp/static/guide/" + name, "rb") as file:
            data = file.read()
        file.close()
        response = HttpResponse(data, content_type="application/force-download")
        response["Content-Disposition"] = "attachment; filename=" + name
        return response

# def ViewGuideAction(request):
#     if 'farmer' not in request.session:
#         return redirect("FarmerLogin")
#     if request.method == "POST":

#         lang = request.POST.get("t1")

#         con = pymysql.connect(
#             host="127.0.0.1",
#             port=3308,
#             user="root",
#             password="root",
#             database="kisansathi",
#             charset="utf8",
#         )

#         guides_list = []

#         with con:
#             cur = con.cursor()
#             cur.execute("SELECT expert_name, guide_description, filename FROM guides")
#             rows = cur.fetchall()

#             for row in rows:
#                 guides_list.append({
#                     "expert_name": row[0],
#                     "description": row[1],
#                     "filename": row[2]
#                 })

#         return render(request, "ViewGuide.html", {
#             "guides": guides_list
#         })


def Chatbot(request):
    if request.method == "GET":
        return render(request, "Chatbot.html", {})


def ViewCropRate(request):
    if 'farmer' not in request.session:
        return redirect("FarmerLogin")

    con = pymysql.connect(
        host="127.0.0.1",
        port=3308,
        user="root",
        password="root",
        database="kisansathi",
        charset="utf8",
    )

    prices = []

    with con:
        cur = con.cursor()
        cur.execute("""
            SELECT crop_name, price, price_date
            FROM cropprices
            ORDER BY price_date DESC
        """)
        rows = cur.fetchall()

        for row in rows:
            prices.append({
                "crop": row[0],
                "price": row[1],
                "date": row[2]
            })

    return render(request, "ViewCropRate.html", {
        "prices": prices
    })

@csrf_exempt
def TextChatData(request):
    if request.method == "GET":
        global username, stop_words, current_request
        input_text = request.GET.get("mytext", False)
        output = "Sorry! I am not train for this question"
        con = pymysql.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="root",
            database="kisansathi",
            charset="utf8",
        )
        with con:
            cur = con.cursor()
            cur.execute(
                "SELECT response FROM chatbot_knowledge WHERE keywords LIKE %s OR question LIKE %s",
                ("%" + input_text + "%", "%" + input_text + "%"),
            )
            rows = cur.fetchall()
            for row in rows:
                output = row[0]
                break
        return HttpResponse("Chatbot: " + output, content_type="text/html")
