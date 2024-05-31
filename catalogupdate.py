import json

def find_app(data, app_name):
    if isinstance(data, dict):
        if app_name in data:
            return app_name, data[app_name]
        else:
            for key, value in data.items():
                result = find_app(value, app_name)
                if result:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_app(item, app_name)
            if result:
                return result
    return None

def generate_output_structure(categories_data, catalog_data, output_file_path):
    apps_data = {}
    for category, apps in categories_data.items():
        category_apps_data = {}
        for app_name in apps:
            result = find_app(catalog_data[category], app_name)
            if result:
                app_name_actual, app_data = result
                category_apps_data[app_name_actual] = app_data
        apps_data[category] = category_apps_data

    output_structure = {
        "charts": {},
        **apps_data
    }

    with open(output_file_path, 'w') as output_file:
        json.dump(output_structure, output_file, indent=2)

    print(f"Output written to {output_file_path}.")

# Paths to the catalog JSON files
base_dir = "/Users/ac1dburn/Documents/GitHub"
catalog_json_path = f"{base_dir}/ac1ds-catalog/catalog.json"
updated_catalog_json_path = f"{base_dir}/ac1ds-catalog/temp/catalog.json"
categories_file_path = f"{base_dir}/ac1ds-catalog/categories.json"

# Read original catalog JSON file
with open(catalog_json_path, 'r') as catalog_file:
    catalog_data = json.load(catalog_file)

# Read updated catalog JSON file
with open(updated_catalog_json_path, 'r') as updated_catalog_file:
    updated_catalog_data = json.load(updated_catalog_file)

# Read categories file
with open(categories_file_path, 'r') as categories_file:
    categories_data = json.load(categories_file)

# Output file path
output_file_path = f"{base_dir}/ac1ds-catalog/catalog.json"

# Generate the output structure and write to file
generate_output_structure(categories_data, catalog_data, output_file_path)


