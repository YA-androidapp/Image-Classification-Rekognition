import os
import random
import pathlib
import glob
import boto3
import json

target_ext = '.png'  # 対象画像の拡張子
collection_id = '5hn'  # 顔コレクションのID
target_bucket = '5hn2'  # 画像ファイルをアップロードしたバケット

labels = [1, 2, 3, 4, 5, 9]
file_num = [462, 433, 502, 385, 496, 131]

labels = [2, 3, 4, 5, 9]
file_num = [433, 502, 385, 496, 131]

client = boto3.client('rekognition','us-west-2')


def index(label, filename):
    print(target_bucket + '\t' + filename)
    response = client.index_faces(
        CollectionId=collection_id,
        Image={
            'S3Object': {
                'Bucket': target_bucket,
                'Name': filename,
            }
        },
        ExternalImageId=label,
        DetectionAttributes=[
            'ALL',
        ]
    )

    response = json.dumps(response)
    print(response)


if __name__ == '__main__':
    i = 0
    for label in labels:
        max_file_num = file_num[i]
        for f in range(max_file_num - 1):
            index(str(label), str(label) + '_' + str(f+1) + target_ext)
        i = i + 1