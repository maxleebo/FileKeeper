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


def removespace(workdir):
    allpath = workdir + '/*'
    allfiles = glob.glob(allpath)
    for onefile in allfiles:
        # print onefile
        if " " in onefile:
            nospaceOneFile = onefile.replace(" ", "_")
            os.rename(onefile, nospaceOneFile)


def categorizedir(nowpath, androiddir, uncatdir):   # TODO: implement the categorization using a map consists of Keyword and Dir pairs
    grepCmd = "find " + nowpath + " -iname " + "*apk*"
    grepInfo = commands.getstatusoutput(grepCmd)
    # print grepInfo[1]
    if "apk" in grepInfo[1]:
        os.system("mv -f " + nowpath + ' ' + androiddir)
        # print 'index',
        # print grepInfo[1].index("apk")
    else:
        os.system("mv -f " + nowpath + ' ' + uncatdir)


def printerror():
    print 'Usage: python fileKeeper.py -OPTION $DIR [$OUTDIR]'
    print 'OPTION:'
    print '-u: uncompress all tars and zips in $DIR'
    print 'e.g. sudo python fileKeeper.py -u /home/max/tmp/testFileKeeper/'
    print '-m: move finished files($OUTDIR w.r.t $DIR) to ../done directory'
    print 'e.g. sudo python fileKeeper.py -m C:\Users\Max\TIFS\logs\googleplay\\fiveCatAppsDir\social\merged\\   ' \
          'C:\Users\Max\TIFS\logs\googleplay\\fiveCatAppsDir\social\mapped\\ '


def invalidinput():
    try:
        raise Exception()
    except:
        printerror()
        sys.exit(ERROR_CODE_INPUT_FORMAT)


def uncompressdir(dir, androiddir, uncatdir, undecompdir):
    tarpath = dir + '/*.tar*'
    tarfiles = glob.glob(tarpath)
    for onetar in tarfiles:
        periodindex = string.index(onetar, ".tar")
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
        periodindex = string.index(onezip, ".zip")
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
        if is_encpted:
            passwd = 'infected666' + zipname[len(zipname) - 1]  # This is default password used, need change for other uses
            for item in zip.namelist():
                try:
                    zip.extract(item, nowzippath, passwd)    # Sometimes password is needed
                except RuntimeError as e:
                    if 'password' in e[0]:
                        passwd = 'infected'
                        try:
                            zip.extract(item, nowzippath, passwd)
                        except RuntimeError as e:
                            print 'nowzip',
                            print onezip
                            print 'RuntimeError in second trail e: ',
                            print e[0]
                            os.system("mv " + onezip + " " + undecompdir)
                            os.system("rm -rf " + nowzippath)
                            break
        else:
            for item in zip.namelist():
                zip.extract(item, nowzippath)

        categorizedir(nowzippath, androiddir, uncatdir)


# Below is starting of main

if len(sys.argv) != 3 and len(sys.argv) != 4:
    invalidinput()
else:
    option = sys.argv[1]
    if option == '-u':
        if len(sys.argv) != 3:
            invalidinput()
        else:
            workDir = sys.argv[2]
            removespace(workDir)
            androidDir = workDir + '/' + 'Android'
            if not os.path.exists(androidDir):
                os.makedirs(androidDir)
            uncatDir = workDir + '/' + 'Uncategorized'
            if not os.path.exists(uncatDir):
                os.makedirs(uncatDir)
            undecompDir = workDir + '/' + 'Undecomped'
            if not os.path.exists(undecompDir):
                os.makedirs(undecompDir)
            uncompressdir(workDir, androidDir, uncatDir, undecompDir)
    elif option == '-m':
        if len(sys.argv) != 4:
            invalidinput()
        else:
            inputDir = sys.argv[2]
            outputDir = sys.argv[3]
            print inputDir
            print outputDir
            doneDir = inputDir[: string.rindex(inputDir, 'merged')] + 'done'
            if not os.path.exists(doneDir):
                os.makedirs(doneDir)
            processedFiles = glob.glob(outputDir + '\\' + '*.txt')
            for oneFile in processedFiles:
                print oneFile
                fileName = oneFile[string.rindex(oneFile, '\\') + 1:string.rindex(oneFile, '.txt')]
                procInputFile = inputDir + '\\' + fileName
                doneFile = doneDir + '\\' + fileName
                os.rename(procInputFile, doneFile)
