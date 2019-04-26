import os
import random
import pathlib
import glob
import boto3
import json

# 対象ディレクトリ(このディレクトリのサブディレクトリ名がラベルを表し、それらの中に画像ファイルが格納されている)
target_dir = 'answer'
target_ext = '.png'  # 対象画像の拡張子
collection_id = '5hn'  # 顔コレクションのID
target_bucket = '5hn2'  # 画像ファイルをアップロードしたバケット

labels = [1, 2, 3, 4, 5, 9]
file_num = [462, 433, 502, 385, 496, 131]

client = boto3.client('rekognition','us-west-2')


def search(label, filename):
    print(target_bucket + '\t' + filename)
    try:
        response = client.search_faces_by_image(
            CollectionId=collection_id,
            Image={
                'S3Object': {
                    'Bucket': target_bucket,
                    'Name': filename,
                }
            },
            MaxFaces = 100,
            FaceMatchThreshold = 80
        )

        response = json.loads(json.dumps(response))
        print(response)

        return (str(label) == str(response['FaceMatches'][0]['Face']['ExternalImageId'])) if 1 else 0
    except:
        return 0


def main(base_dir):
    global target_ext

    p = pathlib.Path(base_dir)
    abs_path = p.resolve()
    print('abs_path: ' + str(abs_path))

    if p.exists() == False:
        return

    if target_ext.startswith('.') == False:
        target_ext = '.' + target_ext

    glob_dir = os.path.join(str(abs_path), '*') + os.path.sep
    dirs = glob.glob(glob_dir)

    count_items_all = 0
    count_items_correct = 0
    if len(dirs) > 0:
        for d in dirs:
            label = os.path.basename(os.path.dirname(d))
            print('label: ' + label + '\td: ' + d)
            files = glob.glob(os.path.join(d, '*') + target_ext)

            for i, f in enumerate(files, 1):
                # print('f: ' + f)
                # count_items_correct += search(label, f)
                f = os.path.basename(f)
                print('f: ' + f)
                count_items_correct += search(label, f)
                count_items_all += 1
    print('Complete. {:.2%}'.format(count_items_correct / count_items_all))


if __name__ == '__main__':
    main(target_dir)
