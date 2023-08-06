
import os
import glob
import re
from collections import OrderedDict as odict

import numpy as np
import pandas as pd

def read_bin(filename, count=-1, keep_2D_zpos=False, part=True):
    """Read TRACMASS binary file"""
    dtype = np.dtype([('id',  'i4'), ('jd',  'f8'),
		      ('xpos','f4'), ('ypos','f4'),
		      ('zpos','f4')])
    runtraj = np.fromfile(open(filename), dtype, count=count)
    dt64 = ((runtraj["jd"])*24*60*60-62135683200).astype("datetime64[s]")
    df = pd.DataFrame(data={"id":runtraj["id"],
                            "xpos":runtraj["xpos"]-1,
                            "ypos":runtraj["ypos"]-1,
                            "zpos":runtraj["zpos"]-1},
                      index=pd.Series(dt64))
    if (not keep_2D_zpos) and (len(df["zpos"].unique())==1):
        del df["zpos"]
    df.sort_index(inplace=True)
    if part:
        if type(part) is bool:
            pstr = re.search(r'_r\d\d_', filename)
            if not pstr:
                return df
            else:
                part = int(pstr[0][2:-1])
                print(part)    
        df["id"] = df.id.astype(np.uint32,copy=False)
        df["id"] = part * 10**(int(np.log10(np.uint32(-1)))-1) + df.id
    return df

def read_asc(filename, keep_2D_zpos=False):
    """Read TRACMASS ascii file"""
    df = pd.read_csv(filename, sep=" ", skipinitialspace=True, 
		     names=["id","jd","xpos","ypos","zpos"], usecols=[0,1,2,3,4])
    dt64 = ((df["jd"])*24*60*60-62135683200).astype("datetime64[s]")
    df.set_index(dt64, inplace=True)
    del df["jd"]
    if (not keep_2D_zpos) and (len(df["zpos"].unique())==1):
        del df["zpos"]
