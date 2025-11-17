#!/usr/bin/env python3
"""
Simplify river coordinate data to match the style of the original 6 rivers.
Uses Douglas-Peucker algorithm for intelligent simplification.
"""

import csv
import math

def douglas_peucker(points, epsilon):
    """
    Simplify a line using the Ramer-Douglas-Peucker algorithm.
    points: list of (lat, lon) tuples
    epsilon: tolerance (higher = more simplification)
    """
    if len(points) < 3:
        return points

    # Find the point with the maximum distance from line between first and last
    dmax = 0
    index = 0
    end = len(points) - 1

    for i in range(1, end):
        d = perpendicular_distance(points[i], points[0], points[end])
        if d > dmax:
            index = i
            dmax = d

    # If max distance is greater than epsilon, recursively simplify
    if dmax > epsilon:
        # Recursive call
        rec_results1 = douglas_peucker(points[:index+1], epsilon)
        rec_results2 = douglas_peucker(points[index:], epsilon)

        # Build the result list
        result = rec_results1[:-1] + rec_results2
    else:
        result = [points[0], points[end]]

    return result

def perpendicular_distance(point, line_start, line_end):
    """Calculate perpendicular distance from point to line."""
    if line_start == line_end:
        return distance(point, line_start)

    # Convert to simple Euclidean distance (good enough for our purposes)
    lat, lon = point
    lat1, lon1 = line_start
    lat2, lon2 = line_end

    # Calculate distance using cross product
    num = abs((lon2 - lon1) * (lat1 - lat) - (lat2 - lat1) * (lon1 - lon))
    denom = math.sqrt((lon2 - lon1)**2 + (lat2 - lat1)**2)

    if denom == 0:
        return 0

    return num / denom

def distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def simplify_to_n_points(coords, target_points=10):
    """
    Simplify coordinates to approximately target_points using Douglas-Peucker.
    """
    if len(coords) <= target_points:
        return coords

    # Try different epsilon values to get close to target
    epsilons = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]

    for epsilon in epsilons:
        simplified = douglas_peucker(coords, epsilon)
        if len(simplified) <= target_points:
            return simplified

    # If still too many points, take evenly spaced subset
    if len(simplified) > target_points:
        step = len(simplified) // target_points
        return [simplified[0]] + [simplified[i] for i in range(step, len(simplified), step)][:target_points-2] + [simplified[-1]]

    return simplified

def parse_coordinates(coord_str):
    """Parse coordinate string to list of (lat, lon) tuples."""
    if not coord_str:
        return []

    coords = []
    for pair in coord_str.split(';'):
        parts = pair.split(',')
        if len(parts) == 2:
            try:
                lat, lon = float(parts[0]), float(parts[1])
                coords.append((lat, lon))
            except ValueError:
                continue
    return coords

def coords_to_string(coords):
    """Convert list of (lat, lon) tuples to CSV string."""
    return ";".join(f"{lat:.4f},{lon:.4f}" for lat, lon in coords)

# Read the messy OSM data
print("Reading rivers_geo_new.csv...")
rivers = []
with open('rivers_geo_new.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        coords = parse_coordinates(row['Coordinates'])
        if coords and len(coords) > 2:
            rivers.append({
                'name': row['Name'],
                'coords': coords
            })

print(f"Found {len(rivers)} rivers with coordinates\n")

# Simplify each river
simplified_rivers = []
for river in rivers:
    original_count = len(river['coords'])
    simplified = simplify_to_n_points(river['coords'], target_points=10)

    # Ensure we have between 8-12 points for consistency with original data
    if len(simplified) < 8:
        simplified = simplify_to_n_points(river['coords'], target_points=8)

    print(f"{river['name']}: {original_count} points -> {len(simplified)} points")

    simplified_rivers.append({
        'Name': river['name'],
        'Coordinates': coords_to_string(simplified)
    })

# Write simplified data
print(f"\nWriting simplified data to rivers_geo_simplified.csv...")
with open('rivers_geo_simplified.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Coordinates'])
    for river in simplified_rivers:
        writer.writerow([river['Name'], river['Coordinates']])

print(f"✓ Done! Created clean paths for {len(simplified_rivers)} rivers")
