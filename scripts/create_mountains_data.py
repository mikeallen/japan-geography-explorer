#!/usr/bin/env python3
"""
Create mountains data with known coordinates.
Data sourced from Wikipedia and official Japanese geographic sources.
"""

import csv

# Mountains data with known coordinates
mountains_data = [
    # Individual Mountains
    {'Name': 'Fuji', 'Japanese': '富士山', 'Type': 'mountain', 'Lat': 35.3606, 'Lon': 138.7274, 'Elev': 3776, 'Prefecture': 'Shizuoka/Yamanashi'},
    {'Name': 'Kitadake', 'Japanese': '北岳', 'Type': 'mountain', 'Lat': 35.6744, 'Lon': 138.2372, 'Elev': 3193, 'Prefecture': 'Yamanashi'},
    {'Name': 'Okuhotaka', 'Japanese': '奥穂高岳', 'Type': 'mountain', 'Lat': 36.2897, 'Lon': 137.6472, 'Elev': 3190, 'Prefecture': 'Nagano/Gifu'},
    {'Name': 'Yari', 'Japanese': '槍ヶ岳', 'Type': 'mountain', 'Lat': 36.3392, 'Lon': 137.6447, 'Elev': 3180, 'Prefecture': 'Nagano'},
    {'Name': 'Tate', 'Japanese': '立山', 'Type': 'mountain', 'Lat': 36.5750, 'Lon': 137.6200, 'Elev': 3015, 'Prefecture': 'Toyama'},
    {'Name': 'Tsurugi', 'Japanese': '剱岳', 'Type': 'mountain', 'Lat': 36.6231, 'Lon': 137.6169, 'Elev': 2999, 'Prefecture': 'Toyama'},
    {'Name': 'Hotaka', 'Japanese': '穂高岳', 'Type': 'mountain', 'Lat': 36.2950, 'Lon': 137.6458, 'Elev': 3190, 'Prefecture': 'Nagano/Gifu'},
    {'Name': 'Yatsugatake', 'Japanese': '八ヶ岳', 'Type': 'mountain', 'Lat': 35.9733, 'Lon': 138.3558, 'Elev': 2899, 'Prefecture': 'Nagano/Yamanashi'},
    {'Name': 'Kita-Hotaka', 'Japanese': '北穂高岳', 'Type': 'mountain', 'Lat': 36.3069, 'Lon': 137.6581, 'Elev': 3106, 'Prefecture': 'Nagano/Gifu'},
    {'Name': 'Daikiretto', 'Japanese': '大キレット', 'Type': 'mountain', 'Lat': 36.3133, 'Lon': 137.6533, 'Elev': 2900, 'Prefecture': 'Nagano/Gifu'},
    {'Name': 'Hakusan', 'Japanese': '白山', 'Type': 'mountain', 'Lat': 36.1561, 'Lon': 136.7719, 'Elev': 2702, 'Prefecture': 'Ishikawa/Gifu'},
    {'Name': 'Norikura', 'Japanese': '乗鞍岳', 'Type': 'mountain', 'Lat': 36.1061, 'Lon': 137.5539, 'Elev': 3026, 'Prefecture': 'Nagano/Gifu'},
    {'Name': 'Ontake', 'Japanese': '御嶽山', 'Type': 'mountain', 'Lat': 35.8939, 'Lon': 137.4803, 'Elev': 3067, 'Prefecture': 'Nagano/Gifu'},
    {'Name': 'Asahi', 'Japanese': '朝日岳', 'Type': 'mountain', 'Lat': 36.5597, 'Lon': 137.6083, 'Elev': 2932, 'Prefecture': 'Toyama'},
    {'Name': 'Kaikomagatake', 'Japanese': '甲斐駒ヶ岳', 'Type': 'mountain', 'Lat': 35.7542, 'Lon': 138.2353, 'Elev': 2967, 'Prefecture': 'Yamanashi/Nagano'},
    {'Name': 'Aino', 'Japanese': '間ノ岳', 'Type': 'mountain', 'Lat': 35.6725, 'Lon': 138.2292, 'Elev': 3190, 'Prefecture': 'Yamanashi/Shizuoka'},
    {'Name': 'Chokai', 'Japanese': '鳥海山', 'Type': 'mountain', 'Lat': 39.0986, 'Lon': 140.0497, 'Elev': 2236, 'Prefecture': 'Yamagata/Akita'},
    {'Name': 'Bandai', 'Japanese': '磐梯山', 'Type': 'mountain', 'Lat': 37.6006, 'Lon': 140.0769, 'Elev': 1816, 'Prefecture': 'Fukushima'},
    {'Name': 'Adatara', 'Japanese': '安達太良山', 'Type': 'mountain', 'Lat': 37.6194, 'Lon': 140.2808, 'Elev': 1728, 'Prefecture': 'Fukushima'},
    {'Name': 'Tsukuba', 'Japanese': '筑波山', 'Type': 'mountain', 'Lat': 36.2256, 'Lon': 140.1053, 'Elev': 877, 'Prefecture': 'Ibaraki'},
    {'Name': 'Nantai', 'Japanese': '男体山', 'Type': 'mountain', 'Lat': 36.7606, 'Lon': 139.4925, 'Elev': 2486, 'Prefecture': 'Tochigi'},
    {'Name': 'Myoko', 'Japanese': '妙高山', 'Type': 'mountain', 'Lat': 36.8853, 'Lon': 138.1172, 'Elev': 2454, 'Prefecture': 'Niigata'},
    {'Name': 'Ishizuchi', 'Japanese': '石鎚山', 'Type': 'mountain', 'Lat': 33.7664, 'Lon': 133.1358, 'Elev': 1982, 'Prefecture': 'Ehime'},
    {'Name': 'Aso', 'Japanese': '阿蘇山', 'Type': 'mountain', 'Lat': 32.8847, 'Lon': 131.1042, 'Elev': 1592, 'Prefecture': 'Kumamoto'},
    {'Name': 'Akagi', 'Japanese': '赤城山', 'Type': 'mountain', 'Lat': 36.5456, 'Lon': 139.1942, 'Elev': 1828, 'Prefecture': 'Gunma'},
    {'Name': 'Haruna', 'Japanese': '榛名山', 'Type': 'mountain', 'Lat': 36.4775, 'Lon': 138.8522, 'Elev': 1449, 'Prefecture': 'Gunma'},
    {'Name': 'Myogi', 'Japanese': '妙義山', 'Type': 'mountain', 'Lat': 36.3114, 'Lon': 138.7675, 'Elev': 1104, 'Prefecture': 'Gunma'},
    {'Name': 'Kobushi', 'Japanese': '甲武信ヶ岳', 'Type': 'mountain', 'Lat': 35.9136, 'Lon': 138.7264, 'Elev': 2475, 'Prefecture': 'Saitama/Nagano/Yamanashi'},
    {'Name': 'Kumotori', 'Japanese': '雲取山', 'Type': 'mountain', 'Lat': 35.8514, 'Lon': 138.9394, 'Elev': 2017, 'Prefecture': 'Tokyo/Saitama/Yamanashi'},
    {'Name': 'Ibuki', 'Japanese': '伊吹山', 'Type': 'mountain', 'Lat': 35.4217, 'Lon': 136.4081, 'Elev': 1377, 'Prefecture': 'Shiga/Gifu'},
    {'Name': 'Ikoma', 'Japanese': '生駒山', 'Type': 'mountain', 'Lat': 34.6797, 'Lon': 135.6806, 'Elev': 642, 'Prefecture': 'Osaka/Nara'},
    {'Name': 'Kongo', 'Japanese': '金剛山', 'Type': 'mountain', 'Lat': 34.4258, 'Lon': 135.6744, 'Elev': 1125, 'Prefecture': 'Osaka/Nara'},
    {'Name': 'Daisen', 'Japanese': '大山', 'Type': 'mountain', 'Lat': 35.3733, 'Lon': 133.5456, 'Elev': 1729, 'Prefecture': 'Tottori'},
    {'Name': 'Tsurugi-Shikoku', 'Japanese': '剣山', 'Type': 'mountain', 'Lat': 33.8722, 'Lon': 134.0928, 'Elev': 1955, 'Prefecture': 'Tokushima'},
    {'Name': 'Sakurajima', 'Japanese': '桜島', 'Type': 'mountain', 'Lat': 31.5858, 'Lon': 130.6572, 'Elev': 1117, 'Prefecture': 'Kagoshima'},
    {'Name': 'Kurikoma', 'Japanese': '栗駒山', 'Type': 'mountain', 'Lat': 38.9608, 'Lon': 140.7872, 'Elev': 1626, 'Prefecture': 'Miyagi/Iwate/Akita'},
    {'Name': 'Sefuri', 'Japanese': '脊振山', 'Type': 'mountain', 'Lat': 33.4464, 'Lon': 130.3664, 'Elev': 1055, 'Prefecture': 'Fukuoka/Saga'},
    {'Name': 'Taisetsu', 'Japanese': '大雪山', 'Type': 'mountain', 'Lat': 43.6608, 'Lon': 142.8544, 'Elev': 2291, 'Prefecture': 'Hokkaido'},
    {'Name': 'Hakkoda', 'Japanese': '八甲田山', 'Type': 'mountain', 'Lat': 40.6561, 'Lon': 140.8786, 'Elev': 1585, 'Prefecture': 'Aomori'},
    {'Name': 'Zao', 'Japanese': '蔵王山', 'Type': 'mountain', 'Lat': 38.1433, 'Lon': 140.4461, 'Elev': 1841, 'Prefecture': 'Yamagata/Miyagi'},
]

# Write to CSV
with open('mountains_new.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Japanese Name', 'Type', 'Latitude', 'Longitude', 'Elevation', 'Prefecture']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for m in mountains_data:
        writer.writerow({
            'Name': m['Name'],
            'Japanese Name': m['Japanese'],
            'Type': m['Type'],
            'Latitude': m['Lat'],
            'Longitude': m['Lon'],
            'Elevation': m['Elev'],
            'Prefecture': m['Prefecture']
        })

print(f"✓ Created mountains_new.csv with {len(mountains_data)} mountains")
