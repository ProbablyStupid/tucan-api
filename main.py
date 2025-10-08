# Copyright (c) 2025 - Celeste Kaliwe
# Licensed under the MIT License

# This is the "console application" for the TUCAN api
# This is a reverse engineering project for the TU-Darmstadt's
# TUCaN web service for students.
# To use the resulting API yourself, consult the documentation and the api.py file.
# Alternatively, you can interact with TUCaN from the terminal using
# this application.

# The MIT License describes a limitation of liability and warranty
# - use at your own risk - this may be against existing or future
# terms of services.

import api
import requests
import env
from maskpass import askpass

def auto_signin():
    if env.check_env():
        auth = env.read_env()
        response = api.signin(str(auth['username']), str(auth['password']))
        # TODO: validate signin
        return response
    else:
        auth = {}
        auth['username'] = input('username: ')
        auth['password'] = askpass(mask="")
        response = api.signin(str(auth['username']), str(auth['password']))
        # TODO: validate signin
        return response

if __name__ == '__main__':
    print("Starting TUCAN-API by Celeste Kaliwe")

    response = auto_signin()
    print(response.text)

   # print("Getting schedule")
   # response = api.getschedule()
   # print(response.text)

   # response = api.download_schedule_week(2025, 42)

   # open('download.ics', 'wb').write(response.content)

    api.signout()

   # print("End of main")
