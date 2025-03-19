Sure! Here's a professional **README.md** template for your project:

---

# 🚀 Web Scraping + Azure Blob & CosmosDB Automation

## 📚 **Project Overview**

This project automates the following pipeline:

1. **Scrape & Download Motorbike Images**  
   From a given dataframe (e.g., from ikman.lk), it downloads images to a local folder named as `images_<today's date>`.

2. **Upload Images to Azure Blob Storage**  
   The downloaded images are uploaded into a **Blob Storage container** called `images4sachith` inside a folder named as today's date.

3. **Process Excel Data and Save to Azure Cosmos DB**  
   Converts `top_5_motorbikes.xlsx` to JSON format and uploads it into **Azure Cosmos DB** under a database `sachithikman` with a **container named as tomorrow's date**.

---

## 🛠 **Tech Stack**

- **Python 3.x**
- **pandas**
- **requests**
- **Azure SDKs**:
  - `azure-storage-blob`
  - `azure-cosmos`
- **dotenv**

---

## 📁 **Folder Structure**

```
D:\
 └── Browns\
     └── Web Scrapping\
         ├── images_YYYY-MM-DD\       # Downloaded images (date-based)
         ├── top_5_motorbikes.xlsx    # Excel data source
         ├── .env                     # Azure credentials
         ├── upload_to_blob_and_cosmos.py
         └── README.md
```

---

## ⚙ **Environment Setup**

1. **Clone this repo or copy files**
2. **Install dependencies:**

```bash
pip install pandas requests python-dotenv azure-storage-blob azure-cosmos
```

3. **Configure your `.env` file:**

```env
key=<your_azure_blob_storage_key>
cosmos_endpoint=https://<your-cosmos-account>.documents.azure.com:443/
cosmos_key=<your_cosmos_primary_key>
```

---

## 🚀 **How It Works**

### **Step 1: Download Motorbike Images**

- Images are pulled from a dataframe's `Image URL` column.
- Saved locally into `images_<today's date>` folder.

### **Step 2: Upload Images to Azure Blob**

- Creates a container: `images4sachith` (if not exists).
- Uploads images under the folder `YYYY-MM-DD/` (based on today’s date).

### **Step 3: Upload Excel Data to Cosmos DB**

- Converts `top_5_motorbikes.xlsx` into JSON.
- Automatically cleans NaN/null values.
- Uploads into Cosmos DB under:
  - Database: `sachithikman`
  - Container: `YYYY-MM-DD` (next day's date)

---

## 🎯 **Usage**

```bash
python upload_to_blob_and_cosmos.py
```

- Will download images, upload to blob storage, and push cleaned data to Cosmos DB.

---

## 📝 **Notes**

- Cosmos DB requires each document to have an `"id"` field (auto-generated in the script).
- Handles `NaN` and empty Excel cells properly to avoid Cosmos JSON errors.
- Supports daily automation (just rerun next day to create new containers).

---

## 🧩 **To-Do / Optional Improvements**
- Add **logging** to a `.log` file for production usage.
- Implement **batch uploads** to Cosmos DB for faster performance.
- Setup **error handling and retry logic** for network issues.

---

## 🔐 **Security**
- Your `.env` file should **never be committed to GitHub**.
- Keep your keys & secrets private.

---

---

Would you like me to also prepare a **`requirements.txt`** file and a sample `.env` template for you? 🚀
"# Web-Scraping-Azure-Blob-CosmosDB-Automation" 
