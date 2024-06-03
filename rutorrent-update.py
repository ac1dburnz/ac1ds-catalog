import os
import shutil
import yaml
from packaging import version

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
        return new_version_dir
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
                            replace_ix_values_yaml(base_dir, "rtorrent-rutorrent", new_version_dir)
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
    main()
