import os
import shutil
import yaml
import json
from packaging import version

# Define base_dir as a global variable
base_dir = "/Users/ac1dburn/Documents/GitHub/ac1ds-catalog"

def get_image_tag(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        image_tag = data.get('image', {}).get('tag', '')
        return image_tag

def extract_version_and_revision_from_tag(tag):
    version_str = tag.split('@')[0]
    version_parts = version_str.split('-')
    if len(version_parts) == 2:
        return version_parts[0], version_parts[1]
    else:
        raise ValueError(f"Invalid tag format: {tag}")

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

def update_app_version(app_dir, current_version):
    try:
        new_version = increment_directory_version(current_version)
        new_version_dir = os.path.join(app_dir, new_version)
        current_version_dir = os.path.join(app_dir, current_version)
        shutil.copytree(current_version_dir, new_version_dir)
        print(f"Incremented version for {app_dir}: {new_version}")

        # Update app_versions.json
        update_app_versions_json(app_dir, "rtorrent-rutorrent", new_version)

        # Replace ix_values.yaml
        replace_ix_values_yaml(base_dir, "rtorrent-rutorrent", new_version_dir)

        # Update Chart.yaml
        update_chart_yaml(base_dir, "rtorrent-rutorrent", new_version_dir)

    except Exception as e:
        print(f"Error updating version for {app_dir}: {e}")

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

def find_highest_version_from_dict(app_versions):
    highest_version = ""
    for version_str in app_versions.keys():
        try:
            version_obj = version.parse(version_str)
            if not highest_version:
                highest_version = version_str
            elif version_obj > version.parse(highest_version):
                highest_version = version_str
        except version.InvalidVersion:
            pass
    return highest_version

def increment_version(version_str):
    version_obj = version.parse(version_str)
    new_version = version.Version(f"{version_obj.major}.{version_obj.minor}.{version_obj.micro + 1}")
    return str(new_version)

def update_versions_recursively(data, old_version, new_version):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "version" and value == old_version:
                data[key] = new_version
            if isinstance(value, (dict, list)):
                update_versions_recursively(value, old_version, new_version)
    elif isinstance(data, list):
        for item in data:
            update_versions_recursively(item, old_version, new_version)

def update_app_versions_json(app_dir, app_name, new_version):
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
        return new_version
    else:
        print(f"No versions found in app_versions.json for {app_name}")
        return None

def update_catalog_json(base_dir, app_name, new_version):
    catalog_json_path = os.path.join(base_dir, "ac1ds-catalog", "catalog.json")
    with open(catalog_json_path, 'r') as catalog_file:
        catalog_data = json.load(catalog_file)

    # Find and update the app data in the catalog
    result = find_app(catalog_data, app_name)
    if result:
        app_name_actual, app_data = result
        app_data['version'] = new_version

        # Write the updated catalog back to the file
        with open(catalog_json_path, 'w') as catalog_file:
            json.dump(catalog_data, catalog_file, indent=2)
        print(f"Updated {app_name_actual} to version {new_version} in {catalog_json_path}")
    else:
        print(f"{app_name} not found in {catalog_json_path}")

def update_chart_yaml(base_dir, app_name, new_version_dir):
    chart_yaml_path = os.path.join(new_version_dir, "Chart.yaml")
    if os.path.exists(chart_yaml_path):
        with open(chart_yaml_path, "r") as chart_yaml_file:
            chart_yaml_data = yaml.safe_load(chart_yaml_file)
        
        # Update the version in Chart.yaml
        chart_yaml_data["version"] = new_version_dir.split("/")[-1]
        
        # Write the updated Chart.yaml back to the file
        with open(chart_yaml_path, "w") as chart_yaml_file:
            yaml.dump(chart_yaml_data, chart_yaml_file, default_flow_style=False)
        
        print(f"Updated version in Chart.yaml for {app_name} to {chart_yaml_data['version']}")
    else:
        print(f"Chart.yaml not found in {new_version_dir}")

def main():
    base_dir = "/Users/ac1dburn/Documents/GitHub/ac1ds-catalog"
    mainfile_dir = os.path.join(base_dir, "mainfiles")
    rtorrent_rutorrent_dir = os.path.join(base_dir, "ac1dsworld", "rtorrent-rutorrent")
    mainfile_path = os.path.join(mainfile_dir, "rtorrent-rutorrent-ix_values.yaml")
    app_dir = rtorrent_rutorrent_dir
    print(f"Mainfile path: {mainfile_path}")
    print(f"App directory: {app_dir}")
    if os.path.exists(mainfile_path) and os.path.exists(app_dir):
        print("Both mainfile and app directory exist.")
        mainfile_tag = get_image_tag(mainfile_path)
        print(f"Mainfile tag: {mainfile_tag}")
        highest_version_dir = find_highest_version_directory(app_dir)
        if highest_version_dir:
            current_app_tag_file = os.path.join(app_dir, highest_version_dir, "ix_values.yaml")
            if os.path.exists(current_app_tag_file):
                current_app_tag = get_image_tag(current_app_tag_file)
                print(f"App tag file: {current_app_tag_file}")
                print(f"App tag: {current_app_tag}")
                if mainfile_tag and current_app_tag:
                    mainfile_version, mainfile_revision = extract_version_and_revision_from_tag(mainfile_tag)
                    app_version, app_revision = extract_version_and_revision_from_tag(current_app_tag)
                    print(f"Version in mainfile rtorrent-rutorrent: {mainfile_version}-{mainfile_revision}")
                    print(f"Version in app directory rtorrent-rutorrent: {app_version}-{app_revision}")
                    if mainfile_version != app_version or mainfile_revision != app_revision:
                        new_version_dir = update_app_version(app_dir, highest_version_dir)
                        if new_version_dir:
                            new_version = update_app_versions_json(new_version_dir, "rtorrent-rutorrent", highest_version_dir)
                            if new_version:
                                update_catalog_json(base_dir, "rtorrent-rutorrent", new_version)
                    else:
                        print("No update required.")
            else:
                print(f"App tag file does not exist: {current_app_tag_file}")
        else:
            print("No version directories found in app directory.")
    else:
        print("Either mainfile or app directory does not exist.")

if __name__ == "__main__":
    main()
