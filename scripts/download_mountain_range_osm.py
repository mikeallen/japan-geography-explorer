#!/usr/bin/env python3
"""
Download actual mountain range boundaries from OpenStreetMap.
"""

import requests
import json
import csv
import time

# Mountain ranges to download (with their Japanese names for better search)
mountain_ranges = [
    {'name': 'Hida Mountains', 'japanese': '飛騨山脈', 'search': 'Hida Mountains'},
    {'name': 'Akaishi Mountains', 'japanese': '赤石山脈', 'search': 'Akaishi Mountains'},
    {'name': 'Kiso Mountains', 'japanese': '木曽山脈', 'search': 'Kiso Mountains'},
    {'name': 'Ou Mountains', 'japanese': '奥羽山脈', 'search': 'Ōu Mountains'},
    {'name': 'Dewa Sanzan', 'japanese': '出羽三山', 'search': 'Dewa Sanzan'},
    {'name': 'Kii Mountains', 'japanese': '紀伊山地', 'search': 'Kii Mountains'},
    {'name': 'Yoshino Mountains', 'japanese': '吉野山', 'search': 'Yoshino Mountains'},
    {'name': 'Shikoku Mountains', 'japanese': '四国山地', 'search': 'Shikoku Mountains'},
    {'name': 'Shirakami Mountains', 'japanese': '白神山地', 'search': 'Shirakami-Sanchi'},
    {'name': 'Kitakami Mountains', 'japanese': '北上山地', 'search': 'Kitakami Mountains'},
    {'name': 'Tanzawa Mountains', 'japanese': '丹沢山地', 'search': 'Tanzawa Mountains'},
    {'name': 'Yatsugatake Mountains', 'japanese': '八ヶ岳連峰', 'search': 'Yatsugatake'},
    {'name': 'Misaka Mountains', 'japanese': '御坂山地', 'search': 'Misaka Mountains'},
    {'name': 'Suzuka Mountains', 'japanese': '鈴鹿山脈', 'search': 'Suzuka Mountains'},
]

def query_overpass(search_name, japanese_name):
    """Query Overpass API for a mountain range."""
    # Overpass API endpoint
    url = "https://overpass-api.de/api/interpreter"

    # Query for mountain ranges in Japan
    # Try searching by English name, Japanese name, or as a natural=mountain_range feature
    query = f"""
    [out:json][timeout:25];
    (
      // Search by name
      area["ISO3166-1"="JP"][admin_level=2];
      (
        way["natural"="mountain_range"]["name"~"{search_name}",i](area);
        relation["natural"="mountain_range"]["name"~"{search_name}",i](area);
        way["natural"="mountain_range"]["name:en"~"{search_name}",i](area);
        relation["natural"="mountain_range"]["name:en"~"{search_name}",i](area);
        way["natural"="mountain_range"]["name:ja"="{japanese_name}"](area);
        relation["natural"="mountain_range"]["name:ja"="{japanese_name}"](area);
      );
    );
    out geom;
    """

    print(f"\nQuerying for: {search_name} ({japanese_name})")

    try:
        response = requests.post(url, data={'data': query}, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('elements'):
                print(f"  ✓ Found {len(data['elements'])} element(s)")
                return data['elements']
            else:
                print(f"  ✗ No data found")
                return None
        else:
            print(f"  ✗ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return None

def extract_coordinates(element):
    """Extract coordinates from an OSM element."""
    coords = []

    if element['type'] == 'way':
        # Simple way - just use the geometry
        if 'geometry' in element:
            for node in element['geometry']:
                coords.append(f"{node['lat']},{node['lon']}")

    elif element['type'] == 'relation':
        # Relation - need to extract from members
        if 'members' in element:
            for member in element['members']:
                if 'geometry' in member:
                    for node in member['geometry']:
                        coords.append(f"{node['lat']},{node['lon']}")

    # Join with semicolons
    return ';'.join(coords) if coords else None

# Download data
results = []
for range_data in mountain_ranges:
    elements = query_overpass(range_data['search'], range_data['japanese'])

    if elements:
        # Use the first (usually largest) element
        coords = extract_coordinates(elements[0])

        if coords:
            results.append({
                'Name': range_data['name'],
                'Japanese Name': range_data['japanese'],
                'Prefectures': '',  # Will fill from existing data
                'Coordinates': coords
            })
            print(f"  → Extracted {len(coords.split(';'))} points")
        else:
            print(f"  ✗ Could not extract coordinates")

    # Be nice to the API
    time.sleep(2)

print(f"\n{'='*60}")
print(f"Successfully downloaded {len(results)} mountain ranges")

if results:
    # Write to CSV
    with open('mountain_ranges_geo_osm.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Name', 'Japanese Name', 'Prefectures', 'Coordinates']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"✓ Written to mountain_ranges_geo_osm.csv")
    print(f"\nDownloaded ranges:")
    for r in results:
        print(f"  • {r['Name']} ({r['Japanese Name']})")
else:
    print("No data was downloaded successfully")
