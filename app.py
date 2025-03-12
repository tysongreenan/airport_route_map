from flask import Flask, render_template, url_for
import folium
from folium import plugins
import os

app = Flask(__name__, static_folder='static')

def create_map():
    # Define the airport data with names and coordinates
    airports = {
        "Los Angeles International Airport (LAX)": (33.9416, -118.4085),
        "San Francisco International Airport (SFO)": (37.6213, -122.3790),
        "Van Nuys Airport (VNY)": (34.2090, -118.4891),
        "Phoenix Sky Harbor International Airport (PHX)": (33.4342, -112.0116),
        "Dallas/Fort Worth International Airport (DFW)": (32.8998, -97.0403),
        "Miami International Airport (MIA)": (25.7959, -80.2870),
        "Orlando International Airport (MCO)": (28.4312, -81.3081),
        "Tampa International Airport (TPA)": (27.9755, -82.5332),
        "Hartsfield-Jackson Atlanta International Airport (ATL)": (33.6407, -84.4277),
        "Washington Dulles International Airport (IAD)": (38.9531, -77.4565),
        "Philadelphia International Airport (PHL)": (39.8744, -75.2424),
        "Newark Liberty International Airport (EWR)": (40.6895, -74.1745),
        "John F. Kennedy International Airport (JFK)": (40.6413, -73.7781),
    }

    # Niagara Falls International Airport (IAG)
    niagara = ("Niagara Falls International Airport (IAG)", (43.0962, -79.0377))

    # Create a Folium map centered on Niagara Falls International Airport
    m = folium.Map(location=niagara[1], zoom_start=5)

    # Add a marker for Niagara Falls International Airport
    folium.Marker(
        location=niagara[1],
        popup=niagara[0],
        icon=folium.Icon(color='red', icon='flag')
    ).add_to(m)

    # Add markers for all other airports and draw lines to Niagara Falls International Airport
    for name, coords in airports.items():
        folium.Marker(
            location=coords,
            popup=name,
            icon=folium.Icon(color='blue', icon='plane')
        ).add_to(m)
        # Draw a line from this airport to Niagara Falls International Airport
        folium.PolyLine(locations=[coords, niagara[1]], color='green', weight=2, opacity=0.7).add_to(m)

    # Draw a circle outlining the 3,300-nautical-mile range from Niagara Falls International Airport
    radius_m = 3300 * 1852  # Convert nautical miles to meters
    folium.Circle(
        location=niagara[1],
        radius=radius_m,
        color='orange',
        fill=False,
        popup="3,300 Nautical Mile Range"
    ).add_to(m)

    return m._repr_html_()

@app.route('/')
def index():
    map_html = create_map()
    return render_template('index.html', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True) 