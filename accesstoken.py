import requests
import os

# Genesys Cloud credentials
client_id = ''
client_secret = ''
environment = 'mypurecloud.com.au'

# Token URL
token_url = f'https://login.{environment}/oauth/token'

# Request payload
payload = {
    'grant_type': 'client_credentials'
}

# Headers
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Make the request for an access token
response = requests.post(token_url, data=payload, headers=headers, auth=(client_id, client_secret))

if response.status_code == 200:
    access_token = response.json()['access_token']
    print(f'Access Token: {access_token}')
else:
    print(f'Failed to get access token: {response.status_code}')
    print(response.json())
