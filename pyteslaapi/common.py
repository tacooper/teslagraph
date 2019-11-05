#!/usr/bin/python3

def handle_result(result):
    if not result.ok:
        # handle error code for invalid response
        print(result)

    # get JSON for in/valid response
    try:
        response = result.json()
    except:
        return None

    if not result.ok:
        # display reason for various formats of invalid request
        if "error" in response:
            print(response["error"])
        elif "error_description" in response:
            print(response["error_description"])
        elif "response" in response:
            print(response["response"])
    else:
        # return valid response for further parsing
        return response

    return None
