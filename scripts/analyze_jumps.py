#!/usr/bin/env python3
"""
Analyze consecutive point distances to find errant jumps.
"""

import csv
import math

def distance(lat1, lon1, lat2, lon2):
    """Calculate approximate distance in km between two lat/lon points."""
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    return math.sqrt((dlat * 111)**2 + (dlon * 91)**2)

# Read river metadata
river_metadata = {}
with open('rivers.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Name']:
            river_metadata[row['Name']] = {
                'length_km': float(row['Length']) if row['Length'] else 0
            }

print("Analyzing consecutive point jumps...\n")

with open('rivers_geo_cleaned.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['Name'] or not row['Coordinates']:
            continue

        name = row['Name']
        coords_str = row['Coordinates']
        coord_pairs = coords_str.split(';')

        if len(coord_pairs) < 2:
            continue

        # Parse all coordinates
        coords = []
        for pair in coord_pairs:
            try:
                lat, lon = map(float, pair.split(','))
                coords.append((lat, lon))
            except:
                pass

        if len(coords) < 2:
            continue

        # Find maximum jump between consecutive points
        max_jump = 0
        max_jump_idx = -1
        total_dist = 0

        for i in range(len(coords) - 1):
            lat1, lon1 = coords[i]
            lat2, lon2 = coords[i + 1]
            dist = distance(lat1, lon1, lat2, lon2)
            total_dist += dist

            if dist > max_jump:
                max_jump = dist
                max_jump_idx = i

        avg_jump = total_dist / (len(coords) - 1)

        # Report rivers with suspiciously large jumps
        # A jump more than 100km or 10x average is likely bad
        if max_jump > 100 or (avg_jump > 0 and max_jump > 10 * avg_jump):
            print(f"⚠ {name}:")
            print(f"   Total points: {len(coords)}")
            print(f"   Average jump: {avg_jump:.1f} km")
            print(f"   Max jump: {max_jump:.1f} km (between points {max_jump_idx} and {max_jump_idx+1})")
            print(f"   Point {max_jump_idx}: {coords[max_jump_idx]}")
            print(f"   Point {max_jump_idx+1}: {coords[max_jump_idx+1]}")

            if name in river_metadata:
                river_length = river_metadata[name]['length_km']
                if river_length > 0:
                    print(f"   River length: {river_length} km (max jump is {max_jump/river_length*100:.0f}% of total)")
            print()
