import pytest
from manifest_parser import parse_manifest

def test_package_json():
    with open('examples/package.json', 'r') as file:
        packages = parse_manifest(file.name)
        assert len(packages) == 6
        assert packages[0]['package'] == 'react'
        assert packages[0]['version'] == '^18.2.0'
        assert packages[0]['manifest_type'] == 'npm'

def test_requirements_txt():
    with open('requirements.txt', 'r') as file:
        packages = parse_manifest(file.name)
        assert len(packages) == 3
        assert packages[0]['package'] == 'typer'
        assert packages[0]['version'] == '>=0.9,<1.0'
        assert packages[0]['manifest_type'] == 'pip'

def test_malformed_line():
    with open('tests/malformed.txt', 'w') as file:
        file.write('invalid==1.2.3')
    with open('tests/malformed.txt', 'r') as file:
        packages = parse_manifest(file.name)
        assert len(packages) == 0