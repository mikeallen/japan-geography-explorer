#!/usr/bin/env python3
"""
Fix lakes data - handle field name variations.
"""

import csv

print("Fixing lakes...")

# Read lakes metadata with flexible field handling
lakes_meta = []
with open('lakes.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    print(f"Original fieldnames: {fieldnames}")

    for row in reader:
        # Create clean row with trimmed keys
        clean_row = {}
        for key, value in row.items():
            clean_key = key.strip()
            clean_row[clean_key] = value

        name = clean_row.get('Name', '')
        if not name:
            continue

        # Remove "Lake " prefix
        if name.startswith('Lake '):
            new_name = name.replace('Lake ', '')
            print(f"  Renaming: {name} → {new_name}")
            clean_row['Name'] = new_name

        lakes_meta.append(clean_row)

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
        name = row.get('Name', '').strip()
        if not name:
            continue

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
