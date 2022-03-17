#!/usr/bin/python3
import argparse
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO
from geometry.point import Point
from geometry.polygon import Polygon


urls = {
        "day_1_conv" : "https://www.spc.noaa.gov/products/outlook/day1otlk_cat.kmz",
        "day_2_conv" : "https://www.spc.noaa.gov/products/outlook/day2otlk_cat.kmz",
        "day_3_conv" : "https://www.spc.noaa.gov/products/outlook/day3otlk_cat.kmz",
        
        "day_1_wind" : "https://www.spc.noaa.gov/products/outlook/day1otlk_wind.kmz",
        "day_2_wind" : "https://www.spc.noaa.gov/products/outlook/day2otlk_wind.kmz",
        "day_3_wind" : "https://www.spc.noaa.gov/products/outlook/day3otlk_wind.kmz",
        
        "day_1_torn" : "https://www.spc.noaa.gov/products/outlook/day1otlk_torn.kmz",
        "day_2_torn" : "https://www.spc.noaa.gov/products/outlook/day2otlk_torn.kmz",
        "day_3_torn" : "https://www.spc.noaa.gov/products/outlook/day3otlk_torn.kmz",

        "day_1_hail" : "https://www.spc.noaa.gov/products/outlook/day1otlk_hail.kmz",
        "day_2_hail" : "https://www.spc.noaa.gov/products/outlook/day2otlk_hail.kmz",
        "day_3_hail" : "https://www.spc.noaa.gov/products/outlook/day3otlk_hail.kmz",

        "day_1_fire" : "https://www.spc.noaa.gov/products/fire_wx/day1fireotlk.kmz",
        "day_2_fire" : "https://www.spc.noaa.gov/products/fire_wx/day2fireotlk.kmz",
        }

def fetch_outlook(url: str):
    name = url.split('/')[-1][:-4]

    with urllib.request.urlopen(url) as r:
        data = r.read()

    with zipfile.ZipFile(BytesIO(data)) as f:
        with f.open(f.namelist()[0]) as k:
            raw_kml = k.read()

    tree = ET.parse(BytesIO(raw_kml))

    root = tree.getroot()
    return root

def check_location(lat: float, lon: float, root):
    doc = root.find('./document/folder')
    namespace = "{http://earth.google.com/kml/2.2}"
    for elem in root.iter(f"{namespace}Placemark"):
        if elem.find(f"{namespace}name") is not None:
            name = elem.find(f'{namespace}name').text 
            polygons = [thing for thing in elem.findall(f"{namespace}MultiGeometry/{namespace}Polygon")] 
            if len(polygons) == 0:
                polygons.append(elem.find(f"{namespace}Polygon"))
            for poly in polygons:
                coords = poly.find(f"{namespace}outerBoundaryIs/{namespace}LinearRing/{namespace}coordinates").text
                points = []
                for point in coords.split(' '):
                    xy = point.split(',')
                    points.append(Point(float(xy[0]), float(xy[1])))

                p = Polygon(points)

                if p.contains(Point(lon, lat)):
                    return name
        return "No Risk"
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('latlon', nargs = 2 , type = float, default = [34.7303, -86.5861], help="lat and lon of location to check")
    parser.add_argument('-d', '--day', type=int, default=1, help="outlook for day 1, 2 or 3")
    parser.add_argument('-p', '--product', type=str, default='conv', help="Product to use. conv, fire, wind, hail, torn")
    

    args = parser.parse_args()
    
    day = args.day
    product = args.product

    url = urls[f"day_{day}_{product}"]
    root = fetch_outlook(url)

    outlook = check_location(args.latlon[0], args.latlon[1], root)

    print(outlook)


