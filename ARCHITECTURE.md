# CI/CD Pipeline
The CI/CD pipeline will consist of the following steps:
1. Checkout code
2. Set up Python 3.11
3. Install dependencies from `requirements.txt`
4. Run `pytest`
5. Run `python main.py audit examples/package.json`
The pipeline will be triggered on push to the `main` branch.
This pipeline ensures that the code is properly tested and audited before it is deployed.