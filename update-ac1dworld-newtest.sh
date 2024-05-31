#!/bin/bash

base_dir="/Users/ac1dburn/Documents/GitHub"

# Generate a branch name with current date and time
branch_name="branch_$(date +'%Y%m%d%H%M%S')"

# Go to directory
cd "$base_dir/ac1ds-catalog"

# Ensure on main branch before creating new one
git checkout main
git pull origin main

# Create and switch to new branch
git checkout -b "$branch_name"

# Remove existing temp directory if exists
if [ -d temp ]; then
  sudo rm -r temp
fi

# Create new temp directory
mkdir temp

# Clone catalog into temp directory
git clone https://github.com/truecharts/catalog.git temp

# Copy apps from ac1dsworld to stable
for app in prowlarr radarr rtorrent-rutorrent sabnzbd sonarr speedtest-exporter thelounge; do
  latest_version=$(ls -1 "$base_dir/ac1ds-catalog/ac1dsworld/$app" | sort -V | tail -n 1)
  if [ "$latest_version" != "$(ls -1 "$base_dir/ac1ds-catalog/stable/$app" | sort -V | tail -n 1)" ]; then
    cp -R "$base_dir/ac1ds-catalog/ac1dsworld/$app/$latest_version" "$base_dir/ac1ds-catalog/stable/$app"
  fi
done

# Copy apps from temp stable to ac1dsworld
for app in prowlarr radarr rtorrent-rutorrent sabnzbd sonarr speedtest-exporter thelounge; do
  latest_version=$(ls -1 "$base_dir/ac1ds-catalog/temp/stable/$app" | sort -V | tail -n 1)
  if [ "$latest_version" != "$(ls -1 "$base_dir/ac1ds-catalog/ac1dsworld/$app" | sort -V | tail -n 1)" ]; then
    cp -R "$base_dir/ac1ds-catalog/temp/stable/$app/$latest_version" "$base_dir/ac1ds-catalog/ac1dsworld/$app"
  fi
done

# Copy apps from temp/premium to ac1dsworld/premium
for app in authelia blocky clusterissuer custom-app grafana metallb-config nextcloud prometheus traefik vaultwarden; do
  latest_version=$(ls -1 "$base_dir/ac1ds-catalog/temp/premium/$app" | sort -V | tail -n 1)
  if [ -n "$latest_version" ]; then
    mkdir -p "$base_dir/ac1ds-catalog/premium/$app"
    cp -R "$base_dir/ac1ds-catalog/temp/premium/$app/$latest_version" "$base_dir/ac1ds-catalog/premium/$app"
  else
    echo "Application $app not found in temp/premium directory"
  fi
done

# Copy apps from temp/system to ac1dsworld/system
for app in cert-manager cloudnative-pg grafana-agent-operator kubeapps kubernetes-reflector metallb openebs prometheus-operator snapshot-controller traefik-crds velero volsync volumesnapshots; do
  latest_version=$(ls -1 "$base_dir/ac1ds-catalog/temp/system/$app" | sort -V | tail -n 1)
  if [ -n "$latest_version" ]; then
    mkdir -p "$base_dir/ac1ds-catalog/system/$app"
    cp -R "$base_dir/ac1ds-catalog/temp/system/$app/$latest_version" "$base_dir/ac1ds-catalog/system/$app"
  else
    echo "Application $app not found in temp/system directory"
  fi
done

# Copy apps from ac1dsworld to Test
for app in rtorrent-rutorrent; do
  latest_version=$(ls -1 "$base_dir/ac1ds-catalog/ac1dsworld/$app" | sort -V | tail -n 1)


# Copy apps from ac1dsworld to Test
for app in rtorrent-rutorrent; do
  latest_version=$(ls -1 "$base_dir/ac1ds-catalog/ac1dsworld/$app" | sort -V | tail -n 1)
  if [ "$latest_version" != "$(ls -1 "$base_dir/ac1ds-catalog/Test/$app" | sort -V | tail -n 1)" ]; then
    cp -R "$base_dir/ac1ds-catalog/ac1dsworld/$app/$latest_version" "$base_dir/ac1ds-catalog/Test/$app"
  fi
done

# Remove unwanted files ac1dsworld
for app in prowlarr radarr rtorrent-rutorrent sabnzbd sonarr speedtest-exporter thelounge; do
  cd "$base_dir/ac1ds-catalog/ac1dsworld/$app" || continue
  latest_version=$(ls -1 | sort -V | tail -n 1)
  rm -rf $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')
  cd "$latest_version"
done

# Remove unwanted files Test
for app in rtorrent-rutorrent; do
  cd "$base_dir/ac1ds-catalog/Test/$app" || continue
  latest_version=$(ls -1 | sort -V | tail -n 1)
  rm -rf $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')
  cd "$latest_version"
done

# Update ix_values.yaml for ac1dsworld
for app in prowlarr radarr rtorrent-rutorrent sabnzbd sonarr speedtest-exporter thelounge; do
  cd "$base_dir/ac1ds-catalog/ac1dsworld/$app" || continue
  latest_version=$(ls -1 | sort -V | tail -n 1)
  cd "$latest_version"

  # Check if mainfiles file exists
  if [ -f "$base_dir/ac1ds-catalog/mainfiles/${app}-ix_values.yaml" ]; then
    rm -f ix_values.yaml
    cp "$base_dir/ac1ds-catalog/mainfiles/${app}-ix_values.yaml" ix_values.yaml
  fi
done

# Update ix_values.yaml for Test
for app in rtorrent-rutorrent; do
  cd "$base_dir/ac1ds-catalog/Test/$app" || continue
  latest_version=$(ls -1 | sort -V | tail -n 1)
  cd "$latest_version"

  # Check if mainfiles file exists
  if [ -f "$base_dir/ac1ds-catalog/mainfiles/${app}-ix_values.yaml" ]; then
    rm -f ix_values.yaml
    cp "$base_dir/ac1ds-catalog/mainfiles/${app}-ix_values.yaml" ix_values.yaml
  fi
done



# Copy catalog.json
cp "$base_dir/ac1ds-catalog/catalog.json" "$base_dir/ac1ds-catalog/catalog-temp.json"

# Run catalog update script  
#python3 "$base_dir/ac1ds-catalog/catalogupdate.py"

# Remove temp directory
# sudo rm -r "$base_dir/ac1ds-catalog/temp" 

# Run catalog fix script
python3 "$base_dir/ac1ds-catalog/pythongluetunfix.py"

python3 "$base_dir/ac1ds-catalog/pythongluetunfix-test.py"


# Commit changes  
git add --all :/
git commit -m "Automatically generated changes on $branch_name"

# Push changes 
git push origin "$branch_name"

# Create PR
repo="ac1dburnz/ac1ds-catalog"
title="Automatically generated changes on $branch_name"
body="This pull request is automatically generated." 

pr_response=$(curl -X POST -H "Authorization: token $github_token" \
  -d '{"title":"'"$title"'","body":"'"$body"'","head":"'"$branch_name"'","base":"main"}' \
  "https://api.github.com/repos/$repo/pulls")

pr_number=$(echo $pr_response | jq '.number')

# Set PR to squash merge 
#curl -X PATCH -H "Authorization: token $github_token" \
#  -d '{"merge_method":"squash"}' \
#  "https://api.github.com/repos/$repo/pulls/$pr_number"

# Merge PR
#curl -X PUT -H "Authorization: token $github_token" \
#  "https://api.github.com/repos/$repo/pulls/$pr_number/merge"

#echo "PR merged successfully"

