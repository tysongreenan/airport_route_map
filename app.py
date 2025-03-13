from flask import Flask, render_template, url_for, request
import folium
from folium import plugins
import os
import math

app = Flask(__name__, static_folder='static')

def haversine_distance(point1, point2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lat1, lon1 = point1
    lat2, lon2 = point2
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371000  # Radius of earth in meters
    return c * r  # Return distance in meters

def create_challenger_map():
    """Create the Challenger 350 map with long-range destinations"""
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

def create_bell429_map():
    """Create the Bell 429 Helicopter map with shorter-range destinations"""
    # The Scotsman Hotel location in Niagara-on-the-Lake
    scotsman = ("The Scotsman Hotel, 95 Johnson St, Niagara-on-the-Lake", (43.2553, -79.0713))
    
    # Define the helicopter destinations with names and coordinates
    destinations = {
        # Ontario Destinations
        "Toronto Downtown": (43.6532, -79.3832),
        "Toronto Pearson Airport": (43.6777, -79.6248),
        "Toronto Billy Bishop Airport": (43.6284, -79.3962),
        "Muskoka (Cottage Country)": (45.0365, -79.3045),
        "Ottawa Downtown": (45.4215, -75.6972),
        "Ottawa International Airport": (45.3223, -75.6674),
        "Kingston": (44.2312, -76.4860),
        "London": (42.9849, -81.2453),
        "Kitchener-Waterloo": (43.4643, -80.5204),
        "Barrie": (44.3894, -79.6903),
        "Windsor": (42.3149, -83.0364),
        "Sudbury": (46.4917, -80.9930),
        "Sault Ste. Marie": (46.5136, -84.3358),
        "North Bay": (46.3091, -79.4608),
        # Thunder Bay removed - approximately 700 NM from Niagara-on-the-Lake, beyond Bell 429's 385 NM range
        
        # Quebec Destinations
        "Montreal Downtown": (45.5017, -73.5673),
        "Montreal-Trudeau Airport": (45.4698, -73.7411),
        # Quebec City removed - approximately 450 NM from Niagara-on-the-Lake, beyond Bell 429's 385 NM range
        "Mont-Tremblant": (46.1185, -74.5962),
        
        # New York State Destinations
        "Buffalo Niagara International Airport": (42.9404, -78.7320),
        "Rochester": (43.1566, -77.6088),
        "Syracuse": (43.0481, -76.1474),
        "Albany": (42.6526, -73.7562),
        "Lake Placid": (44.2795, -73.9799),
        "Adirondacks": (44.3894, -74.2168),
        
        # Pennsylvania Destinations
        "Erie": (42.1292, -80.0851),
        "Pittsburgh": (40.4406, -79.9959),
        
        # Michigan Destinations
        "Detroit Metro Airport": (42.2162, -83.3554),
        "Detroit Downtown": (42.3314, -83.0458),
        "Ann Arbor": (42.2808, -83.7430),
        "Grand Rapids": (42.9634, -85.6681),
        
        # Northern U.S. & East Coast Destinations
        "Cleveland, Ohio": (41.4993, -81.6944),
        "Columbus, Ohio": (39.9612, -82.9988),
        "Toledo, Ohio": (41.6528, -83.5379),
        "Boston, Massachusetts": (42.3601, -71.0589),
        "Washington D.C.": (38.9072, -77.0369),
        "New York City (Manhattan)": (40.7128, -74.0060),
        "JFK Airport": (40.6413, -73.7781),
        "LaGuardia Airport": (40.7769, -73.8740),
        "Newark Airport": (40.6895, -74.1745),
        
        # Resort & Remote Destinations
        "Niagara Falls, Ontario": (43.0896, -79.0849),
        "Niagara Falls International Airport": (43.0962, -79.0377),
        "Blue Mountain Resort": (44.5012, -80.3097),
        "Algonquin Park": (45.8316, -78.3650)
    }

    # Create a Folium map centered on the Scotsman Hotel
    m = folium.Map(location=scotsman[1], zoom_start=6)

    # Add a marker for the Scotsman Hotel (destination)
    folium.Marker(
        location=scotsman[1],
        popup=scotsman[0],
        icon=folium.Icon(color='red', icon='flag')
    ).add_to(m)

    # Draw a circle outlining the 385-nautical-mile range from the Scotsman Hotel
    radius_m = 385 * 1852  # Convert nautical miles to meters
    folium.Circle(
        location=scotsman[1],
        radius=radius_m,
        color='orange',
        fill=False,
        popup="385 Nautical Mile Range (Bell 429)"
    ).add_to(m)

    # Add markers for all origins and draw lines to Scotsman Hotel
    for name, coords in destinations.items():
        # Calculate distance from Scotsman Hotel to origin
        distance = haversine_distance(scotsman[1], coords) / 1852  # Convert meters to nautical miles
        
        # Add a blue marker for each origin with helicopter icon
        helicopter_icon = folium.CustomIcon(
            icon_image=f"{url_for('static', filename='helicopter-48.png')}",
            icon_size=(24, 24),
            icon_anchor=(12, 12)
        )
        
        folium.Marker(
            location=coords,
            popup=f"{name} - {distance:.0f} NM",
            icon=helicopter_icon
        ).add_to(m)
        
        # Draw a green line from origin to destination (Scotsman Hotel)
        folium.PolyLine(
            locations=[coords, scotsman[1]],
            color='green',
            weight=2,
            opacity=0.7,
            popup=f"{name} - {distance:.0f} NM"
        ).add_to(m)

    return m._repr_html_()

@app.route('/')
def index():
    # Get the aircraft type from the query parameter, default to challenger
    aircraft_type = request.args.get('aircraft', 'challenger')
    
    if aircraft_type == 'bell429':
        map_html = create_bell429_map()
        aircraft_name = "Bell 429 Helicopter"
        range_text = "385 NM Range"
    else:
        map_html = create_challenger_map()
        aircraft_name = "Challenger 350"
        range_text = "3,300 NM Range"
    
    return render_template('index.html', 
                          map_html=map_html,
                          aircraft_type=aircraft_type,
                          aircraft_name=aircraft_name,
                          range_text=range_text)

if __name__ == '__main__':
    app.run(debug=True) 