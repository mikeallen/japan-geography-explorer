#!/usr/bin/env python3
"""
Merge original 6 rivers with newly simplified rivers.
Keep the original 6, add the 30 new ones.
"""

import csv

# Read original 6 rivers
print("Reading original rivers...")
original_rivers = {}
with open('rivers_geo_old.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        original_rivers[row['Name']] = row['Coordinates']

print(f"Original rivers: {', '.join(original_rivers.keys())}")

# Read simplified rivers
print("\nReading simplified rivers...")
simplified_rivers = {}
with open('rivers_geo_simplified.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        simplified_rivers[row['Name']] = row['Coordinates']

# Merge: use original for the 6, use simplified for the rest
merged = {}

# First, add all original rivers
for name, coords in original_rivers.items():
    merged[name] = coords
    print(f"  Using original: {name}")

# Then, add new rivers from simplified (skip if already in original)
new_count = 0
for name, coords in simplified_rivers.items():
    if name not in merged:
        merged[name] = coords
        new_count += 1

print(f"\n✓ Merged {len(original_rivers)} original + {new_count} new = {len(merged)} total rivers")

# Write merged data
with open('rivers_geo.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Coordinates'])
    for name, coords in sorted(merged.items()):
        writer.writerow([name, coords])

print(f"✓ Wrote rivers_geo.csv")
