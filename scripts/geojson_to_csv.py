#!/usr/bin/env python3
"""
Convert GeoJSON data to simplified CSV format for Japan geography visualization.

Geometry CSV Format:
- Polygons (prefectures, lakes, etc.): name,coordinates
  Coordinates format: lat1,lon1;lat2,lon2;lat3,lon3;...
- Polylines (rivers): name,coordinates
  Same format as polygons
- Points (mountains): name,latitude,longitude,elevation
"""

import json
import csv
import urllib.request
import sys
from typing import List, Tuple, Dict, Any

def download_json(url: str) -> Dict[str, Any]:
    """Download JSON data from URL."""
    print(f"Downloading from {url}...")
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode('utf-8'))

def coords_to_string(coords: List[List[float]], reverse: bool = True) -> str:
    """
    Convert coordinate array to CSV string format.

    Args:
        coords: List of [longitude, latitude] pairs (GeoJSON format)
        reverse: If True, output as lat,lon; if False, output as lon,lat

    Returns:
        String in format "lat1,lon1;lat2,lon2;..."
    """
    if reverse:
        # GeoJSON uses [lon, lat], we want [lat, lon]
        return ";".join(f"{coord[1]},{coord[0]}" for coord in coords)
    else:
        return ";".join(f"{coord[0]},{coord[1]}" for coord in coords)

def simplify_coordinates(coords: List[List[float]], max_points: int = 100) -> List[List[float]]:
    """
    Simplify coordinate list by keeping only every Nth point.
    Always keeps first and last points.
    """
    if len(coords) <= max_points:
        return coords

    step = len(coords) // (max_points - 1)
    simplified = [coords[i] for i in range(0, len(coords), step)]

    # Ensure last point is included
    if simplified[-1] != coords[-1]:
        simplified.append(coords[-1])

    return simplified

def convert_prefectures_geojson(geojson_url: str, output_csv: str, max_points: int = 150):
    """
    Convert prefecture GeoJSON to CSV format.

    Expected GeoJSON structure:
    {
        "type": "FeatureCollection",
        "features": [{
            "properties": {"name": "...", "name_ja": "..."},
            "geometry": {"type": "Polygon|MultiPolygon", "coordinates": [...]}
        }]
    }
    """
    print(f"\nConverting prefectures from {geojson_url}")

    try:
        data = download_json(geojson_url)
    except Exception as e:
        print(f"Error downloading: {e}")
        print("Using simplified approach...")
        return False

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Japanese Name', 'Coordinates'])

        for feature in data.get('features', []):
            props = feature.get('properties', {})
            geom = feature.get('geometry', {})

            name_en = props.get('name', props.get('nam_en', props.get('NAME_1', '')))
            name_ja = props.get('name_ja', props.get('nam_ja', props.get('NAME_LOCAL', '')))

            coords = geom.get('coordinates', [])
            geom_type = geom.get('type', '')

            # Handle different geometry types
            if geom_type == 'Polygon':
                # Polygon: array of rings, we want the outer ring (first one)
                if coords and len(coords) > 0:
                    outer_ring = simplify_coordinates(coords[0], max_points)
                    coord_str = coords_to_string(outer_ring)
                    writer.writerow([name_en, name_ja, coord_str])

            elif geom_type == 'MultiPolygon':
                # MultiPolygon: array of polygons
                # We'll combine all outer rings
                all_coords = []
                for polygon in coords:
                    if polygon and len(polygon) > 0:
                        all_coords.extend(polygon[0])

                if all_coords:
                    simplified = simplify_coordinates(all_coords, max_points)
                    coord_str = coords_to_string(simplified)
                    writer.writerow([name_en, name_ja, coord_str])

    print(f"✓ Prefectures saved to {output_csv}")
    return True

