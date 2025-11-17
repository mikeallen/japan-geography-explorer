# Data Processing Scripts

This directory contains one-off scripts used to download, process, and enhance the geographic data for the Japan Geography Explorer.

## Data Download Scripts

### download_mountains.py
Downloads mountain data from external sources and creates initial mountains dataset.

### download_rivers_osm.py & download_rivers_simple.py
Downloads river data from OpenStreetMap. Used to gather initial river geometry and metadata.
- `download_rivers_osm.py`: Full OSM query approach
- `download_rivers_simple.py`: Simplified version for specific rivers

### download_mountain_range_osm.py
Downloads mountain range boundaries from OpenStreetMap to create polygon data for mountain ranges.

## Data Creation Scripts

### create_mountains_data.py
Consolidates mountain data from various sources into the final mountains.csv format.

### create_mountain_range_boundaries.py
Generates polygon boundaries for mountain ranges based on geographical data.

### create_accurate_mountain_ranges.py
Refined version of mountain range boundary creation with improved accuracy.

### create_old_provinces.py
Creates the old provinces (kuni) dataset with historical province information.

### create_province_boundaries.py & create_complete_provinces.py
Generates polygon boundaries for historical provinces by mapping them to modern prefectures.

### convert_prefectures.py
Converts prefecture data to standardized CSV format with coordinates.

### geojson_to_csv.py
Utility to convert GeoJSON geographic data to CSV format.

## Data Enhancement Scripts

### add_japanese_names_sake.py
Adds Japanese names (kanji) to all sake rice varieties in sake_rice.csv.

### enhance_importance2.py
Enriches sake rice data by adding detailed information for importance level 2 varieties from research.

### enhance_prefectures.py
Adds additional metadata to prefecture data (regions, old provinces, etc.).

### add_missing_mountains.py
Identifies and adds mountains that were missing from the initial dataset.

## Data Cleaning Scripts

### clean_river_data.py & clean_river_jumps.py
Cleans river coordinate data by removing invalid jumps and simplifying geometry.

### analyze_river_data.py & analyze_jumps.py
Analysis scripts to identify issues in river coordinate data.

### fix_rivers.py
Applies fixes to river data based on analysis results.

### fix_lakes.py
Corrects lake data formatting and coordinates.

### fix_ezo.py
Fixes the naming of Ezo/Hokkaido in the old provinces dataset.

### cleanup_names.py
Standardizes naming conventions across datasets.

## Data Merging Scripts

### merge_mountains.py
Merges multiple mountain data sources into a single consolidated dataset.

### merge_rivers.py
Combines river data from different sources.

### merge_sake_rice.py
Merges sake rice data, combining production statistics with variety information.

### merge_province_boundaries.py
Combines historical province boundaries created from modern prefecture data.

## Usage

Most of these scripts were run once during the initial data preparation phase. They are retained for:
- Documentation of data provenance
- Potential future data updates
- Reference for similar data processing tasks

If you need to update the source data, refer to the specific script for that data type.
