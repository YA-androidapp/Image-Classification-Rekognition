import boto3
import json


collection_id = '5hn'  # 作成する顔コレクションのID


client = boto3.client('rekognition', 'us-west-2')

response = client.create_collection(
    CollectionId=collection_id
)

response = json.dumps(response)
print(response)
