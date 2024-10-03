# RTW Accommodations Data Extraction and Processing

This project automates the extraction of accommodation data from documents (PDF and DOCX formats) and stores the extracted data in an Azure SQL Database. The extracted data includes information about accommodations used in various industries for worker safety, such as descriptions, the body part they aim to assist, and the industry and activity related to the accommodation.

## Table of Contents

- [Overview](#overview)
- <details>
  <summary><strong>Backend</strong></summary>

  - [Requirements](#requirements)
  - [Environment Setup](#environment-setup)
  - [How to Run](#how-to-run)
  
</details>

## Overview

### Key Features

1. **Extracting Text from Files**
   - The script loops through all PDF and DOCX files in a specified directory and extracts text using `PyMuPDF` (for PDFs) and `docx2txt` (for DOCX).

2. **Processing Text with Azure OpenAI**
   - Extracted text is processed by Azure OpenAI to identify and structure accommodations, descriptions, industries, body parts, and activities. The response is returned in JSON format.

3. **Uploading Documents to Azure Blob Storage**
   - Each document is uploaded to Azure Blob Storage, and if a document already exists, its URL is retrieved instead of re-uploading.

4. **Inserting Data into Azure SQL Database**
   - The structured accommodations data is inserted into the Azure SQL Database, ensuring proper relationships between accommodations, injury locations, industries, activities, and documents.

## Backend

### Requirements

Install the necessary Python libraries to run the API:

```bash
cd backend
pip install -r requirements.txt
```

------------
<strong>FOR MAC USERS ONLY</strong>

Install the unixODBC package:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install unixodbc
```
Download the <a href="https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16">ODBC</a> driver for macOS users.

If you are too lazy to read the article just run this:

```bash
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18
```


### Environment Setup
You will need a ```.env``` file in the ```/backend``` folder of your project containing the following variables:

```
AZURE_OPENAI_API_KEY=
AZURE_BLOB_KEY=
DEVELOPMENT_DATABASE_URL=

--- NOTE NOT REQUIRED ---
TEST_DATABASE_URL=
STAGING_DATABASE_URL=
PRODUCTION_DATABASE_URL=
```

### How to Run
After installing all necessary libraries & database drivers and setting your ```.env``` file, run flask in the /backend directory:

```flask run```

This will start a new local server with accessible endpoints.
