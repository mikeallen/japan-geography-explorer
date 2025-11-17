#!/usr/bin/env python3
"""
Create complete old provinces data with modern prefecture mappings.
Based on the historical map and research on Japanese provinces (kuni).
"""

import csv

# Complete list of all Japanese provinces with modern prefecture equivalents
provinces_data = [
    # Kinai Region (5 provinces)
    {'Name': 'Yamato', 'Japanese': '大和国', 'Prefectures': 'Nara', 'Region': 'Kinai'},
    {'Name': 'Yamashiro', 'Japanese': '山城国', 'Prefectures': 'Kyoto', 'Region': 'Kinai'},
    {'Name': 'Settsu', 'Japanese': '摂津国', 'Prefectures': 'Osaka;Hyogo', 'Region': 'Kinai'},
    {'Name': 'Kawachi', 'Japanese': '河内国', 'Prefectures': 'Osaka', 'Region': 'Kinai'},
    {'Name': 'Izumi', 'Japanese': '和泉国', 'Prefectures': 'Osaka', 'Region': 'Kinai'},

    # Tokaido Region (15 provinces)
    {'Name': 'Iga', 'Japanese': '伊賀国', 'Prefectures': 'Mie', 'Region': 'Tokaido'},
    {'Name': 'Ise', 'Japanese': '伊勢国', 'Prefectures': 'Mie', 'Region': 'Tokaido'},
    {'Name': 'Shima', 'Japanese': '志摩国', 'Prefectures': 'Mie', 'Region': 'Tokaido'},
    {'Name': 'Owari', 'Japanese': '尾張国', 'Prefectures': 'Aichi', 'Region': 'Tokaido'},
    {'Name': 'Mikawa', 'Japanese': '三河国', 'Prefectures': 'Aichi', 'Region': 'Tokaido'},
    {'Name': 'Totomi', 'Japanese': '遠江国', 'Prefectures': 'Shizuoka', 'Region': 'Tokaido'},
    {'Name': 'Suruga', 'Japanese': '駿河国', 'Prefectures': 'Shizuoka', 'Region': 'Tokaido'},
    {'Name': 'Izu', 'Japanese': '伊豆国', 'Prefectures': 'Shizuoka', 'Region': 'Tokaido'},
    {'Name': 'Kai', 'Japanese': '甲斐国', 'Prefectures': 'Yamanashi', 'Region': 'Tokaido'},
    {'Name': 'Sagami', 'Japanese': '相模国', 'Prefectures': 'Kanagawa', 'Region': 'Tokaido'},
    {'Name': 'Musashi', 'Japanese': '武蔵国', 'Prefectures': 'Tokyo;Saitama;Kanagawa', 'Region': 'Tokaido'},
    {'Name': 'Awa', 'Japanese': '安房国', 'Prefectures': 'Chiba', 'Region': 'Tokaido'},
    {'Name': 'Kazusa', 'Japanese': '上総国', 'Prefectures': 'Chiba', 'Region': 'Tokaido'},
    {'Name': 'Shimosa', 'Japanese': '下総国', 'Prefectures': 'Chiba;Ibaraki', 'Region': 'Tokaido'},
    {'Name': 'Hitachi', 'Japanese': '常陸国', 'Prefectures': 'Ibaraki', 'Region': 'Tokaido'},

    # Tosando Region (8 provinces)
    {'Name': 'Omi', 'Japanese': '近江国', 'Prefectures': 'Shiga', 'Region': 'Tosando'},
    {'Name': 'Mino', 'Japanese': '美濃国', 'Prefectures': 'Gifu', 'Region': 'Tosando'},
    {'Name': 'Hida', 'Japanese': '飛騨国', 'Prefectures': 'Gifu', 'Region': 'Tosando'},
    {'Name': 'Shinano', 'Japanese': '信濃国', 'Prefectures': 'Nagano', 'Region': 'Tosando'},
    {'Name': 'Kozuke', 'Japanese': '上野国', 'Prefectures': 'Gunma', 'Region': 'Tosando'},
    {'Name': 'Shimotsuke', 'Japanese': '下野国', 'Prefectures': 'Tochigi', 'Region': 'Tosando'},
    {'Name': 'Mutsu', 'Japanese': '陸奥国', 'Prefectures': 'Aomori;Iwate;Miyagi;Fukushima', 'Region': 'Tosando'},
    {'Name': 'Dewa', 'Japanese': '出羽国', 'Prefectures': 'Akita;Yamagata', 'Region': 'Tosando'},

    # Hokurikudo Region (7 provinces)
    {'Name': 'Wakasa', 'Japanese': '若狭国', 'Prefectures': 'Fukui', 'Region': 'Hokurikudo'},
    {'Name': 'Echizen', 'Japanese': '越前国', 'Prefectures': 'Fukui', 'Region': 'Hokurikudo'},
    {'Name': 'Kaga', 'Japanese': '加賀国', 'Prefectures': 'Ishikawa', 'Region': 'Hokurikudo'},
    {'Name': 'Noto', 'Japanese': '能登国', 'Prefectures': 'Ishikawa', 'Region': 'Hokurikudo'},
    {'Name': 'Etchu', 'Japanese': '越中国', 'Prefectures': 'Toyama', 'Region': 'Hokurikudo'},
    {'Name': 'Echigo', 'Japanese': '越後国', 'Prefectures': 'Niigata', 'Region': 'Hokurikudo'},
    {'Name': 'Sado', 'Japanese': '佐渡国', 'Prefectures': 'Niigata', 'Region': 'Hokurikudo'},

    # San'indo Region (8 provinces)
    {'Name': 'Tango', 'Japanese': '丹後国', 'Prefectures': 'Kyoto', 'Region': 'San\'indo'},
    {'Name': 'Tamba', 'Japanese': '丹波国', 'Prefectures': 'Kyoto;Hyogo', 'Region': 'San\'indo'},
    {'Name': 'Tajima', 'Japanese': '但馬国', 'Prefectures': 'Hyogo', 'Region': 'San\'indo'},
    {'Name': 'Inaba', 'Japanese': '因幡国', 'Prefectures': 'Tottori', 'Region': 'San\'indo'},
    {'Name': 'Hoki', 'Japanese': '伯耆国', 'Prefectures': 'Tottori', 'Region': 'San\'indo'},
    {'Name': 'Izumo', 'Japanese': '出雲国', 'Prefectures': 'Shimane', 'Region': 'San\'indo'},
    {'Name': 'Iwami', 'Japanese': '石見国', 'Prefectures': 'Shimane', 'Region': 'San\'indo'},
    {'Name': 'Oki', 'Japanese': '隠岐国', 'Prefectures': 'Shimane', 'Region': 'San\'indo'},

    # San'yodo Region (8 provinces)
    {'Name': 'Harima', 'Japanese': '播磨国', 'Prefectures': 'Hyogo', 'Region': 'San\'yodo'},
    {'Name': 'Mimasaka', 'Japanese': '美作国', 'Prefectures': 'Okayama', 'Region': 'San\'yodo'},
    {'Name': 'Bizen', 'Japanese': '備前国', 'Prefectures': 'Okayama', 'Region': 'San\'yodo'},
    {'Name': 'Bitchu', 'Japanese': '備中国', 'Prefectures': 'Okayama', 'Region': 'San\'yodo'},
    {'Name': 'Bingo', 'Japanese': '備後国', 'Prefectures': 'Hiroshima', 'Region': 'San\'yodo'},
    {'Name': 'Aki', 'Japanese': '安芸国', 'Prefectures': 'Hiroshima', 'Region': 'San\'yodo'},
    {'Name': 'Suo', 'Japanese': '周防国', 'Prefectures': 'Yamaguchi', 'Region': 'San\'yodo'},
    {'Name': 'Nagato', 'Japanese': '長門国', 'Prefectures': 'Yamaguchi', 'Region': 'San\'yodo'},

    # Nankaido Region (6 provinces)
    {'Name': 'Kii', 'Japanese': '紀伊国', 'Prefectures': 'Wakayama;Mie', 'Region': 'Nankaido'},
    {'Name': 'Awaji', 'Japanese': '淡路国', 'Prefectures': 'Hyogo', 'Region': 'Nankaido'},
    {'Name': 'Awa', 'Japanese': '阿波国', 'Prefectures': 'Tokushima', 'Region': 'Nankaido'},
    {'Name': 'Sanuki', 'Japanese': '讃岐国', 'Prefectures': 'Kagawa', 'Region': 'Nankaido'},
    {'Name': 'Iyo', 'Japanese': '伊予国', 'Prefectures': 'Ehime', 'Region': 'Nankaido'},
    {'Name': 'Tosa', 'Japanese': '土佐国', 'Prefectures': 'Kochi', 'Region': 'Nankaido'},

    # Saikaido Region (11 provinces)
    {'Name': 'Chikuzen', 'Japanese': '筑前国', 'Prefectures': 'Fukuoka', 'Region': 'Saikaido'},
    {'Name': 'Chikugo', 'Japanese': '筑後国', 'Prefectures': 'Fukuoka', 'Region': 'Saikaido'},
    {'Name': 'Buzen', 'Japanese': '豊前国', 'Prefectures': 'Fukuoka;Oita', 'Region': 'Saikaido'},
    {'Name': 'Bungo', 'Japanese': '豊後国', 'Prefectures': 'Oita', 'Region': 'Saikaido'},
    {'Name': 'Hizen', 'Japanese': '肥前国', 'Prefectures': 'Saga;Nagasaki', 'Region': 'Saikaido'},
    {'Name': 'Higo', 'Japanese': '肥後国', 'Prefectures': 'Kumamoto', 'Region': 'Saikaido'},
    {'Name': 'Hyuga', 'Japanese': '日向国', 'Prefectures': 'Miyazaki', 'Region': 'Saikaido'},
    {'Name': 'Osumi', 'Japanese': '大隅国', 'Prefectures': 'Kagoshima', 'Region': 'Saikaido'},
    {'Name': 'Satsuma', 'Japanese': '薩摩国', 'Prefectures': 'Kagoshima', 'Region': 'Saikaido'},
    {'Name': 'Iki', 'Japanese': '壱岐国', 'Prefectures': 'Nagasaki', 'Region': 'Saikaido'},
    {'Name': 'Tsushima', 'Japanese': '対馬国', 'Prefectures': 'Nagasaki', 'Region': 'Saikaido'},

    # Hokkaido (added later, not part of original provinces)
    {'Name': 'Ezo', 'Japanese': '蝦夷地', 'Prefectures': 'Hokkaido', 'Region': 'Hokkaido'},
]

print(f"Creating data for {len(provinces_data)} provinces...")

# Write the CSV file
with open('old_provinces.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Prefectures', 'Region']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for province in provinces_data:
        writer.writerow({
            'Name': province['Name'],
            'Japanese Name': province['Japanese'],
            'Prefectures': province['Prefectures'],
            'Region': province['Region']
        })
        print(f"+ {province['Name']} ({province['Japanese']}) → {province['Prefectures']}")

print(f"\n✓ Created old_provinces.csv with {len(provinces_data)} provinces")
print("\nBreakdown by region:")
regions = {}
for p in provinces_data:
    region = p['Region']
    if region not in regions:
        regions[region] = 0
    regions[region] += 1

for region, count in sorted(regions.items()):
    print(f"  {region}: {count} provinces")
