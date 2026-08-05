from license_agent import check_compliance
from manifest_parser import parse_manifest


def test_allowed():
    with open('tests/policy_allowed.json', 'w') as file:
        file.write('{"denied": [], "warning": [], "allowed": ["MIT"]}')
    with open('tests/license_db_allowed.json', 'w') as file:
        file.write('{"react": "MIT"}')
    packages = parse_manifest('examples/package.json')
    results = check_compliance(packages, 'tests/policy_allowed.json')
    assert results[0]['status'] == 'allowed'
    assert results[0]['citation'] == "license 'MIT' matches the 'allowed' list in policy.json"

def test_denied():
    with open('tests/policy_denied.json', 'w') as file:
        file.write('{"denied": ["MIT"], "warning": [], "allowed": []}')
    with open('tests/license_db_denied.json', 'w') as file:
        file.write('{"react": "MIT"}')
    packages = parse_manifest('examples/package.json')
    results = check_compliance(packages, 'tests/policy_denied.json')
    assert results[0]['status'] == 'denied'
    assert results[0]['citation'] == "license 'MIT' matches the 'denied' list in policy.json"

def test_unknown():
    with open('tests/policy_unknown.json', 'w') as file:
        file.write('{"denied": [], "warning": [], "allowed": []}')
    with open('tests/license_db_unknown.json', 'w') as file:
        file.write('{}')
    packages = parse_manifest('examples/package.json')
    results = check_compliance(packages, 'tests/policy_unknown.json')
    assert results[0]['status'] == 'unknown'
    assert results[0]['citation'] == "license 'MIT' has unknown status"

def test_requirements_txt():
    with open('requirements.txt', 'r') as file:
        packages = parse_manifest(file.name)
        assert len(packages) == 3
        assert packages[0]['package'] == 'typer'
        assert packages[0]['version'] == '>=0.9,<1.0'
        assert packages[1]['package'] == 'rich'
        assert packages[1]['version'] == '>=10.0.0'
        assert packages[2]['package'] == 'pytest'
        assert packages[2]['version'] == '>=6.2,<7.0'

def test_malformed_line():
    with open('tests/malformed.txt', 'w') as file:
        file.write('invalid==1.2.3')
    with open('tests/malformed.txt', 'r') as file:
        packages = parse_manifest(file.name)
        assert len(packages) == 0
