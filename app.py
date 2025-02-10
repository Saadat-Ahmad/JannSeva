import datetime
from flask import Flask, request, render_template, redirect, jsonify, session, flash
from flask_session import Session
from openMeteo import weather, sunshine
import google.generativeai as genai
from aqi import airpolution
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from twilio.rest import Client
import random

app = Flask(__name__)
app.secret_key = '12345'


genai.configure(api_key="GOOGLE_API")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jannseva.db'
Session(app)


conn = sqlite3.connect('jannseva.db', check_same_thread=False)
db = conn.cursor()
table = "CREATE TABLE IF NOT EXISTS 'users' (id INTEGER PRIMARY KEY AUTOINCREMENT, phonenumber TEXT UNIQUE NOT NULL, history TEXT );"
db.execute(table)

generation_config = {
    "temperature": 0.7,          
    "top_p": 0.9,                
    "top_k": 40,                 
    "max_output_tokens": 2048,   
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
]


model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

chat = model.start_chat()

state_to_language = {
    "Andhra Pradesh": "te",  # Telugu
    "Arunachal Pradesh": "en",  # English (official)
    "Assam": "as",  # Assamese
    "Bihar": "hi",  # Hindi
    "Chhattisgarh": "hi",  # Hindi
    "Goa": "kok",  # Konkani
    "Gujarat": "gu",  # Gujarati
    "Haryana": "hi",  # Hindi
    "Himachal Pradesh": "hi",  # Hindi
    "Jharkhand": "hi",  # Hindi
    "Karnataka": "kn",  # Kannada
    "Kerala": "ml",  # Malayalam
    "Madhya Pradesh": "hi",  # Hindi
    "Maharashtra": "mr",  # Marathi
    "Manipur": "mni",  # Meitei (Manipuri)
    "Meghalaya": "en",  # English
    "Mizoram": "mzn",  # Mizo
    "Nagaland": "en",  # English
    "Odisha": "or",  # Odia
    "Punjab": "pa",  # Punjabi
    "Rajasthan": "hi",  # Hindi
    "Sikkim": "ne",  # Nepali
    "Tamil Nadu": "ta",  # Tamil
    "Telangana": "te",  # Telugu
    "Tripura": "bn",  # Bengali
    "Uttar Pradesh": "HINDI",  # Hindi
    "Uttarakhand": "hi",  # Hindi
    "West Bengal": "bn",  # Bengali

    # Union Territories
    "Andaman and Nicobar Islands": "hi",  # Hindi
    "Chandigarh": "hi",  # Hindi (Punjabi & English are also spoken)
    "Dadra and Nagar Haveli and Daman and Diu": "gu",  # Gujarati
    "Lakshadweep": "ml",  # Malayalam
    "Delhi": "hi",  # Hindi
    "Jammu and Kashmir": "ur",  # Urdu
    "Ladakh": "bo",  # Ladakhi (Bodhi)
    "Puducherry": "ta",  # Tamil
}

