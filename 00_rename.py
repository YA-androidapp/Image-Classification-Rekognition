import glob
import os
import pathlib
import random


# 対象ディレクトリ(このディレクトリのサブディレクトリ名がラベルを表し、それらの中に画像ファイルが格納されている)
target_dir = 'train'
target_ext = '.png'  # 対象画像の拡張子
enable_random = True  # 連番をランダムに付与するか


def main(base_dir, target_ext, enable_random):
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

            # random
            if enable_random == True:
                random.shuffle(files)
            else:
                files.sort()

            for i, f in enumerate(files, 1):
                ftitle, fext = os.path.splitext(f)  # fextの先頭はピリオド
                new_name = label + '_{0:d}'.format(i) + fext
                os.rename(f, os.path.join(os.path.dirname(d), new_name))
                print('\t' + f + ' => ' + new_name)
    print('done')


if __name__ == '__main__':
    main(target_dir, target_ext, enable_random)
