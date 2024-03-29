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

# Copy apps from stable to ac1dsworld
if [ "$latest" != "$(ls -1 "$base_dir/ac1ds-catalog/ac1dsworld/$app" | sort -V | tail -n 1)" ]; then
  for app in prowlarr radarr rtorrent-rutorrent sabnzbd sonarr speedtest-exporter thelounge; do
    cp -R "$base_dir/ac1ds-catalog/ac1dsworld/$app" "$base_dir/ac1ds-catalog/stable"
  done
fi

# Copy apps from temp to ac1dsworld 
if [ "$latest" != "$(ls -1 "$base_dir/ac1ds-catalog/temp/stable/$app" | sort -V | tail -n 1)" ]; then
  for app in prowlarr radarr rtorrent-rutorrent sabnzbd sonarr speedtest-exporter thelounge; do
    cp -R "$base_dir/ac1ds-catalog/temp/stable/$app" "$base_dir/ac1ds-catalog/ac1dsworld"
  done
fi

# Remove unwanted files  
for app in prowlarr radarr rtorrent-rutorrent sabnzbd sonarr speedtest-exporter thelounge; do
  cd "$base_dir/ac1ds-catalog/ac1dsworld/$app"
  rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d') 
done

# Update ix_values.yaml
for app in prowlarr radarr rtorrent-rutorrent sabnzbd sonarr speedtest-exporter thelounge; do
  cd "$base_dir/ac1ds-catalog/ac1dsworld/$app"
  cd "$(ls -1d */ | sort -V | tail -n 1)"
  
  # Check if mainfiles file exists
  if [ -f "$base_dir/ac1ds-catalog/mainfiles/${app}-ix_values.yaml" ]; then
    rm ix_values.yaml
    cp "$base_dir/ac1ds-catalog/mainfiles/${app}-ix_values.yaml" ix_values.yaml
  fi
done
# Copy catalog.json
cp "$base_dir/ac1ds-catalog/catalog.json" "$base_dir/ac1ds-catalog/catalog-temp.json"

# Run catalog update script  
python3 "$base_dir/ac1ds-catalog/catalogupdate.py"

# Remove temp directory
sudo rm -r "$base_dir/ac1ds-catalog/temp" 

# Run catalog fix script
python3 "$base_dir/ac1ds-catalog/pythongluetunfix.py"

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
curl -X PATCH -H "Authorization: token $github_token" \
  -d '{"merge_method":"squash"}' \
  "https://api.github.com/repos/$repo/pulls/$pr_number"

# Merge PR
curl -X PUT -H "Authorization: token $github_token" \
  "https://api.github.com/repos/$repo/pulls/$pr_number/merge"

echo "PR merged successfully"

