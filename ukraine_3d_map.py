import pandas as pd
import geopandas as gpd
import pydeck as pdk
import matplotlib
import matplotlib.pyplot as plt

# 1. Aggregate Regional Data (Attacks and Fatalities)
# Calculate total fatalities and total attacks for each region (admin1)
regional_stats = acled.groupby('admin1').agg(
    attack_count=('event_id_cnty', 'count'),
    regional_fatalities=('fatalities', 'sum')
).reset_index()

# Normalize the attack count for the color intensity scale
min_attacks = regional_stats['attack_count'].min()
max_attacks = regional_stats['attack_count'].max()
regional_stats['normalized_intensity'] = (regional_stats['attack_count'] - min_attacks) / (max_attacks - min_attacks)

# 2. Load and Prepare Ukraine GeoJSON
geojso_url = "https://raw.githubusercontent.com/martynafford/natural-earth-geojson/master/10m/cultural/ne_10m_admin_1_states_provinces.json"
world_regions = gpd.read_file(geojso_url)

# FIX: Broaden filter to include Crimea/Sevastopol if they are labeled as 'Russia' or 'Disputed'
crimea_names = ['Crimea', 'Avtonomna Respublika Krym', 'Krym', 'Sevastopol', 'm. Sevastopol']
ukraine_regions = world_regions[
    (world_regions['admin'] == 'Ukraine') |
    (world_regions['name'].isin(crimea_names))
].copy()

# Robust Mapping to align GeoJSON names with ACLED
name_mapping = {
    'Kiev': 'Kyiv',
    'Kiev City': 'Kyiv City',
    "Dnipropetrovs'k": 'Dnipropetrovsk',
    'Zaporizhzhya': 'Zaporizhia',
    'Mykolayiv': 'Mykolaiv',
    'Avtonomna Respublika Krym': 'Crimea',
    'Krym': 'Crimea',
    'm. Sevastopol': 'Sevastopol',
    "Donets'k": 'Donetsk',
    'Odessa': 'Odesa',
    "Luhans'k": 'Luhansk',
    "Khmel'nyts'kyy": 'Khmelnytskyi',
    "Ivano-Frankivs'k": 'Ivano-Frankivsk',
    "L'viv": 'Lviv',
    "Ternopil'": 'Ternopil',
    "Vinnytsya": 'Vinnytsia'
}
ukraine_regions['name'] = ukraine_regions['name'].replace(name_mapping)

# Merge aggregated stats into the GeoJSON
ukraine_regions = ukraine_regions.merge(
    regional_stats,
    left_on='name',
    right_on='admin1',
    how='left'
)

# --- Tooltip Preparation: Unify Column Names to avoid "undefined" ---
ukraine_regions['attack_count'] = ukraine_regions['attack_count'].fillna(0)
ukraine_regions['regional_fatalities'] = ukraine_regions['regional_fatalities'].fillna(0)
ukraine_regions['individual_fatalities'] = "N/A (Hover over a bar)"
ukraine_regions['admin1_display'] = ukraine_regions['name']

# Color the regions based on attack intensity
cmap = matplotlib.colormaps['Oranges']
ukraine_regions['fill_color'] = ukraine_regions['normalized_intensity'].apply(
    lambda x: [int(c * 255) for c in cmap(x)[:3]] + [180] if not pd.isna(x) else [0, 0, 0, 0]
)

# 3. Prepare Strike Data (3D Bars)
fatal_strikes = acled[acled['fatalities'] > 0].copy()
fatal_strikes = fatal_strikes.dropna(subset=['longitude', 'latitude'])

# Merge regional stats into individual strike data for the tooltip
fatal_strikes = fatal_strikes.merge(regional_stats, on='admin1', how='left')
fatal_strikes['individual_fatalities'] = fatal_strikes['fatalities']
fatal_strikes['admin1_display'] = fatal_strikes['admin1']

# 4. Define PyDeck Layers
region_layer = pdk.Layer(
    "GeoJsonLayer",
    ukraine_regions,
    opacity=0.8,
    stroked=True,
    filled=True,
    get_fill_color="fill_color",
    get_line_color= [80,80,80],
    pickable=True
)

column_layer = pdk.Layer(
    "ColumnLayer",
    data=fatal_strikes,
    get_position=['longitude', 'latitude'],
    get_elevation='individual_fatalities',
    elevation_scale=3000,
    radius=3000,
    get_fill_color= [136, 8, 8], # Pure Red bars
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=49.0, longitude=32.0, zoom=5.5, pitch=50, bearing=0)

# Unified Tooltip to fix the "undefined" error
tooltip = {
    "html": '''
<b>Region:</b> {admin1_display} <br/>
<b>Total Regional Attacks:</b> {attack_count} <br/>
<b>Total Regional Fatalities:</b> {regional_fatalities} <br/>
<hr style="margin: 5px 0;">
<b>Strike Fatalities:</b> {individual_fatalities}
    ''',
    "style": {"background": "#333333", "color": "white", "font-family": 'Arial', "z-index": "10000"}
}

r = pdk.Deck(layers=[region_layer, column_layer], initial_view_state=view_state, tooltip=tooltip, map_style='dark')

# Display the map
display(r.show())

# 5. Legend for the Poster
fig, ax = plt.subplots(figsize=(8, 1))
fig.subplots_adjust(bottom=0.5)
norm = matplotlib.colors.Normalize(vmin=min_attacks, vmax=max_attacks)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cb = fig.colorbar(sm, cax=ax, orientation='horizontal')
cb.set_label('Total Regional Air/Drone Attacks (Intensity Scale)')
plt.show()
