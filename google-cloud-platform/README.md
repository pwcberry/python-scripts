# Working with the Google Cloud Platform

When you have secrets for the relevant project and API, these are moved into the project folder as the `credentials.json` file. 

This file is used by the Google Cloud SDK to authenticate your requests.

Google's OAuth 2.0 library generates the tokens it needs and saves them in the `token.json` file. 

This file is created automatically when you run the application for the first time and successfully authenticate with Google. 

It contains the access and refresh tokens needed for subsequent API requests.

## Python virtual environments

The projects in this repository are run in Python virtual environments to ensure they execute on the preferred runtime.

When you want to run a script within a particular project, go into the project directory and execute (assuming `python` is an alias for `python3`):

```
python -m venv .venv

source ./.venv/bin/activate

# If present:
pip install -r requirements.txt

```

Then run a script:

```
python3 football.py
```

To exit the virtual environment:

```
deactivate

```

To clean up the virtual environment, remove the `.venv` directory.

## Gotchas

If you encounter this error:

```
google.auth.exceptions.RefreshError: ('deleted_client: The OAuth client was deleted.', {'error': 'deleted_client', 'error_description': 'The OAuth client was deleted.'})
```

the `token.json` file must be deleted so that Google can refresh the API token using the credentials stored in `credentials.json`.

The `token.json` file usually has a lifespan of 1 hour.