def create_sample_japan_outline(output_csv: str):
    """
    Create a simplified but reasonably accurate outline of Japan.
    This uses key points for the four main islands.
    """
    print("\nCreating simplified Japan outline...")

    # Simplified coordinates for Japan's main islands
    # Format: [lat, lon]
    japan_outline = {
        "Hokkaido": [
            [45.52, 141.38], [45.35, 141.68], [44.98, 142.05], [44.52, 143.18],
            [43.98, 144.68], [43.32, 145.58], [42.95, 145.82], [42.52, 145.35],
            [41.88, 145.08], [41.52, 140.95], [41.65, 140.45], [42.05, 140.12],
            [42.68, 140.38], [43.18, 140.78], [43.82, 141.08], [44.38, 141.28],
            [45.05, 141.52], [45.52, 141.38]
        ],
        "Honshu": [
            [41.52, 140.52], [41.38, 140.35], [40.85, 140.12], [40.32, 139.85],
            [39.72, 140.05], [39.18, 139.52], [38.52, 139.82], [37.92, 138.95],
            [37.52, 138.25], [36.95, 137.52], [36.52, 137.12], [36.05, 136.85],
            [35.52, 136.52], [35.18, 136.12], [34.85, 135.52], [34.52, 135.12],
            [34.18, 134.52], [34.05, 134.12], [34.38, 133.52], [34.52, 133.18],
            [34.85, 132.85], [35.18, 132.52], [35.52, 131.85], [35.85, 131.18],
            [36.18, 131.52], [36.52, 132.18], [36.85, 132.85], [37.18, 133.52],
            [37.52, 134.18], [37.85, 135.12], [38.18, 136.52], [38.52, 137.82],
            [38.85, 139.12], [39.18, 139.82], [39.52, 140.52], [39.85, 141.18],
            [40.18, 141.52], [40.52, 141.38], [40.85, 141.12], [41.18, 140.85],
            [41.52, 140.52]
        ],
        "Shikoku": [
            [34.25, 133.52], [34.05, 133.82], [33.85, 134.12], [33.68, 134.52],
            [33.52, 134.82], [33.35, 134.68], [33.18, 134.35], [33.05, 133.85],
            [33.12, 133.35], [33.25, 132.85], [33.52, 132.52], [33.85, 132.68],
            [34.12, 133.18], [34.25, 133.52]
        ],
        "Kyushu": [
            [33.85, 131.18], [33.68, 131.52], [33.35, 131.82], [33.05, 131.52],
            [32.68, 131.35], [32.35, 131.18], [31.95, 131.05], [31.52, 130.85],
            [31.18, 130.52], [30.85, 130.35], [30.52, 130.18], [30.35, 130.45],
            [30.52, 130.82], [30.85, 131.18], [31.18, 131.52], [31.52, 131.85],
            [31.85, 132.18], [32.18, 132.52], [32.52, 132.82], [32.85, 133.12],
            [33.18, 133.35], [33.35, 133.12], [33.52, 132.52], [33.68, 131.85],
            [33.85, 131.18]
        ]
    }

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Japanese Name', 'Coordinates'])

        island_names_ja = {
            'Hokkaido': '北海道',
            'Honshu': '本州',
            'Shikoku': '四国',
            'Kyushu': '九州'
        }

        for island_name, coords in japan_outline.items():
            coord_str = ";".join(f"{lat},{lon}" for lat, lon in coords)
            writer.writerow([island_name, island_names_ja[island_name], coord_str])

    print(f"✓ Japan outline saved to {output_csv}")

def main():
    """Main function to convert various GeoJSON sources."""

    print("=" * 60)
    print("Japan Geography Data Converter")
    print("=" * 60)

    # Try to download prefecture data from various sources
    prefecture_sources = [
        "https://raw.githubusercontent.com/dataofjapan/land/master/japan.geojson",
        "https://raw.githubusercontent.com/amay077/JapanPrefGeoJson/master/prefectures.geojson"
    ]

    success = False
    for source_url in prefecture_sources:
        try:
            if convert_prefectures_geojson(source_url, "prefectures_geo.csv", max_points=150):
                success = True
                break
        except Exception as e:
            print(f"Failed to process {source_url}: {e}")
            continue

    if not success:
        print("\nCouldn't download prefecture data. Creating simplified version...")
        create_sample_japan_outline("japan_outline_geo.csv")

    print("\n" + "=" * 60)
    print("Conversion complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the generated CSV files")
    print("2. Add data for rivers, lakes, mountains, etc.")
    print("3. Use these files in your visualization application")

if __name__ == "__main__":
    main()
