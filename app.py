import boto3
import os 
from google.cloud import pubsub_v1, storage
from publisher import *
from subscriber import *

s3_bucket_name = os.environ["S3_BUCKET"]
topic_name = os.environ["TOPIC"]
subscription_name = os.environ["SUBSCRIPTION"]
google_project_id = os.environ["GOOGLE_PROJECT_ID"]
gcs_bucket_name = os.environ["GCS_BUCKET"]
s3_client = boto3.client("s3")
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
gcs_client = storage.Client()

if os.environ["is_publisher"]:
    keys  = fetch_keys(s3_client, s3_bucket_name)
    for key in keys:
        push_to_topic(publisher, google_project_id, topic_name, key)
    print("Operation completed!!!")
else:
    def upload(message):
        print(f"Received message: {message.data.decode()}")
        download_from_s3(s3_client, s3_bucket_name, message.data.decode())
        upload_to_gcs(gcs_client, google_project_id, gcs_bucket_name, message.data.decode())
        os.remove("temp\/"+ message.data.decode().split("/")[1])
        print("upload successful")
        message.ack()
    get_message(subscriber, google_project_id, subscription_name, upload)
