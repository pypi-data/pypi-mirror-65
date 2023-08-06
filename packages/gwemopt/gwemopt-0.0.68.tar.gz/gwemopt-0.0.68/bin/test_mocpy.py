
import numpy as np

import matplotlib
#matplotlib.rc('text', usetex=True)
matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 16})
matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
from matplotlib import path, patches
import matplotlib.pyplot as plt

from astropy.coordinates import SkyCoord, Angle
import astropy.units as u

from mocpy import MOC, WCS

import gwemopt.utils

filename = "../input/ZTF.tess"
fields = np.recfromtxt(filename, usecols=range(3), names=['field_id', 'ra', 'dec'])

nside = 512
nside_new = 64

moc_order = int(np.log(nside)/ np.log(2))
print(moc_order)
mocs = []
FOV = 6.86
for field_id, ra, dec in fields:
    print(field_id, ra, dec)
    ipix, radecs, patch, area = gwemopt.utils.getSquarePixels(
        ra, dec, FOV, nside)
    if len(radecs) == 4:
        idx = [0, 1, 3, 2]
        radecs = radecs[idx,:]
    idx1 = np.where(radecs[:,0]>=180.0)[0]
    idx2 = np.where(radecs[:,0]<180.0)[0]
    idx3 = np.where(radecs[:,0]>300.0)[0]
    idx4 = np.where(radecs[:,0]<60.0)[0]
    if (len(idx1)>0 and len(idx2)>0) and not (len(idx3)>0 and len(idx4)>0):
        continue
    try:
        moc = MOC.from_healpix_cells(ipix, np.log2(nside)*np.ones(ipix.shape))
        #moc = MOC.from_polygon(radecs[:,0]*u.degree, radecs[:,1]*u.degree,
        #                       max_depth=moc_order)
    except:
        continue
    moc = moc.degrade_to_order(int(np.log2(nside_new)))

    mocs.append(moc)

fig = plt.figure(figsize=(15, 10))
with WCS(fig,
          fov=330 * u.deg,
          center=SkyCoord(0, 0, unit='deg', frame='galactic'),
          coordsys='galactic',
          rotation=Angle(0, u.degree),
          projection="AIT") as wcs:
    ax = fig.add_subplot(1, 1, 1, projection=wcs)
    for moc in mocs:
        moc.fill(ax=ax, wcs=wcs, edgecolor='r', facecolor='r', linewidth=1.0, fill=True, alpha=0.5)
        moc.border(ax=ax, wcs=wcs, color="black", alpha=0.5)

plt.xlabel('ra')
plt.ylabel('dec')
plt.grid(color="black", linestyle="dotted")
plt.show()
plt.savefig('../output/moc/moc.pdf')
plt.close()
