#!/usr/bin/env python3
"""
Add new sake rice varieties to sake_rice.csv - all importance level 2
"""

import csv

# New varieties with researched data
new_varieties = [
    # Akita
    {
        'Name': 'Gin no Sei',
        'Japanese Name': '吟の精',
        'Prefecture': 'Akita',
        'Parents': 'Akikei No. 53 x Aikawa No. 1',
        'Year': '1990/1993',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Registered 1993, developed 1990. Created to address Miyama Nishiki\'s unsuitability for ginjo. Larger than Miyama Nishiki with better polishing characteristics. Does not break easily, easier to handle in brewing. Considered rare, almost endangered.'
    },
    {
        'Name': 'Ichihozumi',
        'Japanese Name': '一穂積',
        'Prefecture': 'Akita',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Akita Prefecture sake rice variety known for producing clean, refined sake.'
    },
    {
        'Name': 'Hyakuden',
        'Japanese Name': '百田',
        'Prefecture': 'Akita',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Akita Prefecture variety used for quality sake production.'
    },
    # Yamagata
    {
        'Name': 'Kissui',
        'Japanese Name': '亀粋',
        'Prefecture': 'Yamagata',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Yamagata Prefecture sake rice variety.'
    },
    # Fukushima
    {
        'Name': 'Fuku no Ka',
        'Japanese Name': '福乃香',
        'Prefecture': 'Fukushima',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Fukushima Prefecture sake rice. Name means "Fragrance of Fortune".'
    },
    # Ibaraki
    {
        'Name': 'Hitachi Nishiki',
        'Japanese Name': '常陸錦',
        'Prefecture': 'Ibaraki',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Ibaraki Prefecture sake rice variety.'
    },
    # Tochigi
    {
        'Name': 'Tochigi No. 14',
        'Japanese Name': '栃木14号',
        'Prefecture': 'Tochigi',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Tochigi Prefecture experimental variety for sake brewing.'
    },
    # Niigata
    {
        'Name': 'Ipponjime',
        'Japanese Name': '一本〆',
        'Prefecture': 'Niigata',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Niigata Prefecture sake rice developed for cold climate brewing.'
    },
    {
        'Name': 'Kikusui',
        'Japanese Name': '菊水',
        'Prefecture': 'Niigata',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Historic Niigata variety, ancestor of Gohyakumangoku. Important in the lineage of modern sake rice.'
    },
    {
        'Name': 'Shira Fuji',
        'Japanese Name': '白藤',
        'Prefecture': 'Niigata',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Niigata Prefecture sake rice variety.'
    },
    {
        'Name': 'Hokuriku No. 14',
        'Japanese Name': '北陸14号',
        'Prefecture': 'Niigata',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Hokuriku region experimental variety used in Niigata.'
    },
    # Ishikawa
    {
        'Name': 'Ishikawa Mon',
        'Japanese Name': '石川門',
        'Prefecture': 'Ishikawa',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Ishikawa Prefecture sake rice variety.'
    },
    # Fukui
    {
        'Name': 'Oku Honmare',
        'Japanese Name': '奥の誉',
        'Prefecture': 'Fukui',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Fukui Prefecture sake rice variety.'
    },
    # Yamanashi
    {
        'Name': 'Yume Sansui',
        'Japanese Name': '夢山水',
        'Prefecture': 'Yamanashi',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Yamanashi Prefecture sake rice. Name means "Dream Mountain Water".'
    },
    # Nagano
    {
        'Name': 'Sankei Nishiki',
        'Japanese Name': '山恵錦',
        'Prefecture': 'Nagano',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Nagano Prefecture sake rice variety.'
    },
    {
        'Name': 'Takane Nishiki',
        'Japanese Name': '高嶺錦',
        'Prefecture': 'Nagano',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Nagano Prefecture variety. Parent of Miyama Nishiki, which was created through gamma ray mutation of Takane Nishiki.'
    },
    {
        'Name': 'Shirakaba Nishiki',
        'Japanese Name': '白樺錦',
        'Prefecture': 'Nagano',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Nagano Prefecture sake rice. Name means "White Birch Brocade".'
    },
    # Nara
    {
        'Name': 'Akitsu Ho',
        'Japanese Name': '秋津穂',
        'Prefecture': 'Nara',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Nara Prefecture sake rice variety.'
    },
    # Ehime
    {
        'Name': 'Shizuku Hime',
        'Japanese Name': 'しずく媛',
        'Prefecture': 'Ehime',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Ehime Prefecture sake rice. Name means "Droplet Princess".'
    },
    # Kochi
    {
        'Name': 'Tosa Uhara',
        'Japanese Name': '土佐宇原',
        'Prefecture': 'Kochi',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Kochi Prefecture sake rice variety.'
    },
    {
        'Name': 'Tosa Nishiki',
        'Japanese Name': '土佐錦',
        'Prefecture': 'Kochi',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Kochi Prefecture sake rice variety.'
    },
    {
        'Name': 'Kaze Naruko',
        'Japanese Name': '風鳴子',
        'Prefecture': 'Kochi',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Kochi Prefecture sake rice. Name means "Wind Chime".'
    },
    # Fukuoka
    {
        'Name': 'Jugemu',
        'Japanese Name': '寿限無',
        'Prefecture': 'Fukuoka',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Fukuoka Prefecture sake rice. Named after a famous Japanese folktale character.'
    },
    {
        'Name': 'Saikai No. 134',
        'Japanese Name': '西海134号',
        'Prefecture': 'Fukuoka',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Fukuoka Prefecture experimental variety for sake brewing.'
    },
    {
        'Name': 'Yume Ikon',
        'Japanese Name': '夢一献',
        'Prefecture': 'Fukuoka',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Fukuoka Prefecture sake rice. Name means "Dream Offering".'
    },
    # Saga
    {
        'Name': 'Saga no Hana',
        'Japanese Name': '佐賀の華',
        'Prefecture': 'Saga',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Saga Prefecture sake rice. Name means "Flower of Saga".'
    },
    {
        'Name': 'Reihou',
        'Japanese Name': '麗峰',
        'Prefecture': 'Saga',
        'Parents': '',
        'Year': '',
        'Production_Tonnes': '',
        'Importance': '2',
        'Notes': 'Saga Prefecture sake rice. Name means "Beautiful Peak".'
    },
]

# Read existing CSV
existing_varieties = []
with open('sake_rice.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        existing_varieties.append(row)

# Check for duplicates and add new varieties
existing_names = {v['Name'] for v in existing_varieties}
added_count = 0

for new_var in new_varieties:
    if new_var['Name'] not in existing_names:
        existing_varieties.append(new_var)
        added_count += 1
        print(f"✓ Added: {new_var['Name']} ({new_var['Japanese Name']}) - {new_var['Prefecture']}")
    else:
        print(f"  Skipped (already exists): {new_var['Name']}")

# Write updated CSV
with open('sake_rice.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(existing_varieties)

print(f"\n✓ Added {added_count} new sake rice varieties")
print(f"✓ Total varieties: {len(existing_varieties)}")
