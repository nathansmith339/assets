// .fn.py
// Copyright 2017 Nathan Smith, All Rights Reserved
// https://github.com/nathansmith339

import glob, os, shutil, filecmp, sys, random, getpass

ASSETS_ABS_PATH = 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets'
EXT = '.jpg'
BAD_DIR = '.\\BAD'
count = 0
files_changed = ''
filesList = []


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
        
# fetches assets files
print('fetching assets from %s', ASSETS_ABS_PATH)
src_files = os.listdir(ASSETS_ABS_PATH)
for file_name in src_files:
    full_file_name = os.path.join(ASSETS_ABS_PATH, file_name)
    if (os.path.isfile(full_file_name)):
        if isJPEG(full_file_name):
            filename = os.path.join(full_file_name)
            width, height = getImageDims(full_file_name)
            if width == 1920 and height == 1080:
                shutil.copy(full_file_name, os.getcwd())


# check files for duplicates: both in name and data
for filename in glob.iglob(os.path.join('.', '*')): 
    base_file, ext = os.path.splitext(filename)
    if filename != BAD_DIR and not (filename in filesList):
        filesList.append(filename)
    if ext != EXT and base_file != BAD_DIR:
        try:
            if not os.path.exists(BAD_DIR):
                os.makedirs(BAD_DIR)
            os.rename(filename, base_file + EXT)
            files_changed += base_file + '\n'
            count += 1
        except FileExistsError:
            shutil.move(base_file, BAD_DIR + '\\' + base_file[2:] + EXT)
            files_changed += base_file + '\n'
            count += 1
    for file in filesList:
        try:
            if filecmp.cmp(filename, file) and filename != file and filename != BAD_DIR:
                    shutil.move(filename, BAD_DIR + '\\' + filename[:2])
                    files_changed += filename + ' (duplicate-data file)\n'
                    count += 1
                    break
        except FileNotFoundError:
            continue
        except shutil.Error:
            newname = ''.join([random.choice('0123456789abcdef') for x in range(64)]) + EXT
            shutil.move(filename, BAD_DIR + '\\' + newname)
            files_changed += filename + ' -> ' + BAD_DIR + '\\' + newname + '\n'
            count += 1

print('changed %d files\n' % count)
if (files_changed != '' and count != 0):
    print('files changed:\n%s' % files_changed)

input("Press Enter to continue...")
