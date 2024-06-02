import os
import json
from packaging import version

base_dir = "/Users/ac1dburn/Documents/GitHub"
ignored_apps = ["prowlarr", "radarr", "rtorrent-rutorrent", "sabnzbd", "sonarr", "speedtest-exporter", "thelounge", "traefik"]

def find_highest_version(app_versions):
    highest_version = ""
    for version_str in app_versions.keys():
        try:
            version_obj = version.parse(version_str)
            if not highest_version or version_obj > version.parse(highest_version):
                highest_version = version_str
        except version.InvalidVersion:
            pass
    return highest_version

def increment_version(version_str):
    version_obj = version.parse(version_str)
    new_version = version.Version(f"{version_obj.major}.{version_obj.minor}.{version_obj.micro + 1}")
    return str(new_version)

def update_app_versions_json(app_dir, app_name):
    app_versions_path = os.path.join(app_dir, "app_versions.json")
    if os.path.exists(app_versions_path):
        with open(app_versions_path, "r") as file:
            app_versions = json.load(file)
    else:
        app_versions = {}

    highest_version = find_highest_version(app_versions)
    if highest_version:
        new_version = increment_version(highest_version)
        latest_version_data = app_versions[highest_version]
        latest_version_data["human_version"] = f"2.52.0_{new_version}"
        latest_version_data["version"] = new_version
        app_versions[new_version] = latest_version_data

        with open(app_versions_path, "w") as file:
            json.dump(app_versions, file, indent=2)

        print(f"Updated app_versions.json for {app_name} with new version {new_version}")

def main():
    for app_dir in os.listdir(base_dir):
        app_dir_path = os.path.join(base_dir, app_dir)
        if os.path.isdir(app_dir_path) and app_dir not in ignored_apps:
            update_app_versions_json(app_dir_path, app_dir)

if __name__ == "__main__":
    main()
