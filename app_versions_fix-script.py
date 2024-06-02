import os
import json
from packaging import version

base_dir = "/Users/ac1dburn/Documents/GitHub/ac1ds-catalog"
ignored_apps = ["prowlarr", "rtorrent-rutorrent", "sabnzbd", "sonarr", "speedtest-exporter", "thelounge", "traefik"]
ignored_dirs = ["mainfiles"]

def find_highest_version(app_dir):
    app_versions_path = os.path.join(app_dir, "app_versions.json")
    if os.path.exists(app_versions_path):
        with open(app_versions_path, "r") as file:
            app_versions = json.load(file)
            return find_highest_version_from_dict(app_versions)
    return ""

def find_highest_version_from_dict(app_versions):
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

    highest_version = find_highest_version_from_dict(app_versions)
    if highest_version:
        new_version = increment_version(highest_version)
        latest_version_data = app_versions[highest_version]
        latest_version_data["human_version"] = f"2.52.0_{new_version}"
        latest_version_data["version"] = new_version
        app_versions[new_version] = latest_version_data

        with open(app_versions_path, "w") as file:
            json.dump(app_versions, file, indent=2)

        print(f"Updated app_versions.json for {app_name} with new version {new_version}")
    else:
        print(f"No versions found in the app_versions.json file for {app_name}")

def main():
    for dir_name in os.listdir(base_dir):
        parent_dir_path = os.path.join(base_dir, dir_name)
        if os.path.isdir(parent_dir_path) and dir_name not in ignored_dirs:
            for sub_dir_name in os.listdir(parent_dir_path):
                sub_dir_path = os.path.join(parent_dir_path, sub_dir_name)
                if os.path.isdir(sub_dir_path) and sub_dir_name not in ignored_apps:
                    app_dir_path = os.path.join(sub_dir_path)
                    versions_dir = os.path.join(app_dir_path, find_highest_version(app_dir_path))
                    if versions_dir:
                        print(f"Processing app directory: {sub_dir_name}")
                        update_app_versions_json(versions_dir, sub_dir_name)

if __name__ == "__main__":
    main()
