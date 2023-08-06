import os
import tempfile
from urllib.request import urlretrieve

from grass.script.core import parse_command
from grass_session import Session

NAME_GEOTIF = "cea.tif"
URL_GEOTIF_SAMPLE = "https://download.osgeo.org/geotiff/samples/gdal_eg/cea.tif"

# create a temporary directory
TMPDIR = tempfile.mkdtemp()
TMP_TIF = os.path.join(TMPDIR, NAME_GEOTIF)

# dowload a sample geotif file
urlretrieve(URL_GEOTIF_SAMPLE, filename=TMP_TIF)

with Session(gisdb=TMPDIR, location="loc", create_opts=TMP_TIF) as sess:
    print("\nPROJ")
    print(parse_command("g.proj", flags="g"))
    print("\nREGION")
    print(parse_command("g.region", flags="g"))
