import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Azure credentials from environment variables
AZURE_STORAGE_CONNECTION_STRING = os.getenv("key")
CONTAINER_NAME = "sachith_imagecontainer"

# Initialize Azure Blob Service
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Read Excel file to get image URLs
df = pd.read_excel("top_5_motorbikes.xlsx")

# Folder to temporarily save images
os.makedirs("images", exist_ok=True)

# Process each image
for index, row in df.iterrows():
    image_url = row["Image URL"]
    
    # Generate a unique blob name
    blob_name = f"motorbike_{index+1}.jpg"
    
    try:
        # Download the image
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # Save locally before uploading
            image_path = f"images/{blob_name}"
            with open(image_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            
            # Upload to Azure Blob Storage
            blob_client = container_client.get_blob_client(blob_name)
            with open(image_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            
            print(f"Uploaded {blob_name} successfully!")
        else:
            print(f"Failed to download {image_url}")
    
    except Exception as e:
        print(f"Error processing {image_url}: {e}")
