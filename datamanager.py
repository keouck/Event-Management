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

# user_data = {
#     'name': 'Amay',
#      'email': 'amay.agarwal_ug2024@ashoka.edu.in',
#      'phone_number': '9999999999',
#      'university_name': "Ashoka University",
#      'sport': "Football",
#      'status': False,
#      'breakfast': 0,
#      'lunch': 0,
#      'user_image': 'https://via.placeholder.com/150',
#      'qr_val': r'9a5dcfe0f68382aa8688f4d7722c22b0505229a8d4571f030ed911f562d2374860170b29dd0548744cebce615680bae7d12437d9b1f0df01238fc0b163b4f78a8256e2aad8dc3d5d68e4ce0371ac8fe5a680245ec903a8b39e65d7934cb3f531873d0c8c'
#      }

# def add_user(user_data):
#     try:
#         doc = databases.create_document(database_id='677eca45003cf2bf8797', collection_id='678017ef002edc0bfa1e', document_id=ID.unique(), data = user_data)
#     except Exception as e:
#         print("An error occurred:", e)

# add_user(user_data)

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

# queried_data = get_user_info(r'9a5dcfe0f68382aa8688f4d7722c22b0505229a8d4571f030ed911f562d2374860170b29dd0548744cebce615680bae7d12437d9b1f0df01238fc0b163b4f78a8256e2aad8dc3d5d68e4ce0371ac8fe5a680245ec903a8b39e65d7934cb3f531873d0c8c')
# print(queried_data)