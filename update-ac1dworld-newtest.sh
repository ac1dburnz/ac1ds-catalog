#!/bin/bash

catalog="/Users/ac1dburn/Documents/GitHub/catalog"
ac1dsworld="/Users/ac1dburn/Documents/GitHub/ac1ds-catalog/ac1dsworld"
stable="/Users/ac1dburn/Documents/GitHub/ac1ds-catalog/stable"
mainfiles="/Users/ac1dburn/Documents/GitHub/ac1ds-catalog/mainfiles"

apps=("prowlarr" "radarr" "rtorrent-rutorrent" "sabnzbd" "sonarr" "speedtest-exporter" "thelounge")

for app in "${apps[@]}"; do
    # Copy files from prowlarr, radarr, etc. to stable folder
    if cp -R "$ac1dsworld/$app" "$stable"; then
        echo "Copied files for $app to stable"
    else
        echo "Error copying files for $app to stable"
        exit 1
    fi

    # Remove unnecessary files
    if cd "$ac1dsworld/$app" && rm -R $(ls -1 | grep -vE 'app_versions.json|item.yaml' | sort -V | sed '$d'); then
        echo "Removed unnecessary files for $app"
    else
        echo "Error removing unnecessary files for $app"
        exit 1
    fi

    # Go into the latest versioned directory and update ix_values.yaml
    if cd "$ac1dsworld/$app" && cd $(ls -1d */ | sort -V | tail -n 1) && rm ix_values.yaml && cp "$mainfiles/${app}-ix_values.yaml" ix_values.yaml; then
        echo "Updated ix_values.yaml for $app"
    else
        echo "Error updating ix_values.yaml for $app"
        exit 1
    fi
done

echo "Script completed successfully"
