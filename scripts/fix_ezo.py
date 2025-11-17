#!/usr/bin/env python3
"""
Fix Ezo entry in old_provinces_geo.csv by copying Hokkaido coordinates.
"""

import csv

# Read Hokkaido coordinates from prefectures_geo.csv
hokkaido_coords = None
with open('prefectures_geo.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Name'] == 'Hokkaido':
            hokkaido_coords = row['Coordinates']
            break

print(f"Hokkaido coordinates: {len(hokkaido_coords)} characters")

# Read old provinces
provinces = []
with open('old_provinces_geo.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Name'] == 'Ezo':
            # Replace with full Hokkaido coordinates
            row['Coordinates'] = hokkaido_coords
            print(f"Updated Ezo with Hokkaido coordinates")
        provinces.append(row)

# Write back
with open('old_provinces_geo.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Modern Prefecture', 'Coordinates']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(provinces)

print(f"✓ Fixed Ezo in old_provinces_geo.csv")
print(f"✓ Total provinces: {len(provinces)}")
