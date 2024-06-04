import os
import shutil
import json
from packaging import version
from datetime import datetime

base_dir = "/Users/ac1dburn/Documents/GitHub/ac1ds-catalog"
ignored_dirs = set()  # Add any directories to ignore if needed
ignored_apps = set()  # Add any apps to ignore if needed

def increment_version(version_str):
    version_parts = version_str.split('.')
    if len(version_parts) == 3:
        version_parts[2] = str(int(version_parts[2]) + 1)
        return '.'.join(version_parts)
    else:
        raise ValueError(f"Invalid version format: {version_str}")

def find_highest_version_from_dict(version_dict):
    highest_version = None
    for key in version_dict:
        try:
            key_version = version.parse(key)
            if highest_version is None or key_version > highest_version:
                highest_version = key_version
        except version.InvalidVersion:
            continue
    return str(highest_version) if highest_version else None

def find_highest_version(app_dir):
    highest_version = None
    for entry in os.listdir(app_dir):
        entry_path = os.path.join(app_dir, entry)
        if os.path.isdir(entry_path):
            try:
                entry_version = version.parse(entry)
                if highest_version is None or entry_version > highest_version:
                    highest_version = entry_version
            except version.InvalidVersion:
                continue
    return str(highest_version) if highest_version else None

def update_versions_recursively(data, old_version, new_version):
    for key, value in data.items():
        if isinstance(value, dict):
            update_versions_recursively(value, old_version, new_version)
        elif isinstance(value, str) and old_version in value:
            data[key] = value.replace(old_version, new_version)

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

        # Update all version fields in the app_versions dictionary
        update_versions_recursively(app_versions, highest_version, new_version)

        # Sort the dictionary keys in descending order
        sorted_app_versions = dict(sorted(app_versions.items(), key=lambda x: version.parse(x[0]), reverse=True))

        with open(app_versions_path, "w") as file:
            json.dump(sorted_app_versions, file, indent=2)

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
