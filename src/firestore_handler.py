# firestore_handler.py, Path: facw7x3-copygen-api/src/firestore_handler.py

import datetime
from google.cloud import firestore

def store_responses(db, data):
    # Create a new document in the "responses" collection
    doc_ref = db.collection("responses").document()
    # Add a timestamp field to the data
    data["timestamp"] = datetime.datetime.now()
    # Set the document data
    doc_ref.set(data)

def get_latest_responses(db):
    # Get the latest document from the "responses" collection
    query = db.collection("responses").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1)
    docs = query.stream()
    # Extract the responses from the document
    responses = [doc.to_dict() for doc in docs]
    return responses

def load_system_role_prompt(db):
    # Retrieve the system role prompt from Firestore
    doc_ref = db.collection("prompts").document("a7djMKpmCftCtBfb9UBP")
    doc = doc_ref.get()
    return doc.get("ai_role_direct_response_email_copywriter")

def load_email_prompt(db, selected_template):
    # Retrieve the corresponding email prompt from Firestore based on the selected template
    doc_ref = db.collection("prompts").document("TapKYDTAtPgcpGM66YWE")
    doc = doc_ref.get()
    field_name = {
        "email-template-1": "email001_unique_solution",
        "email-template-2": "email002_emotional_impact",
        "email-template-3": "email003_negatively_perceived_item"
    }.get(selected_template)
    return doc.get(field_name)

def create_context(data, system_role_prompt, selected_template):
    # Initialize an empty context string
    context = ""

    # Replace the placeholders with the corresponding values from the request data
    context += system_role_prompt
    context = context.replace("<<Answer to question 1>>", data['targetMarket'])
    context = context.replace("<<Answer to question 2>>", data['problemToSolve'])
    context = context.replace("<<Answer to question 3>>", data['dislikedSolutions'])
    context = context.replace("<<Answer to question 4>>", data['uniqueSolution'])
    context = context.replace("<<Answer to question 5>>", data['solutionMechanism'])
    context = context.replace("<<Answer to question 6>>", data['credibility'])

    # Add the separator and the selected email template to the context
    context += "\nHere's the template:\n"
    context += selected_template + "\n"

    return context