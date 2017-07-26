# .fn.py
# Copyright 2017 Nathan Smith, All Rights Reserved
# https://github.com/nathansmith339

import platform, glob, os, shutil, filecmp, sys, random, getpass    
ASSETS_ABS_PATH = 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets'
EXT = '.jpg'
PICTURES_DIR = '.\\AssetsPictures'
BAD_DIR = '.\\DUPLICATES'
BAD_FLAG = False
IGNORED_EXTS = ['.exe', '.lnk', EXT, BAD_DIR, PICTURES_DIR]
EMPTY_EXT = ''
filesList = []
count = 0


def getImageDims(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    height = int(data[163:165].hex(), 16)
    width = int(data[165:167].hex(), 16)
    return width, height


def isJPEG(filename):
    with open(filename, 'rb') as file:
        data = file.read()
        return data[6:10] == b'JFIF'


def moveFile(filename):
    if not os.path.exists(BAD_DIR):
        os.makedirs(BAD_DIR)
    try:
        shutil.move(filename, BAD_DIR + '\\' + filename)
    except shutil.Error:
        newname = ''.join([random.choice('0123456789abcdef') for x in range(64)]) + EXT
        shutil.move(filename, BAD_DIR + '\\' + newname)


def fetchAssets():
    # fetches valid assets files
    count = 0
    print('Fetching assets pictures...')
    if not os.path.exists(PICTURES_DIR):
        os.makedirs(PICTURES_DIR)
    for file_name in os.listdir(ASSETS_ABS_PATH):
        full_file_name = os.path.join(ASSETS_ABS_PATH, file_name)
        if (os.path.isfile(full_file_name)):
            if isJPEG(full_file_name):
                filename = os.path.join(full_file_name)
                width, height = getImageDims(full_file_name)
                if width == 1920 and height == 1080:
                    shutil.copy(full_file_name, os.getcwd() + PICTURES_DIR[1:] + '\\' + file_name + EXT)
                    count += 1
    os.chdir(PICTURES_DIR)
    return count


if __name__ == "__main__":
    if platform.system() != 'Windows':
        raise ValueError('This file is not compatible with %s. This is intended for Windows' % (platform.system()))
    duplicate_file_count = 0
    count = fetchAssets()
    # check files for duplicates: both in name and data
    for filename in os.listdir(os.getcwd()):
        base_file, ext = os.path.splitext(filename)
        if filename != BAD_DIR and filename != PICTURES_DIR:
            filesList.append(filename)

        if ext == EMPTY_EXT and not os.path.isdir(filename):
            try:
                os.rename(filename, base_file + EXT)
            except FileExistsError:
                duplicate_file_count += 1
                moveFile(filename)
                
        for file in filesList:
            try:
                os.rename(filename, PICTURES_DIR[1:] + '\\' + base_file + EXT)
                if filecmp.cmp(filename, file) and filename != file and filename not in IGNORED_EXTS:
                    duplicate_file_count += 1
                    moveFile(filename)
                fileList.remove(filename)
            except FileNotFoundError:
                continue
            
                
    print('Found %d files as pictures\nSaved to new directory "%s"' % (count, PICTURES_DIR[2:]))
    if duplicate_file_count:
        print('%d file(s) found as duplicates have been found. Duplicates can be in both name and/or content. Check the duplicates folder for the files.' % (duplicate_file_count))
    input("Press Enter to continue...")
