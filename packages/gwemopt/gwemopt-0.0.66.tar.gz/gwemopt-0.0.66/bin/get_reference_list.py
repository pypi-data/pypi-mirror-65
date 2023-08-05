import os
from astropy import time
import astropy.units as u
from astropy.table import Table
from celery.task import PeriodicTask
from celery.utils.log import get_task_logger
from celery.local import PromiseProxy
import numpy as np
import pyvo.dal
import requests

client = pyvo.dal.TAPService('https://irsa.ipac.caltech.edu/TAP',)

import matplotlib
#matplotlib.rc('text', usetex=True)
matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 16})
matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
import matplotlib.pyplot as plt
from matplotlib import cm

def ztf_references():
    refstable = client.search("""
    SELECT field, fid, maglimit FROM ztf.ztf_current_meta_ref
    WHERE (nframes >= 15) AND (startobsdate >= '2018-02-05T00:00:00Z')
    AND (field < 2000)
    """).to_table()

    refs = refstable.group_by(['field', 'fid']).groups.aggregate(np.mean)
    refs = refs.filled()

    refs_grouped_by_field = refs.group_by('field').groups
    g, r, i = [], [], []
    for field_id, rows in zip(refs_grouped_by_field.keys,
                              refs_grouped_by_field):
        idx = np.where(rows['fid'] == 1)[0]
        if len(idx) > 0:
            g.append(np.array(rows['maglimit'][idx])[0])
        idx = np.where(rows['fid'] == 2)[0]
        if len(idx) > 0:
            r.append(np.array(rows['maglimit'][idx])[0])
        
    plt.figure()
    plt.hist(g, 20, facecolor='green', alpha=0.5, label='g')
    plt.hist(r, 20, facecolor='red', alpha=0.5, label='r')
    plt.savefig('limmag.pdf')
    plt.close()

ztf_references()
 
