from google.cloud import storage

def download_from_storage(bucket_name, source_blob_name, destination_file_name):
    """[Function to download object from google cloud storage to local]
    
    Arguments:
        bucket_name {[string]} -- [Name of bucket in google cloud storage]
        source_blob_name {[string]} -- [Path to object in google cloud storage]
        destination_file_name {[string]} -- [Name and Path object in local]
    
    Returns:
        object  -- [Downloaded object from storage]
    """    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def upload_to_storage(bucket_name, file_bytes, destination_blob_name, content_type):
    """[Function to upload object from local to google cloud storage]
    
    Arguments:
        bucket_name {[string]} -- [Name of bucket in google cloud storage]
        file_bytes {[bytes]} -- [Bytes of object that want to upload to google cloud storage]
        destination_blob_name {[string]} -- [Name and Path object in google cloud storage]
        content_type {[string]} -- [Type of data to save object in google cloud storage]
    """    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(file_bytes, content_type=content_type)