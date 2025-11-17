#!/usr/bin/env python3
"""
Download mountain coordinate data from GeoNames API.
"""

import csv
import requests
import time

# GeoNames API endpoint for search
GEONAMES_SEARCH_URL = "http://api.geonames.org/searchJSON"
USERNAME = "mikeallen"  # Free GeoNames username

def search_mountain(name, japanese_name, mountain_type):
    """Search for a mountain in Japan using GeoNames API."""

    # Try searching with both names
    search_terms = [japanese_name, name]

    for search_term in search_terms:
        if not search_term:
            continue

        params = {
            'name_equals': search_term,
            'country': 'JP',
            'featureClass': 'T',  # Mountains, hills, rocks, etc
            'maxRows': 5,
            'username': USERNAME
        }

        try:
            response = requests.get(GEONAMES_SEARCH_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'geonames' in data and len(data['geonames']) > 0:
                # Get the first result
                result = data['geonames'][0]
                return {
                    'lat': result.get('lat'),
                    'lon': result.get('lng'),
                    'elevation': result.get('elevation', ''),
                    'found_name': result.get('name', ''),
                    'feature_code': result.get('fcode', '')
                }
        except Exception as e:
            print(f"  Error searching for {search_term}: {e}")

        # Be nice to the API
        time.sleep(0.5)

    return None

# Read mountains list
print("Reading mountains list...")
mountains = []
with open('mountains_list.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        mountains.append(row)

print(f"Found {len(mountains)} mountains/ranges to download\n")

# Download coordinates
results = []
for i, mountain in enumerate(mountains, 1):
    name = mountain['Name']
    japanese_name = mountain['Japanese Name']
    mountain_type = mountain['Type']

    print(f"[{i}/{len(mountains)}] {name} ({japanese_name})...", end=' ')

    data = search_mountain(name, japanese_name, mountain_type)

    if data:
        print(f"✓ {data['lat']}, {data['lon']} (elev: {data['elevation']}m)")
        results.append({
            'Name': name,
            'Japanese Name': japanese_name,
            'Type': mountain_type,
            'Latitude': data['lat'],
            'Longitude': data['lon'],
            'Elevation': data['elevation'],
            'Notes': mountain.get('Notes', '')
        })
    else:
        print("✗ Not found")
        results.append({
            'Name': name,
            'Japanese Name': japanese_name,
            'Type': mountain_type,
            'Latitude': '',
            'Longitude': '',
            'Elevation': '',
            'Notes': mountain.get('Notes', '')
        })

# Write results
output_file = 'mountains_new.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Type', 'Latitude', 'Longitude', 'Elevation', 'Notes']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

found_count = sum(1 for r in results if r['Latitude'])
print(f"\n{'='*60}")
print(f"Download complete!")
print(f"  Successfully found: {found_count}/{len(mountains)} mountains")
print(f"  Output: {output_file}")
print(f"{'='*60}")
