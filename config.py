import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_AI_BASE_URL = os.getenv("OPENAI_BASE_URL")

firebaseConfig = {
  'apiKey': os.getenv("apiKey"),
  'authDomain':  os.getenv('authDomain'),
  'projectId':  os.getenv('projectId'),
  'storageBucket':  os.getenv('storageBucket'),
  'messagingSenderId':  os.getenv('messagingSenderId'),
  'appId':  os.getenv('appId'),
  'measurementId':  os.getenv('measurementId'),
  "databaseURL":  os.getenv("databaseURL")
}

# serviceAccount = {
#   "type": os.getenv('SERVICE_ACCOUNT_TYPE'),
#   "project_id": os.getenv('SERVICE_ACCOUNT_PROJECT_ID'),
#   "private_key_id": os.getenv('SERVICE_ACCOUNT_PRIVATE_KEY_ID'),
#   "private_key": os.getenv('SERVICE_ACCOUNT_PRIVATE_KEY').replace("\\n", "\n"),
#   "client_email": os.getenv('SERVICE_ACCOUNT_CLIENT_EMAIL'),
#   "client_id": os.getenv('SERVICE_ACCOUNT_CLIENT_ID'),
#   "auth_uri": os.getenv('SERVICE_ACCOUNT_AUTH_URI'),
#   "token_uri": os.getenv('SERVICE_ACCOUNT_TOKEN_URI'),
#   "auth_provider_x509_cert_url": os.getenv('SERVICE_ACCOUNT_AUTH_PROVIDER_X509_CERT_URL'),
#   "client_x509_cert_url": os.getenv('SERVICE_ACCOUNT_CLIENT_X509_CERT_URL'),
#   "universe_domain": os.getenv('SERVICE_ACCOUNT_UNIVERSE_DOMAIN')
# }


SERVICE_ACCOUNT = os.getenv("FIREBASE_CREDENTIAL_PATH","serviceAccount.json")
  
