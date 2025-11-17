#!/usr/bin/env python3
"""
Convert Japan prefecture GeoJSON to CSV format with high accuracy.
"""

import json
import csv
from typing import List, Tuple

def simplify_coordinates(coords: List[List[float]], tolerance: int = 50) -> List[List[float]]:
    """
    Simplify coordinate list while maintaining shape accuracy.
    Keep every Nth point but always include first and last.
    """
    if len(coords) <= tolerance:
        return coords

    step = max(1, len(coords) // tolerance)
    simplified = [coords[0]]  # Always keep first

    for i in range(step, len(coords), step):
        simplified.append(coords[i])

    # Always include last point if not already included
    if simplified[-1] != coords[-1]:
        simplified.append(coords[-1])

    return simplified

def extract_outer_ring(geometry) -> List[List[float]]:
    """
    Extract and flatten coordinates from MultiPolygon or Polygon geometry.
    Returns the largest/outer ring.
    """
    geom_type = geometry.get('type')
    coords = geometry.get('coordinates', [])

    all_rings = []

    if geom_type == 'Polygon':
        # Polygon: array of rings (first is outer)
        if coords and len(coords) > 0:
            all_rings.append(coords[0])

    elif geom_type == 'MultiPolygon':
        # MultiPolygon: array of polygons, each with rings
        for polygon in coords:
            if polygon and len(polygon) > 0:
                all_rings.append(polygon[0])  # Get outer ring of each polygon

    # Find the largest ring (most points = main boundary)
    if not all_rings:
        return []

    largest_ring = max(all_rings, key=len)
    return largest_ring

def coords_to_csv_string(coords: List[List[float]], simplify: int = 200) -> str:
    """
    Convert coordinate array to CSV string format.
    GeoJSON uses [lon, lat], we convert to "lat,lon;lat,lon;..."
    """
    simplified = simplify_coordinates(coords, simplify)
    # Convert from [lon, lat] to "lat,lon"
    return ";".join(f"{coord[1]},{coord[0]}" for coord in simplified)

def convert_prefectures(input_file: str, output_file: str, max_points: int = 200):
    """
    Convert prefecture GeoJSON to CSV format.
    """
    print(f"Loading {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    features = data.get('features', [])
    print(f"Found {len(features)} prefectures")

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Japanese Name', 'ID', 'Coordinates'])

        for feature in features:
            props = feature.get('properties', {})
            geom = feature.get('geometry', {})

            name_en = props.get('nam', '')
            name_ja = props.get('nam_ja', '')
            pref_id = props.get('id', '')

            # Extract coordinates
            outer_ring = extract_outer_ring(geom)

            if not outer_ring:
                print(f"Warning: No coordinates for {name_en}")
                continue

            # Convert to CSV format
            coord_str = coords_to_csv_string(outer_ring, max_points)

            print(f"  {name_en} ({name_ja}): {len(outer_ring)} points -> {len(coord_str.split(';'))} points")

            writer.writerow([name_en, name_ja, pref_id, coord_str])

    print(f"\n✓ Saved {output_file}")

def main():
    print("=" * 60)
    print("Japan Prefecture GeoJSON to CSV Converter")
    print("=" * 60)

    convert_prefectures(
        'japan_prefectures.geojson',
        'prefectures_geo.csv',
        max_points=200  # Points per prefecture
    )

    print("\n" + "=" * 60)
    print("Conversion complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
