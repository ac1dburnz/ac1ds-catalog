#!/bin/bash

base_dir="/Users/ac1dburn/Documents/GitHub"
charts_repo="https://github.com/truecharts/charts.git"
ignored_apps=("prowlarr" "radarr" "rtorrent-rutorrent" "sabnzbd" "sonarr" "speedtest-exporter" "thelounge")

echo "Cloning or updating the truecharts/charts repository..."
# Clone the charts repository
if [ ! -d "$base_dir/charts" ]; then
  git clone "$charts_repo" "$base_dir/charts"
else
  cd "$base_dir/charts"
  git pull
fi

# Function to update ix_values.yaml
update_app() {
  local app_dir="$1"
  local app_name="$(basename "$app_dir")"
  local highest_version="$(ls -1d "$app_dir"/* | sort -V | tail -n 1)"

  if [[ ! " ${ignored_apps[*]} " =~ " ${app_name} " ]]; then
    for category in "premium" "system" "stable"; do
      charts_values="$base_dir/charts/charts/$category/$app_name/values.yaml"
      if [ -f "$charts_values" ]; then
        echo "Checking for updates in $app_name ($category)..."
        echo "Highest version: $highest_version"
        echo "Checking file: $charts_values"
        if cmp --silent "$charts_values" "$highest_version/values.yaml"; then
          echo "No updates found for $app_name in $charts_values"
        else
          echo "Updates found for $app_name in $charts_values"
          cp "$charts_values" "$highest_version/ix_values.yaml"
        fi
      fi
    done
  else
    echo "Skipping $app_name (ignored)."
  fi
}

echo "Updating apps in ac1dsworld..."
for app in "$base_dir/ac1ds-catalog/ac1dsworld"/*; do
  update_app "$app"
done

echo "Updating apps in stable..."
for app in "$base_dir/ac1ds-catalog/stable"/*; do
  update_app "$app"
done

echo "Updating apps in premium..."
for app in "$base_dir/ac1ds-catalog/premium"/*; do
  update_app "$app"
done

echo "Updating apps in system..."
for app in "$base_dir/ac1ds-catalog/system"/*; do
  update_app "$app"
done

echo "Updating apps in Test..."
for app in "$base_dir/ac1ds-catalog/Test"/*; do
  update_app "$app"
done
