import os
import shutil
from packaging import version

base_dir = "/Users/ac1dburn/Documents/GitHub"

# List of apps for each category
apps_ac1dsworld_to_stable = [
    "prowlarr", "radarr", "rtorrent-rutorrent", "sabnzbd", "sonarr",
    "speedtest-exporter", "thelounge", "overseerr", "pihole", "lldap",
    "plextraktsync", "ispy-agent-dvr", "wg-easy", "tautulli"
]

apps_temp_stable_to_ac1dsworld = apps_ac1dsworld_to_stable
apps_temp_premium_to_premium = [
    "authelia", "blocky", "clusterissuer", "custom-app", "grafana",
    "metallb-config", "nextcloud", "prometheus", "traefik", "vaultwarden"
]

apps_temp_system_to_system = [
    "cert-manager", "cloudnative-pg", "grafana-agent-operator", "kubeapps",
    "kubernetes-reflector", "metallb", "openebs", "prometheus-operator",
    "snapshot-controller", "traefik-crds", "velero", "volsync", "volumesnapshots"
]

apps_ac1dsworld_to_test = ["rtorrent-rutorrent"]

def get_highest_version(dir_path):
    versions = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    return max(versions, key=version.parse) if versions else None

def copy_if_newer(src_base, dest_base, apps):
    for app in apps:
        src_dir = os.path.join(src_base, app)
        dest_dir = os.path.join(dest_base, app)

        print(f"Source directory: {src_dir}")
        print(f"Destination directory: {dest_dir}")

        if not os.path.exists(dest_dir):
            print(f"Destination directory {dest_dir} does not exist. Copying entire directory...")
            shutil.copytree(src_dir, dest_dir)
            continue

        src_latest = get_highest_version(src_dir)
        dest_latest = get_highest_version(dest_dir)

        print(f"Latest version in source directory: {src_latest}")
        print(f"Latest version in destination directory: {dest_latest}")

        if src_latest and (not dest_latest or version.parse(src_latest) > version.parse(dest_latest)):
            print(f"Newer version found in source directory {src_dir}. Copying directory...")
            shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
            print(f"Directory copied successfully!")
        else:
            print(f"No newer version found in source directory {src_dir}. Skipping copy.")

# Copy apps from ac1dsworld to stable
copy_if_newer(
    os.path.join(base_dir, "ac1ds-catalog/ac1dsworld"),
    os.path.join(base_dir, "ac1ds-catalog/stable"),
    apps_ac1dsworld_to_stable
)

# Copy apps from temp stable to ac1dsworld
copy_if_newer(
    os.path.join(base_dir, "ac1ds-catalog/temp/stable"),
    os.path.join(base_dir, "ac1ds-catalog/ac1dsworld"),
    apps_temp_stable_to_ac1dsworld
)

# Copy apps from temp premium to premium
copy_if_newer(
    os.path.join(base_dir, "ac1ds-catalog/temp/premium"),
    os.path.join(base_dir, "ac1ds-catalog/premium"),
    apps_temp_premium_to_premium
)

# Copy apps from temp system to system
copy_if_newer(
    os.path.join(base_dir, "ac1ds-catalog/temp/system"),
    os.path.join(base_dir, "ac1ds-catalog/system"),
    apps_temp_system_to_system
)

# Copy apps from ac1dsworld to test
copy_if_newer(
    os.path.join(base_dir, "ac1ds-catalog/ac1dsworld"),
    os.path.join(base_dir, "ac1ds-catalog/Test"),
    apps_ac1dsworld_to_test
)
