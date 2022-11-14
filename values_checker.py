# This Script will check if there are any missing values in the deployment values.yaml file


# File Path for values_base.yaml
base_values_file_path = "./QPP-Chart/values_base.yaml"

# File Path For Deployment values.yaml
values_file_path = ""
if not values_file_path:
    raise Exception("Please specify a values file path")

# Open Both Files
base_values_content = open(base_values_file_path, "r").read()
values_content = open(values_file_path, "r").read()

# Find All Values in values.yaml
def get_params_from_yaml(file_content):
    params = []
    prefix = ""
    for line in file_content.splitlines():
        # Get Param Name
        param = line.strip().split(":")[0].replace("#", "").strip()

        # Filter Out Comments
        if ":" not in line or " " in param:
            continue
        # Nested Params should include the parent category
        if line.replace("#", "").startswith(" "):
            params.append(f"{prefix}.{param}")
        else:
            params.append(param)
            # Reset Prefix
            prefix = param
    return params

params_in_base = get_params_from_yaml(base_values_content)
params_in_values = get_params_from_yaml(values_content)

# Find Missing Values
missing_values = [line for line in params_in_base if line not in params_in_values]

if missing_values:
    print("Detected the following missing values which were present in base_values.yaml but not present in deployment values.yaml\n")
    for val in missing_values:
        print("\t" + val)
else:
    print("No missing values detected")
