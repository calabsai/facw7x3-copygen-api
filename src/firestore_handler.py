# firestore_handler.py, Path: facw7x3-copygen-api/src/firestore_handler.py

import datetime
from google.cloud import firestore
import logging

# Configure logging
logging.basicConfig(filename='firestore_handler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    try:
        # Retrieve the system role prompt from Firestore
        doc_ref = db.collection("system_roles").document("email_copywriter")
        doc = doc_ref.get()
        
        # Print and log the retrieved document
        print("Retrieved document:", doc.to_dict())
        logging.info("Retrieved document: %s", doc.to_dict())
        
        # Extract the field value (replace "correct_field_name" with the actual field name)
        field_value = doc.get("systemRoleEmailCopywriterV2_20230502")
        
        # Print and log the extracted field value
        print("Field value:", field_value)
        logging.info("Field value: %s", field_value)
        
        return field_value
    except Exception as e:
        # Print and log any exceptions that occur
        print("Error:", e)
        logging.error("Error: %s", e)
        return None

def load_email_prompt(db, selected_template):
    # Retrieve the corresponding email prompt from Firestore based on the selected template
    doc_ref = db.collection("prompts").document("email_templates")
    doc = doc_ref.get()
    field_name = {
        "email-template-1": "email001UniqueSolutionV1_20230425",
        "email-template-2": "email002EmotionalImpactV1_20230425",
        "email-template-3": "email003NegativelyPerceivedItemV1_20230425"
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
    context += "\nDo not include any unnecessary greetings or explanations. Simply generate the copy. Note: Replace the placeholders in square brackets with appropriate text. Use the following template to create the email:\n";
    context += selected_template + "\n";

    return context

def add_carriage_returns_to_document_fields(db, collection_name, document_name):
    # Get a reference to the specified document
    doc_ref = db.collection(collection_name).document(document_name)
    
    # Retrieve the document data
    doc = doc_ref.get()
    if not doc.exists:
        print("Document not found.")
        return
    
    # Get the document fields as a dictionary
    doc_fields = doc.to_dict()
    
    # Iterate over each field value and add carriage returns
    modified_fields = {}
    for field_name, field_value in doc_fields.items():
        if isinstance(field_value, str):
            # Modify the field value by adding carriage returns (e.g., replace double spaces with '\n\n')
            modified_field_value = field_value.replace('  ', '\n\n\n')
            modified_fields[field_name] = modified_field_value
    
    # Update the fields in the document
    doc_ref.update(modified_fields)