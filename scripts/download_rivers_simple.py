#!/usr/bin/env python3
"""
Simple script to download river geometry from OpenStreetMap.
"""

import requests
import csv
import time

def download_river(name_ja):
    """Download river from OSM by Japanese name."""
    query = f"""
    [out:json][timeout:25];
    (
      way["waterway"="river"]["name"="{name_ja}"](30,128,46,146);
      relation["waterway"="river"]["name"="{name_ja}"](30,128,46,146);
    );
    out geom;
    """

    try:
        response = requests.get(
            "http://overpass-api.de/api/interpreter",
            params={'data': query},
            timeout=40
        )
        data = response.json()

        if not data.get('elements'):
            return None

        # Extract coordinates
        coords = []
        for element in data['elements']:
            if 'geometry' in element:
                for node in element['geometry']:
                    coords.append((node['lat'], node['lon']))
            elif 'members' in element:
                for member in element['members']:
                    if 'geometry' in member:
                        for node in member['geometry']:
                            coords.append((node['lat'], node['lon']))

        if not coords:
            return None

        # Simplify to ~50 points
        if len(coords) > 50:
            step = len(coords) // 50
            coords = [coords[0]] + [coords[i] for i in range(step, len(coords), step)]
            if coords[-1] != coords[-1]:
                coords.append(coords[-1])

        # Format as CSV string
        return ";".join(f"{lat},{lon}" for lat, lon in coords)

    except Exception as e:
        print(f"  Error: {e}")
        return None

# Read rivers
print("Reading rivers.csv...")
rivers = []
with open('rivers.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rivers.append(row)

print(f"Found {len(rivers)} rivers\n")

# Download each river
results = []
for i, river in enumerate(rivers, 1):
    name_en = river['Name']
    name_ja = river['Japanese Name']

    print(f"[{i}/{len(rivers)}] {name_en} ({name_ja})...", end=' ', flush=True)

    coord_str = download_river(name_ja)

    if coord_str:
        num_points = len(coord_str.split(';'))
        print(f"✓ {num_points} points")
        results.append({'Name': name_en, 'Coordinates': coord_str})
    else:
        print("✗ Not found")

    # Be nice to OSM servers
    time.sleep(2)

# Write results
print(f"\nSuccessfully downloaded {len(results)}/{len(rivers)} rivers")
print("Writing to rivers_geo_new.csv...")

with open('rivers_geo_new.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Coordinates'])
    for result in results:
        writer.writerow([result['Name'], result['Coordinates']])

print(f"✓ Done! Saved {len(results)} rivers")
