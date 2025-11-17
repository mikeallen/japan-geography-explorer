#!/usr/bin/env python3
"""
Clean river coordinate data by removing outlier points that are far
from the expected prefecture location.
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

# Read and clean river geometry
print("\nCleaning river coordinates...\n")
cleaned_rivers = []
stats = {'total': 0, 'cleaned': 0, 'removed_points': 0}

with open('rivers_geo_new.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['Name']:
            continue

        stats['total'] += 1
        name = row['Name']

        if name not in river_metadata:
            cleaned_rivers.append({'Name': name, 'Coordinates': row['Coordinates']})
            continue

        prefecture = river_metadata[name]['prefecture']
        prefectures = [p.strip() for p in prefecture.split(';')]

        # Get expected coordinates
        expected_coords = []
        for pref in prefectures:
            if pref in PREFECTURE_COORDS:
                expected_coords.append(PREFECTURE_COORDS[pref])

        if not expected_coords:
            cleaned_rivers.append({'Name': name, 'Coordinates': row['Coordinates']})
            continue

        # Parse coordinates
        coords_str = row['Coordinates']
        if not coords_str:
            cleaned_rivers.append({'Name': name, 'Coordinates': ''})
            continue

        coord_pairs = coords_str.split(';')
        cleaned_coords = []
        removed = []

        # Filter out outliers
        for pair in coord_pairs:
            try:
                lat, lon = map(float, pair.split(','))

                # Find minimum distance to any expected prefecture
                min_dist = float('inf')
                for exp_lat, exp_lon in expected_coords:
                    dist = distance(lat, lon, exp_lat, exp_lon)
                    min_dist = min(min_dist, dist)

                # Keep only if within 200km of expected prefecture
                # (rivers can be long, so give generous buffer)
                if min_dist <= 200:
                    cleaned_coords.append(pair)
                else:
                    removed.append((lat, lon, min_dist))
                    stats['removed_points'] += 1
            except:
                pass

        if removed:
            stats['cleaned'] += 1
            print(f"✓ {name} ({prefecture}): removed {len(removed)} outlier points, kept {len(cleaned_coords)}")

        # Only add river if we have at least some coordinates left
        if cleaned_coords:
            cleaned_rivers.append({
                'Name': name,
                'Coordinates': ';'.join(cleaned_coords)
            })
        else:
            print(f"⚠ {name}: all points were outliers, skipping river")

# Write cleaned data
output_file = 'rivers_geo_cleaned.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Coordinates'])
    for river in cleaned_rivers:
        writer.writerow([river['Name'], river['Coordinates']])

print(f"\n{'='*60}")
print(f"Cleaning complete!")
print(f"  Total rivers: {stats['total']}")
print(f"  Rivers cleaned: {stats['cleaned']}")
print(f"  Total outlier points removed: {stats['removed_points']}")
print(f"  Output: {output_file}")
print(f"{'='*60}")
