#!/usr/bin/python
import os
import sys

fitsinput = sys.argv[1]
fitsoutput = sys.argv[2]

os.system("cd  /usr/local/OAIS/fits; ./fits.sh -i " + fitsinput + " -o " + fitsoutput)
