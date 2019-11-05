#!/usr/bin/python3

import pyteslaapi.common as common
import requests

# define constants
API_URL = "https://owner-api.teslamotors.com/oauth/token"
CLIENT_ID = "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384"
CLIENT_SECRET = "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3"
REFRESH_TOKEN_FILE = "refresh_token.txt"

# uses account email/password or refresh token to obtain access token for authenticating API calls
class Authentication:
    def __init__(self):
        self.refresh_token = None
        self.headers = None

    def save_refresh_token(self):
        # open and write refresh token to file
        file = open(REFRESH_TOKEN_FILE, "w")
        file.write(self.refresh_token)
        file.close()

    def load_refresh_token(self):
        # open and read refresh token from file
        file = open(REFRESH_TOKEN_FILE, "r")
        self.refresh_token = file.read()
        file.close()

    def send_initial_request(self, email, password):
        # build request with email/password
        request_data = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "email": email,
            "password": password
        }

        self.send_request(request_data)

    def send_refresh_request(self):
        # build request with refresh token
        request_data = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": self.refresh_token
        }

        self.send_request(request_data)

    def send_request(self, request_data):
        # send request to get response with access token
        result = requests.post(API_URL, data=request_data)
        response = common.handle_result(result)
        if response:
            # store refresh token and authorization headers for API calls
            self.refresh_token = response["refresh_token"]
            self.headers = {
                "Authorization": "Bearer " + response["access_token"]
            }
