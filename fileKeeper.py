#!/usr/bin/python
# Filename: fileKeeper.py
__author__ = 'maxleebo'

ERROR_CODE_INPUT_FORMAT = -1

import glob
import errno
import os
import sys
import tarfile
import zipfile
import string
import commands


def categorizedir(nowpath, androiddir, uncatdir):   # TODO: implement the categorization using a map consists of Keyword and Dir pairs
    grepCmd = "grep -ir 'apk' " + nowpath
    grepInfo = commands.getstatusoutput(grepCmd)
    # print grepInfo[1]
    if "apk" in grepInfo[1]:
        os.system("mv -f " + nowpath + ' ' + androiddir)
        # print 'index',
        # print grepInfo[1].index("apk")
    else:
        os.system("mv -f " + nowpath + ' ' + uncatdir)

def printerror():
    print 'Usage: python fileKeeper.py -OPTION $DIR'
    print 'OPTION:'
    print '-u: uncompress all tars and zips in $DIR'
    print 'e.g. sudo python fileKeeper.py -u /home/max/tmp/testFileKeeper/'


def uncompressdir(dir, androiddir, uncatdir):
    tarpath = dir + '/*.tar*'
    tarfiles = glob.glob(tarpath)
    for onetar in tarfiles:
        periodindex = string.index(onetar, ".")
        lastslashindex = string.rindex(onetar, "/")
        tarname = onetar[lastslashindex+1 : periodindex]
        nowtarpath = dir + '/' + tarname
        if not os.path.exists(nowtarpath):
            os.makedirs(nowtarpath)
        tar = tarfile.open(onetar, 'r')
        for item in tar:
            tar.extract(item, nowtarpath)
        categorizedir(nowtarpath, androiddir, uncatdir)

    zippath = dir + '/*.zip'
    zipfiles = glob.glob(zippath)
    for onezip in zipfiles:
        periodindex = string.index(onezip, ".")
        lastslashindex = string.rindex(onezip, "/")
        zipname = onezip[lastslashindex+1 : periodindex]
        nowzippath = dir + '/' + zipname
        if not os.path.exists(nowzippath):
            os.makedirs(nowzippath)
        fZip = open(onezip, 'rb')
        zip = zipfile.ZipFile(fZip)
        is_encpted = 0
        for zinfo in zip.infolist():
            is_encpted = zinfo.flag_bits & 0x1
            if is_encpted:
                break
        passwd = 'infected666' + zipname[len(zipname) - 1]  # This is default password used, need change for other uses
        if is_encpted:
            for item in zip.namelist():
                zip.extract(item, nowzippath,passwd)    # Sometimes password is needed
        else:
            for item in zip.namelist():
                zip.extract(item, nowzippath)
        categorizedir(nowzippath, androiddir, uncatdir)


# Below is starting of main

if len(sys.argv) != 3:
    try:
        raise Exception()
    except:
        printerror()
        sys.exit(ERROR_CODE_INPUT_FORMAT)
else:
    option = sys.argv[1]
    if option == '-u':
        workDir = sys.argv[2]
        androidDir = workDir + '/' + 'Android'
        if not os.path.exists(androidDir):
            os.makedirs(androidDir)
        uncatDir = workDir + '/' + 'Uncategorized'
        if not os.path.exists(uncatDir):
            os.makedirs(uncatDir)
        uncompressdir(workDir, androidDir, uncatDir)
    else:
        printerror()