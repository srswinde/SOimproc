from astropy.io import fits
import ccdproc
import os
import matplotlib.pyplot as plt
import numpy as np
import ds9
import sys
def fixfits( imname ):

	fitsfd = fits.open( imname )
	fitsfd[0].header['EPOCH'] = 2000.0
	fitsfd[0].header['EQUINOX'] = 2000.0
	fitsfd[1].header['CTYPE1'] = 'RA---TAN'
	fitsfd[1].header['CTYPE2'] = 'DEC--TAN'
	fitsfd[2].header['CTYPE1'] = 'RA---TAN'
	fitsfd[2].header['CTYPE2'] = 'DEC--TAN'
	return fitsfd


def m4kproc( fitsfd ):
	dummy_name = "dummy.fits"
	if os.path.exists(dummy_name): os.remove(dummy_name)
	fitsfd.writeto(dummy_name)
	amp1 = ccdproc.fits_ccddata_reader( dummy_name, hdu=1 )
	amp2 = ccdproc.fits_ccddata_reader( dummy_name, hdu=2 )
	procdata1 = ccdproc.ccd_process( amp1, oscan=fitsfd[1].header['biassec'], trim=fitsfd[1].header['TRIMSEC'] )
	procdata2 = ccdproc.ccd_process( amp2, oscan=fitsfd[2].header['biassec'], trim=fitsfd[2].header['TRIMSEC'] )
	os.remove(dummy_name)
	return procdata1, procdata2

def m4kmerge( amp1, amp2 ):
	#amp1 = fitsfd[1].data
	#amp2 = fitsfd[2].data
	
	merged = np.concatenate( (amp1, np.fliplr( amp2 ) ), axis=1 )
	
	return merged

def addwcs( fitsfd ):
	fitsfd[0].header['ctype1'] = 'RA---TNX'
	fitsfd[0].header['ctype2'] = 'DEC--TNX'
	fitsfd[0].header['crval1'] = 86.0999166666666
	fitsfd[0].header['crval2'] = 4.979694444444444
	fitsfd[0].header['crpix1'] = 682
	fitsfd[0].header['crpix2'] = 682
	fitsfd[0].header['CD1_1']  = 0.000833333353511989
	fitsfd[0].header['CD1_2']  = 0.0
	fitsfd[0].header['CD2_1']  = 0.0
	fitsfd[0].header['CD2_2']   = 0.000833333353511989

"""
CCDNAME = 'ccd1    '           / CCD name                                       
DETSIZE = '[1:4096,1:4096]'    / Detector size                                  
CCDSIZE = '[1:4096,1:4096]'    / CCD size                                       
BIASSEC = '[683:702,1:1365]'   / Bias section                                   
DATASEC = '[1:682,1:1365]'     / Data section                                   
TRIMSEC = '[1:682,1:1365]'     / Trim section                                   
AMPSEC  = '[1:2048,1:4096]'    / Amplifier section                              
DETSEC  = '[1:2048,1:4096]'    / Detector section                               
CCDSEC  = '[1:2048,1:4096]'    / CCD section                                    CCDSEC1 = '[1:682,1:1365]'     / CCD section with binning                       OVRSCAN1=                   20 / Overscan on axis 1                             OVRSCAN2=                    0 / Overscan on axis 2 
"""

def main(imname, outdir="merged", outname=None):
	
	if imname.endswith(".fits"):
		bname = imname[:-5]
	else:
		bname = imname

	if outdir.endswith("/"):
		outdir = outdir[:-1]
	
	if not os.path.exists( outdir ):
		os.mkdir( outdir )

	elif outdir == "":
		outdir = '.'
	
	if not outname:
		outpath = "{0}/{1}_merged.fits".format(outdir, bname)
	else:
		outpath = "{0}/{1}".format(outdir, outname)

	

	fitsfd =  fixfits( imname )
	
	
	
	procdata1, procdata2 =  m4kproc(fitsfd)
	unity = m4kmerge( procdata1, procdata2 )


	hdu = fits.PrimaryHDU(unity)
	hdu.header=fitsfd[0].header
	hdulist = fits.HDUList([hdu])
	
	#WCS stuff
	hdulist[0].header['ctype1'] =fitsfd[1].header['ctype1']
	hdulist[0].header['ctype2'] = fitsfd[1].header['ctype2']
	hdulist[0].header['crval1'] = fitsfd[1].header['crval1']
	hdulist[0].header['crval2'] = fitsfd[1].header['crval2']
	hdulist[0].header['crpix1'] = unity.shape[0]/2
	hdulist[0].header['crpix2'] = unity.shape[1]/2
	hdulist[0].header['CD1_1']  = fitsfd[1].header['CD1_1']
	hdulist[0].header['CD1_2']  = fitsfd[1].header['CD1_2'] 
	hdulist[0].header['CD2_1']  = fitsfd[1].header['CD2_1']
	hdulist[0].header['CD2_2']  = fitsfd[1].header['CD2_2']
	



	if os.path.exists( outpath ):
		os.remove(outpath)
		
	hdulist.writeto(outpath)

	#d=ds9.ds9()
	#d.set("file {0}".format(outpath))


for name in sys.argv[1:]:
	print name
	main(name)




