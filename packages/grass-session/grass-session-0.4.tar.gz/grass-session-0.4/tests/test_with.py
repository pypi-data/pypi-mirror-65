#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 01:02:54 2018

@author: pietro


import os
import sys
import subprocess

location = "G" if 'location' not in locals() else location
mapset = "PERMANENT" if 'mapset' not in locals() else mapset

startcmd = ['grass72', '--config', 'path']
p = subprocess.Popen(startcmd, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
gisbase = out.decode('utf-8').strip()
os.environ['GISBASE'] = gisbase
sys.path.append(os.path.join(gisbase, "etc", "python"))
gisdb = os.path.join(".")
os.environ['GISDBASE'] = gisdb
import grass.script as gs
import grass.script.setup as gsetup
rcfile = gsetup.init(gisbase, gisdb, location, mapset)


from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import vector as v
from grass.pygrass.modules.shortcuts import display as d
from grass.script import array as garray

g.mapsets(flags="l")
g.list(type="raster", flags="m")
"""
import os

# import grass python libraries
from grass.pygrass.modules.shortcuts import general as g

# import grass_session
from grass_session import Session

# set some common environmental variables, like:
os.environ.update(dict(GRASS_COMPRESS_NULLS="1", GRASS_COMPRESSOR="ZSTD"))

# create a PERMANENT mapset
# create a Session instance
with Session(gisdb="/tmp", location="mytest", create_opts="EPSG:4326") as PERMANENT:
    # execute some command inside PERMANENT
    g.mapsets(flags="l")
    g.list(type="raster", flags="m")

# create a new mapset in the same location
with Session(gisdb="/tmp", location="mytest", mapset="user", create_opts="") as user:
    # execute some command inside user
    g.mapsets(flags="l")
    g.list(type="raster", flags="m")
