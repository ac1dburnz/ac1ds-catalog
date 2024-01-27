#!/bin/bash

# For prowlarr
cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/prowlarr
cp -R * /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/stable/prowlarr

# For radarr
cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/radarr
cp -R * /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/stable/radarr

# For rtorrent-rutorrent
cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/rtorrent-rutorrent
cp -R * /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/stable/rtorrent-rutorrent

# For sabnzbd
cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/sabnzbd
cp -R * /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/stable/sabnzbd

# For sonarr
cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/sonarr
cp -R * /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/stable/sonarr

# For speedtest-exporter
cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/speedtest-exporter
cp -R * /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/stable/speedtest-exporter

# For thelounge
cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/thelounge
cp -R * /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/stable/thelounge


# Copy the specified directories from catalog to ac1dsworld
cp -R /Users/ac1dburn/Documents/GitHub/catalog/stable/prowlarr /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld
cp -R /Users/ac1dburn/Documents/GitHub/catalog/stable/radarr /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld
cp -R /Users/ac1dburn/Documents/GitHub/catalog/stable/rtorrent-rutorrent /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld
cp -R /Users/ac1dburn/Documents/GitHub/catalog/stable/sabnzbd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld
cp -R /Users/ac1dburn/Documents/GitHub/catalog/stable/sonarr /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld
cp -R /Users/ac1dburn/Documents/GitHub/catalog/stable/speedtest-exporter /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld
cp -R /Users/ac1dburn/Documents/GitHub/catalog/stable/thelounge /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/prowlarr
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/radarr
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/rtorrent-rutorrent
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/sabnzbd
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/sonarr
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/speedtest-exporter
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/thelounge
rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d')

# Go into the latest versioned directory of each app and remove ix_values.yaml and add the modified one

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/prowlarr && cd $(ls -1d */ | sort -V | tail -n 1)
rm ix_values.yaml
cp /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/mainfiles/prowlarr-ix_values.yaml ix_values.yaml

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/radarr && cd $(ls -1d */ | sort -V | tail -n 1)
rm ix_values.yaml
cp /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/mainfiles/radarr-ix_values.yaml ix_values.yaml 

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/rtorrent-rutorrent && cd $(ls -1d */ | sort -V | tail -n 1)
rm ix_values.yaml
cp /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/mainfiles/rtorrent-rutorrent-ix_values.yaml ix_values.yaml 

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/sabnzbd && cd $(ls -1d */ | sort -V | tail -n 1)
rm ix_values.yaml
cp /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/mainfiles/sabnzbd-ix_values.yaml ix_values.yaml

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/sonarr && cd $(ls -1d */ | sort -V | tail -n 1)
rm ix_values.yaml
cp /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/mainfiles/sonarr-ix_values.yaml ix_values.yaml

cd /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld/thelounge && cd $(ls -1d */ | sort -V | tail -n 1)
rm ix_values.yaml
cp /Users/ac1dburn/Documents/GitHub/ac1ds-catalog/mainfiles/thelounge-ix_values.yaml ix_values.yaml



