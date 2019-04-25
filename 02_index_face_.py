import os
import random
import pathlib
import glob
import boto3
import json

# 対象ディレクトリ(このディレクトリのサブディレクトリ名がラベルを表し、それらの中に画像ファイルが格納されている)
target_dir = 'class'
target_ext = '.png'  # 対象画像の拡張子
collection_id = '5hn' # 顔コレクションのID
target_bucket = '5hn' # 画像ファイルをアップロードしたバケット

client = boto3.client('rekognition','us-west-2')


def index(label, file):
    response = client.index_faces(
        CollectionId=collection_id,
        Image={
            'S3Object': {
                'Bucket': target_bucket,
                'Name': label + '/' + file,
            }
        },
        ExternalImageId=label,
        DetectionAttributes=[
            'ALL',
        ]
    )

    response = json.dumps(response)
    print(response)


def main(base_dir, target_ext):
    p = pathlib.Path(base_dir)
    abs_path = p.resolve()
    print('abs_path: ' + str(abs_path))

    if p.exists() == False:
        return

    if target_ext.startswith('.') == False:
        target_ext = '.' + target_ext

    glob_dir = os.path.join(str(abs_path), '*') + os.path.sep
    dirs = glob.glob(glob_dir)

    if len(dirs) > 0:
        for d in dirs:
            label = os.path.basename(os.path.dirname(d))
            print('label: ' + label + '\td: ' + d)
            files = glob.glob(os.path.join(d, '*') + target_ext)

            for i, f in enumerate(files, 1):
                filename = os.path.basename(f)
                print('\tfilename: ' + filename)
                index(label, filename)
    print('done')


if __name__ == '__main__':
    main(target_dir, target_ext)
