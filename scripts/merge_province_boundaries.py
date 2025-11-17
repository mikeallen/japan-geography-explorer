#!/usr/bin/env python3
"""
Create historical province boundaries by merging modern prefecture boundaries.
"""

import csv
from collections import defaultdict

print("Loading data...")

# Load old provinces metadata
provinces = []
with open('old_provinces.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        provinces.append(row)

# Load prefecture geometries - need to handle the "Ken/Fu/To" suffixes
prefecture_geo = {}
with open('prefectures_geo.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Store both with and without suffix
        full_name = row['Name']
        prefecture_geo[full_name] = row['Coordinates']

        # Also store without suffix for matching
        base_name = full_name.replace(' Ken', '').replace(' Fu', '').replace(' To', '').replace(' Do', '')
        if base_name != full_name:
            prefecture_geo[base_name] = row['Coordinates']

print(f"Loaded {len(provinces)} provinces")
print(f"Loaded {len(prefecture_geo)} prefecture name variations")

# Create province boundaries
province_boundaries = []
missing_provinces = []

for province in provinces:
    province_name = province['Name']
    japanese_name = province['Japanese Name']
    prefectures_str = province['Prefectures']
    region = province['Region']

    # Split by semicolon to get list of prefectures
    prefecture_list = [p.strip() for p in prefectures_str.split(';')]

    print(f"\n{province_name} ({japanese_name}) → {', '.join(prefecture_list)}")

    # Collect all coordinate points from the prefectures
    all_coord_strings = []
    found_count = 0

    for pref in prefecture_list:
        # Try exact match first
        if pref in prefecture_geo:
            all_coord_strings.append(prefecture_geo[pref])
            found_count += 1
            print(f"  ✓ Found {pref}")
        # Try with Ken suffix
        elif f"{pref} Ken" in prefecture_geo:
            all_coord_strings.append(prefecture_geo[f"{pref} Ken"])
            found_count += 1
            print(f"  ✓ Found {pref} Ken")
        # Try with Fu suffix
        elif f"{pref} Fu" in prefecture_geo:
            all_coord_strings.append(prefecture_geo[f"{pref} Fu"])
            found_count += 1
            print(f"  ✓ Found {pref} Fu")
        # Try with To suffix
        elif f"{pref} To" in prefecture_geo:
            all_coord_strings.append(prefecture_geo[f"{pref} To"])
            found_count += 1
            print(f"  ✓ Found {pref} To")
        # Try with Do suffix
        elif f"{pref} Do" in prefecture_geo:
            all_coord_strings.append(prefecture_geo[f"{pref} Do"])
            found_count += 1
            print(f"  ✓ Found {pref} Do")
        # Try with space before Do (for Hokkai Do)
        elif "Hokkai Do" in prefecture_geo and pref == "Hokkaido":
            all_coord_strings.append(prefecture_geo["Hokkai Do"])
            found_count += 1
            print(f"  ✓ Found Hokkai Do")
        else:
            print(f"  ✗ MISSING: {pref}")

    if found_count > 0:
        # Merge all coordinates into one polygon
        # For multi-prefecture provinces, concatenate all boundary points
        if len(all_coord_strings) == 1:
            # Single prefecture - use its boundary
            boundary = all_coord_strings[0]
        else:
            # Multiple prefectures - parse coordinates and find convex hull or merge
            # For now, just concatenate (simple approach)
            # Better: find outer boundary of all polygons
            all_points = []
            for coord_str in all_coord_strings:
                points = coord_str.split(';')
                all_points.extend(points)

            # Remove duplicates while preserving some order
            seen = set()
            unique_points = []
            for point in all_points:
                if point not in seen:
                    seen.add(point)
                    unique_points.append(point)

            boundary = ';'.join(unique_points)

        province_boundaries.append({
            'Name': province_name,
            'Japanese Name': japanese_name,
            'Modern Prefecture': ', '.join(prefecture_list),
            'Coordinates': boundary
        })
        print(f"  → Created boundary with {len(boundary.split(';'))} points")
    else:
        print(f"  ✗ NO BOUNDARIES FOUND")
        missing_provinces.append(province_name)

print(f"\n{'='*60}")
print(f"Created {len(province_boundaries)} province boundaries")
print(f"Missing {len(missing_provinces)} provinces: {', '.join(missing_provinces)}")

# Write to CSV
with open('old_provinces_geo.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Modern Prefecture', 'Coordinates']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(province_boundaries)

print(f"\n✓ Written to old_provinces_geo.csv")

# Statistics
single_pref = sum(1 for p in provinces if ';' not in p['Prefectures'])
multi_pref = len(provinces) - single_pref
print(f"\nStatistics:")
print(f"  Single prefecture provinces: {single_pref}")
print(f"  Multi-prefecture provinces: {multi_pref}")
print(f"  Total provinces created: {len(province_boundaries)}")
