#!/usr/bin/env python3
"""
Download river geometry from OpenStreetMap using Overpass API.
Converts to CSV format compatible with our visualization system.
"""

import requests
import json
import csv
import time
from typing import List, Tuple

def query_overpass(river_name: str, japanese_name: str = None) -> dict:
    """
    Query Overpass API for a specific river in Japan.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Build query to search for river by name (English or Japanese)
    # Search within Japan's bounding box: roughly 30-46N, 128-146E
    query = f"""
    [out:json][timeout:25];
    (
      way["waterway"="river"]["name"="{river_name}"](30,128,46,146);
      relation["waterway"="river"]["name"="{river_name}"](30,128,46,146);
    """

    # Add Japanese name search if provided
    if japanese_name:
        query += f"""
      way["waterway"="river"]["name"="{japanese_name}"](30,128,46,146);
      relation["waterway"="river"]["name"="{japanese_name}"](30,128,46,146);
    """

    query += """
    );
    out geom;
    """

    print(f"Querying for: {river_name} ({japanese_name})...", flush=True)

    try:
        response = requests.get(overpass_url, params={'data': query}, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  Error querying {river_name}: {e}", flush=True)
        return None

def extract_coordinates(element: dict) -> List[Tuple[float, float]]:
    """
    Extract coordinates from an OSM element.
    Returns list of (lat, lon) tuples.
    """
    coords = []

    if element['type'] == 'way':
        # Direct way with geometry
        if 'geometry' in element:
            for node in element['geometry']:
                coords.append((node['lat'], node['lon']))

    elif element['type'] == 'relation':
        # Relation containing multiple ways
        if 'members' in element:
            for member in element['members']:
                if member['type'] == 'way' and 'geometry' in member:
                    for node in member['geometry']:
                        coords.append((node['lat'], node['lon']))

    return coords

def coords_to_csv_string(coords: List[Tuple[float, float]]) -> str:
    """
    Convert coordinate list to CSV format: "lat,lon;lat,lon;..."
    """
    if not coords:
        return ""
    return ";".join(f"{lat},{lon}" for lat, lon in coords)

def simplify_coordinates(coords: List[Tuple[float, float]], max_points: int = 50) -> List[Tuple[float, float]]:
    """
    Simplify coordinate list by keeping every Nth point.
    Always keeps first and last points.
    """
    if len(coords) <= max_points:
        return coords

    step = max(1, len(coords) // max_points)
    simplified = [coords[0]]  # Always keep first

    for i in range(step, len(coords), step):
        simplified.append(coords[i])

    # Always keep last if not already included
    if simplified[-1] != coords[-1]:
        simplified.append(coords[-1])

    return simplified

def download_river(river_name: str, japanese_name: str = None, max_points: int = 50) -> str:
    """
    Download a river from OSM and return as CSV coordinate string.
    """
    data = query_overpass(river_name, japanese_name)

    if not data or 'elements' not in data or len(data['elements']) == 0:
        print(f"  No data found for {river_name}", flush=True)
        return None

    # Collect all coordinates from all elements
    all_coords = []
    for element in data['elements']:
        coords = extract_coordinates(element)
        all_coords.extend(coords)

    if not all_coords:
        print(f"  No coordinates extracted for {river_name}", flush=True)
        return None

    # Simplify to reduce file size
    simplified = simplify_coordinates(all_coords, max_points)

    print(f"  Found {len(all_coords)} points -> simplified to {len(simplified)} points", flush=True)

    return coords_to_csv_string(simplified)

def main():
    """
    Download river geometry for all rivers in our metadata CSV.
    """
    print("=" * 60)
    print("OpenStreetMap River Data Downloader")
    print("=" * 60)

    # Read our rivers metadata
    rivers = []
    with open('rivers.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rivers.append(row)

    print(f"\nFound {len(rivers)} rivers in rivers.csv")
    print("\nDownloading geometry from OpenStreetMap...")
    print("This may take several minutes...\n")

    # Try to download each river
    results = []
    for i, river in enumerate(rivers, 1):
        name = river['Name']
        japanese_name = river.get('Japanese Name', '')

        print(f"[{i}/{len(rivers)}] {name} ({japanese_name})")

        coord_string = download_river(name, japanese_name)

        if coord_string:
            results.append({
                'Name': name,
                'Coordinates': coord_string
            })

        # Rate limiting - be nice to OSM servers
        time.sleep(1)

    # Write results to CSV
    print(f"\n\nSuccessfully downloaded {len(results)} rivers")
    print("Writing to rivers_geo_new.csv...")

    with open('rivers_geo_new.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Coordinates'])

        for result in results:
            writer.writerow([result['Name'], result['Coordinates']])

    print(f"\n✓ Saved {len(results)} rivers to rivers_geo_new.csv")
    print("\nNote: Rivers not found in OSM may need manual geometry data")
    print("=" * 60)

if __name__ == '__main__':
    main()
