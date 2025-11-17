#!/usr/bin/env python3
"""
Convert all CSV data files to a single JavaScript file for embedding.
"""

import csv
import json

# Files to convert
files = {
    'prefectures': 'prefectures.csv',
    'prefectures_geo': 'prefectures_geo.csv',
    'old_provinces': 'old_provinces.csv',
    'old_provinces_geo': 'old_provinces_geo.csv',
    'lakes': 'lakes.csv',
    'lakes_geo': 'lakes_geo.csv',
    'rivers': 'rivers.csv',
    'rivers_geo': 'rivers_geo_final.csv',
    'mountains': 'mountains.csv',
    'mountains_geo': 'mountains_geo.csv',
    'mountain_ranges': 'mountain_ranges_geo.csv',
    'sake_rice': 'sake_rice.csv'
}

def read_csv(filename):
    """Read CSV file and return as list of dictionaries."""
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Filter out completely empty rows
                if any(v.strip() for v in row.values()):
                    data.append(row)
        print(f"✓ Loaded {filename}: {len(data)} rows")
    except Exception as e:
        print(f"✗ Error loading {filename}: {e}")
        data = []
    return data

# Load all data
all_data = {}
for key, filename in files.items():
    all_data[key] = read_csv(filename)

# Write to JavaScript file in parent directory
with open('../japan_geo_data.js', 'w', encoding='utf-8') as f:
    f.write('// Japan Geography Data - Auto-generated from CSV files\n')
    f.write('// Do not edit manually - regenerate using convert_csv_to_js.py\n\n')
    f.write('const JAPAN_GEO_DATA = ')
    json.dump(all_data, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print(f"\n✓ Created japan_geo_data.js with {sum(len(v) for v in all_data.values())} total records")
print(f"  Data keys: {', '.join(all_data.keys())}")
