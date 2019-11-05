#!/usr/bin/python3

import argparse
from pyteslaapi import Authentication, Vehicles, State

def run_tests(args):
    # optionally initialize refresh token
    authentication = Authentication()
    if args.init_refresh_token:
        # use email/password to get refresh token for account
        print("Sending request for initial authentication...")
        email = "email"
        password = "password"
        authentication.send_initial_request(email, password)
        print()

        # save valid refresh token to file
        if authentication.refresh_token is not None:
            authentication.save_refresh_token()

    # load valid refresh token to get access token for account (and update saved refresh token)
    print("Sending request for refresh authentication...")
    authentication.load_refresh_token()
    authentication.send_refresh_request()
    authentication.save_refresh_token()
    print()

    # use access token to get list of vehicles for account (and get first vehicle)
    print("Sending request for vehicles list...")
    vehicles = Vehicles(authentication.headers)
    vehicles.send_list_request()
    vehicle_0 = vehicles.get_vehicle(0)
    print("Vehicle 0:")
    print(str(vehicle_0))
    print()

    # wake up vehicle if asleep
    if vehicle_0.state == State.ASLEEP:
        vehicle_0.send_wake_up_request()
        print()

    # get all data for vehicle if awake
    if vehicle_0.state == State.ONLINE:
        vehicle_0.send_vehicle_data_request()
        print()

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init-refresh-token", action="store_true",
                        help="initialize refresh token using hard-coded email/password")
    args = parser.parse_args()

    # run tests for Tesla API
    run_tests(args)
