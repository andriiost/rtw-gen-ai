import os
from azure.storage.blob import BlobServiceClient

# Azure Blob Storage setup
blob_service_client = BlobServiceClient(
    account_url=f"https://{os.getenv('AZURE_STORAGE_ACCOUNT')}.blob.core.windows.net",
    credential=os.getenv('AZURE_BLOB_KEY')
)
container_name = os.getenv("AZURE_BLOB_CONTAINER")
