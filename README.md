# Deluge-Zoho-Integration

Deluge-Zoho-Integration provides Python code to integrate Zoho Books with the Deluge platform. It automates data ingestion, API authentication, and logging for financial workflows.

## Project Structure


```text
Deluge-Zoho-Integration/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── zoho_integration.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   └── test_zoho_integration.py
└── .gitignore
```

## Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/icedmoca/Deluge-Zoho-Integration
   cd Deluge-Zoho-Integration

## Install Dependencies:
```bash
pip install -r requirements.txt
```

## Configure Credentials:

Edit `src/config.py` with your Zoho Books credentials and any required configuration.

## Usage:

```bash
python src/zoho_integration.py
```
## Tests:
`pytest`
