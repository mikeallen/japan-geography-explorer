#!/usr/bin/env python3
"""
Enhance importance 2 varieties with researched data.
"""

import csv

# Enhanced data for importance 2 varieties based on research
enhancements = {
    'Koshi Tanrei': {
        'Year': '1989/2004',
        'Production_Tonnes': '1200',
        'Notes': 'Hybrid of Yamada Nishiki and Gohyakumangoku. Crossed in 1989, officially introduced 2004, registered 2007. Developed specifically for daiginjo sake making since it can be polished to lower levels than Gohyakumangoku without cracking (40%+ seimai-buai vs 50% limit). Good water absorbency, dissolves well in moromi. Creates sake that is clean with rich flavors - inherits attributes of both parents: clean aftertaste from Gohyakumangoku and full body/ginjo-ka from Yamada Nishiki. Over 1200 tonnes produced in 2019, ranking 10th in total Japanese production.'
    },
    'Senbon nishiki': {
        'Year': '1990/2002',
        'Notes': 'Premium sake rice from Hiroshima Prefecture. Developed by crossing Yamada Nishiki and Nakate Shinsenbon, first cultivated 1990, officially registered 2002. Created to be a unique Hiroshima varietal adapted to local climate with excellent properties for premium ginjo-shu. Makes sake that is fragrant with rich flavor and mildly bitter fresh finish. Often used for ginjo-shu production.'
    },
    'Yukimegami': {
        'Year': '2001/2015',
        'Parents': 'Yamada Nishiki (one parent confirmed)',
        'Notes': 'Snow Goddess from Yamagata Prefecture. First Daiginjo-specific rice developed to lessen reliance on Yamadanishiki. Development started 2001, introduced 2015. Created specifically for Yamagata climate and daiginjo production. Low protein content inhibits amino acids during brewing, producing refreshingly sweet, clear, delicate sake with smooth texture and low amino acid content. Makes clean and smooth sake.'
    },
    'Misato Nishiki': {
        'Year': 'Early 2000s',
        'Parents': 'Yamada Nishiki x Miyama Nishiki',
        'Notes': 'Hybrid of Yamada Nishiki and Miyama Nishiki developed by Akita Prefectural Agriculture Research Center in early 2000s. Considered one of best sake rice varieties in Akita. Makes it possible to produce deep and heavy sake while having fruity aroma like sake made from Yamada Nishiki.'
    },
    'Kairyo Omachi': {
        'Year': '1960',
        'Notes': '改良 (kairyō) translates to "improvement" or "revised" - a strain bred to be more manageable than original Omachi rice. Developed in Shimane 1960. Crossbreeding with more durable strains reduced height of Omachi\'s towering stalks, tamed wild shinpaku, and shortened cultivation time. Created because Omachi is difficult for both farmers and brewers to handle. Still used in Shimane sake production today.'
    },
    'Yume Sasara': {
        'Year': 'Released 2017',
        'Notes': 'Tochigi Prefecture sake rice. Cross between Yamada Nishiki and Tochigi 25. Released in 2017. Developed for Tochigi\'s climate and sake production needs.'
    },
    'Kan no mai': {
        'Notes': 'New unique savory, smoky saline sake rice of Shimane. Developed to withstand cold climates. Prone to cracking at 70% polish. Used to brew Rihaku "Dance of Discovery" sake. Creates distinctive umami-forward sake profile.'
    },
}

# Load current data
varieties = []
with open('sake_rice.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name']
        if name in enhancements:
            # Apply enhancements
            for key, value in enhancements[name].items():
                if value:  # Only update if we have data
                    row[key] = value
        varieties.append(row)

# Write enhanced data
with open('sake_rice.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Name', 'Prefecture', 'Parents', 'Year', 'Production_Tonnes', 'Importance', 'Notes']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(varieties)

print(f"✓ Enhanced {len(enhancements)} importance 2 varieties")
print(f"✓ Total varieties in file: {len(varieties)}")
