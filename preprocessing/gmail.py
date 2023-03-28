from dotenv import load_dotenv
load_dotenv()

import base64
import datetime
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores import Pinecone

# Set up Gmail API credentials
CLIENT_SECRET_FILE = "credentials.json"
API_NAME = "gmail"
API_VERSION = "v1"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Authenticate and access Gmail API
creds = None
if os.path.exists("token.pickle"):
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)

gmail = googleapiclient.discovery.build(
    API_NAME, API_VERSION, credentials=creds)
embeddings = OpenAIEmbeddings()
pinecone.init(environment="us-west4-gcp")
index_name = "tvanas-emails"

# Retrieve the last 100 days of emails from Gmail
now = datetime.datetime.utcnow()
past_100_days = now - datetime.timedelta(days=100)
query = f"after:{past_100_days.strftime('%Y/%m/%d')} -label:noindex"

results = gmail.users().messages().list(
    userId="me", q=query).execute()
messages = results.get("messages", [])


next_page_token = None
while True:
    documents = []
    results = gmail.users().messages().list(userId="me", q=query, maxResults=100, pageToken=next_page_token).execute()
    messages = results.get("messages", [])

    # Iterate through emails, embed them using OpenAI, and store in Pinecone
    for message in messages:
        msg = gmail.users().messages().get(userId="me", id=message["id"]).execute()
        subject = ""
        body = ""
        from_address = ""
        to_address = ""

        for header in msg["payload"]["headers"]:
            if header["name"] == "Subject":
                subject = header["value"]
            if header["name"] == "From":
                from_address = header["value"]
            if header["name"] == "To":
                to_address = header["value"]

        if "parts" in msg["payload"]:
            for part in msg["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    if 'data' in part["body"]:
                        body = base64.urlsafe_b64decode(
                            part["body"]["data"]).decode("utf-8")

        content = f"{subject}\n{body}"
        documents.append(Document(page_content=content, metadata={
            "from_address": from_address,
        }))

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    next_page_token = results.get("nextPageToken")
    docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
    print("next_page_token", next_page_token)
    if not next_page_token:
        break

query = "What emails are there regarding my subaru"
docs = docsearch.similarity_search(query)

for doc in docs:
    print(doc.page_content)
