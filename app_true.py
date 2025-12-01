from shiny import App, ui
import geopandas as gpd

# Load shapefile
gdf = gpd.read_file("belgium_map_simplified.shp")

# Convert to GeoJSON
geojson_data = gdf.to_json()

app_ui = ui.page_fluid(
    ui.h2("Belgium map with nouveau_PO"),

    ui.tags.div(id="map", style="height: 300px; border: 1px solid #ccc;"),

    # Leaflet includes
    ui.tags.link(
        rel="stylesheet",
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    ),
    ui.tags.script(src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"),

    # JavaScript code as a Python string 
    
    
ui.tags.script(
    f"""
    const geojson = {geojson_data};

    document.addEventListener("DOMContentLoaded", () => {{

        // Default style for all regions
        function style(feature) {{
            return {{
                weight: 0.5,
                color: "#666",
                fillColor: "#cccccc",
                fillOpacity: 0.4
            }};
        }}

        // Highlight on hover
        function highlightFeature(e) {{
            const layer = e.target;

            layer.setStyle({{
                weight: 2,
                color: '#000',
                fillOpacity: 0.7
            }});

            // Bring the highlighted region to the front visually
            layer.bringToFront();
        }}

        // Reset style when cursor leaves
        function resetHighlight(e) {{
            geoLayer.resetStyle(e.target);
        }}

        // Click popup
        function onClickFeature(e, feature) {{
            const v = feature.properties?.nouveau_PO;
            const text = v ? ("nouveau_PO: " + v) : "No data";
            e.target.bindPopup(text).openPopup(e.latlng);
        }}

        // Create map
        const map = L.map('map').setView([50.85, 4.35], 8);

        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            maxZoom: 19
        }}).addTo(map);

        // Add geojson layer
        const geoLayer = L.geoJSON(geojson, {{
            style: style,
            onEachFeature: function(feature, layer) {{
                layer.on({{
                    mouseover: highlightFeature,
                    mouseout: resetHighlight,
                    click: function(e) {{ onClickFeature(e, feature); }}
                }});
            }}
        }}).addTo(map);

        map.fitBounds(geoLayer.getBounds());
    }});
    """
    )

    #################



)

app = App(app_ui, server=None)
