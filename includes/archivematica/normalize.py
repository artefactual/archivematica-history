#!/usr/bin/python

import os
import sys

fileType = sys.argv[5]


def video(filePath,dirPath,fileUUID,shortFile):
  try:
    os.system("ffmpeg -i " + filePath + " -vcodec mpeg2video -qscale 1 -qmin 1 -intra -ar 48000 " + dirPath + "/" + shortFile + ".mxf")
  except OSerror, e:
    print "ffmpegerror(): %s" % e.sterror
    sys.exit(-1)

def image(filePath,dirPath,fileUUID,shortFile):
  try:
    os.system("convert " + filePath + " +compress " + dirPath + "/" + shortFile + ".tif")
  except OSerror, e:
    print "image converterror(): %s" % e.sterror
    sys.exit(-1)

def audio(filePath,dirPath,fileUUID,shortFile):
  try:
    os.system("ffmpeg -i " + filePath + " -ar 44100 " + dirPath + "/" + shortFile + ".wav")
  except OSerror, e:
    print "audio converterror(): %s" % e.sterror
    sys.exit(-1)

def xena(filePath,dirPath,fileUUID,shortFile):
  try:
    os.system("java -jar /opt/externals/xena/xena.jar -f " + filePath + " -o " + dirPath + " -p /opt/externals/xena/plugins/")
  except OSerror, e:
    print "xena converterror(): %s" % e.sterror
    sys.exit(-1)


if fileType == "video":
  video(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

elif fileType == "image":
  image(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

elif fileType == "audio":
  audio(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

else:
  xena(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
