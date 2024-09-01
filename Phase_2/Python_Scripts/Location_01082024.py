import pandas as pd
import folium
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def generate_train_route_map(file_path):
    # Load the dataset with the correct header row
    data = pd.read_excel(file_path, header=1)  # Adjust header row if necessary

    # Extract the relevant columns for plotting (Longitude and Latitude)
    longitude = data['Longitude_value']
    latitude = data['Latitude_value']

    # Remove rows with NaN values in longitude or latitude
    clean_data = data.dropna(subset=['Longitude_value', 'Latitude_value'])
    clean_longitude = clean_data['Longitude_value']
    clean_latitude = clean_data['Latitude_value']

    # Create a base map centered around the mean of the cleaned latitude and longitude values
    m = folium.Map(location=[clean_latitude.mean(), clean_longitude.mean()], zoom_start=11, tiles='CartoDB positron')

    # Add a line tracing the train's path with increased thickness
    clean_points = list(zip(clean_latitude, clean_longitude))
    folium.PolyLine(clean_points, color="red", weight=8, opacity=0.7).add_to(m)

    # Add a green marker for the start of the route
    folium.Marker(location=clean_points[0], popup="Start", icon=folium.Icon(color="green")).add_to(m)

    # Add a red marker for the end of the route
    folium.Marker(location=clean_points[-1], popup="End", icon=folium.Icon(color="red")).add_to(m)

    # Add a title to the map
    title_html = '''
                 <h3 align="center" style="font-size:20px"><b>Train Route</b></h3>
                 '''
    m.get_root().html.add_child(folium.Element(title_html))

    # Add a legend to explain the start and end markers
    legend_html = '''
    <div style="position: fixed; 
         bottom: 50px; left: 50px; width: 250px; height: 90px; 
         background-color: white; z-index:9999; font-size:14px;
         border:2px solid grey; padding: 10px;">
         <strong>Legend</strong><br>
         <i class="fa fa-map-marker fa-2x" style="color:green"></i>&nbsp; Start of the Route<br>
         <i class="fa fa-map-marker fa-2x" style="color:red"></i>&nbsp; End of the Route
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save the improved map as an HTML file with the legend
    output_path = 'train_route_map_with_legend.html'
    m.save(output_path)
    print(f"Map saved as {output_path}")

def select_file():
    Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
    file_path = askopenfilename(title="Select the dataset file", filetypes=[("Excel files", "*.xlsx *.xls")])
    return file_path

# Usage example
file_path = select_file()
if file_path:
    generate_train_route_map(file_path)
else:
    print("No file selected.")
