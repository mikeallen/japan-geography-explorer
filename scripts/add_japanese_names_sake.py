#!/usr/bin/env python3
"""
Add Japanese names to sake rice CSV file.
"""

import csv

# Japanese names for sake rice varieties
japanese_names = {
    'Yamadanishiki': '山田錦',
    'Gohyakumangoku': '五百万石',
    'Miyama Nishiki': '美山錦',
    'Omachi': '雄町',
    'Dewasansan': '出羽燦々',
    'Dewa no sato': '出羽の里',
    'Hattan Nishiki': '八反錦',
    'Akita Sake Komachi': '秋田酒こまち',
    'Ginpu': '吟風',
    'Kame no O': '亀の尾',
    'Iwai': '祝',
    'Hanafubuki': '華吹雪',
    'Ginginga': '吟ぎんが',
    'Kura no Hana': '蔵の華',
    'Sasa nishiki': 'ササニシキ',
    'Yume no Kaori': '夢の香',
    'Hitogokochi': 'ひとごこち',
    'Tamasakae': '玉栄',
    'Aiyama': '愛山',
    'Hida Honmare': '飛騨誉',
    'Koshi Tanrei': '越淡麗',
    'Wataribune': '渡船',
    'Shiga Wataribune #6': '渡船6号',
    '(Shin) Yamada Ho': '(新)山田穂',
    'Shinriki': '神力',
    'Hattan-so': '八反草',
    'Senbon nishiki': '千本錦',
    'Yukimegami': '雪女神',
    'Hyakumangoku no Shiro': '百万石乃白',
    'Homare Fuji': '誉富士',
    'Misato Nishiki': '美郷錦',
    'Gin no Sato': '吟のさと',
    'Koshi Hikari': 'コシヒカリ',
    'Oseto': '雄山錦',
    'Goriki': '五力',
    'Mai kaze': '舞風',
    'Gin Otome': '吟おとめ',
    'Sake Mushashi': '酒武蔵',
    'Oyama nishiki': '夢山水',
    'Kinmon nishiki': '金紋錦',
    'Tsuyubakaze': '露葉風',
    'Saka honmare': '五百万石',
    'Wakamizu': '若水',
    'Yume Sansui': '夢山水',
    'Yume Ginga': '夢吟香',
    'Kairyo Omachi': '改良雄町',
    'Yume Sasara': '夢ささら',
    'Fusa no mai': 'ふさの舞',
    'Kan no mai': '神の舞',
    'Saito no Shizuku': '西都の雫',
    'Matsuyama Mitsui': '松山三井',
    'Suisei': '彗星',
    'Kita shizuku': 'きたしずく',
    'Hanaomoi': '華想い',
    'Yuinoka': '結の香',
    'yuki hotaka': '雪ほたか',
    'Tomi no kaori': '富の香',
    'Hana echizen': '華越前',
    'koshi no shizuku': '越の雫',
    'Shiragiku': '白菊',
    'kami no ho': '神の穂',
    'ise nishiki': '伊勢錦',
    'Yuminare ho': '弓成穂',
    'Ukon nishiki': '右近錦',
    'Gin fukubi': '吟吹雪',
    'Saka nishiki': '佐香錦',
    'Kokurio miyako': '国京',
    'Sanuki Yoimai': 'さぬきよいまい',
    'Oidemai': 'おいでまい',
    'Gin no Yume': '吟の夢',
    'Hana nishiki': '華錦'
}

# Read current CSV
rows = []
with open('sake_rice.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

    # Add Japanese Name after Name if not already there
    if 'Japanese Name' not in fieldnames:
        new_fieldnames = ['Name', 'Japanese Name'] + [f for f in fieldnames if f != 'Name']
    else:
        new_fieldnames = fieldnames

    for row in reader:
        # Add Japanese name if available
        if row['Name'] in japanese_names:
            row['Japanese Name'] = japanese_names[row['Name']]
        elif 'Japanese Name' not in row:
            row['Japanese Name'] = ''
        rows.append(row)

# Write updated CSV
with open('sake_rice.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=new_fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✓ Updated sake_rice.csv with Japanese names")
print(f"  Added {sum(1 for r in rows if r.get('Japanese Name'))} Japanese names")
print(f"  Total varieties: {len(rows)}")
