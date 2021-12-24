# AUTOGENERATED! DO NOT EDIT! File to edit: 00_geoloader.ipynb (unless otherwise specified).

__all__ = ['detect_shapefile_encoding', 'read_file_shp']

# Cell
import chardet
import pandas as pd
from pathlib import Path
import shapefile
from shapely.geometry import Polygon, MultiPolygon
from shapely.geometry import shape
from os import listdir
from os.path import join

# Cell
def detect_shapefile_encoding(path) -> str:
    """Read the encoding of a dbf file associated to a shapefile."""
    path = Path(path)
    file = path.with_suffix(".dbf")

    with open(file, 'rb') as rawdata:
        character_encoding = chardet.detect(rawdata.read())['encoding']

    if character_encoding:
        return character_encoding

    return "utf-8"

# Cell
def read_file_shp(path):
    charenc = detect_shapefile_encoding(path)
    try:
        sf = shapefile.Reader(path, encoding= charenc)

    except:
        try:
            sf = shapefile.Reader(path, encoding= "utf-8")
        except:
            print("Ce fichier est illisible")
            print(path)


    col = [x[0] for x in sf.fields[1:]]

    df = pd.DataFrame(data = sf.records(), columns = col)

    shapes = [sf.shapes()[i] for i in range(len(sf.shapes()))]
    shapes = [shape(x) for x in shapes] #convert shapefile.shape to shapely.shape in order to make the conversion to multipolygons easier
    shapes = [MultiPolygon([x]) if x.geom_type != 'MultiPolygon' and x.area > 0 else None for x in shapes]

    df['geometry'] = shapes

    df = df[df['geometry']!=None]
    return df