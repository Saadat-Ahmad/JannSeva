# JannSeva

JannSeva is a Flask-based web application designed to address rural healthcare challenges in India by overcoming language barriers. It provides localized health information, clinic/hospital details, and supports multi-language interactions.

## Features
- **Automatic Language Detection:** Loads the website in the local language based on the user's location.
- **Location-Based Health Reports:** Uses Open-Meteo API for past weather data and Google's Gemini API to generate health-related reports.
- **Healthcare Query Support:** Allows users to submit health-related queries, providing AI-generated responses.
- **Twilio OTP Authentication:** Secure user authentication using Twilio OTP, with phone numbers stored as primary keys in SQLite.
- **User Chat History:** Stores a summary of all conversations for context-aware responses.

## Tech Stack
- **Backend:** Flask, SQLAlchemy, SQLite
- **Frontend:** HTML, CSS, JavaScript
- **APIs Used:**
  - Open-Meteo (weather data)
  - Google Gemini (health reports & responses)
  - Twilio (OTP authentication)
  - Nominatim OpenStreetMap (location data)

## Setup Instructions

### Prerequisites
- Python 3.x
- Flask and other dependencies
- Twilio account for OTP authentication
- Google Gemini API access

## App Flow Chart
![App Flow Chart](SERVER (1).png)
