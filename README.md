# RSS Server for Mirantis Software Releases

Simple script to query the pagerduty api for escalation policies and post them as a custom event to opslevel


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

Make sure you have python3 installed as a pre-requisite.

Clone the repository:
```shell
git clone https://github.com/yourusername//opslevel.git
cd rss-server
```

Set up a virtual environment and activate it:

```shell
python -m venv venv
# For Windows
.\venv\Scripts\activate
# For Unix or MacOS
source venv/bin/activate
```

Install the required Python packages:
```shell
pip install -r requirements.txt
```

## Usage

Run the app:

```shell
python on_call_rotation.py
```

Run the test suite:
```shell
pip install pytest
pytest -v test_on_call_rotation.py
```

## Configuration

Requires the following environment variables:

- PAGERDUTY_API_TOKEN
- OPSLEVEL_API_TOKEN

It also takes the custom environment variable:
- ENVIRONMENT=production

This will only output error logging to save on disk space.

For Kubernetes integration
```shell
kubectl create secret generic api-tokens --from-literal=PAGERDUTY_API_TOKEN='yourTokenHere' --from-literal=OPSLEVEL_API_TOKEN='yourTokenHere'
```

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test them.
4. Commit your changes with clear and concise messages.
5. Push your changes to your fork.
6. Create a pull request to the main repository.

## License

This project is licensed under the MIT License.