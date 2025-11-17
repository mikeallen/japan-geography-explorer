#!/usr/bin/env python3
"""
Merge new mountains with existing ones.
"""

import csv

# Read existing mountains
print("Reading existing mountains...")
existing = {}
with open('mountains.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Name']:
            existing[row['Name']] = {
                'japanese': row['Japanese Name'],
                'prefecture': row['Prefecture'],
                'elevation': row['Elevation'],
                'range': row['Mountain Range']
            }

# Read existing geo data
existing_geo = {}
with open('mountains_geo.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Name']:
            existing_geo[row['Name']] = {
                'lat': row['Latitude'],
                'lon': row['Longitude'],
                'elevation': row['Elevation']
            }

# Read new mountains
print("Reading new mountains...")
new_mountains = {}
with open('mountains_new.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Name']:
            new_mountains[row['Name']] = {
                'japanese': row['Japanese Name'],
                'prefecture': row['Prefecture'],
                'elevation': row['Elevation'],
                'lat': row['Latitude'],
                'lon': row['Longitude']
            }

# Merge: existing takes priority, add new ones
merged_metadata = {}
merged_geo = {}

# Add all existing
for name, data in existing.items():
    merged_metadata[name] = data

for name, data in existing_geo.items():
    merged_geo[name] = data

# Add new mountains (skip if already exists)
added_count = 0
for name, data in new_mountains.items():
    # Normalize name for comparison
    base_name = name.replace('Mount ', '')

    # Check if this mountain already exists
    exists = False
    for existing_name in existing.keys():
        if base_name in existing_name or existing_name in base_name:
            exists = True
            break

    if not exists:
        # Add to both metadata and geo
        merged_metadata[name] = {
            'japanese': data['japanese'],
            'prefecture': data['prefecture'],
            'elevation': data['elevation'],
            'range': 'Standalone'  # Default, can be updated
        }
        merged_geo[name] = {
            'lat': data['lat'],
            'lon': data['lon'],
            'elevation': data['elevation']
        }
        added_count += 1
        print(f"  + {name}")

print(f"\nAdded {added_count} new mountains")

# Write merged metadata
with open('mountains.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Prefecture', 'Elevation', 'Mountain Range']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for name, data in sorted(merged_metadata.items()):
        writer.writerow({
            'Name': name,
            'Japanese Name': data['japanese'],
            'Prefecture': data['prefecture'],
            'Elevation': data['elevation'],
            'Mountain Range': data['range']
        })

# Write merged geo data
with open('mountains_geo.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Latitude', 'Longitude', 'Elevation']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for name, data in sorted(merged_geo.items()):
        writer.writerow({
            'Name': name,
            'Latitude': data['lat'],
            'Longitude': data['lon'],
            'Elevation': data['elevation']
        })

print(f"\n✓ Updated mountains.csv ({len(merged_metadata)} mountains)")
print(f"✓ Updated mountains_geo.csv ({len(merged_geo)} mountains)")
