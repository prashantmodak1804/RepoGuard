import json

def parse_manifest(file_path: str) -> list[dict]:
    """
    This function detects whether the file is `package.json` or `requirements.txt` and parses it accordingly.
    
    Args:
    file_path (str): The path to the manifest file.
    
    Returns:
    list[dict]: A standardized list of dictionaries containing package information.
    """
    
    # Initialize an empty list to store the parsed package information
    packages = []
    
    # Try to open the file in read mode
    try:
        with open(file_path, 'r') as file:
            # Check if the file is `package.json`
            if file_path.endswith('package.json'):
                # Load the JSON data from the file
                data = json.load(file)
                
                # Extract the dependencies and devDependencies from the data
                dependencies = data.get('dependencies', {})
                dev_dependencies = data.get('devDependencies', {})
                
                # Combine the dependencies and devDependencies into a single dictionary
                all_dependencies = {**dependencies, **dev_dependencies}
                
                # Iterate over the combined dependencies
                for package, version in all_dependencies.items():
                    # Create a dictionary to store the package information
                    package_info = {
                        "package": package,
                        "version": version,
                        "manifest_type": "npm"
                    }
                    
                    # Add the package information to the list of packages
                    packages.append(package_info)
            
            # Check if the file is `requirements.txt`
            elif file_path.endswith('requirements.txt'):
                # Iterate over each line in the file
                for line in file:
                    # Strip the line of leading and trailing whitespace
                    line = line.strip()
                    
                    # Check if the line contains a package specification (e.g., `package==1.2.3`)
                    if '==' in line or '>=' in line or '<=' in line:
                        # Split the line into package and version parts
                        package, version = line.split('==') if '==' in line else line.split('>=') if '>=' in line else line.split('<=')
                        
                        # Create a dictionary to store the package information
                        package_info = {
                            "package": package.strip(),
                            "version": version.strip(),
                            "manifest_type": "pip"
                        }
                        
                        # Add the package information to the list of packages
                        packages.append(package_info)
    
    # Handle any exceptions that occur during file parsing
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Return the list of parsed package information
    return packages