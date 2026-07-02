# The Heat Beneath the City: Austin Urban Heat Island Analysis

**An interactive scrollytelling web map of summer land surface temperature across Austin, Texas, and how it tracks tree canopy, impervious surface, and household income, measured across all 65 of the city's neighborhood planning areas.**

**Live story map:** https://nirajan550123.github.io/projects/austin-heat-storymap/
**Methodology write-up:** https://nirajan550123.github.io/projects/austin-heat-storymap/methodology.html

![Story map preview](preview.jpg)

## What it shows

As the reader scrolls, a sticky Leaflet map recolors Austin's neighborhoods through four variables (land surface temperature, tree canopy, impervious surface, and median income) while the narrative moves from where the city runs hottest, to why (canopy and pavement), to who the heat falls on (income), to what can be done. Statistical scatter plots appear alongside the relevant sections.

The whole thing is built from measured satellite and census data, not illustration, and the analysis code that produced every number is in this repository.

## Key findings

Across all 65 neighborhoods, summer land surface temperature is tightly governed by the physical landscape. The two correlations below are computed directly from the committed data file `data/austin_heat_stats.csv` (n = 65, reproducible with `src/verify_correlations.py`):

- **Tree canopy:** Pearson r = -0.87 (p < 1e-20). More canopy, cooler surface.
- **Impervious surface:** Pearson r = +0.83 (p < 1e-16). More pavement, hotter surface.

A third relationship comes from the separate census-and-PostGIS arm of the pipeline:

- **Median income:** moderate negative correlation (about r = -0.51), computed by area-weighting census-tract income to neighborhoods in PostGIS (`src/05_income_spatial_join.sql`). Lower-income neighborhoods tend to be hotter, but income tracks heat far more weakly than canopy or pavement do.

The headline: heat follows the built and vegetated surface much more tightly than it follows income. Canopy and impervious cover explain most of the neighborhood-to-neighborhood variation; income is a secondary, socially important signal layered on top.

## How to read the temperatures

The temperature values are **land surface temperature, not air temperature.** Summer LST in the dataset ranges from roughly 45 to 52 degrees Celsius across neighborhoods. That is expected: a sunlit parking lot or roof reaches surface temperatures well above the air temperature a thermometer would read. The analysis compares neighborhoods to each other on a consistent surface-temperature basis; it is not a claim about how hot the air felt.

## Data and provenance

| Variable | Source | Processing |
|---|---|---|
| Land surface temperature | Landsat 8/9 Collection 2 Level-2 thermal band (ST_B10) | Median of clear-sky summer scenes (Jun to Aug, 2022 to 2024), cloud-masked, scaled to Celsius, in Google Earth Engine |
| Tree canopy | USFS / NLCD Tree Canopy Cover (2023 release) | Zonal mean per neighborhood |
| Impervious surface | NLCD impervious layer (2021 release) | Zonal mean per neighborhood |
| Median income | U.S. Census ACS (B19013), via tidycensus | Area-weighted from tracts to neighborhoods in PostGIS |
| Boundaries | City of Austin Neighborhood Planning Areas | Dissolved by name to 65 areas |

## Pipeline

```
src/01_create_boundary_asset.js    GEE: build neighborhood asset, dissolve to 65
src/02_heat_analysis.js            GEE: LST composite, NLCD zonal stats, correlations, CSV export
src/03_census_income.R             R:  pull ACS tract income, load to PostGIS
src/04_neighborhoods_to_postgis.R  R:  dissolve neighborhoods, load to PostGIS
src/05_income_spatial_join.sql     PostGIS: SRID transform + area-weighted income join
verify_correlations.py         Recompute the canopy/impervious r values from the CSV
index.html                         Leaflet + Chart.js scrollytelling map
methodology.html                   Full methodology write-up
data/austin_heat_stats.csv    Per-neighborhood LST, canopy, impervious (the analysis output)
data/austin_heat.geojson      Merged neighborhood data the web map reads
```

Stages run in order. Earth Engine produces the temperature, canopy, and impervious statistics; R and PostGIS produce the income values; the results merge into `data/austin_heat.geojson`, which the web map renders.

## A note on the within-neighborhood spread

`02_heat_analysis.js` also records a standard deviation of LST within each neighborhood. That value describes how much surface temperature varies inside a neighborhood (how much the single mean is smoothing over). It is **not** an error bar and is not used as a basis for significance testing. The correlations above are across the 65 neighborhood means.

## Built with

Google Earth Engine (JavaScript API) for satellite compositing and zonal statistics; PostgreSQL and PostGIS for the spatial database and the area-weighted income join; R (tidycensus, sf, RPostgres) for census retrieval and loading; Leaflet for the interactive map; Chart.js for the scatter plots; vanilla JavaScript, GeoJSON, and CARTO basemap tiles.

## Running it

The web map is static: `index.html` reads `data/austin_heat.geojson`, so serving the repository folder (or opening `index.html` from a local server) renders the live map.

To reproduce the data pipeline:

1. Run `src/01` and `src/02` in the Google Earth Engine Code Editor and export the stats CSV.
2. Install PostgreSQL and PostGIS; create the `austin_heat` database with the PostGIS extension.
3. Set your database password and Census API key as environment variables, then run `src/03` and `src/04` to load PostGIS, and `src/05` for the area-weighted income join.
4. Merge the Earth Engine stats and the income output into `data/austin_heat.geojson`.

Credentials (database password, API key) are read from environment variables and are not stored in the code.

## Verify the headline numbers

```bash
python src/verify_correlations.py
```
Recomputes the canopy and impervious correlations from `data/austin_heat_stats.csv` so the two reproducible findings can be checked in seconds.

## Skills demonstrated

Remote sensing and Google Earth Engine (Landsat LST compositing, cloud masking, NLCD zonal statistics); spatial SQL in PostGIS (coordinate reprojection, area-weighted spatial join); census data retrieval and integration in R; interactive web mapping and data visualization (Leaflet, Chart.js); and communicating a quantitative result to a general audience through scrollytelling.

---

*Author: Nirajan Tripathi, M.S. Geography (GIS and remote sensing), Texas State University.*
[Portfolio](https://nirajan550123.github.io/) · [LinkedIn](https://www.linkedin.com/in/nirajan-tripathi/) · [GitHub](https://github.com/nirajan550123)
