import json

def find_app(data, app_name):
    if isinstance(data, dict):
        if app_name in data:
            return app_name, data[app_name]
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

def generate_output_structure(test_apps_data, ac1dsworld_apps_data, new_ac1dsworld_apps_data, premium_apps_data, system_apps_data, output_file_path):
    output_structure = {
        "charts": {},
        "Test": test_apps_data,
        "stable": ac1dsworld_apps_data,
        "ac1dsworld": new_ac1dsworld_apps_data,
        "premium": premium_apps_data,
        "system": system_apps_data,
    }

    with open(output_file_path, 'w') as output_file:
        json.dump(output_structure, output_file, indent=2)

    print(f"Output written to {output_file_path}.")

# Paths to the catalog JSON files
base_dir = "/Users/ac1dburn/Documents/GitHub"
catalog_json_path = f"{base_dir}/ac1ds-catalog/catalog.json"
updated_catalog_json_path = f"{base_dir}/ac1ds-catalog/temp/catalog.json"

# Read original catalog JSON file
with open(catalog_json_path, 'r') as catalog_file:
    catalog_data = json.load(catalog_file)

# App names to read from the "Test" section
test_app_names_to_read = ["prowlarr", "sonarr", "radarr", "rtorrent-rutorrent", "sabnzbd", "thelounge", "speedtest-exporter", "qbittorrent"]

# Find the specific app data for each app name in the "Test" section
test_apps_data = {}
for app_name in test_app_names_to_read:
    result = find_app(catalog_data["Test"], app_name)
    if result:
        app_name_actual, app_data = result
        test_apps_data[app_name_actual] = app_data

# Read "ac1dsworld" section from original catalog JSON file
ac1dsworld_app_names_to_read = ["prowlarr", "sonarr", "radarr", "sabnzbd", "rtorrent-rutorrent", "thelounge", "speedtest-exporter"]
ac1dsworld_apps_data = {}
for app_name in ac1dsworld_app_names_to_read:
    result = find_app(catalog_data["ac1dsworld"], app_name)
    if result:
        app_name_actual, app_data = result
        ac1dsworld_apps_data[app_name_actual] = app_data

# Read "ac1dsworld" section from updated catalog JSON file
with open(updated_catalog_json_path, 'r') as updated_catalog_file:
    updated_catalog_data = json.load(updated_catalog_file)

new_ac1dsworld_app_names_to_read = ["prowlarr", "sonarr", "radarr", "sabnzbd", "rtorrent-rutorrent", "thelounge", "speedtest-exporter"]
new_ac1dsworld_apps_data = {}
for app_name in new_ac1dsworld_app_names_to_read:
    result = find_app(updated_catalog_data["stable"], app_name)
    if result:
        app_name_actual, app_data = result
        new_ac1dsworld_apps_data[app_name_actual] = app_data

# Read "premium" section from updated catalog JSON file
premium_app_names_to_read = ["authelia", "blocky", "clusterissuer", "custom-app", "grafana", "metallb-config", "nextcloud", "prometheus", "traefik", "vaultwarden"]
premium_apps_data = {}
for app_name in premium_app_names_to_read:
    result = find_app(updated_catalog_data["premium"], app_name)
    if result:
        app_name_actual, app_data = result
        premium_apps_data[app_name_actual] = app_data

# Read "system" section from updated catalog JSON file
system_app_names_to_read = ["cert-manager", "cloudnative-pg", "grafana-agent-operator", "kubeapps", "kubernetes-reflector", "metallb", "openebs", "prometheus-operator", "snapshot-controller", "traefik-crds", "velero", "volsync", "volumesnapshots"]
system_apps_data = {}
for app_name in system_app_names_to_read:
    result = find_app(updated_catalog_data["system"], app_name)
    if result:
        app_name_actual, app_data = result
        system_apps_data[app_name_actual] = app_data

# Output file path
output_file_path = f"{base_dir}/ac1ds-catalog/catalog.json"

# Generate the output structure and write to file
generate_output_structure(test_apps_data, ac1dsworld_apps_data, new_ac1dsworld_apps_data, premium_apps_data, system_apps_data, output_file_path)
