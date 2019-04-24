import os
import random
import pathlib
import glob
import boto3
import json

target_ext = '.png'  # 対象画像の拡張子
collection_id = '5hn'  # 顔コレクションのID
target_bucket = '5hn'  # 画像ファイルをアップロードしたバケット

labels = [1, 2, 3, 4, 5, 9]
file_num = [462, 433, 502, 385, 496, 131]

client = boto3.client('rekognition')


def index(label, filename):
    print(filename)
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
    for label in labels:
        for max_file_num in file_num:
            for f in range(max_file_num):
                index(str(label), str(label) + '_' + str(f+1) + target_ext)
