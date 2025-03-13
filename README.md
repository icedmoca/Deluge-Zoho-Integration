# Deluge-Zoho Integration

A robust Python integration between Zoho Books and the Deluge platform, providing secure and efficient access to Zoho Books' financial data.

## Features

- Secure OAuth2 authentication with Zoho Books API
- Efficient data retrieval with automatic token refresh
- Comprehensive error handling and logging
- Retry mechanism for failed API requests
- Unit tests with high coverage
- Type hints and documentation

## Project Structure

```
deluge-zoho-integration/
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── zoho_integration.py
├── tests/
│   ├── __init__.py
│   └── test_zoho_integration.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Prerequisites

- Python 3.8 or higher
- Zoho Books account with API access
- Zoho API credentials (Client ID, Client Secret, and Refresh Token)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/icedmoca/deluge-zoho-integration.git
cd deluge-zoho-integration
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root with your Zoho credentials:
```env
ZOHO_CLIENT_ID=your_client_id
ZOHO_CLIENT_SECRET=your_client_secret
ZOHO_REFRESH_TOKEN=your_refresh_token
ZOHO_ORGANIZATION_ID=your_organization_id
```

## Usage

Here's a simple example of how to use the integration:

```python
from src.zoho_integration import ZohoBooks

# Initialize the client
zoho = ZohoBooks()

# Get invoices for a specific date range
invoices = zoho.get_invoices(
    from_date="2024-01-01",
    to_date="2024-01-31",
    status="sent"
)

# Process the invoices
for invoice in invoices:
    print(f"Invoice {invoice['invoice_number']}: ${invoice['total']}")
```

## Running Tests

Run the test suite using pytest:

```bash
pytest
```

For test coverage report:

```bash
pytest --cov=src tests/
```

## Error Handling

The integration includes two main exception types:

- `ZohoAuthError`: Raised for authentication-related issues
- `ZohoAPIError`: Raised for API request failures

All errors are logged to `zoho_integration.log` with appropriate context.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security

- Credentials are handled securely using environment variables
- Sensitive data is never logged
- Access tokens are automatically refreshed
- All requests use HTTPS

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
