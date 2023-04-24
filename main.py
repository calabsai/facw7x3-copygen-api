# main.py, Path: backend/app/src/main.py

import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS
from google.cloud import secretmanager

# Import custom modules
from src import (
    firestore_handler,
    openai_handler,
    openai_gpt_3_5_t_handler,
    anthropic_handler
)

# Create the Secret Manager client
client = secretmanager.SecretManagerServiceClient()

# Retrieve secrets from Google Cloud Secret Manager
def get_secret(secret_name):
    project_id = "facw7x3"
    secret_version = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": secret_version})
    return response.payload.data.decode("UTF-8")

# Retrieve credentials and API keys
google_application_credentials = get_secret("facw7x3-906d4f9a9f33")
openai_api_key = get_secret("openai-api-key")
anthropic_api_key = get_secret("anthropic-api-key")

# Load credentials
cred_dict = json.loads(google_application_credentials)
cred = credentials.Certificate(cred_dict)

# Initialize the Firebase app and Firestore client
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    # App already initialized, do nothing
    pass
db = firestore.client()

app = Flask(__name__, static_folder='static')
CORS(app, resources={r'*': {'origins': '*'}})

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route("/", methods=["GET"])
def index():
    # This route will only serve the main page
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        # This route will handle text generation requests
        data = request.get_json()
        print(f"Request data: {data}")

        # Extract the selected email template and language model from the request data
        selected_template = data.get("selectedTemplate")
        language_model = data.get("languageModel")
        print(f"Selected language model: {language_model}")

        # Load the email prompt using the new function `load_email_prompt`
        prompt = firestore_handler.load_email_prompt(db, selected_template)
        print(f"Loaded email prompt: {prompt}")

        # Fetch the latest responses from Firestore using `get_latest_responses`
        responses = firestore_handler.get_latest_responses(db)
        print(f"Latest responses: {responses}")

        # Load the system role prompt using the new function `load_system_role_prompt`
        system_role_prompt = firestore_handler.load_system_role_prompt(db)
        print(f"Loaded system role prompt: {system_role_prompt}")

        # Create a context string based on the latest responses and system role prompt
        context = firestore_handler.create_context_from_responses(responses, system_role_prompt)
        print(f"Created context: {context}")
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})

    # Generate copy using the appropriate language model handler
    if language_model == "gpt-4":
        generated_copy = openai_handler.generate_copy(system_role_prompt, context, prompt, openai_api_key=openai_api_key)    
    elif language_model == "gpt-3.5-turbo":
        generated_copy = openai_gpt_3_5_t_handler.generate_copy(system_role_prompt, context, prompt, openai_api_key=openai_api_key)
    elif language_model == "claude-v1.3":
        generated_copy = anthropic_handler.generate_copy(system_role_prompt, context, prompt, api_key=anthropic_api_key)
    else:
        return jsonify({"error": "Invalid language model selected"})

    return jsonify({"generated_copy": generated_copy})

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host=host, port=port)