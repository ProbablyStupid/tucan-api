import api
import requests
import env

if __name__ == '__main__':
    print("Starting TUCAN-API by Celeste Kaliwe")

    auth = env.read_env()
    print(str(auth['username']))
    print(str(auth['password']))

    response = api.signin(str(auth['username']), str(auth['password']))

    print(response.text)

    print("Getting schedule")
    response = api.getschedule()
    print(response.text)

    response = api.download_schedule_week(2025, 42)

    open('download.ics', 'wb').write(response.content)

    api.signout()

    print("End of main")