#!/usr/bin/env python3
"""
Add missing mountains from the original list.
"""

import csv

# Missing mountains with coordinates
missing_mountains = [
    # Individual peaks
    {'Name': 'Akaishi', 'Japanese': '赤石岳', 'Type': 'mountain', 'Lat': 35.6272, 'Lon': 138.1881, 'Elev': 3121, 'Prefecture': 'Nagano;Shizuoka'},
    {'Name': 'Futago', 'Japanese': '双子山', 'Type': 'mountain', 'Lat': 35.6167, 'Lon': 138.1833, 'Elev': 2860, 'Prefecture': 'Yamanashi;Nagano'},
    {'Name': 'Onitsuke', 'Japanese': '鬼岳', 'Type': 'mountain', 'Lat': 24.4367, 'Lon': 124.1683, 'Elev': 315, 'Prefecture': 'Okinawa'},
    {'Name': 'Osuzu', 'Japanese': '於鈴山', 'Type': 'mountain', 'Lat': 33.2167, 'Lon': 131.5833, 'Elev': 647, 'Prefecture': 'Oita'},
    {'Name': 'Funagata', 'Japanese': '舟形山', 'Type': 'mountain', 'Lat': 38.5500, 'Lon': 140.1333, 'Elev': 1500, 'Prefecture': 'Yamagata'},
    {'Name': 'Hakkyo', 'Japanese': '八経ヶ岳', 'Type': 'mountain', 'Lat': 34.1806, 'Lon': 135.9556, 'Elev': 1915, 'Prefecture': 'Nara'},

    # Mountain ranges (using approximate center points)
    {'Name': 'Hida Mountains', 'Japanese': '飛騨山脈', 'Type': 'range', 'Lat': 36.3500, 'Lon': 137.6500, 'Elev': 3000, 'Prefecture': 'Nagano;Gifu;Toyama'},
    {'Name': 'Akaishi Mountains', 'Japanese': '赤石山脈', 'Type': 'range', 'Lat': 35.6500, 'Lon': 138.2000, 'Elev': 3000, 'Prefecture': 'Nagano;Shizuoka;Yamanashi'},
    {'Name': 'Kiso Mountains', 'Japanese': '木曽山脈', 'Type': 'range', 'Lat': 35.8000, 'Lon': 137.8000, 'Elev': 2900, 'Prefecture': 'Nagano'},
    {'Name': 'Ou Mountains', 'Japanese': '奥羽山脈', 'Type': 'range', 'Lat': 39.5000, 'Lon': 140.5000, 'Elev': 2000, 'Prefecture': 'Aomori;Iwate;Miyagi;Akita;Yamagata;Fukushima'},
    {'Name': 'Dewa Sanzan', 'Japanese': '出羽三山', 'Type': 'range', 'Lat': 38.5500, 'Lon': 140.0000, 'Elev': 1984, 'Prefecture': 'Yamagata'},
    {'Name': 'Kii Mountains', 'Japanese': '紀伊山地', 'Type': 'range', 'Lat': 34.0000, 'Lon': 135.8000, 'Elev': 1915, 'Prefecture': 'Nara;Wakayama;Mie'},
    {'Name': 'Yoshino Mountains', 'Japanese': '吉野山', 'Type': 'range', 'Lat': 34.3667, 'Lon': 135.8667, 'Elev': 858, 'Prefecture': 'Nara'},
    {'Name': 'Shikoku Mountains', 'Japanese': '四国山地', 'Type': 'range', 'Lat': 33.7500, 'Lon': 133.5000, 'Elev': 1982, 'Prefecture': 'Tokushima;Kochi;Ehime'},
    {'Name': 'Shirakami Mountains', 'Japanese': '白神山地', 'Type': 'range', 'Lat': 40.4833, 'Lon': 140.1500, 'Elev': 1250, 'Prefecture': 'Aomori;Akita'},
    {'Name': 'Kitakami Mountains', 'Japanese': '北上山地', 'Type': 'range', 'Lat': 39.5000, 'Lon': 141.5000, 'Elev': 1917, 'Prefecture': 'Iwate;Miyagi'},
    {'Name': 'Tanzawa Mountains', 'Japanese': '丹沢山地', 'Type': 'range', 'Lat': 35.4833, 'Lon': 139.1500, 'Elev': 1673, 'Prefecture': 'Kanagawa'},
    {'Name': 'Yatsugatake Mountains', 'Japanese': '八ヶ岳連峰', 'Type': 'range', 'Lat': 35.9733, 'Lon': 138.3558, 'Elev': 2899, 'Prefecture': 'Nagano;Yamanashi'},
    {'Name': 'Misaka Mountains', 'Japanese': '御坂山地', 'Type': 'range', 'Lat': 35.5500, 'Lon': 138.7500, 'Elev': 1787, 'Prefecture': 'Yamanashi'},
    {'Name': 'Suzuka Mountains', 'Japanese': '鈴鹿山脈', 'Type': 'range', 'Lat': 35.0500, 'Lon': 136.4000, 'Elev': 1247, 'Prefecture': 'Mie;Shiga'},
]

# Read existing mountains metadata
existing = []
with open('mountains.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing.append(row)

# Add missing mountains
for m in missing_mountains:
    existing.append({
        'Name': m['Name'],
        'Japanese Name': m['Japanese'],
        'Prefecture': m['Prefecture'],
        'Elevation': m['Elev'],
        'Mountain Range': 'Range' if m['Type'] == 'range' else 'Standalone'
    })
    print(f"+ {m['Name']} ({m['Japanese']})")

# Write updated metadata
with open('mountains.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Prefecture', 'Elevation', 'Mountain Range']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(existing)

print(f"\n✓ Updated mountains.csv: {len(existing)} mountains")

# Read existing mountains geo
existing_geo = []
with open('mountains_geo.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        existing_geo.append(row)

# Add missing mountains geo
for m in missing_mountains:
    existing_geo.append({
        'Name': m['Name'],
        'Latitude': m['Lat'],
        'Longitude': m['Lon'],
        'Elevation': m['Elev']
    })

# Write updated geo
with open('mountains_geo.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Latitude', 'Longitude', 'Elevation']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(existing_geo)

print(f"✓ Updated mountains_geo.csv: {len(existing_geo)} mountains")
