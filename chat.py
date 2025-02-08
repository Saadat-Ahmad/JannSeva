import google.generativeai as genai

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

def main():
    while True:
        prompt = input("prompt: ")
        if prompt == "history":
            print(chat.history)
            return
        chat.send_message(prompt)
        response = chat.last.text
        print(response) 
main()