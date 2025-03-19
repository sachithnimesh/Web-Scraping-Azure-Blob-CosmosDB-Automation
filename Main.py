import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv


# URL of the website to scrape
url = 'https://ikman.lk/en/ads/sri-lanka/motorbikes-scooters'
response = requests.get(url)
print(response.text)  # Shows the HTML content of the page

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())  # Displays a formatted version of the HTML

# Extract the first 5 motorbike data
motorbikes_data = []

# Find all the motorbike listings (li elements with class 'normal--2QYVk')
motorbike_elements = soup.find_all('li', class_='normal--2QYVk')[:5]

for motorbike in motorbike_elements:
    title = motorbike.find('h2', class_='heading--2eONR').text if motorbike.find('h2', class_='heading--2eONR') else 'N/A'
    kilometers = motorbike.find_all('div')[1].text if len(motorbike.find_all('div')) > 1 else 'N/A'
    location_category = motorbike.find('div', class_='description--2-ez3').text if motorbike.find('div', class_='description--2-ez3') else 'N/A'
    price = motorbike.find('div', class_='price--3SnqI').span.text if motorbike.find('div', class_='price--3SnqI') else 'N/A'
    image_url = motorbike.find('img')['src'] if motorbike.find('img') else 'N/A'
    link = "https://ikman.lk" + motorbike.find('a', class_='card-link--3ssYv')['href'] if motorbike.find('a', class_='card-link--3ssYv') else 'N/A'

    motorbikes_data.append({
        'Title': title,
        'Kilometers': kilometers,
        'Location & Category': location_category,
        'Price': price,
        'Image URL': image_url,
        'Link': link
    })

# Convert the data into a DataFrame
df = pd.DataFrame(motorbikes_data)

# Save the data to an Excel file
df.to_excel('top_5_motorbikes.xlsx', index=False)

print("Data has been saved to 'top_5_motorbikes.xlsx'")
print(df)



##################################################################################
##################################################################################
##################################################################################
##################################################################################

# Load environment variables from .env file
load_dotenv()

# Get Azure credentials from environment variables
AZURE_STORAGE_CONNECTION_STRING = os.getenv("key")
CONTAINER_NAME = "imagecontainer"

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

######################################################
###################################################
########################### image to blob storage

import os
import requests
import pandas as pd
from datetime import datetime


# Get today's date
today_date = datetime.today().strftime('%Y-%m-%d')

# Define the project folder path and image folder with today's date
project_dir = r"D:\Browns\Web Scrapping"
image_folder = f"images_on_{today_date}"
save_dir = os.path.join(project_dir, image_folder)

# Create the directory if it does not exist
os.makedirs(save_dir, exist_ok=True)

# Loop to download images
for index, row in df.iterrows():
    image_url = row['Image URL']
    if pd.notnull(image_url) and len(image_url) > 10:
        image_name = f"image_{index+1}_{today_date}.jpg"
        image_path = os.path.join(save_dir, image_name)
        try:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Downloaded: {image_name}")
            else:
                print(f"Failed to download: {image_url} - Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {image_url}: {e}")

print(f"All images are saved in folder: {save_dir}")


import os
import requests
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Step 1: Load Azure Key from .env file
load_dotenv()
azure_key = os.getenv("key")
account_name = "<your_storage_account_name>"  # Replace with your actual account name
connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={azure_key};EndpointSuffix=core.windows.net"


# Step 5: Upload to Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Create container if it doesn't exist
container_name = f"images4sachith"
try:
    blob_service_client.create_container(container_name)
    print(f"Container '{container_name}' created.")
except Exception as e:
    print(f"Container may already exist or error: {e}")

container_name = "images4sachith"

# Upload files
for root, dirs, files in os.walk(save_dir):
    for file in files:
        file_path = os.path.join(root, file)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"{today_date}/{file}")
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data=data, overwrite=True)
        print(f"Uploaded {file} to container '{container_name}'")

print("Upload to Azure Blob Storage completed.")

####################################################################
####################################################################
####################################################################
#################################################################### df to cosmos server 


