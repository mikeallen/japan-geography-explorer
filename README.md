# Japan Geography Explorer

An interactive web-based visualization tool for exploring Japan's geography, including prefectures, historical provinces, mountains, rivers, lakes, mountain ranges, and sake rice varieties.

## Features

- **Interactive Map**: Pan, zoom, and explore Japan's geography
- **Multiple Layers**:
  - Modern Prefectures (47 prefectures)
  - Historical Provinces (69 old provinces/kuni)
  - Mountains (62 major peaks with elevations)
  - Rivers (43 major rivers with lengths)
  - Lakes (6 major lakes with areas)
  - Mountain Ranges (14 major mountain ranges)
  - Sake Rice Varieties (71 varieties with production data)
- **Smart Labeling**: Distributed labels with leader lines for easy reading
- **Prefecture Filtering**: Click any prefecture to filter data for that region
- **Detailed Information**: Click on any feature to see comprehensive details
- **Japanese Names**: All features include both English and Japanese names

## Quick Start

### Running the Application

1. **No server required!** Simply open `index.html` in any modern web browser
2. The application loads all data from the embedded `japan_geo_data.js` file

### Updating Data

If you modify any CSV files in the `data/` directory:

```bash
cd data
python3 convert_csv_to_js.py
```

This regenerates `japan_geo_data.js` with the latest data from all CSV files.

Then refresh your browser to see the changes.

## Project Structure

```
.
├── index.html              # Main application (standalone, no server needed)
├── japan_geo_data.js       # Embedded data (auto-generated, do not edit)
├── README.md               # This file
│
├── data/                   # All data files and conversion script
│   ├── README.md                  # Data directory documentation
│   ├── convert_csv_to_js.py       # Script to regenerate japan_geo_data.js
│   │
│   ├── Active Data Files (CSV)
│   │   ├── prefectures.csv            # Prefecture metadata
│   │   ├── prefectures_geo.csv        # Prefecture boundaries
│   │   ├── old_provinces.csv          # Historical province metadata
│   │   ├── old_provinces_geo.csv      # Historical province boundaries
│   │   ├── mountains.csv              # Mountain metadata
│   │   ├── mountains_geo.csv          # Mountain coordinates
│   │   ├── rivers.csv                 # River metadata
│   │   ├── rivers_geo_final.csv       # River coordinates
│   │   ├── lakes.csv                  # Lake metadata
│   │   ├── lakes_geo.csv              # Lake coordinates
│   │   ├── mountain_ranges_geo.csv    # Mountain range polygons
│   │   └── sake_rice.csv              # Sake rice varieties
│   │
│   └── archive/                   # Old/intermediate data files
│       └── README.md              # Archive documentation
│
└── scripts/                # Data processing/download scripts
    └── README.md           # Script documentation
```

## Data Sources

### Prefecture Data
- **Source**: Japanese Ministry of Internal Affairs and Communications
- **Boundaries**: Generalized from official administrative boundary data
- **Regions**: Based on standard Japanese regional divisions

### Historical Provinces (Old Provinces)
- **Source**: Historical records and Wikipedia
- **Boundaries**: Approximated by mapping to modern prefectures
- **Reference**: https://en.wikipedia.org/wiki/Provinces_of_Japan

### Mountains
- **Source**: Multiple sources including:
  - Geospatial Information Authority of Japan (GSI)
  - Wikipedia's list of mountains in Japan
  - OpenStreetMap
- **Data**: Includes elevation, coordinates, and prefecture location

### Rivers
- **Source**: OpenStreetMap and Ministry of Land, Infrastructure, Transport and Tourism
- **Data**: Length, coordinates, and prefecture information
- **Processing**: Coordinate data simplified to reduce file size while maintaining accuracy

### Lakes
- **Source**: Geospatial Information Authority of Japan and Wikipedia
- **Data**: Surface area, coordinates, and prefecture location

### Mountain Ranges
- **Source**: OpenStreetMap and geographic references
- **Boundaries**: Approximate polygons based on geographic extent

### Sake Rice (Sakamai)
- **Source**: Multiple sources including:
  - Japan Sake and Shochu Makers Association
  - Prefecture agricultural departments
  - Sake industry publications
  - Internet research for Japanese names and production statistics
- **Data**: Includes variety names (English and Japanese), prefecture, parent varieties, year developed, production tonnage, and detailed notes

## Data Format

All data is stored in CSV format for easy editing:

- **Metadata files**: Basic information (name, prefecture, area/elevation/length, etc.)
- **Geometry files** (_geo.csv): Coordinate data for rendering polygons, lines, and points
- **Coordinates**: Stored as latitude,longitude pairs separated by semicolons

## Development

### Adding New Data

1. Edit the appropriate CSV file(s) in the `data/` directory
2. Run the data conversion script:
   ```bash
   cd data
   python3 convert_csv_to_js.py
   ```
3. Refresh your browser to see the changes

### Modifying the Application

The application is a single-file HTML application with embedded JavaScript:
- All code is in `index.html`
- Data is loaded from `japan_geo_data.js`
- No build process or dependencies required

### Controls

- **Pan**: Click and drag on the map
- **Zoom**: Mouse wheel or trackpad scroll
- **Reset**: Click the ⟲ button to reset view and reload data
- **Filter**: Click any prefecture to filter data for that region
- **Layer Selection**: Click layer buttons in the left sidebar

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari

## Credits

Created by Mike Allen

Data compiled from various open sources including OpenStreetMap, Wikipedia, Japanese government agencies, and sake industry publications.

## License

The application code is provided as-is for educational and reference purposes.

Geographic data is compiled from public sources. Please refer to original data sources for their respective licenses:
- OpenStreetMap: © OpenStreetMap contributors, ODbL
- Wikipedia: CC BY-SA
- Japanese government data: Generally public domain
