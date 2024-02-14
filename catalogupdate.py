import json

def find_app(data, app_name):
    if isinstance(data, dict):
        if app_name in data:
            return {app_name: data[app_name]}
        else:
            for key, value in data.items():
                result = find_app(value, app_name)
                if result:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_app(item, app_name)
            if result:
                return result
    return None

def generate_output_structure(apps_data, output_file_path):
    output_structure = {
        "charts": {},
        "ac1dsworld": apps_data,
    }

    with open(output_file_path, 'w') as output_file:
        json.dump(output_structure, output_file, indent=2)

    print(f"Output written to {output_file_path}.")

# Path to the catalog JSON file
catalog_json_path = "/Users/ac1dburn/Documents/GitHub/catalog/catalog.json"

# Read catalog JSON file
with open(catalog_json_path, 'r') as catalog_file:
    catalog_data = json.load(catalog_file)

# App names to read
app_names_to_read = ["prowlarr", "sonarr", "radarr", "sabnzbd", "rtorrent-rutorrent"]

# Find the specific app data for each app name
apps_data = {}
for app_name in app_names_to_read:
    app_data = find_app(catalog_data, app_name)
    if app_data:
        apps_data.update(app_data)

# Output file path
output_file_path = "/Users/ac1dburn/Documents/GitHub/ac1ds-catalog/output.json"

# Generate the output structure and write to file
generate_output_structure(apps_data, output_file_path)

