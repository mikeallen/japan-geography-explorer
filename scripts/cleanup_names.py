#!/usr/bin/env python3
"""
Clean up mountain and lake names - remove prefixes and duplicates.
"""

import csv

# Clean mountains
print("Cleaning mountains...")

# Mountains to remove (duplicates)
REMOVE_MOUNTAINS = ['Hakusan', 'Okuhotaka']

# Read mountains metadata
mountains_meta = []
with open('mountains.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name']

        # Skip duplicates
        if name in REMOVE_MOUNTAINS:
            print(f"  Removing duplicate: {name}")
            continue

        # Remove "Mount " prefix
        if name.startswith('Mount '):
            new_name = name.replace('Mount ', '')
            print(f"  Renaming: {name} → {new_name}")
            row['Name'] = new_name

        mountains_meta.append(row)

# Write cleaned mountains metadata
with open('mountains.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Prefecture', 'Elevation', 'Mountain Range']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(mountains_meta)

print(f"✓ Cleaned mountains.csv: {len(mountains_meta)} mountains")

# Read mountains geo
mountains_geo = []
with open('mountains_geo.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name']

        # Skip duplicates
        if name in REMOVE_MOUNTAINS:
            continue

        # Remove "Mount " prefix
        if name.startswith('Mount '):
            row['Name'] = name.replace('Mount ', '')

        mountains_geo.append(row)

# Write cleaned mountains geo
with open('mountains_geo.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Latitude', 'Longitude', 'Elevation']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(mountains_geo)

print(f"✓ Cleaned mountains_geo.csv: {len(mountains_geo)} mountains")

# Clean lakes
print("\nCleaning lakes...")

# Read lakes metadata
lakes_meta = []
with open('lakes.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name']

        # Remove "Lake " prefix
        if name.startswith('Lake '):
            new_name = name.replace('Lake ', '')
            print(f"  Renaming: {name} → {new_name}")
            row['Name'] = new_name

        lakes_meta.append(row)

# Write cleaned lakes metadata
with open('lakes.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Prefecture', 'Area', 'Depth']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(lakes_meta)

print(f"✓ Cleaned lakes.csv: {len(lakes_meta)} lakes")

# Read lakes geo
lakes_geo = []
with open('lakes_geo.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name']

        # Remove "Lake " prefix
        if name.startswith('Lake '):
            row['Name'] = name.replace('Lake ', '')

        lakes_geo.append(row)

# Write cleaned lakes geo
with open('lakes_geo.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Coordinates']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(lakes_geo)

print(f"✓ Cleaned lakes_geo.csv: {len(lakes_geo)} lakes")

print("\n" + "="*60)
print("Cleanup complete!")
print(f"  Mountains: {len(mountains_meta)} (removed {len(REMOVE_MOUNTAINS)} duplicates)")
print(f"  Lakes: {len(lakes_meta)}")
print("="*60)
