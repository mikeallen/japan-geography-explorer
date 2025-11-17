#!/usr/bin/env python3
"""Verify final cleaned data has no large jumps."""

import csv
import math

def distance(lat1, lon1, lat2, lon2):
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    return math.sqrt((dlat * 111)**2 + (dlon * 91)**2)

print("Verifying final cleaned data...\n")
issues = 0

with open('rivers_geo_final.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['Name'] or not row['Coordinates']:
            continue

        name = row['Name']
        coord_pairs = row['Coordinates'].split(';')

        coords = []
        for pair in coord_pairs:
            try:
                lat, lon = map(float, pair.split(','))
                coords.append((lat, lon))
            except:
                pass

        if len(coords) < 2:
            continue

        # Check for large jumps
        max_jump = 0
        for i in range(len(coords) - 1):
            lat1, lon1 = coords[i]
            lat2, lon2 = coords[i + 1]
            dist = distance(lat1, lon1, lat2, lon2)
            if dist > max_jump:
                max_jump = dist

        # Report if any jump exceeds 50km
        if max_jump > 50:
            print(f"⚠ {name}: max jump = {max_jump:.1f} km")
            issues += 1

if issues == 0:
    print("✓ All rivers verified! No jumps exceed 50km.")
    print("\nSample of cleaned rivers:")

    # Show sample stats
    with open('rivers_geo_final.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if count >= 10 or not row['Name'] or not row['Coordinates']:
                if row['Name']:
                    count += 1
                continue

            name = row['Name']
            coord_pairs = row['Coordinates'].split(';')
            print(f"  {name}: {len(coord_pairs)} points")
            count += 1
else:
    print(f"\n⚠ Found {issues} rivers with large jumps")
