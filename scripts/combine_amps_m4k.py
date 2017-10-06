#!/usr/bin/env python

from astropy.io import fits
import ccdproc
import os
import sys
from m4kproc import *

def main(imname, outdir=".", outname=None):
	
	if imname.endswith(".fits"):
		bname = imname[:-5]
	else:
		bname = imname

	
	outpath = "{}_merged.fits".format(bname)


	fitsfd = fits.open(imname)

	merged_fits = mergem4k( fitsfd )
	
	fitsfd.close()


	if os.path.exists( outpath ):
		os.remove(outpath)
		
	merged_fits.writeto(outpath)
	merged_fits.close()
	#d=ds9.ds9()
	#d.set("file {0}".format(outpath))

if __name__ == "__main__":
	for name in sys.argv[1:]:

		main(name)




