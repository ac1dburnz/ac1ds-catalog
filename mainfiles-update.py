import os
import shutil
import yaml
import json
import hashlib
from packaging import version
from datetime import datetime

base_dir = "/Users/ac1dburn/Documents/GitHub/ac1ds-catalog"

def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

def increment_directory_version(version_str):
    version_parts = version_str.split('.')
    if len(version_parts) == 3:
        version_parts[2] = str(int(version_parts[2]) + 1)
        new_version_str = '.'.join(version_parts)
        return new_version_str
    else:
        raise ValueError(f"Invalid version format: {version_str}")

def find_highest_version_directory(app_dir):
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

def update_app_version(app_dir, current_version, app_name):
    try:
        new_version = increment_directory_version(current_version)
        new_version_dir = os.path.join(app_dir, new_version)
        current_version_dir = os.path.join(app_dir, current_version)
        shutil.copytree(current_version_dir, new_version_dir)
        print(f"Incremented version for {app_dir}: {new_version}")

        replace_ix_values_yaml(base_dir, app_name, new_version_dir)
        update_chart_yaml(base_dir, app_name, new_version_dir)

        return new_version
    except Exception as e:
        print(f"Error updating version for {app_dir}: {e}")
        return None

def replace_ix_values_yaml(base_dir, app_name, version_dir):
    mainfile_path = os.path.join(base_dir, "mainfiles", f"{app_name}-ix_values.yaml")
    target_ix_values_path = os.path.join(version_dir, "ix_values.yaml")
    if os.path.exists(mainfile_path):
        if os.path.exists(target_ix_values_path):
            os.remove(target_ix_values_path)
            print(f"Removed existing {target_ix_values_path}")
        shutil.copy(mainfile_path, target_ix_values_path)
        print(f"Copied {mainfile_path} to {target_ix_values_path}")
    else:
        print(f"Mainfile {mainfile_path} does not exist")

def find_app(data, app_name, specific_key=None):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == specific_key and app_name in value:
                return app_name, data[key][app_name]
            result = find_app(value, app_name, specific_key)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_app(item, app_name, specific_key)
            if result:
                return result
    return None

def update_catalog_json(base_dir, app_name, new_version):
    catalog_json_path = os.path.join(base_dir, "catalog.json")
    print(f"Catalog JSON Path: {catalog_json_path}")

    with open(catalog_json_path, 'r') as catalog_file:
        catalog_data = json.load(catalog_file)

    result = find_app(catalog_data, app_name, "ac1dsworld")
    print(f"Catalog Result: {result}")

    if result:
        app_name_actual, app_data = result
        print(f"Current app data: {app_data}")

        existing_version = app_data.get('latest_version', '')
        print(f"Existing version: {existing_version}")
        print(f"New version: {new_version}")

        if existing_version != new_version:
            print(f"New version {new_version} found. Updating catalog...")
            app_data['latest_version'] = new_version
            app_data['latest_human_version'] = f"{app_data['latest_app_version']}_{new_version}"
            app_data['last_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Updated app data: {app_data}")

            with open(catalog_json_path, 'w') as catalog_file:
                json.dump(catalog_data, catalog_file, indent=2)
                print(f"Updated {app_name_actual} to version {new_version} in {catalog_json_path}")
        else:
            print("No update required. Existing version is the same as the new version.")
    else:
        print(f"{app_name} not found in {catalog_json_path}")

def update_chart_yaml(base_dir, app_name, new_version_dir):
    chart_yaml_path = os.path.join(new_version_dir, "Chart.yaml")
    if os.path.exists(chart_yaml_path):
        with open(chart_yaml_path, "r") as chart_yaml_file:
            chart_yaml_data = yaml.safe_load(chart_yaml_file)
        
        chart_yaml_data["version"] = new_version_dir.split("/")[-1]
        
        with open(chart_yaml_path, "w") as chart_yaml_file:
            yaml.dump(chart_yaml_data, chart_yaml_file, default_flow_style=False)
        
        print(f"Updated version in Chart.yaml for {app_name} to {chart_yaml_data['version']}")
    else:
        print(f"Chart.yaml not found in {new_version_dir}")

def update_app_versions_json(base_dir, sub_dir, app_name, new_version):
    app_versions_json_path = os.path.join(base_dir, sub_dir, app_name, "app_versions.json")
    print(f"App Versions JSON Path: {app_versions_json_path}")

    if os.path.exists(app_versions_json_path):
        with open(app_versions_json_path, 'r') as app_versions_file:
            app_versions_data = json.load(app_versions_file)

        if 'latest_app_version' in app_versions_data:
            old_version = app_versions_data['latest_human_version'].split('_')[-1]
            
            # Update the version in all relevant fields
            for key in app_versions_data:
                if isinstance(app_versions_data[key], dict) and 'version' in app_versions_data[key]:
                    if app_versions_data[key]['version'] == old_version:
                        app_versions_data[key]['version'] = new_version
                        app_versions_data[key]['human_version'] = app_versions_data['latest_app_version'] + "_" + new_version
                        app_versions_data[key]['last_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        app_versions_data[key]['location'] = app_versions_data[key]['location'].replace(old_version, new_version)
            
            app_versions_data[new_version] = app_versions_data.pop(old_version)
            app_versions_data['latest_human_version'] = f"{app_versions_data['latest_app_version']}_{new_version}"
            app_versions_data['last_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(app_versions_json_path, 'w') as app_versions_file:
                json.dump(app_versions_data, app_versions_file, indent=2)
                print(f"Updated app_versions.json for {app_name} to version {new_version}")
        else:
            print("Error: 'latest_app_version' key not found in app_versions.json")
    else:
        print(f"Error: {app_versions_json_path} does not exist")

def process_app(app_name):
    mainfile_dir = os.path.join(base_dir, "mainfiles")
    app_dir = os.path.join(base_dir, "ac1dsworld", app_name)
    mainfile_path = os.path.join(mainfile_dir, f"{app_name}-ix_values.yaml")

    print(f"Mainfile path: {mainfile_path}")
    print(f"App directory: {app_dir}")

    if os.path.exists(mainfile_path) and os.path.exists(app_dir):
        print("Both mainfile and app directory exist.")
        mainfile_hash = get_file_hash(mainfile_path)
        highest_version_dir = find_highest_version_directory(app_dir)
        if highest_version_dir:
            current_app_tag_file = os.path.join(app_dir, highest_version_dir, "ix_values.yaml")
            if os.path.exists(current_app_tag_file):
                current_app_hash = get_file_hash(current_app_tag_file)
                print(f"Mainfile hash: {mainfile_hash}")
                print(f"App tag file: {current_app_tag_file}")
                print(f"App file hash: {current_app_hash}")

                if mainfile_hash != current_app_hash:
                    new_version_dir = update_app_version(app_dir, highest_version_dir, app_name)
                    print(f"New version directory: {new_version_dir}")
                else:
                    print("No update required.")
                
                # Always update the catalog version if the highest version changes
                update_catalog_json(base_dir, app_name, highest_version_dir)
        else:
            print(f"No version directories found in {app_dir}")

def main():
    apps = ["sonarr", "radarr", "lidarr"]
    for app_name in apps:
        process_app(app_name)

if __name__ == "__main__":
    main()
