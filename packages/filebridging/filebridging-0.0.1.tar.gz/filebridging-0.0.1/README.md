# filebridging

Share files via a bridge server using TCP over SSL and end-to-end encryption.

## Requirements
Python3.8+ is needed for this package.

## Usage
If you need a virtual environment, create it.
```bash
python3.8 -m venv env;
alias pip="env/bin/pip";
alias python="env/bin/python";
```

Install filebridging and read the help.
```bash
pip install filebridging
python -m filebridging.server --help
python -m filebridging.client --help
```

## Examples
* Client-server example
    ```bash
    # 3 distinct tabs
    python -m filebridging.server --host localhost --port 5000 --certificate ~/.ssh/server.crt --key ~/.ssh/server.key
    python -m filebridging.client s --host localhost --port 5000 --certificate ~/.ssh/server.crt --token 12345678 --password supersecretpasswordhere --path ~/file_to_send 
    python -m filebridging.client r --host localhost --port 5000 --certificate ~/.ssh/server.crt --token 12345678 --password supersecretpasswordhere --path ~/Downloads 
    ```

* Client-client example
    ```bash
    # 2 distinct tabs
    python -m filebridging.client s --host localhost --port 5000 --certificate ~/.ssh/server.crt --key ~/.ssh/private.key --token 12345678 --password supersecretpasswordhere --path ~/file_to_send --standalone
    python -m filebridging.client r --host localhost --port 5000 --certificate ~/.ssh/server.crt --token 12345678 --password supersecretpasswordhere --path ~/Downloads 
    ```
    The receiver client may be standalone as well: just add the `--key` parameter (for SSL-secured sessions) and the `--standalone` flag. 

* Configuration file example
    ```python
    #!/bin/python
    
    host = "www.example.com"
    port = 5000
    certificate = "/path/to/public.crt"
    key = "/path/to/private.key"
    
    action = 'r'
    password = 'verysecretpassword'
    token = 'sessiontok'
    file_path = '.'
    ```
