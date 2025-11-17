#!/usr/bin/env python3
"""
Simplify the river data for Kuma, Watarase, and Katsura rivers.
"""

import csv

# Read all rivers
rivers = []
with open('rivers_geo_final.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rivers.append(row)

# Simplified river data (keeping key points along the path)
simplified_rivers = {
    'Kuma': '32.495,130.603;32.432,130.656;32.366,130.642;32.306,130.609;32.248,130.659;32.212,130.758;32.222,130.849;32.269,130.941;32.320,131.009;32.378,131.022;32.439,130.970',

    'Watarase': '36.172,139.691;36.207,139.692;36.267,139.580;36.302,139.499;36.340,139.410;36.380,139.352;36.449,139.283;36.490,139.275;36.536,139.354;36.597,139.406;36.631,139.434',

    'Katsura': '34.953,135.732;35.012,135.686;35.018,135.626;35.072,135.536;35.115,135.518;35.141,135.639;35.187,135.676;35.207,135.775;35.244,135.767'
}

# Update the rivers
for river in rivers:
    if river['Name'] in simplified_rivers:
        river['Coordinates'] = simplified_rivers[river['Name']]
        print(f"Simplified {river['Name']}: {len(river['Coordinates'].split(';'))} points")

# Write back to file
with open('rivers_geo_final.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Coordinates']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rivers)

print(f"\n✓ Updated rivers_geo_final.csv")
