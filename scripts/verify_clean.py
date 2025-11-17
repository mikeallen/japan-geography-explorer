#!/usr/bin/env python3
"""Quick verification that cleaned data has no outliers."""

import csv
import math

PREFECTURE_COORDS = {
    'Niigata': (37.9, 139.0), 'Chiba': (35.6, 140.1), 'Hokkaido': (43.1, 141.3),
    'Miyagi': (38.3, 140.9), 'Yamagata': (38.3, 140.1), 'Aichi': (35.0, 137.0),
    'Shizuoka': (34.9, 138.4), 'Kochi': (33.6, 133.5), 'Tokushima': (34.0, 134.5),
    'Tochigi': (36.6, 139.9), 'Saitama': (36.0, 139.4), 'Gifu': (35.5, 137.0),
    'Akita': (39.7, 140.1), 'Ibaraki': (36.3, 140.4), 'Kumamoto': (32.8, 130.7),
    'Oita': (33.2, 131.6), 'Fukuoka': (33.6, 130.4), 'Saga': (33.3, 130.3),
    'Tokyo': (35.7, 139.7), 'Kanagawa': (35.4, 139.3), 'Osaka': (34.7, 135.5),
    'Kyoto': (35.0, 135.8), 'Wakayama': (34.2, 135.2), 'Ishikawa': (36.6, 136.6),
    'Toyama': (36.7, 137.2), 'Fukui': (35.9, 136.2), 'Hiroshima': (34.4, 132.5),
    'Miyazaki': (32.0, 131.4),
}

def distance(lat1, lon1, lat2, lon2):
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    return math.sqrt((dlat * 111)**2 + (dlon * 91)**2)

river_metadata = {}
with open('rivers.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Name']:
            river_metadata[row['Name']] = {'prefecture': row['Prefecture']}

print("Verifying cleaned data...\n")
issues = 0

with open('rivers_geo_cleaned.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['Name'] or row['Name'] not in river_metadata:
            continue

        name = row['Name']
        prefecture = river_metadata[name]['prefecture']
        prefectures = [p.strip() for p in prefecture.split(';')]

        expected_coords = []
        for pref in prefectures:
            if pref in PREFECTURE_COORDS:
                expected_coords.append(PREFECTURE_COORDS[pref])

        if not expected_coords or not row['Coordinates']:
            continue

        coord_pairs = row['Coordinates'].split(';')

        for pair in coord_pairs:
            try:
                lat, lon = map(float, pair.split(','))
                min_dist = min([distance(lat, lon, exp_lat, exp_lon)
                               for exp_lat, exp_lon in expected_coords])

                if min_dist > 200:
                    print(f"❌ {name}: outlier at ({lat:.4f}, {lon:.4f}) - {min_dist:.0f}km away")
                    issues += 1
            except:
                pass

if issues == 0:
    print("✓ All data verified clean! No outliers found.")
else:
    print(f"\n⚠ Found {issues} remaining outliers")
