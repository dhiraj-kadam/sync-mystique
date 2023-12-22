def upload_to_gcs(client, project_id, bucket_name, key):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(key)
    blob.upload_from_filename("temp\/"+key.split("/")[1])

def download_from_s3(client, bucket_name, key):
    client.download_file(bucket_name, key, "temp\/"+ key.split("/")[1])

# def callback(message):
#     print(f"Received message: {message.data.decode()}")
#     download_from_s3("cloudmaratha-test", message.data.decode())
#     upload_to_gcs("cogent-sunspot-408823", "cloudmaratha-backup", message.data.decode())
#     os.remove("temp\/"+ message.data.decode().split("/")[1])
#     print("upload successful")
#     message.ack()

def get_message(client, project_id, sub_name, callback):
    subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
        project_id=project_id,
        sub=sub_name,
    )

    with client as subscriber:
        future = subscriber.subscribe(subscription_name, callback)
        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()

# subscriber = pubsub_v1.SubscriberClient()
# gcs_client = storage.Client()
# get_message(subscriber, "cogent-sunspot-408823","s3-objects")