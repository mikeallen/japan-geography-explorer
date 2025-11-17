#!/usr/bin/env python3
"""
Enhance prefecture data with region kanji and old province mappings.
"""

import csv

# Region kanji mapping
region_kanji = {
    'Hokkaido': '北海道',
    'Tohoku': '東北',
    'Kanto': '関東',
    'Chubu': '中部',
    'Kansai': '関西',
    'Chugoku': '中国',
    'Shikoku': '四国',
    'Kyushu': '九州'
}

# Load old provinces data to create reverse mapping (prefecture -> provinces)
pref_to_provinces = {}
with open('old_provinces.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        province_name = row['Name']
        province_japanese = row['Japanese Name']
        prefectures_str = row['Prefectures']

        # Split by semicolon to get list of prefectures
        prefecture_list = [p.strip() for p in prefectures_str.split(';')]

        for pref in prefecture_list:
            # Normalize prefecture name
            pref_normalized = pref.strip()

            if pref_normalized not in pref_to_provinces:
                pref_to_provinces[pref_normalized] = []

            pref_to_provinces[pref_normalized].append({
                'name': province_name,
                'japanese': province_japanese
            })

print(f"Loaded old province mappings for {len(pref_to_provinces)} prefectures")

# Load and enhance prefecture data
prefectures = []
with open('prefectures.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pref_name = row['Name']
        region = row['Region']

        # Add region kanji
        row['Region Kanji'] = region_kanji.get(region, region)

        # Find old provinces for this prefecture
        old_provinces = pref_to_provinces.get(pref_name, [])

        # Format: "Province1 (Japanese1); Province2 (Japanese2)"
        if old_provinces:
            province_str = '; '.join([f"{p['name']} ({p['japanese']})" for p in old_provinces])
            row['Old Provinces'] = province_str
        else:
            row['Old Provinces'] = ''

        prefectures.append(row)
        print(f"{pref_name}: {row['Region']} ({row['Region Kanji']}) - {len(old_provinces)} old provinces")

# Write enhanced data
with open('prefectures.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Region', 'Region Kanji', 'Old Provinces', 'Population', 'Area']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(prefectures)

print(f"\n✓ Enhanced prefectures.csv with region kanji and old province mappings")
print(f"✓ Updated {len(prefectures)} prefectures")
