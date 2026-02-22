# Working with the Google Cloud Platform

When you have secrets for the relevant project and API, these are moved into the project folder as the `credentials.json` file. 
This file is used by the Google Cloud SDK to authenticate your requests.

Google's OAuth 2.0 library generates the tokens it needs and saves them in the `token.json` file. 
This file is created automatically when you run the application for the first time and successfully authenticate with Google. 
It contains the access and refresh tokens needed for subsequent API requests.
