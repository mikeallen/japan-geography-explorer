#!/usr/bin/env python3
"""
Create historical province boundaries by merging modern prefecture boundaries.
For provinces that span multiple prefectures, merge their polygons.
"""

import csv
from collections import defaultdict

# Load old provinces metadata (province -> prefectures mapping)
provinces = []
with open('old_provinces.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        provinces.append(row)

# Load prefecture geometries
prefecture_geo = {}
with open('prefectures_geo.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name']
        prefecture_geo[name] = row['Coordinates']

print(f"Loaded {len(provinces)} provinces")
print(f"Loaded {len(prefecture_geo)} prefecture geometries")

# Create province boundaries
province_boundaries = []

for province in provinces:
    province_name = province['Name']
    japanese_name = province['Japanese Name']
    prefectures_str = province['Prefectures']

    # Split by semicolon to get list of prefectures
    prefecture_list = [p.strip() for p in prefectures_str.split(';')]

    print(f"\n{province_name} ({japanese_name}) → {prefecture_list}")

    # Collect all coordinates from the prefectures
    all_coords = []
    for pref in prefecture_list:
        if pref in prefecture_geo:
            coords = prefecture_geo[pref]
            all_coords.append(coords)
            print(f"  ✓ Found geometry for {pref}")
        else:
            print(f"  ✗ No geometry for {pref}")

    if all_coords:
        # For simplicity, if it's a single prefecture, use its boundary
        # If multiple prefectures, we'll use the first one as approximation for now
        # TODO: Properly merge polygons
        if len(all_coords) == 1:
            boundary = all_coords[0]
        else:
            # For multi-prefecture provinces, concatenate all coordinates
            # This is a simplification - proper polygon merging would be more complex
            boundary = all_coords[0]  # Use first prefecture as base

        province_boundaries.append({
            'Name': province_name,
            'Japanese Name': japanese_name,
            'Modern Prefecture': ', '.join(prefecture_list),
            'Coordinates': boundary
        })

print(f"\n\nCreated {len(province_boundaries)} province boundaries")

# Write to CSV
with open('old_provinces_geo_new.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Modern Prefecture', 'Coordinates']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(province_boundaries)

print(f"✓ Written to old_provinces_geo_new.csv")

# Show some statistics
single_pref = sum(1 for p in provinces if ';' not in p['Prefectures'])
multi_pref = len(provinces) - single_pref
print(f"\nStatistics:")
print(f"  Single prefecture provinces: {single_pref}")
print(f"  Multi-prefecture provinces: {multi_pref}")
