def fetch_keys(s3_client, bucket_name):
    paginator = s3_client.get_paginator("list_objects_v2")

    page_iterator = paginator.paginate(Bucket=bucket_name)
    keys = (item['Key'] for page in page_iterator for item in page['Contents'])
    
    return list(keys)

def push_to_topic(client, project_id, topic_name, message):
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=project_id,
        topic=topic_name,
    )
    
    future = client.publish(topic_name, message.encode())
    future.result()

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Dhiraj\Documents\dhiraj\python\migration-utility\pubsub.json"
# s3 = boto3.client("s3")
# publisher = pubsub_v1.PublisherClient()

# key_list  = fetch_keys(s3, "cloudmaratha-test")

# for key in key_list:
#     push_to_topic(publisher, "cogent-sunspot-408823","s3-objects", key)