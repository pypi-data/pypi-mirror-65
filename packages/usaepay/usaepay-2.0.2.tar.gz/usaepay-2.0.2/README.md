# USAePay Python SDK

Package for connecting to USAePay's rest API using python 3.6 or later.

### Prerequisites

#### Python version 3.6+
Download from https://www.python.org/downloads/

#### Pip3 (optional)
Should be automatically installed with python but if not:
```
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python3 get-pip.py --user
pip3 --version
```

#### Requests
Installed automatically if Pip is used.  For source code visit https://github.com/psf/requests

### Installation


## Deployment

This package requires a USAePay account.  You will also need to create an API key with a PIN in your account.  It is recommend to run usaepay.api.setAuthentication('key','pin') before any other calls.

## Version
 
0.0.1

## Authors

* **USAePay** - [USAePay](https://secure.usaepay.com)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details
