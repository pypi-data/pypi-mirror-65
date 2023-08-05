import json
import uuid
import json
import dateutil.parser
import folium
import random
import os
import glob
from folium import FeatureGroup
from collections import OrderedDict


class LocationUpdate():
    def __init__(self, data):
        self.deviceId = data["deviceId"]
        self.longitude = float(data["longitude"])
        self.latitude = float(data["latitude"])
        time = data["timestamp"].replace(" UTC", "")
        self.timestamp = dateutil.parser.isoparse(time)
        self.accuracy = float(data["accuracy"])*.2


color_options = ['black', 'blue', 'cadetblue', 'darkblue', 'darkgreen', 'darkpurple', 'darkred', 'gray',
                 'green', 'lightblue', 'lightgray', 'lightgreen', 'lightred', 'orange', 'pink', 'purple', 'red']


def load_all_locations(path):
    all_locations = []
    # only process .JSON files in folder.
    for filename in glob.glob(os.path.join(path, '*.json')):
        print(f"found file {filename}")
        with open(filename, encoding='utf-8', mode='r') as currentFile:
            thing = parse_locations(currentFile.read())
            for loc in thing:
                all_locations.append(loc)

    if len(all_locations) < 1:
      print(f"No .json files found in directory: {path}")
    return all_locations

def parse_locations(content):
    data_collection = json.loads(content)
    location_list = []
    for data in data_collection:
        location_list.append(LocationUpdate(data))
    return sorted(location_list, key=lambda i: i.timestamp, reverse=True)


def main():
    path = os.getcwd()
    message = f"Grabbing infected at {path} 👌"
    print(message)

    all_locations = load_all_locations(path)

    print(f"👀 Found {len(all_locations)} locations")

    if len(all_locations) > 1:

        m = folium.Map(location=[all_locations[0].latitude, all_locations[0].longitude],
                    tiles='OpenStreetMap',
                    zoom_start=18,
                    max_zoom=20)

        points = {}

        for s in all_locations:
            date = s.timestamp.strftime('%d/%m/%Y')

            if date not in points:
                points[date] = {}
                points[date][s.deviceId] = []
                points[date][s.deviceId].append(s)
            else:
                if s.deviceId not in points[date]:
                    points[date][s.deviceId] = []
                points[date][s.deviceId].append(s)

        dict1 = OrderedDict(sorted(points.items())) 

        for day, users in dict1.items():
            for user, coordinates in users.items():
                feature_group = FeatureGroup(name=f"{day} - {user}", show=False)
                col = random.choice(color_options)
                line = []
                for p in coordinates:
                    line.append((p.latitude, p.longitude))
                    tooltip = p.timestamp
                    popup_content = f"""
            <b>Device ID: {p.deviceId}</b>
            <br>
            <p>Accuracy: {p.accuracy}</p>
            <br>
            <p>Timestamp: {p.timestamp}</p>
            <br>
            <p></p>
            """
                    folium.Circle([p.latitude, p.longitude], radius=p.accuracy, fill=True,
                                color=col, popup=popup_content, tooltip=tooltip).add_to(feature_group)

                folium.PolyLine(line, color=col).add_to(feature_group)
                feature_group.add_to(m)

        folium.LayerControl().add_to(m)

        m.save('index.html')
    else:
        print("Failed.")




def version():
    print("version")


if __name__ == '__main__':
    main()
