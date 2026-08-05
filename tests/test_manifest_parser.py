import json
from manifest_parser import parse_manifest

def test_requirements_txt():
    # Test parsing of requirements.txt
    with open("requirements.txt", "r") as file:
        packages = parse_manifest(file.name)
    assert len(packages) == 7
    assert packages[0]["package"] == "typer"
    assert packages[0]["version"] == ">=0.9,<1.0"
    assert packages[0]["manifest_type"] == "pip"