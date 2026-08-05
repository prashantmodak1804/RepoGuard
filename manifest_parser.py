import json
import re

def parse_manifest(file_path: str) -> list[dict]:
    """
    This function detects whether the file is `package.json` or `requirements.txt` and parses it accordingly.
    
    Args:
    file_path (str): The path to the manifest file.
    
    Returns:
    list[dict]: A standardized list of dictionaries containing package information.
    """
    packages = []
    
    # Check if the file is `package.json`
    if file_path.endswith('package.json'):
        with open(file_path, 'r') as file:
            data = json.load(file)
            dependencies = data.get('dependencies', {})
            dev_dependencies = data.get('devDependencies', {})
            all_dependencies = {**dependencies, **dev_dependencies}
            
            # Iterate over the combined dependencies
            for package, version in all_dependencies.items():
                package_info = {
                    "package": package,
                    "version": version,
                    "manifest_type": "npm"
                }
                packages.append(package_info)
    
    # Check if the file is `requirements.txt`
    elif file_path.endswith('requirements.txt'):
        with open(file_path, 'r') as file:
            for line in file:
                # Strip the line of leading and trailing whitespace
                line = line.strip()
                
                # Check if the line contains a package specification (e.g., `package==1.2.3`)
                if '==' in line or '>=' in line or '<=' in line:
                    # Split the line into package and version parts
                    match = re.split(r'([==|>=|<=])', line, maxsplit=1, flags=re.IGNORECASE)
                    package = match[0].strip()
                    version = match[1] + match[2].strip()
                    
                    # Handle package names with hyphens
                    if '-' in package:
                        package = package.replace('-', '\\-')
                    
                    package_info = {
                        "package": package,
                        "version": version,
                        "manifest_type": "pip"
                    }
                    packages.append(package_info)
                else:
                    # If the line does not contain a package specification, skip it
                    continue
    
    return packages