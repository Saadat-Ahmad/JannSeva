from flask import Flask, request, render_template, jsonify
from openMeteo import weather, sunshine
import google.generativeai as genai
from aqi import airpolution


app = Flask(__name__)

genai.configure(api_key="AIzaSyBXMdpq9ZPC2-tsUMQ4KOtY-cnJgwmDSOM")

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
    "Uttar Pradesh": "hi",  # Hindi
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
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        city = data.get("city")
        state = data.get("state")
        postcode = data.get("pincode")
        lat = float(data.get("latitude"))
        lng = float(data.get("longitude"))
        print(city, state, postcode, lat, lng)
        lang = state_to_language.get(state, "en")
        print(lang)
        chat.send_message(f"the following data set is the sunshine duration in the {city} region.\n"+str(sunshine(lat, lng))+f"\nthe following dataset contains various weather factors over the last few days in the {city} region\n" + str(weather(lat,lng)) + f"\nthe data about air polution around {city} is listed below\n" + str(airpolution(lat,lng))+ f"make a report for a health clinics and hospitals in the {city} region on what the environmental factors leading to now can impact health. if you find the airpolution")
        weatherReport = chat.last.text
        print(weatherReport)
        while True:
            prompt = input("ask: ")
            chat.send_message(f"i live in {city}, use {lang} and its characters/script when talking to me and try to speak in the dialect of my city/region, that is {city}. speak to me ONLY in the local language of that region, DO NOT use any other language! under no circumstances give a response that contains any other language other than the language of the region. dont put jargons. your response yould be easy to understand. Act as a professional doctor (female) give only professional sounding advices. try to solve the problem of mine. use {weatherReport} if required. ASK FOLLOW UP QUESTIONS to get better understanding of my situation. you can ask questions like age, gender, weight etc. and then help me with my problem. keep the response short.and also recommend expert help if necessary, mention government hospitals and clinics in {city}, GIVE ADDRESS. respond to the following {prompt}")
            response = chat.last.text
            print(response)

    elif lang == "en":
        print(lang)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
