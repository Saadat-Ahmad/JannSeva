import datetime
from flask import Flask, request, render_template, redirect, jsonify, session, flash
from flask_session import Session
from openMeteo import weather, sunshine
import google.generativeai as genai
from aqi import airpolution
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = '12345'

genai.configure(api_key="GOOGLE_API")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
Session(app)


conn = sqlite3.connect('users.db', check_same_thread=False)
db = conn.cursor()
table = "CREATE TABLE IF NOT EXISTS 'users' (id INTEGER PRIMARY KEY AUTOINCREMENT, phonenumber TEXT UNIQUE NOT NULL, hashed_password TEXT NOT NULL, history TEXT );"
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
        print(city, state, postcode, lat, lng)
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
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        name = db.execute("SELECT * FROM users WHERE phonenumber = ?", (phoneNumber, )).fetchone()
        if not phoneNumber:
            flash("Input phonenumber", "error")
            return render_template("create.html")
        if not password:
            flash("Input password", "error")
            return render_template("create.html")
        if len(password) < 8:
            flash("Password should have at least 8 characters", "error")
            return render_template("create.html")
        if not confirmation:
            flash("Please Confirm password", "error")
            return render_template("create.html")
        if password != confirmation:
            flash("Password was not confirmed correctly", "error")
            return render_template("create.html")
        elif name:
            flash("Account with this phonenumber already exists", "error")
            return render_template("create.html")
        else:
            hashed_password = generate_password_hash(password)
            db.execute("INSERT INTO users (phonenumber, hashed_password) VALUES(?, ?)", (phoneNumber, hashed_password))
            conn.commit()
            rows = db.execute(
            "SELECT * FROM users WHERE phonenumber = ?", (phoneNumber,)).fetchall()
            

            session["user_id"] = rows[0][0] 
            session["context"] = rows[0][3]
            print(rows[0][3], "context")
            return redirect("/")
    return render_template('create.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("phoneNumber"):
            flash("Must provide phone number", "error")
            return render_template("use.html")
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password", "error")
            return render_template("use.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE phonenumber = ?", (request.form.get("phoneNumber"), )).fetchall()
        # Ensure username exists and password is correct
        if (not rows) or (not check_password_hash(rows[0][2], request.form.get("password"))):
            flash("invalid phone number and/or password", "error")
            return render_template("use.html")
        #print(rows)
        # Remember which user has logged in
        session["user_id"] = rows[0][0]
        session["context"] = rows[0][3]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("use.html")


if __name__ == '__main__':
    app.run(debug=True)
