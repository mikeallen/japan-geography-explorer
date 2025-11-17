#!/usr/bin/env python3
"""
Create geographic boundaries for mountain ranges by using the prefecture areas they span.
"""

import csv

print("Loading data...")

# Mountain ranges to create boundaries for
mountain_ranges = []
with open('mountains.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Mountain Range'] == 'Range':
            mountain_ranges.append(row)

print(f"Found {len(mountain_ranges)} mountain ranges")

# Load prefecture geometries
prefecture_geo = {}
with open('prefectures_geo.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        full_name = row['Name']
        prefecture_geo[full_name] = row['Coordinates']

        # Also store without suffix
        base_name = full_name.replace(' Ken', '').replace(' Fu', '').replace(' To', '').replace(' Do', '')
        if base_name != full_name:
            prefecture_geo[base_name] = row['Coordinates']

print(f"Loaded {len(prefecture_geo)} prefecture name variations")

# Create range boundaries
range_boundaries = []

for range_data in mountain_ranges:
    range_name = range_data['Name']
    japanese_name = range_data['Japanese Name']
    prefectures_str = range_data['Prefecture']

    # Split by semicolon to get list of prefectures
    prefecture_list = [p.strip() for p in prefectures_str.split(';')]

    print(f"\n{range_name} ({japanese_name})")
    print(f"  Prefectures: {', '.join(prefecture_list)}")

    # Collect coordinates from all prefectures
    all_coord_strings = []
    found_count = 0

    for pref in prefecture_list:
        # Try various name formats
        found = False
        for suffix in ['', ' Ken', ' Fu', ' To', ' Do']:
            pref_name = f"{pref}{suffix}" if suffix else pref
            if pref_name in prefecture_geo:
                all_coord_strings.append(prefecture_geo[pref_name])
                found_count += 1
                print(f"  ✓ Found {pref_name}")
                found = True
                break

        if not found:
            print(f"  ✗ MISSING: {pref}")

    if found_count > 0:
        # Merge all coordinates
        if len(all_coord_strings) == 1:
            boundary = all_coord_strings[0]
        else:
            # Multiple prefectures - merge coordinates
            all_points = []
            for coord_str in all_coord_strings:
                points = coord_str.split(';')
                all_points.extend(points)

            # Remove duplicates while preserving order
            seen = set()
            unique_points = []
            for point in all_points:
                if point not in seen:
                    seen.add(point)
                    unique_points.append(point)

            boundary = ';'.join(unique_points)

        range_boundaries.append({
            'Name': range_name,
            'Japanese Name': japanese_name,
            'Prefectures': prefectures_str,
            'Coordinates': boundary
        })
        print(f"  → Created boundary with {len(boundary.split(';'))} points")
    else:
        print(f"  ✗ NO BOUNDARIES FOUND")

print(f"\n{'='*60}")
print(f"Created {len(range_boundaries)} mountain range boundaries")

# Write to CSV
with open('mountain_ranges_geo.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Prefectures', 'Coordinates']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(range_boundaries)

print(f"✓ Written to mountain_ranges_geo.csv")

# List all ranges created
print(f"\nMountain ranges created:")
for r in range_boundaries:
    print(f"  • {r['Name']} ({r['Japanese Name']}) - {r['Prefectures']}")
