#!/bin/bash

base_dir="/Users/ac1dburn/Documents/GitHub"
charts_repo="https://github.com/truecharts/charts.git"
ignored_apps=("prowlarr" "radarr" "rtorrent-rutorrent" "sabnzbd" "sonarr" "speedtest-exporter" "thelounge")

# Generate a branch name with current date and time
branch_name="branch_$(date +'%Y%m%d%H%M%S')"

# Go to directory
cd "$base_dir/ac1ds-catalog"

# Ensure on main branch before creating new one
echo "Checking out main branch and pulling latest changes..."
git checkout main
git pull origin main

# Create and switch to new branch
echo "Creating new branch: $branch_name"
git checkout -b "$branch_name"

# Remove existing temp directory if exists
if [ -d temp ]; then
  echo "Removing existing temp directory..."
  sudo rm -r temp
fi

# Create new temp directory
echo "Creating new temp directory..."
mkdir temp

# Clone catalog into temp directory
echo "Cloning truecharts/catalog repository into temp directory..."
git clone https://github.com/truecharts/catalog.git temp

echo "Cloning or updating the truecharts/charts repository..."
# Clone the charts repository
if [ ! -d "$base_dir/charts" ]; then
  git clone "$charts_repo" "$base_dir/charts"
else
  cd "$base_dir/charts"
  git pull
fi

# Function to update ix_values.yaml and increment version
update_app() {
  local app_dir="$1"
  local app_name="$(basename "$app_dir")"
  local latest_version="$(ls -1d "$app_dir"/* | sort -V | tail -n 1)"
  local new_version="$(echo "$latest_version" | awk -F'/' '{print $NF+1}')"

  if [[ ! " ${ignored_apps[*]} " =~ " ${app_name} " ]]; then
    charts_values="$base_dir/charts/$app_name/values.yaml"
    if [ -f "$charts_values" ]; then
      echo "Updating $app_name from $latest_version to $new_version..."
      mkdir -p "$app_dir/$new_version"
      cp -r "$latest_version"/* "$app_dir/$new_version"
      cp "$charts_values" "$app_dir/$new_version/ix_values.yaml"
    else
      echo "No updates found for $app_name."
    fi
  else
    echo "Skipping $app_name (ignored)."
  fi
}

# Copy apps from ac1dsworld to stable
if [ "$latest" != "$(ls -1 "$base_dir/ac1ds-catalog/ac1dsworld/$app" | sort -V | tail -n 1)" ]; then
  for app in "${ignored_apps[@]}"; do
    echo "Copying $app from ac1dsworld to stable..."
    cp -R "$base_dir/ac1ds-catalog/ac1dsworld/$app" "$base_dir/ac1ds-catalog/stable"
  done
fi

# Copy apps from temp stable to ac1dsworld
if [ "$latest" != "$(ls -1 "$base_dir/ac1ds-catalog/temp/stable/$app" | sort -V | tail -n 1)" ]; then
  for app in "${ignored_apps[@]}"; do
    echo "Copying $app from temp/stable to ac1dsworld..."
    cp -R "$base_dir/ac1ds-catalog/temp/stable/$app" "$base_dir/ac1ds-catalog/ac1dsworld"
  done
fi

# Copy apps from temp/premium to ac1dsworld/premium
for app in authelia blocky clusterissuer custom-app grafana metallb-config nextcloud prometheus traefik vaultwarden; do
  echo "Copying $app from temp/premium to ac1dsworld/premium..."
  mkdir -p "$

base_dir/ac1ds-catalog/premium/$app"
  cp -R "$base_dir/ac1ds-catalog/temp/premium/$app"/* "$base_dir/ac1ds-catalog/premium/$app"
done

# Copy apps from temp/system to ac1dsworld/system
for app in cert-manager cloudnative-pg grafana-agent-operator kubeapps kubernetes-reflector metallb openebs prometheus-operator snapshot-controller traefik-crds velero volsync volumesnapshots; do
  echo "Copying $app from temp/system to ac1dsworld/system..."
  mkdir -p "$base_dir/ac1ds-catalog/system/$app"
  cp -R "$base_dir/ac1ds-catalog/temp/system/$app"/* "$base_dir/ac1ds-catalog/system/$app"
done

# Copy apps from ac1dsworld to test
if [ "$latest" != "$(ls -1 "$base_dir/ac1ds-catalog/ac1dsworld/$app" | sort -V | tail -n 1)" ]; then
  for app in rtorrent-rutorrent; do
    echo "Copying $app from ac1dsworld to Test..."
    cp -R "$base_dir/ac1ds-catalog/ac1dsworld/$app" "$base_dir/ac1ds-catalog/Test"
  done
fi

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

# Remove unwanted files ac1dsworld
for app in "${ignored_apps[@]}"; do
  echo "Removing unwanted files from $app in ac1dsworld..."
  cd "$base_dir/ac1ds-catalog/ac1dsworld/$app"
  rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')
done

# Remove unwanted files Test
for app in "${ignored_apps[@]}"; do
  echo "Removing unwanted files from $app in Test..."
  cd "$base_dir/ac1ds-catalog/Test/$app"
  rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')
done

# Update ix_values.yaml for ac1dsworld
for app in "${ignored_apps[@]}"; do
  echo "Updating ix_values.yaml for $app in ac1dsworld..."
  cd "$base_dir/ac1ds-catalog/ac1dsworld/$app"
  cd "$(ls -1d */ | sort -V | tail -n 1)"

  # Check if mainfiles file exists
  if [ -f "$base_dir/ac1ds-catalog/mainfiles/${app}-ix_values.yaml" ]; then
    rm ix_values.yaml
    cp "$base_dir/ac1ds-catalog/mainfiles/${app}-ix_values.yaml" ix_values.yaml
  fi
done

# Update ix_values.yaml for Test
for app in "${ignored_apps[@]}"; do
  echo "Updating ix_values.yaml for $app in Test..."
  cd "$base_dir/ac1ds-catalog/Test/$app"
  cd "$(ls -1d */ | sort -V | tail -n 1)"

  # Check if mainfiles file exists for test
  if [ -f "$basedir/ac1ds-catalog/mainfiles/${app}_Test_ix_values.yaml" ]; then
    rm ix_values.yaml
    cp "$base_dir/ac1ds-catalog/mainfiles/${app}_Test_ix_values.yaml" ix_values.yaml
  fi
done

# Copy catalog.json
echo "Copying catalog.json to catalog-temp.json..."
cp "$base_dir/ac1ds-catalog/catalog.json" "$base_dir/ac1ds-catalog/catalog-temp.json"

# Run catalog update script
echo "Running catalog update script..."
python3 "$base_dir/ac1ds-catalog/catalogupdate.py"

# Remove temp directory
echo "Removing temp directory..."
sudo rm -r "$base_dir/ac1ds-catalog/temp"

# Run catalog fix script
echo "Running catalog fix script..."
# Add the command to run the catalog fix script here

echo "Update process completed."