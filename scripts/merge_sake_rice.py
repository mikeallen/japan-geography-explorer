#!/usr/bin/env python3
"""
Merge sake rice data - keep all varieties from backup, add production/importance data.
"""

import csv

print("Loading backup data...")

# Load backup data (has all varieties)
backup_data = []
with open('sake_rice_backup.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Clean up the name (remove trailing spaces)
        row['Name'] = row['Name'].strip()
        backup_data.append(row)

print(f"Loaded {len(backup_data)} varieties from backup")

# Production data from research (tonnes per year)
production_data = {
    'Yamadanishiki': 22916,
    'Gohyakumangoku': 21000,
    'Miyama Nishiki': 6408,
    'Omachi': 2723,
    'Dewasansan': 1436,
    'Hanafubuki': 1044,
    'Hattan Nishiki': 900,
    'Akita Sake Komachi': 800,
    'Ginpu': 700,
    'Dewa no sato': 600,
    'Kame no O': 500,
    'Iwai': 400,
    'Ginginga': 350,
    'Kura no Hana': 320,
}

# Enhanced notes for key varieties
enhanced_notes = {
    'Yamadanishiki': 'Known as the "King of Sake Rice." A cross between Yamadaho and Tankan-wataribune developed in 1923, distributed 1936. Prized for its large uniform starch core (shinpaku). Used to produce premium highly aromatic sakes. Cannot grow above 300m. Tankan-wataribune also descended from Omachi. Accounts for 35% of all sake rice production in Japan.',
    'Gohyakumangoku': 'Second most cultivated sakamai. Produces clean crisp light sake with simple refreshing profile. Developed 1938 by crossing Kikusui (ancestor of Omachi) and Shin No. 200 (ancestor of Kame no O). Name from 1957 bumper crop yielding 5 million koku (Gohyakumangoku). Developed for Niigata\'s cold climate. Easy to make koji with lends itself to Echigo toji\'s tsuki haze koji creating sharp crisp light clean sake - foundation of Niigata\'s tanre karakuchi style. Large round shinpaku cannot be polished below 50% without cracking. Yoshikawa ward in southern Joetsu is largest cultivation area.',
    'Miyama Nishiki': 'Third most produced sake rice. Creates rich bold slightly earthy-flavored sake. Well-suited for winter brewing in colder climates. Miyama means Beautiful Mountain. Developed through gamma ray mutation of Takane Nishiki.',
    'Omachi': 'Considered heirloom variety dating to 19th century (discovered 1859). Creates complex rich sake with earthy herbal notes. Parent variety of many modern sake rices. Table rice variety also used for sake.',
    'Kame no O': 'Heirloom rice variety with strong distinct flavor profile. Discovered 1893. Revived in recent years for craft sake. Table rice variety.',
}

# Determine exclusive prefecture rices (only rice for that prefecture in dataset)
prefecture_counts = {}
for row in backup_data:
    pref = row['Prefecture'].strip()
    if pref:
        prefecture_counts[pref] = prefecture_counts.get(pref, 0) + 1

exclusive_prefectures = {pref for pref, count in prefecture_counts.items() if count == 1}

# Build merged data
merged_data = []

for row in backup_data:
    name = row['Name']

    # Add production tonnes
    production = production_data.get(name, '')

    # Determine importance
    # 1 = top 15 by production OR exclusive prefecture rice OR has detailed parents/year/notes in backup
    # 2 = has some data
    # 3 = minimal data
    is_top_producer = name in production_data
    is_exclusive = row['Prefecture'].strip() in exclusive_prefectures if row['Prefecture'].strip() else False
    has_details = bool(row.get('Parents') or row.get('Year') or (row.get('Notes') and len(row.get('Notes', '').strip()) > 20))

    if is_top_producer or is_exclusive:
        importance = 1
    elif has_details:
        importance = 2
    else:
        importance = 3

    # Use enhanced notes if available, otherwise use backup notes
    notes = enhanced_notes.get(name, row.get('Notes', ''))

    merged_data.append({
        'Name': name,
        'Prefecture': row['Prefecture'],
        'Parents': row.get('Parents', ''),
        'Year': row.get('Year', ''),
        'Production_Tonnes': production,
        'Importance': importance,
        'Notes': notes
    })

print(f"Merged {len(merged_data)} varieties")
print(f"  Importance 1: {sum(1 for r in merged_data if r['Importance'] == 1)}")
print(f"  Importance 2: {sum(1 for r in merged_data if r['Importance'] == 2)}")
print(f"  Importance 3: {sum(1 for r in merged_data if r['Importance'] == 3)}")

# Write merged data
with open('sake_rice.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Prefecture', 'Parents', 'Year', 'Production_Tonnes', 'Importance', 'Notes']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged_data)

print(f"\n✓ Written to sake_rice.csv")
