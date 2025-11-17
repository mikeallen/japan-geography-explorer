# Data Directory

This directory contains all the geographic data for the Japan Geography Explorer application and the script to convert it to the embedded JavaScript format.

## Structure

```
data/
├── README.md                   # This file
├── convert_csv_to_js.py        # Data conversion script
│
├── Active Data Files (CSV)
│   ├── prefectures.csv         # Prefecture metadata
│   ├── prefectures_geo.csv     # Prefecture boundaries
│   ├── old_provinces.csv       # Historical province metadata
│   ├── old_provinces_geo.csv   # Historical province boundaries
│   ├── mountains.csv           # Mountain metadata
│   ├── mountains_geo.csv       # Mountain coordinates
│   ├── rivers.csv              # River metadata
│   ├── rivers_geo_final.csv    # River coordinates
│   ├── lakes.csv               # Lake metadata
│   ├── lakes_geo.csv           # Lake coordinates
│   ├── mountain_ranges_geo.csv # Mountain range polygons
│   └── sake_rice.csv           # Sake rice varieties
│
└── archive/                    # Old/intermediate data files
    └── README.md               # Archive documentation
```

## Updating Data

### Making Changes to Data

1. **Edit CSV files** directly in this directory using any text editor or spreadsheet application
   - Metadata files contain names, descriptions, and attributes
   - Geometry files (_geo.csv) contain coordinate data
   - Coordinates are stored as latitude,longitude pairs separated by semicolons

2. **Regenerate the embedded data file** by running:
   ```bash
   cd data
   python3 convert_csv_to_js.py
   ```

3. **Refresh your browser** to see the changes in the application
   - The script generates `japan_geo_data.js` in the parent directory
   - The application loads this file automatically

### convert_csv_to_js.py

This is the primary data processing script that:
- Reads all CSV files in this directory
- Combines them into a single JavaScript data object
- Writes `japan_geo_data.js` to the parent directory for use by the application
- Must be run from the `data/` directory

**Important:** Never edit `japan_geo_data.js` manually - always regenerate it using this script after making CSV changes.

## Data Files Description

### Prefecture Data
- **prefectures.csv**: 47 modern prefectures with names, regions, capitals, area, population
- **prefectures_geo.csv**: Polygon boundaries for each prefecture

### Historical Provinces (Old Provinces/Kuni)
- **old_provinces.csv**: 69 historical provinces with names and modern prefecture mappings
- **old_provinces_geo.csv**: Approximate boundaries based on modern prefectures

### Mountains
- **mountains.csv**: 62 major peaks with elevations, coordinates, and prefecture locations
- **mountains_geo.csv**: Point coordinates for mountain locations

### Rivers
- **rivers.csv**: 43 major rivers with lengths and prefecture information
- **rivers_geo_final.csv**: Simplified polyline coordinates for river courses

### Lakes
- **lakes.csv**: 6 major lakes with surface areas and prefecture locations
- **lakes_geo.csv**: Polygon boundaries for lake surfaces

### Mountain Ranges
- **mountain_ranges_geo.csv**: Approximate polygon boundaries for 14 major mountain ranges

### Sake Rice (Sakamai)
- **sake_rice.csv**: 97 sake rice varieties with:
  - English and Japanese names
  - Prefecture of origin
  - Parent varieties and development year
  - Production tonnage (where available)
  - Importance rating (1-3)
  - Detailed notes on characteristics and usage

## Data Format

All CSV files use:
- UTF-8 encoding
- Comma-separated values
- Double quotes for fields containing commas
- Semicolons to separate coordinate pairs within geometry fields

### Coordinate Format
```csv
Name,Coordinates
Example River,"lat1,lon1;lat2,lon2;lat3,lon3"
```

## Data Sources

See the main README.md in the parent directory for detailed information about data sources and credits.

## Archive Directory

The `archive/` subdirectory contains:
- Intermediate data files from the development process
- Old versions of data before major updates
- Source files (GeoJSON, etc.) from external sources
- Log files from data download scripts

These files are retained for historical reference and potential future use but are not actively loaded by the application.
