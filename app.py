from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

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
        postcode = data.get("postcode")
        lat = data.get("latitude")
        lng = data.get("longitude")
        print(city, state, postcode, lat, lng)
        lang = state_to_language.get(state, "en")
        print(lang)
    elif lang == "en":
        print(lang)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