@app.route('/', methods=['GET', 'POST'])
def home():
    lang = "en"
    context = ""
    if request.method == 'POST':
        text_input = request.form.get('text_input')
        city = request.form.get('city')
        state = request.form.get('state')
        try:
            lat = float(request.form.get('latitude'))
            lng = float(request.form.get('longitude'))
        except:
            pass
        postcode = request.form.get('pincode')
        print(city, state, postcode)
        lang = state_to_language.get(state, "en")
        print(lang)
        chat.send_message(f"the following data set is the sunshine duration in the {city}, {state} region.\n"+str(sunshine(lat, lng))+f"\nthe following dataset contains various weather factors over the last few days in the {city} region\n" + str(weather(lat,lng)) + f"\nthe data about air polution around {city} is listed below\n" + str(airpolution(lat,lng))+ f"make a report for a health clinics and hospitals in the {city} region on what the environmental factors leading to now can impact health. if you find the airpolution")
        weatherReport = chat.last.text
        report = True
        print("weather reported")
        print(weatherReport)
        try:
            if session["context"]:
                session["context"] = session["context"] + "user: " + text_input
                context = session["context"] 
            else:
               session["context"] = "user: " + text_input
               context = session["context"] 
        except:
            print("passed")
            session["context"] = "user: " + text_input
            context = session["context"] 
            pass
        # while True:
        #     prompt = input("ask: ")
        #     chat.send_message(f"i live in {city}, use {lang} and its characters/script when talking to me and try to speak in the dialect of my city/region, that is {city}. speak to me ONLY in the local language of that region, DO NOT use any other language! under no circumstances give a response that contains any other language other than the language of the region. dont put jargons. your response yould be easy to understand. Act as a professional doctor (female) give only professional sounding advices. try to solve the problem of mine. use {weatherReport} if required. ASK FOLLOW UP QUESTIONS to get better understanding of my situation. you can ask questions like age, gender, weight etc. and then help me with my problem. keep the response short.and also recommend expert help if necessary, mention government hospitals and clinics in {city}, GIVE ADDRESS. respond to the following {prompt}")
        #     response = chat.last.text
        #     print(response)
        print(city, state, postcode, lat, lng)
        try:
            prompt = context
            dateTime = datetime.datetime.now()
            print(context)
            chat.send_message(f"I live in {city}. Communicate with me ONLY in {lang}, using its script and the local dialect of {city}. DO NOT use any other language under any circumstances. Act as a professional female healthcare worker, providing clear, jargon-free advice. Address my concern directly and keep responses concise. DONOT put placeholders or variables in the response. Use {weatherReport} only if weather conditions could be affecting my health. Ask relevant follow-up questions (e.g., age, gender, weight) to better understand my situation before advising. If expert help is needed, recommend government hospitals and clinics in {city}. Today is {dateTime} consider the season and weather during this time of the year before giving a response .Now, respond to my health concern: {prompt}")
            print(chat.last.text)
            context = context + "\nAI: " + chat.last.text
            session["context"] = context
            
            return jsonify({
            'response': chat.last.text
        })
        except Exception as e:
            # Catch specific exceptions and access the exception object
            print(f"An error occurred: {e}")
            return render_template('chat.html')
    elif lang == "en":
        print(lang)
    return render_template('chat.html')

@app.route("/logout")
def logout():
    # store the report in the database
    try:
        db.execute("UPDATE users SET history = ? WHERE id = ?", (session["context"], session["user_id"]))
        conn.commit()
    except Exception as e:
        print(e)
        pass
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        phoneNumber = request.form.get("phoneNumber")
        name = db.execute("SELECT * FROM users WHERE phonenumber = ?", (phoneNumber, )).fetchone()
        if not phoneNumber:
            flash("Input phonenumber", "error")
            return render_template("create.html")
        elif name:
            session["number"] = phoneNumber
            return redirect("/loginOTP", code=303)
        else:
            session["number"] = phoneNumber
            return redirect("/getOTP", code=303)
            
    return render_template('create.html')



@app.route("/getOTP", methods = ["GET", "POST"])
def otp():
    if request.method == "GET":
        number = session["number"]
        account_sid = 'ACCOUNT_SID'
        auth_token = 'AUTH_TOKEN'
        otp = random.randint(100000,999999)
        sms = f"Your JANNSEVA verification code is: {otp}"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        from_='NUM',
        body=sms,
        to=number
        )
        session["otp"] = str(otp)
        return render_template("auth.html")

    if request.method == "POST":
        code = request.form.get("OTP")
        if code == session["otp"]:
            db.execute("INSERT INTO users (phonenumber) VALUES(?)", (session["number"],))
            conn.commit()
            rows = db.execute(
            "SELECT * FROM users WHERE phonenumber = ?", (session["number"],)).fetchall()
            
            session["user_id"] = rows[0][0] 
            session["context"] = rows[0][2]
            print(rows[0][2], "context")
            return redirect("/")
        else:
            return redirect("/getOTP", code=303)


@app.route("/loginOTP", methods = ["GET", "POST"])
def loginotp():
    if request.method == "GET":
        number = session["number"]
        account_sid = 'ACCOUNT_SID'
        auth_token = 'AUTH_TOKEN'
        otp = random.randint(100000,999999)
        sms = f"Your JANNSEVA verification code is: {otp}"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        from_='NUM',
        body=sms,
        to=number
        )
        session["otp"] = str(otp)
        return render_template("login.html")

    if request.method == "POST":
        code = request.form.get("OTP")
        if code == session["otp"]:
            rows = db.execute(
            "SELECT * FROM users WHERE phonenumber = ?", (session["number"],)).fetchall()
            session["user_id"] = rows[0][0] 
            session["context"] = rows[0][2]
            print(rows[0][2], "context")
            return redirect("/")
        else:
            return redirect("/loginOTP", code=303)

    
    

if __name__ == '__main__':
    app.run(debug=True)
