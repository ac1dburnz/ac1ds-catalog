import os
import shutil
import subprocess
import filecmp
import json
from packaging import version

base_dir = "/Users/ac1dburn/Documents/GitHub"
charts_repo = "https://github.com/truecharts/charts.git"
ignored_apps = ["prowlarr", "radarr", "rtorrent-rutorrent", "sabnzbd", "sonarr", "speedtest-exporter", "thelounge"]
catalog_path = os.path.join(base_dir, "ac1ds-catalog", "catalog.json")

def clone_or_update_charts_repo():
    """Clone the charts repository if it doesn't exist, or update it if it does."""
    charts_dir = os.path.join(base_dir, "charts")
    if not os.path.exists(charts_dir):
        subprocess.run(["git", "clone", charts_repo, charts_dir])
    else:
        subprocess.run(["git", "pull"], cwd=charts_dir)

def find_highest_version(app_dir):
    """Find the highest version directory within an app directory."""
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
    """Increment the micro part of the version string."""
    version_obj = version.parse(version_str)
    new_version = version.Version(f"{version_obj.major}.{version_obj.minor}.{version_obj.micro + 1}")
    return str(new_version)

def remove_old_versions(app_dir, highest_version):
    """Remove all version directories except the highest version."""
    for dir_name in os.listdir(app_dir):
        dir_path = os.path.join(app_dir, dir_name)
        if os.path.isdir(dir_path) and dir_name != highest_version:
            shutil.rmtree(dir_path)

def update_chart_yaml(new_version_dir, new_version):
    """Update the version in the Chart.yaml file."""
    chart_yaml_path = os.path.join(new_version_dir, "Chart.yaml")
    with open(chart_yaml_path, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith("version:"):
            lines[i] = f"version: {new_version}\n"
            break

    with open(chart_yaml_path, "w") as file:
        file.writelines(lines)

def load_catalog():
    """Load the catalog.json file."""
    with open(catalog_path, "r") as file:
        return json.load(file)

def save_catalog(catalog):
    """Save the catalog.json file."""
    with open(catalog_path, "w") as file:
        json.dump(catalog, file, indent=2)

def update_catalog(catalog, app_name, new_version):
    """Update the catalog.json with the new version."""
    for category in catalog.values():
        if app_name in category:
            category[app_name]["latest_version"] = new_version
            latest_app_version = category[app_name].get("latest_app_version", "")
            category[app_name]["latest_human_version"] = f"{latest_app_version}_{new_version}"
            break

def update_app(app_dir, app_name, highest_version, catalog):
    """Update the app if there are changes in the values.yaml file."""
    if app_name in ignored_apps:
        print(f"Skipping {app_name} (ignored).")
        return

    for category in ["premium", "system", "stable"]:
        charts_values = os.path.join(base_dir, "charts", "charts", category, app_name, "values.yaml")
        if os.path.exists(charts_values):
            print(f"Checking for updates in {app_name} ({category})...")
            if not highest_version:
                print(f"No versions found for {app_name}")
                continue

            if filecmp.cmp(charts_values, os.path.join(app_dir, highest_version, "values.yaml")):
                print(f"No updates found for {app_name} in {charts_values}")
            else:
                print(f"Updates found for {app_name} in {charts_values}")
                shutil.copy2(charts_values, os.path.join(app_dir, highest_version, "ix_values.yaml"))

                # Check if the ix_values.yaml file has been modified
                ix_values_path = os.path.join(app_dir, highest_version, "ix_values.yaml")
                git_diff_cmd = ["git", "diff", "--quiet", ix_values_path]
                git_diff_result = subprocess.run(git_diff_cmd, cwd=os.path.join(base_dir, "ac1ds-catalog"), capture_output=True)

                if git_diff_result.returncode == 0:
                    print(f"No updates found for {app_name} in {ix_values_path}")
                else:
                    new_version = increment_version(highest_version)
                    new_version_dir = os.path.join(app_dir, new_version)
                    os.makedirs(new_version_dir, exist_ok=True)
                    highest_version_dir = os.path.join(app_dir, highest_version)
                    for item in os.listdir(highest_version_dir):
                        src = os.path.join(highest_version_dir, item)
                        dst = os.path.join(new_version_dir, item)
                        if os.path.isdir(src):
                            shutil.copytree(src, dst)
                        else:
                            shutil.copy2(src, dst)
                    print(f"Incremented version for {app_name}: {new_version}")
                    remove_old_versions(app_dir, new_version)
                    update_chart_yaml(new_version_dir, new_version)
                    update_catalog(catalog, app_name, new_version)

def main():
    """Main function to clone/update the repository and process each app."""
    print("Cloning or updating the truecharts/charts repository...")
    clone_or_update_charts_repo()

    catalog = load_catalog()

    for category in ["ac1dsworld", "stable", "premium", "system", "Test"]:
        category_dir = os.path.join(base_dir, "ac1ds-catalog", category)
        print(f"Updating apps in {category}...")
        if os.path.exists(category_dir):
            for app_name in os.listdir(category_dir):
                app_dir = os.path.join(category_dir, app_name)
                if os.path.isdir(app_dir):
                    highest_version = find_highest_version(app_dir)
                    update_app(app_dir, app_name, highest_version, catalog)

    save_catalog(catalog)

if __name__ == "__main__":
    main()

