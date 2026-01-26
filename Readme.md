# Branch Package Comparator

CLI utility for comparing binary packages between ALT Linux branches (Sisyphus and p11).

## Features

- Fetch package lists from ALT Linux REST API
- Compare packages between Sisyphus and p11 branches
- Identify unique packages in each branch
- Compare package versions according to RPM rules
- Output results in JSON format

## Installation

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Git
#### Commands for ALT Linux
- apt-get update
- apt-get install -y python3 curl
- curl -s https://bootstrap.pypa.io/get-pip.py | python3
- apt-get install -y python3-module-virtualenv

### Setup

```bash
# Clone the repository
git clone https://github.com/sasha9905/cli_utility
cd cli_utility

# Create virtual environment (optional)
python3 -m virtualenv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

## Basic Usage
The utility provides three main commands:

### 1. Find packages only in p11
python3 main.py p11-not-in-sisyphus

### 2. Find packages only in sisyphus
python3 main.py sisyphus-not-in-p11

### 3. Compare package versions
python3 main.py compare-versions
