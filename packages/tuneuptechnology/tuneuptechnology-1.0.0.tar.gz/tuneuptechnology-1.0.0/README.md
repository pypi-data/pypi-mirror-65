# Tuneup Technology App Python Client Library

The Python client library for the Tuneup Technology App.

[![Build Status](https://travis-ci.com/ncr4/tuneuptechnology-python.svg?branch=master)](https://travis-ci.com/ncr4/tuneuptechnology-python)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

This library allows you to interact with the customers, tickets, inventory, and locations objects without needing to do the hard work of binding your calls and data to endpoints. Simply call an action such as `create_customer` and pass some data and let the library do the rest.

## Install

```bash
pip3 install tuneuptechnology
```

## Example

```python
"""Create a customer record by passing in all required data"""
import os
from dotenv import load_dotenv
import tuneuptechnology

load_dotenv()
API_EMAIL = os.getenv('API_EMAIL')
API_KEY = os.getenv('API_KEY')

CUSTOMER = tuneuptechnology.Customers.create_customer(
    data={
        'auth': API_EMAIL,
        'api_key': API_KEY,
        'firstname': 'Jake',
		'lastname': 'Peralta',
		'email': 'jake@example.com',
		'phone': '8015551234',
		'user_id': 1,
		'notes': 'Believes he is a good detective.',
		'location_id': 1,
    }
)

tuneuptechnology.Util.pretty_print(CUSTOMER)
```

Other examples can be found in the `/examples` directory. Alter according to your needs.

## Usage

```bash
API_EMAIL=email@example.com API_KEY=123... python3 create_customer.py
```

## Documentation

Up-to-date API documentation can be [found here](https://app.tuneuptechnology.com/docs/api).

## Releasing

As a separate PR from the feature/bug PR:

1. Update the Version constant in `client.py` & `setup.py`
1. Update `CHANGELOG`
1. Create a GitHub tag with proper Python version semantics (eg: v1.0.0)
1. Publish to PyPI
