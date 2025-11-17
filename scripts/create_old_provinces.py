#!/usr/bin/env python3
"""
Create old provinces geometry by mapping to modern prefectures.
This is an approximation since historical boundaries don't match exactly.
"""

import csv
from collections import defaultdict

# Mapping of old provinces to modern prefectures
# Format: old_province_name -> list of prefecture names (from prefectures_geo.csv)
PROVINCE_TO_PREFECTURE = {
    # Kinai Region (5 provinces around Kyoto/Osaka)
    'Yamato': ['Nara Ken'],
    'Yamashiro': ['Kyoto Fu'],  # Southern part, but we'll use whole Kyoto
    'Settsu': ['Osaka Fu'],  # Osaka + parts of Hyogo
    'Kawachi': ['Osaka Fu'],  # Eastern Osaka (duplicate, will merge)
    'Izumi': ['Osaka Fu'],  # Southern Osaka (duplicate, will merge)

    # Kanto Region
    'Musashi': ['Tokyo To', 'Saitama Ken'],  # Tokyo + Saitama + part of Kanagawa
    'Sagami': ['Kanagawa Ken'],
    'Awa': ['Chiba Ken'],  # Southern Chiba
    'Kazusa': ['Chiba Ken'],  # Central Chiba
    'Shimosa': ['Chiba Ken'],  # Northern Chiba
    'Hitachi': ['Ibaraki Ken'],
    'Shimotsuke': ['Tochigi Ken'],
    'Kozuke': ['Gunma Ken'],

    # Tokaido Region
    'Kai': ['Yamanashi Ken'],
    'Izu': ['Shizuoka Ken'],  # Eastern Shizuoka
    'Suruga': ['Shizuoka Ken'],  # Central Shizuoka
    'Totomi': ['Shizuoka Ken'],  # Western Shizuoka
    'Mikawa': ['Aichi Ken'],  # Eastern Aichi
    'Owari': ['Aichi Ken'],  # Western Aichi
    'Ise': ['Mie Ken'],  # Northern Mie
    'Shima': ['Mie Ken'],  # Eastern Mie
    'Iga': ['Mie Ken'],  # Western Mie

    # Hokuriku Region
    'Echizen': ['Fukui Ken'],  # Northern Fukui
    'Echigo': ['Niigata Ken'],
    'Etchu': ['Toyama Ken'],
    'Noto': ['Ishikawa Ken'],  # Northern Ishikawa
    'Kaga': ['Ishikawa Ken'],  # Southern Ishikawa

    # Tosando Region (Central mountains)
    'Shinano': ['Nagano Ken'],
    'Hida': ['Gifu Ken'],  # Northern Gifu
    'Mino': ['Gifu Ken'],  # Southern Gifu

    # Kinai/Tokaido
    'Omi': ['Shiga Ken'],
    'Wakasa': ['Fukui Ken'],  # Southern Fukui

    # San'indo/San'yo (Western Honshu)
    'Tango': ['Kyoto Fu'],  # Northern Kyoto
    'Tajima': ['Hyogo Ken'],  # Northern Hyogo
    'Tamba': ['Hyogo Ken'],  # Central Hyogo
    'Harima': ['Hyogo Ken'],  # Southern Hyogo
    'Inaba': ['Tottori Ken'],  # Eastern Tottori
    'Hoki': ['Tottori Ken'],  # Western Tottori
    'Izumo': ['Shimane Ken'],  # Eastern Shimane
    'Iwami': ['Shimane Ken'],  # Western Shimane
    'Oki': ['Shimane Ken'],  # Oki Islands
    'Mimasaka': ['Okayama Ken'],  # Northern Okayama
    'Bizen': ['Okayama Ken'],  # Southern Okayama
    'Bitchu': ['Okayama Ken'],  # Western Okayama
    'Bingo': ['Hiroshima Ken'],  # Eastern Hiroshima
    'Aki': ['Hiroshima Ken'],  # Western Hiroshima
    'Suo': ['Yamaguchi Ken'],  # Eastern Yamaguchi
    'Nagato': ['Yamaguchi Ken'],  # Western Yamaguchi

    # Shikoku
    'Awa': ['Tokushima Ken'],
    'Sanuki': ['Kagawa Ken'],
    'Iyo': ['Ehime Ken'],
    'Tosa': ['Kochi Ken'],

    # Kyushu
    'Chikuzen': ['Fukuoka Ken'],  # Northern Fukuoka
    'Chikugo': ['Fukuoka Ken'],  # Southern Fukuoka
    'Buzen': ['Fukuoka Ken', 'Oita Ken'],  # Eastern Fukuoka + Northern Oita
    'Bungo': ['Oita Ken'],
    'Hizen': ['Saga Ken', 'Nagasaki Ken'],
    'Higo': ['Kumamoto Ken'],
    'Hyuga': ['Miyazaki Ken'],
    'Osumi': ['Kagoshima Ken'],  # Eastern Kagoshima
    'Satsuma': ['Kagoshima Ken'],  # Western Kagoshima
}

def load_prefecture_geometry():
    """Load prefecture geometry from CSV."""
    prefectures = {}

    with open('prefectures_geo.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name']
            prefectures[name] = row

    return prefectures

def merge_coordinates(coord_strings):
    """Merge multiple coordinate strings into one (simple concatenation for now)."""
    if len(coord_strings) == 1:
        return coord_strings[0]

    # For provinces spanning multiple prefectures, use the first prefecture
    # This is a simplification - ideally we'd merge the polygons properly
    return coord_strings[0]

def create_old_provinces_geometry():
    """Create old provinces geometry file."""
    print("Loading prefecture geometry...")
    prefectures = load_prefecture_geometry()

    print(f"Loaded {len(prefectures)} prefectures")

    # Group provinces that share prefectures
    old_provinces = {}

    for province, pref_list in PROVINCE_TO_PREFECTURE.items():
        coords_list = []
        japanese_name = ''

        for pref_name in pref_list:
            if pref_name in prefectures:
                coords_list.append(prefectures[pref_name]['Coordinates'])
                if not japanese_name:
                    japanese_name = prefectures[pref_name].get('Japanese Name', '')

        if coords_list:
            old_provinces[province] = {
                'coordinates': merge_coordinates(coords_list),
                'japanese_name': japanese_name,
                'modern_prefecture': ', '.join(pref_list)
            }

    # Write to CSV
    print(f"\nCreating old_provinces_geo.csv with {len(old_provinces)} provinces...")

    with open('old_provinces_geo.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Japanese Name', 'Modern Prefecture', 'Coordinates'])

        for province, data in sorted(old_provinces.items()):
            writer.writerow([
                province,
                data['japanese_name'],
                data['modern_prefecture'],
                data['coordinates']
            ])
            print(f"  {province} -> {data['modern_prefecture']}")

    print(f"\n✓ Created old_provinces_geo.csv with {len(old_provinces)} provinces")
    print("\nNote: These are approximations based on modern prefecture boundaries.")
    print("Historical province boundaries were often different from current prefectures.")

if __name__ == '__main__':
    create_old_provinces_geometry()
