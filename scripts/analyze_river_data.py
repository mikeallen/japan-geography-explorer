#!/usr/bin/env python3
"""
Analyze river coordinate data for outliers.
Check if any coordinates are far from the expected prefecture location.
"""

import csv
import math

# Expected prefecture coordinates (approximate centers)
PREFECTURE_COORDS = {
    'Niigata': (37.9, 139.0),
    'Chiba': (35.6, 140.1),
    'Hokkaido': (43.1, 141.3),
    'Miyagi': (38.3, 140.9),
    'Yamagata': (38.3, 140.1),
    'Aichi': (35.0, 137.0),
    'Shizuoka': (34.9, 138.4),
    'Kochi': (33.6, 133.5),
    'Tokushima': (34.0, 134.5),
    'Tochigi': (36.6, 139.9),
    'Saitama': (36.0, 139.4),
    'Gifu': (35.5, 137.0),
    'Akita': (39.7, 140.1),
    'Ibaraki': (36.3, 140.4),
    'Kumamoto': (32.8, 130.7),
    'Oita': (33.2, 131.6),
    'Fukuoka': (33.6, 130.4),
    'Saga': (33.3, 130.3),
    'Tokyo': (35.7, 139.7),
    'Kanagawa': (35.4, 139.3),
    'Osaka': (34.7, 135.5),
    'Kyoto': (35.0, 135.8),
    'Wakayama': (34.2, 135.2),
    'Ishikawa': (36.6, 136.6),
    'Toyama': (36.7, 137.2),
    'Fukui': (35.9, 136.2),
    'Hiroshima': (34.4, 132.5),
    'Miyazaki': (32.0, 131.4),
}

def distance(lat1, lon1, lat2, lon2):
    """Calculate approximate distance in km between two lat/lon points."""
    # Simple euclidean distance for rough estimation
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Rough conversion: 1 degree lat ≈ 111km, 1 degree lon ≈ 91km at lat 36
    return math.sqrt((dlat * 111)**2 + (dlon * 91)**2)

# Read river metadata
print("Reading river metadata...")
river_metadata = {}
with open('rivers.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Name']:
            river_metadata[row['Name']] = {
                'prefecture': row['Prefecture'],
                'japanese': row['Japanese Name']
            }

# Read river geometry
print("\nAnalyzing river coordinates for outliers...\n")
issues_found = []

with open('rivers_geo_new.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['Name']:
            continue

        name = row['Name']
        if name not in river_metadata:
            continue

        prefecture = river_metadata[name]['prefecture']

        # Handle multiple prefectures (separated by semicolon)
        prefectures = [p.strip() for p in prefecture.split(';')]

        # Get expected coordinates
        expected_coords = []
        for pref in prefectures:
            if pref in PREFECTURE_COORDS:
                expected_coords.append(PREFECTURE_COORDS[pref])

        if not expected_coords:
            continue

        # Parse coordinates
        coords_str = row['Coordinates']
        if not coords_str:
            continue

        coord_pairs = coords_str.split(';')

        # Check each coordinate
        outliers = []
        for i, pair in enumerate(coord_pairs):
            try:
                lat, lon = map(float, pair.split(','))

                # Find minimum distance to any expected prefecture
                min_dist = float('inf')
                for exp_lat, exp_lon in expected_coords:
                    dist = distance(lat, lon, exp_lat, exp_lon)
                    min_dist = min(min_dist, dist)

                # Flag if more than 200km from expected prefecture
                if min_dist > 200:
                    outliers.append({
                        'index': i,
                        'lat': lat,
                        'lon': lon,
                        'distance': min_dist
                    })
            except:
                pass

        if outliers:
            issues_found.append({
                'river': name,
                'prefecture': prefecture,
                'total_points': len(coord_pairs),
                'outliers': outliers
            })

            print(f"❌ {name} ({prefecture}):")
            for outlier in outliers:
                print(f"   Point {outlier['index']}: ({outlier['lat']:.4f}, {outlier['lon']:.4f}) "
                      f"- {outlier['distance']:.0f}km from expected location")
            print()

if not issues_found:
    print("✓ No outliers found!")
else:
    print(f"\nFound {len(issues_found)} rivers with outlier data points")
