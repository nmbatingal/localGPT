import os
import sys
import tempfile
import requests
import time
import argparse

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(__name__)
app.secret_key = "LeafmanZSecretKey"

API_HOST = "http://localhost:5110/api"
CONVERSATION_FILE = 'conversation.txt'

def save_conversation(conversation):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(CONVERSATION_FILE, 'a') as f:
        f.write(f'{timestamp} - User: {user_prompt}\n')
        f.write(f'{timestamp} - User: {response}\n')

def load_conversations():
    conversation = []
    try:
        with open('conversation.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                conversation.append(line.strip())
    except FileNotFoundError:
        pass
    return conversation

# PAGES #
@app.route("/", methods=["GET", "POST"])
def home_page():
    response_dict = {'Answer' : 'This is a placeholder answer.'}
    conversation = load_conversations()
    if request.method == "POST":
        if "user_prompt" in request.form:
            user_prompt = request.form["user_prompt"]
            # Simulate a delay for generating the response 
            time.sleep(2)
            # process the user prompt and generate a response
            response_dict['Answer'] = f'You asked: {user_prompt}'
            save_conversation(user_prompt, response_dict['Answer'])
            # print(f"User Prompt: {user_prompt}")
            # response_dict['Answer'] =f'{user_prompt}'

            # main_prompt_url = f"{API_HOST}/prompt_route"
            # response = requests.post(main_prompt_url, data={"user_prompt": user_prompt})

            # print(response.status_code)  # print HTTP response status code for debugging
            # if response.status_code == 200:
                # print(response.json())  # Print the JSON data from the response
                # return render_template("home.html", show_response_modal=True, response_dict=response.json(), conversations=conversations)
        elif "documents" in request.files:
            documents = request.files.getlist('documents')
            action = request.form.get('action')
            # Handle file upload and processing based on the action
            response_dict['Answer'] = f'{len(documents)} documents uploaded with action: {action}'
            save_conversation('Documents uploaded', response_dict['Answer'])

            # delete_source_url = f"{API_HOST}/delete_source"  # URL of the /api/delete_source endpoint
            # if request.form.get("action") == "reset":
            #     response = requests.get(delete_source_url)

            # save_document_url = f"{API_HOST}/save_document"
            # run_ingest_url = f"{API_HOST}/run_ingest"  # URL of the /api/run_ingest endpoint
            # files = request.files.getlist("documents")
            # for file in files:
            #     print(file.filename)
            #     filename = secure_filename(file.filename)
            #     with tempfile.SpooledTemporaryFile() as f:
            #         f.write(file.read())
            #         f.seek(0)
            #         response = requests.post(save_document_url, files={"document": (filename, f)})
            #         print(response.status_code)  # print HTTP response status code for debugging
            # # Make a GET request to the /api/run_ingest endpoint
            # response = requests.get(run_ingest_url)
            # response_dict['Answer'] = f'{len(files)} document uploaded with action: {request.form.get("action")}'
            # print(response.status_code)  # print HTTP response status code for debugging

    # Display the form for GET request
    return render_template(
        "home.html",
        # show_response_modal=False,
        # response_dict={"Prompt": "None", "Answer": "None", "Sources": [("ewf", "wef")]},
        response_dict=response_dict,
        conversation=conversation,
    )

@app.route('/generate_response', methods=['POST'])
def generate_response():
    user_prompt = request.form['user_prompt']
    # Simulate a delay for generating the response
    time.sleep(2)
    # Process the user prompt and generate a response
    response = f'You asked: {user_prompt}'
    save_conversation(user_prompt, response)
    return jsonify({'Answer': response})
    # main_prompt_url = f"{API_HOST}/prompt_route"
    # response = requests.post(main_prompt_url, data={"user_prompt": user_prompt})
    # if response.status_code == 200:
        # return jsonify(response.json())
    # return jsonify({'Answer': 'An error occured while generating the response.'})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080, help="Port to run the UI on. Defaults to 8080.")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to run the UI on. Defaults to 127.0.0.1. "
        "Set to 0.0.0.0 to make the UI externally "
        "accessible from other devices.",
    )
    args = parser.parse_args()
    app.run(debug=True, host=args.host, port=args.port)
