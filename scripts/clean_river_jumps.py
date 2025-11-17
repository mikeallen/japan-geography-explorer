#!/usr/bin/env python3
"""
Clean river data by removing points that create unreasonably large jumps.
Strategy: Find the largest connected segment and keep only that.
"""

import csv
import math

def distance(lat1, lon1, lat2, lon2):
    """Calculate approximate distance in km between two lat/lon points."""
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    return math.sqrt((dlat * 111)**2 + (dlon * 91)**2)

def find_largest_connected_segment(coords, max_jump_km=50):
    """
    Find the largest segment of consecutive points where no jump exceeds max_jump_km.
    Returns list of indices forming the largest connected segment.
    """
    if len(coords) <= 1:
        return list(range(len(coords)))

    # Build segments separated by large jumps
    segments = []
    current_segment = [0]

    for i in range(len(coords) - 1):
        lat1, lon1 = coords[i]
        lat2, lon2 = coords[i + 1]
        dist = distance(lat1, lon1, lat2, lon2)

        if dist <= max_jump_km:
            current_segment.append(i + 1)
        else:
            # Large jump - start new segment
            if len(current_segment) > 0:
                segments.append(current_segment)
            current_segment = [i + 1]

    # Add final segment
    if len(current_segment) > 0:
        segments.append(current_segment)

    # Return largest segment
    if not segments:
        return []

    largest = max(segments, key=len)
    return largest

# Read river metadata
print("Reading river metadata...")
river_metadata = {}
with open('rivers.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Name']:
            river_metadata[row['Name']] = {
                'length_km': float(row['Length']) if row['Length'] else 0
            }

print("\nCleaning rivers by removing jump-causing points...\n")
cleaned_rivers = []
stats = {'total': 0, 'cleaned': 0, 'points_removed': 0}

with open('rivers_geo_cleaned.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['Name']:
            continue

        stats['total'] += 1
        name = row['Name']
        coords_str = row['Coordinates']

        if not coords_str:
            cleaned_rivers.append({'Name': name, 'Coordinates': ''})
            continue

        # Parse coordinates
        coord_pairs = coords_str.split(';')
        coords = []
        for pair in coord_pairs:
            try:
                lat, lon = map(float, pair.split(','))
                coords.append((lat, lon))
            except:
                pass

        if len(coords) <= 1:
            cleaned_rivers.append({'Name': name, 'Coordinates': coords_str})
            continue

        # For short rivers, use stricter threshold (30km)
        # For longer rivers, allow up to 50km jumps
        river_length = river_metadata.get(name, {}).get('length_km', 100)
        max_jump = 30 if river_length < 100 else 50

        # Find largest connected segment
        keep_indices = find_largest_connected_segment(coords, max_jump)

        # Filter coordinates
        kept_coords = [coord_pairs[i] for i in keep_indices]
        removed_count = len(coord_pairs) - len(kept_coords)

        if removed_count > 0:
            stats['cleaned'] += 1
            stats['points_removed'] += removed_count
            print(f"✓ {name}: removed {removed_count} points (from {len(coord_pairs)} to {len(kept_coords)})")

            # Show what was removed if significant
            if removed_count > 5 or removed_count / len(coord_pairs) > 0.3:
                print(f"   Kept largest connected segment (indices {min(keep_indices)}-{max(keep_indices)})")

        if kept_coords:
            cleaned_rivers.append({
                'Name': name,
                'Coordinates': ';'.join(kept_coords)
            })
        else:
            print(f"⚠ {name}: no valid connected segment found")

# Write cleaned data
output_file = 'rivers_geo_final.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Coordinates'])
    for river in cleaned_rivers:
        writer.writerow([river['Name'], river['Coordinates']])

print(f"\n{'='*60}")
print(f"Jump cleaning complete!")
print(f"  Total rivers: {stats['total']}")
print(f"  Rivers cleaned: {stats['cleaned']}")
print(f"  Total points removed: {stats['points_removed']}")
print(f"  Output: {output_file}")
print(f"{'='*60}")
