from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.query import Query
import os
from dotenv import load_dotenv

load_dotenv('.env')

client = Client()
client.set_endpoint('https://appwrite.agneepath.co.in/v1')
client.set_project(os.getenv('APPWRITE_PROJECT_ID'))
client.set_key(os.getenv('APPWRITE_API_KEY'))
databases = Databases(client)

def get_user_info(qr_val):
    result = databases.list_documents(
        database_id = os.getenv('APPWRITE_DB_ID'),
        collection_id = os.getenv('APPWRITE_COLLECTION_ID'),
        queries = [
            Query.select(["name", "sport", "user_image"]),
            Query.equal("qr_val", [qr_val])
        ]
    )

    return result['documents'][0]


def on_campus():
    result = databases.list_documents(
        database_id = os.getenv('APPWRITE_DB_ID'),
        collection_id = os.getenv('APPWRITE_COLLECTION_ID'),
        queries = [
            Query.select(["name", "phone_number"]),
            Query.equal('status', True)
        ]
    )

    return result['documents']

def check_user_in(qr_val):
    response = databases.list_documents(
            database_id = os.getenv('APPWRITE_DB_ID'),
            collection_id = os.getenv('APPWRITE_COLLECTION_ID'),
            queries=[Query.equal('qr_val', qr_val)]
        )
    document_id = response['documents'][0]['$id']
    update_response = databases.update_document(
        database_id = os.getenv('APPWRITE_DB_ID'),
        collection_id = os.getenv('APPWRITE_COLLECTION_ID'),
        document_id=document_id,                
        data={'status': True}
    )
    return "Successfully checked in!"

def check_user_out(qr_val):
    response = databases.list_documents(
            database_id = os.getenv('APPWRITE_DB_ID'),
            collection_id = os.getenv('APPWRITE_COLLECTION_ID'),
            queries=[Query.equal('qr_val', qr_val)]
        )
    document_id = response['documents'][0]['$id']
    update_response = databases.update_document(
        database_id = os.getenv('APPWRITE_DB_ID'),
        collection_id = os.getenv('APPWRITE_COLLECTION_ID'),
        document_id=document_id,                
        data={'status': False}
    )
    return "Successfully checked out!"

def breakfast_collected(qr_val):
    response = databases.list_documents(
        database_id = os.getenv('APPWRITE_DB_ID'),
        collection_id = os.getenv('APPWRITE_COLLECTION_ID'),
        queries=[Query.equal('qr_val', qr_val)]
    )
    document_id = response['documents'][0]['$id']
    breakfast_status = response['documents'][0]['breakfast'] + 1
    
    if breakfast_status >= 4:
        return "Player has already finished quota"

    update_response = databases.update_document(
        database_id = os.getenv('APPWRITE_DB_ID'),
        collection_id = os.getenv('APPWRITE_COLLECTION_ID'),
        document_id=document_id,                
        data={'breakfast': breakfast_status}
    )
    return "Breakfast Status Updated"

def lunch_collected(qr_val):
    response = databases.list_documents(
        database_id = os.getenv('APPWRITE_DB_ID'),
        collection_id = os.getenv('APPWRITE_COLLECTION_ID'),
        queries=[Query.equal('qr_val', qr_val)]
    )
    document_id = response['documents'][0]['$id']
    lunch_status = response['documents'][0]['lunch'] + 1

    if lunch_status >= 4:
        return "Player has already finished quota"

    update_response = databases.update_document(
        database_id = os.getenv('APPWRITE_DB_ID'),
        collection_id = os.getenv('APPWRITE_COLLECTION_ID'),
        document_id=document_id,                
        data={'lunch': lunch_status}
    )
    return "Lunch Status Updated"
