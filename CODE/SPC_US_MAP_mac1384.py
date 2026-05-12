import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.feature import NaturalEarthFeature
from shapely.geometry import box
import matplotlib.patches as mpatches

risk_order = ["TSTM", "MRGL", "SLGT", "ENH", "MDT", "HIGH"]

proj = ccrs.LambertConformal(
    central_longitude=-96.,
    central_latitude=39.,
    standard_parallels=(33., 45.)
)

fig = plt.figure(figsize=(19.2, 10.8))
ax = plt.axes(projection=proj)
ax.set_extent([-125., -70., 22., 50.])

STATES = NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none'
)

ax.add_feature(cf.LAND, color='white')
ax.add_feature(cf.OCEAN, color='lightblue')
ax.add_feature(cf.COASTLINE, edgecolor='black', linewidth=1.0, zorder=4)
ax.add_feature(STATES, edgecolor='black', linewidth=1.0, zorder=4)
ax.add_feature(cf.BORDERS, edgecolor='black', linewidth=1.0, zorder=4)
ax.add_feature(cf.LAKES, color='lightblue', linewidth=1.0,edgecolor='black', zorder=4)
legend_handles = [
    mpatches.Patch(facecolor='#c1e9c1', edgecolor="black", label="TSTM"),
    mpatches.Patch(facecolor='#66a366', edgecolor="black", label="MRGL"),
    mpatches.Patch(facecolor='#ffe066', edgecolor="black", label="SLGT"),
    mpatches.Patch(facecolor='#ffa366',  edgecolor="black", label="ENH"),
    mpatches.Patch(facecolor='#e06666',  edgecolor="black", label="MDT"),
    mpatches.Patch(facecolor='#ee99ee', edgecolor="black", label="HIGH")
]

ax.legend(
    handles=legend_handles,
    title="SPC Categorical Outlook",
    loc="lower left",
    frameon=True,
    fontsize=12,
    title_fontsize=18,
)

SPC_COLORS = {
    "TSTM": "#c1e9c1",
    "MRGL": "#66a366",
    "SLGT": "#ffe066",
    "ENH":  "#ffa366",
    "MDT":  "#e06666",
    "HIGH": "#ee99ee"
}

SPC_FILE = "day1otlk_20250425_1630_cat.lyr.geojson"

# Load GeoJSON (EPSG:4326)
spc_raw = gpd.read_file(SPC_FILE)

# Clip box in EPSG:4326
map_extent = gpd.GeoDataFrame(
    geometry=[box(-125, 20, -70, 60)],
    crs="EPSG:4326"
)

# Clip BEFORE projecting
spc_raw = gpd.clip(spc_raw, map_extent)

# Handle MultiPolygons
spc_raw = spc_raw.explode(index_parts=False)

# Draw polygons
for risk in risk_order:
    subset = spc_raw[spc_raw["LABEL"] == risk]
    if not subset.empty:
        subset.plot(
            ax=ax,
            facecolor=SPC_COLORS[risk],
            edgecolor="none",
            linewidth=1.2,
            alpha=1,
            zorder=3.9,
            transform=ccrs.PlateCarree()
        )

ax.gridlines(draw_labels=True, color='gray', alpha=0.4, linestyle='--')
ax.set_title("SPC Outlook – 1630Z April 25th, 2025", fontsize=18)

plt.savefig("SPCOutlookGraphic.png")
plt.show()
