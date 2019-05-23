import boto3
import datetime
import glob
import json
import os
import pathlib
import random


# $ aws s3 mb s3://5hntest
# $ aws s3 sync test s3://5hntest --acl public-read


scrpath = os.path.abspath(os.path.dirname(__file__))
os.chdir(scrpath)

# 対象ディレクトリ(このディレクトリのサブディレクトリ名がラベルを表し、それらの中に画像ファイルが格納されている)
target_dir = 'test'
target_ext = '.png'  # 対象画像の拡張子
collection_id = '5hn'  # 顔コレクションのID
target_bucket = '5hntest'  # 画像ファイルをアップロードしたバケット

# テスト結果を出力するテキストファイル名
nowstr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
result_filename = 'result-test-'+nowstr+'.txt'

client = boto3.client('rekognition', 'us-west-2')


def search(label, filename):
    print('search: ' + target_bucket + '\t' + label + '/' + filename)
    try:
        response = client.search_faces_by_image(
            CollectionId=collection_id,
            Image={
                'S3Object': {
                    'Bucket': target_bucket,
                    'Name': label + '/' + filename,
                }
            },
            MaxFaces=1,
            FaceMatchThreshold=80
        )

        response = json.loads(json.dumps(response))
        # print(response)
        name = str(response['FaceMatches'][0]['Face']['ExternalImageId'])
        pred = str(response['FaceMatches'][0]['Face']['Confidence'])
        print(name, pred)

        return (str(label) == str(response['FaceMatches'][0]['Face']['ExternalImageId'])) if 1 else 0
    except Exception as e:
        print(e)
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
                f = os.path.basename(f)
                count_items_correct += search(label, f)
                count_items_all += 1

    if count_items_all > 0:
        mes = 'Complete. accuracy:{} / {} = {:.2%}'.format(
            count_items_correct, count_items_all, count_items_correct / count_items_all)
    else:
        mes = 'Complete.'
    mes += ' ' + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    print(mes)
    with open(os.path.join(scrpath, result_filename), mode='a') as f:
        f.write(mes + '\n')


if __name__ == '__main__':
    main(target_dir)
