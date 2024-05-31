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

# Define latest modification time for ac1dsworld
latest=$(stat -c %Y "$base_dir/ac1ds-catalog/ac1dsworld/$app" | sort -n | tail -n 1)

# Copy apps from ac1dsworld to stable
if [ "$latest" != "$(ls -1 "$base_dir/ac1ds-catalog/ac1dsworld/$app" | sort -V | tail -n 1)" ]; then
  for app in prowlarr radarr rtorrent-rutorrent sabnzbd sonarr speedtest-exporter thelounge; do
    cp -R "$base_dir/ac1ds-catalog/ac1dsworld/$app" "$base_dir/ac1ds-catalog/stable"
  done
fi

# Define latest modification time for temp/stable
latest=$(stat -c %Y "$base_dir/ac1ds-catalog/temp/stable/$app" | sort -n | tail -n 1)

# Copy apps from temp - stable to ac1dsworld 
if [ "$latest" != "$(ls -1 "$base_dir/ac1ds-catalog/temp/stable/$app" | sort -V | tail -n 1)" ]; then
  for app in sonarr speedtest-exporter radarr sabnzbd prowlarr thelounge rtorrent-rutorrent overseerr metallb-config openebs pihole metallb lldap plex plextraktsync ispy-agent-dvr traefik prometheus-operator prometheus grafana ptp-uploader wg-easy tautulli authelia cert-manager cloudnative-pg clusterissuer custom-app; do
    cp -R "$base_dir/ac1ds-catalog/temp/stable/$app" "$base_dir/ac1ds-catalog/ac1dsworld"
  done
fi

# Define latest modification time for temp/dependency
latest=$(stat -c %Y "$base_dir/ac1ds-catalog/temp/dependency/$app" | sort -n | tail -n 1)

# Copy apps from temp - dependency to ac1dsworld 
if [ "$latest" != "$(ls -1 "$base_dir/ac1ds-catalog/temp/dependency/$app" | sort -V | tail -n 1)" ]; then
  for app in sonarr speedtest-exporter radarr sabnzbd prowlarr thelounge rtorrent-rutorrent overseerr metallb-config openebs pihole metallb lldap plex plextraktsync ispy-agent-dvr traefik prometheus-operator prometheus grafana ptp-uploader wg-easy tautulli authelia cert-manager cloudnative-pg clusterissuer custom-app; do
    cp -R "$base_dir/ac1ds-catalog/temp/dependency/$app" "$base_dir/ac1ds-catalog/ac1dsworld"
  done
fi

# Define latest modification time for temp/enterprise
latest=$(stat -c %Y "$base_dir/ac1ds-catalog/temp/enterprise/$app" | sort -n | tail -n 1)

# Copy apps from temp - enterprise to ac1dsworld 
if [ "$latest" != "$(ls -1 "$base_dir/ac1ds-catalog/temp/enterprise/$app" | sort -V | tail -n 1)" ]; then
  for app in sonarr speedtest-exporter radarr sabnzbd prowlarr thelounge rtorrent-rutorrent overseerr metallb-config openebs pih

