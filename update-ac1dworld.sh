#!/bin/bash

base_dir="/Users/ac1dburn/Documents/GitHub"

sudo rm -r temp

mkdir temp

git clone https://github.com/truecharts/catalog.git temp
 
# For prowlarr
cd "$base_dir/ac1ds-catalog/ac1dsworld/prowlarr"
cp -R * "$base_dir/ac1ds-catalog/stable/prowlarr"

# For radarr
cd "$base_dir/ac1ds-catalog/ac1dsworld/radarr"
cp -R * "$base_dir/ac1ds-catalog/stable/radarr"

# For rtorrent-rutorrent
cd "$base_dir/ac1ds-catalog/ac1dsworld/rtorrent-rutorrent"
cp -R * "$base_dir/ac1ds-catalog/stable/rtorrent-rutorrent"

# For sabnzbd
cd "$base_dir/ac1ds-catalog/ac1dsworld/sabnzbd"
cp -R * "$base_dir/ac1ds-catalog/stable/sabnzbd"

# For sonarr
cd "$base_dir/ac1ds-catalog/ac1dsworld/sonarr"
cp -R * "$base_dir/ac1ds-catalog/stable/sonarr"

# For speedtest-exporter
cd "$base_dir/ac1ds-catalog/ac1dsworld/speedtest-exporter"
cp -R * "$base_dir/ac1ds-catalog/stable/speedtest-exporter"

# For thelounge
cd "$base_dir/ac1ds-catalog/ac1dsworld/thelounge"
cp -R * "$base_dir/ac1ds-catalog/stable/thelounge"

# Copy the specified directories from catalog to ac1dsworld
cp -R "$base_dir/catalog/stable/prowlarr" "$base_dir/ac1ds-catalog/ac1dsworld"
cp -R "$base_dir/catalog/stable/radarr" "$base_dir/ac1ds-catalog/ac1dsworld"
cp -R "$base_dir/catalog/stable/rtorrent-rutorrent" "$base_dir/ac1ds-catalog/ac1dsworld"
cp -R "$base_dir/catalog/stable/sabnzbd" "$base_dir/ac1ds-catalog/ac1dsworld"
cp -R "$base_dir/catalog/stable/sonarr" "$base_dir/ac1ds-catalog/ac1dsworld"
cp -R "$base_dir/catalog/stable/speedtest-exporter" "$base_dir/ac1ds-catalog/ac1dsworld"
cp -R "$base_dir/catalog/stable/thelounge" "$base_dir/ac1ds-catalog/ac1dsworld"

# Remove unwanted files
cd "$base_dir/ac1ds-catalog/ac1dsworld/prowlarr"
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd "$base_dir/ac1ds-catalog/ac1dsworld/radarr"
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd "$base_dir/ac1ds-catalog/ac1dsworld/rtorrent-rutorrent"
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd "$base_dir/ac1ds-catalog/ac1dsworld/sabnzbd"
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd "$base_dir/ac1ds-catalog/ac1dsworld/sonarr"
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd "$base_dir/ac1ds-catalog/ac1dsworld/speedtest-exporter"
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd "$base_dir/ac1ds-catalog/ac1dsworld/thelounge"
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

# Go into the latest versioned directory of each app and remove ix_values.yaml and add the modified one

cd "$base_dir/ac1ds-catalog/ac1dsworld/prowlarr" && cd "$(ls -1d */ | sort -V | tail -n 1)"
rm ix_values.yaml
cp "$base_dir/ac1ds-catalog/mainfiles/prowlarr-ix_values.yaml" ix_values.yaml

cd "$base_dir/ac1ds-catalog/ac1dsworld/radarr" && cd "$(ls -1d */ | sort -V | tail -n 1)"
rm ix_values.yaml
cp "$base_dir/ac1ds-catalog/mainfiles/radarr-ix_values.yaml" ix_values.yaml 

cd "$base_dir/ac1ds-catalog/ac1dsworld/rtorrent-rutorrent" && cd "$(ls -1d */ | sort -V | tail -n 1)"
rm ix_values.yaml
cp "$base_dir/ac1ds-catalog/mainfiles/rtorrent-rutorrent-ix_values.yaml" ix_values.yaml 

cd "$base_dir/ac1ds-catalog/ac1dsworld/sabnzbd" && cd "$(ls -1d */ | sort -V | tail -n 1)"
rm ix_values.yaml
cp "$base_dir/ac1ds-catalog/mainfiles/sabnzbd-ix_values.yaml" ix_values.yaml

cd "$base_dir/ac1ds-catalog/ac1dsworld/sonarr" && cd "$(ls -1d */ | sort -V | tail -n 1)"
rm ix_values.yaml
cp "$base_dir/ac1ds-catalog/mainfiles/sonarr-ix_values.yaml" ix_values.yaml

cd "$base_dir/ac1ds-catalog/ac1dsworld/thelounge" && cd "$(ls -1d */ | sort -V | tail -n 1)"
rm ix_values.yaml
cp "$base_dir/ac1ds-catalog/mainfiles/thelounge-ix_values.yaml" ix_values.yaml

cp "$base_dir/ac1ds-catalog/catalog.json" "$base_dir/ac1ds-catalog/catalog-temp.json" 

python3 "$base_dir/ac1ds-catalog/catalogupdate.py"  

sudo rm -r "$base_dir/ac1ds-catalog/temp"
