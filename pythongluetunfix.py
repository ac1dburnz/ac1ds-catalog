import os
import tarfile
import re
import ruamel.yaml
import shutil

def get_latest_version_folder(path):
    if os.path.exists(path) and os.path.isdir(path):
        folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
        if folders:
            latest_version_folder = max(folders, key=lambda x: [int(i) for i in x.split('.')])
            return os.path.join(path, latest_version_folder)
    return None

def extract_version_from_filename(filename):
    match = re.match(r"common-(\d+\.\d+\.\d+).tgz", filename)
    return match.group(1) if match else None

def update_values_yaml(values_yaml_path):
    with open(values_yaml_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if 'gluetunImage:' in line:
            lines[i + 1] = '  repository: ghcr.io/ac1dburnz/gluetun\n'
            lines[i + 2] = '  tag: v3.39.0@sha256:96efd91a674827556209eeb26032445ba4acb0c129ba6c640b4de2cf4a11cbbf\n'
            lines[i + 3] = '  pullPolicy: IfNotPresent\n'

    with open(values_yaml_path, 'w') as file:
        file.writelines(lines)

def recompress_common(charts_folder, common_folder, original_tgz_file):
    common_tgz_path = os.path.join(charts_folder, original_tgz_file)

    with tarfile.open(common_tgz_path, 'w:gz') as tar:
        tar.add(common_folder, arcname='common')

# Specify the base directory
base_dir = "/Users/ac1dburn/Documents/GitHub"

# Specify the path to the "rtorrent-rutorrent" directory inside "ac1ds-catalog/ac1dsworld"
rtorrent_rutorrent_path = os.path.join(base_dir, "ac1ds-catalog", "ac1dsworld", "rtorrent-rutorrent")

# Get the latest version folder
latest_version_folder = get_latest_version_folder(rtorrent_rutorrent_path)

if latest_version_folder:
    os.chdir(latest_version_folder)
    print(f"Current working directory: {os.getcwd()}")

    charts_folder = os.path.join(latest_version_folder, "charts")
    if os.path.exists(charts_folder) and os.path.isdir(charts_folder):
        common_tgz_files = [file for file in os.listdir(charts_folder) if file.startswith("common-") and file.endswith(".tgz")]

        if common_tgz_files:
            versions = [extract_version_from_filename(file) for file in common_tgz_files]
            highest_version_file = max(zip(common_tgz_files, versions), key=lambda x: [int(i) for i in x[1].split('.')])

            common_tgz_file, highest_version = highest_version_file
            common_tgz_path = os.path.join(charts_folder, common_tgz_file)
            with tarfile.open(common_tgz_path, 'r:gz') as tar:
                tar.extractall(charts_folder)

            print(f"File '{common_tgz_file}' with version '{highest_version}' decompressed in 'charts' folder.")

            common_folder = os.path.join(charts_folder, "common")
            values_yaml_path = os.path.join(common_folder, "values.yaml")

            if os.path.exists(values_yaml_path) and os.path.isfile(values_yaml_path):
                print(f"Found 'common/values.yaml' in '{common_folder}'. Updating the file.")
                update_values_yaml(values_yaml_path)
            else:
                print(f"Error: 'common/values.yaml' not found in '{common_folder}'.")

            recompress_common(charts_folder, common_folder, common_tgz_file)
            print(f"Common folder recompressed to '{common_tgz_file}'.")

            # Remove the extracted "common" folder
            if os.path.exists(common_folder) and os.path.isdir(common_folder):
                print(f"Removing extracted 'common' folder: {common_folder}")
                shutil.rmtree(common_folder)
            else:
                print(f"Error: Extracted 'common' folder not found: {common_folder}")
        else:
            print("Error: No 'common' tgz files found.")
    else:
        print("Error: 'charts' folder not found.")
else:
    print("No version folders found.")

