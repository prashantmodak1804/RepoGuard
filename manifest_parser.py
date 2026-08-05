import json
import re


def parse_manifest(filepath):
    if filepath.endswith('.json'):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                packages = []
                deps = data.get('dependencies', {})
                for pkg, ver in deps.items():
                    packages.append({
                        'package': pkg,
                        'version': ver,
                        'manifest_type': 'npm'
                    })
                return packages
        except Exception:
            return []

    elif filepath.endswith('.txt'):
        packages = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    # Match valid pip requirements lines (package name + specifiers >= or <)
                    match = re.match(r'^([a-zA-Z0-9_.-]+)\s*([><]=?.*)$', line)
                    if match:
                        pkg_name = match.group(1)
                        version = match.group(2) or ''
                        packages.append({
                            'package': pkg_name,
                            'version': version,
                            'manifest_type': 'pip'
                        })
        except Exception:
            return []
        return packages

    return []
