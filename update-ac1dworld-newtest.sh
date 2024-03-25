#!/bin/bash

echo "Setting base directory"
base_dir="/Users/ac1dburn/Documents/GitHub"

echo "Generating branch name"  
branch_name="$(date +'%Y%m%d%H%M%S')"

echo "Going to directory"
cd "$base_dir/ac1ds-catalog"

echo "Checking out main branch and pulling from origin"
git checkout main
git pull origin main
git checkout -b "$branch_name"

echo "Removing existing temp directory if it exists"
if [ -d temp ]; then
  echo "Removing temp directory"
  sudo rm -r temp
fi

echo "Creating new temp directory"
mkdir temp

echo "Cloning catalog into temp directory"
git clone https://github.com/truecharts/catalog.git temp

# Loop through each app
for app in prowlarr radarr rtorrent-rutorrent sabnzbd sonarr speedtest-exporter thelounge; do

  echo "Processing $app"
  
  # Get latest version
  latest=$(ls -1 "$base_dir/ac1ds-catalog/ac1dsworld/$app" | sort -V | tail -n 1)

  # Only copy if version changed
  if [ "$latest" != "$(ls -1 "$base_dir/ac1ds-catalog/temp/stable/$app" | sort -V | tail -n 1)" ]; then
    echo "Copying $app to stable"
    cp -R "$base_dir/ac1ds-catalog/ac1dsworld/$app" "$base_dir/ac1ds-catalog/stable/$app"
    echo "Copying $app from temp" 
    cp -R "$base_dir/ac1ds-catalog/temp/stable/$app" "$base_dir/ac1ds-catalog/ac1dsworld/$app"
  fi

  # Clean up extra files
  echo "Removing unwanted files for $app"
  cd "$base_dir/ac1ds-catalog/ac1dsworld/$app"
  rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

  # Update ix_values.yaml
  echo "Updating ix_values.yaml for $app"
  cd "$base_dir/ac1ds-catalog/ac1dsworld/$app"
  cd "$(ls -1d */ | sort -V | tail -n 1)"
  rm ix_values.yaml
  cp "$base_dir/ac1ds-catalog/mainfiles/${app}-ix_values.yaml" ix_values.yaml
  
done

echo "Copying catalog.json"
cp "$base_dir/ac1ds-catalog/catalog.json" "$base_dir/ac1ds-catalog/catalog-temp.json"

echo "Running catalog update script"
python3 "$base_dir/ac1ds-catalog/catalogupdate.py" 

echo "Removing temp directory"
sudo rm -r "$base_dir/ac1ds-catalog/temp"

echo "Running catalog fix script"
python3 "$base_dir/ac1ds-catalog/pythongluetunfix.py"

echo "Committing changes"
git add --all :/
git commit -m "Automated changes on $branch_name"

echo "Pushing changes"
git push origin "$branch_name"

# Create PR
echo "Creating pull request"
repo="ac1dburnz/ac1ds-catalog"
title="Automatically generated changes on $branch_name"
body="This pull request is automatically generated."

curl -X POST -H "Authorization: token $github_token" \
  -d '{"title":"'"$title"'","body":"'"$body"'","head":"'"$branch_name"'","base":"main"}' \
  "https://api.github.com/repos/$repo/pulls"

echo "Script completed successfully"
