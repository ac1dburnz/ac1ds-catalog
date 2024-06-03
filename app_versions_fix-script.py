import os
import json
from packaging import version

base_dir = "/Users/ac1dburn/Documents/GitHub/ac1ds-catalog"
ignored_apps = ["prowlarr", "rtorrent-rutorrent", "sabnzbd", "sonarr", "speedtest-exporter", "thelounge", "traefik"]
ignored_dirs = ["mainfiles"]

def find_highest_version(app_dir):
    highest_version = ""
    for item in os.listdir(app_dir):
        item_path = os.path.join(app_dir, item)
        if os.path.isdir(item_path):
            try:
                version_obj = version.parse(item)
                if not highest_version:
                    highest_version = item
                elif version_obj > version.parse(highest_version):
                    highest_version = item
            except version.InvalidVersion:
                pass
    return highest_version

def find_highest_version_from_dict(app_versions):
    highest_version = ""
    for version_str in app_versions.keys():
        try:
            version_obj = version.parse(version_str)
            print(f"Parsed version: {version_obj}")
            if not highest_version:
                highest_version = version_str
                print(f"Setting highest_version to: {highest_version}")
            elif version_obj > version.parse(highest_version):
                highest_version = version_str
                print(f"Updating highest_version to: {highest_version}")
        except version.InvalidVersion:
            print(f"Invalid version string: {version_str}")
            pass
    print(f"Returning highest_version: {highest_version}")
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
        print(f"Current highest version for {app_name}: {highest_version}")
        new_version = increment_version(highest_version)
        latest_version_data = app_versions.pop(highest_version)
        
        # Get the current human_version
        current_human_version = latest_version_data.get("human_version", "")
        
        # Increment the human_version based on the new_version
        if current_human_version:
            version_parts = current_human_version.split("_")
            if len(version_parts) == 2:
                prefix, old_version = version_parts
                latest_version_data["human_version"] = f"{prefix}_{new_version}"
            else:
                print(f"Warning: Invalid human_version format for {app_name}: {current_human_version}")
        else:
            print(f"Warning: No human_version found for {app_name} in app_versions.json")
        
        latest_version_data["version"] = new_version
        app_versions[new_version] = latest_version_data

        # Sort the dictionary keys in descending order
        sorted_app_versions = dict(sorted(app_versions.items(), key=lambda x: version.parse(x[0]), reverse=True))

        with open(app_versions_path, "w") as file:
            json.dump(app_versions, file, indent=2)

        print(f"Updated app_versions.json for {app_name} with new version {new_version}")
    else:
        print(f"No versions found in app_versions.json for {app_name}")

def main():
    print(f"Base directory: {base_dir}")
    for dir_name in os.listdir(base_dir):
        parent_dir_path = os.path.join(base_dir, dir_name)
        if os.path.isdir(parent_dir_path) and dir_name not in ignored_dirs:
            for sub_dir_name in os.listdir(parent_dir_path):
                sub_dir_path = os.path.join(parent_dir_path, sub_dir_name)
                if os.path.isdir(sub_dir_path) and sub_dir_name not in ignored_apps:
                    app_dir_path = os.path.join(sub_dir_path)
                    versions_dir = find_highest_version(app_dir_path)
                    if versions_dir:
                        app_versions_path = os.path.join(app_dir_path, "app_versions.json")
                        if os.path.exists(app_versions_path):
                            with open(app_versions_path, "r") as file:
                                app_versions = json.load(file)
                                print(f"Contents of {app_versions_path} (first 20 lines):")
                                for i, line in enumerate(json.dumps(app_versions, indent=2).split("\n"), start=1):
                                    print(line)
                                    if i >= 20:
                                        print("... (truncated)")
                                        break
                            highest_version_in_json = find_highest_version_from_dict(app_versions)
                            print(f"App: {sub_dir_name}")
                            print(f"Highest version in app_versions.json: {highest_version_in_json}")
                            print(f"Highest version directory: {versions_dir}")
                            if highest_version_in_json != versions_dir:
                                print(f"New version found: {versions_dir}")
                                print(f"Processing app directory: {sub_dir_name}")
                                update_app_versions_json(app_dir_path, sub_dir_name)
                            else:
                                print(f"No new version found for {sub_dir_name}")
                        else:
                            print(f"app_versions.json not found at: {app_versions_path}")
                    else:
                        print(f"No versions found for app: {sub_dir_name}")

if __name__ == "__main__":
    main()

