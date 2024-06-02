import os
import json
from packaging import version

base_dir = "/Users/ac1dburn/Documents/GitHub"
ignored_apps = ["prowlarr", "radarr", "rtorrent-rutorrent", "sabnzbd", "sonarr", "speedtest-exporter", "thelounge", "traefik"]

def find_highest_version(app_dir):
    highest_version = ""
    for dir_name in os.listdir(app_dir):
        dir_path = os.path.join(app_dir, dir_name)
        if os.path.isdir(dir_path):
            version_str = dir_name.split("-")[-1]
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

def update_app_versions_json(app_dir, app_name, highest_version, human_version):
    app_versions_path = os.path.join(app_dir, "app_versions.json")
    if os.path.exists(app_versions_path):
        with open(app_versions_path, "r") as file:
            app_versions = json.load(file)
    else:
        app_versions = {}

    new_version = increment_version(highest_version)
    app_versions[new_version] = {
        "human_version": human_version,
        "version": new_version,
        # Add any other metadata you want to include for this version
    }

    with open(app_versions_path, "w") as file:
        json.dump(app_versions, file, indent=2)

    print(f"Updated app_versions.json for {app_name} with new version {new_version}")

def main():
    for app_dir in os.listdir(base_dir):
        app_dir_path = os.path.join(base_dir, app_dir)
        if os.path.isdir(app_dir_path) and app_dir not in ignored_apps:
            app_versions_path = os.path.join(app_dir_path, "app_versions.json")
            if os.path.exists(app_versions_path):
                highest_version = find_highest_version(app_dir_path)
                if highest_version:
                    # Assuming you have a way to get the human_version for the app
                    human_version = "2.52.0_18.2.9"  # Replace with the actual human_version
                    update_app_versions_json(app_dir_path, app_dir, highest_version, human_version)

if __name__ == "__main__":
    main()

