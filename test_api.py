#!/usr/bin/python3

import argparse
from pyteslaapi import *

def run_tests(args):
    # optionally initialize refresh token
    authentication = Authentication()
    if args.init_refresh_token:
        # use email/password to get refresh token for account
        print("Sending request for initial authentication...")
        email = "email"
        password = "password"
        authentication.send_initial_request(email, password)

        # save valid refresh token to file
        if authentication.refresh_token is not None:
            authentication.save_refresh_token()

    # load valid refresh token to get access token for account (and update saved refresh token)
    print("Sending request for refresh authentication...")
    authentication.load_refresh_token()
    authentication.send_refresh_request()
    authentication.save_refresh_token()

    # use access token to get list of vehicles for account
    print("Sending request for vehicles list...")
    vehicles = Vehicles(authentication.headers)
    vehicles.send_list_request()
    vehicle_0 = vehicles.vehicle_list[0]
    print("Vehicle[0]: " + str(vehicle_0))

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init-refresh-token", action="store_true",
                        help="initialize refresh token using hard-coded email/password")
    args = parser.parse_args()

    # run tests for Tesla API
    run_tests(args)
