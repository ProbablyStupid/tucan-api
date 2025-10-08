import requests
import re

session = requests.Session()

# !!! WIP !!!
class tucan_session:
    def __init__(self):
        self.sessionNo = '000000000000001'
        self.sessionString = '-N000000000000001'

    def setSession(self, sessionString):
        print(f"setting session string: {sessionString}")
        self.sessionString = sessionString
        self.sessionNo = re.search('-N([0-9]+)', sessionString).groups()[0]

apisession = tucan_session()

def init():
    session = requests.Session()
    apisession = tucan_session()

# returns the requests-response
def signin(username, password):
    url = "https://www.tucan.tu-darmstadt.de/scripts/mgrqispi.dll"

    # This is the default payload structure taken from a front-page login on TUCAN
    # payload = {
    #     'usrname': f'{username}',
    #     'pass': f'{password}',
    #     'APPNAME': 'CampusNet',
    #     'PRGNAME': 'LOGINCHECK',
    #     'ARGUMENTS': 'clino,usrname,pass,menuno,menu_type,browser,platform',
    #     'clino': '000000000000001',
    #     'menuno': '000344',
    #     'menu_type': 'classic',
    #     'browser': '',
    #     'platform': '',
    # }

    payload = f'usrname={username}&pass={password}%21&APPNAME=CampusNet&PRGNAME=LOGINCHECK&ARGUMENTS=clino%2Cusrname%2Cpass%2Cmenuno%2Cmenu_type%2Cbrowser%2Cplatform&clino=000000000000001&menuno=000344&menu_type=classic&browser=&platform='

    r = session.post(url, data=payload)

    print(r.text)

    refresh_header = r.headers.get('REFRESH')
    print(f'refresh_header: {refresh_header}')

    # TODO: more gracefully shut down when signing in doesn't work!
    # Because this not matching crashes the application

    apisession.setSession(re.search('ARGUMENTS=(.{17})', refresh_header).groups()[0])
    print(f"Session String = {apisession.sessionString}")

    return r

def signout():
    print("Signing out of TUCAN")
    url = f'https://www.tucan.tu-darmstadt.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=LOGOUT&ARGUMENTS={apisession.sessionString},-N001'
    r = session.get(url)
    return r

# This returns the WEBPAGE of the schedule. It's a little bit useless.
def getschedule():
    url = "https://www.tucan.tu-darmstadt.de/scripts/mgrqispi.dll"
    payload = f'APPNAME=CampusNet&PRGNAME=SCHEDULER'

    testurl = f'https://www.tucan.tu-darmstadt.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=SCHEDULER&ARGUMENTS={apisession.sessionString},-N000268,-A,-A,-N1'
    r = session.get(testurl)
    return r

def download_schedule_week(year, calendar_week):
    # This api wants multiple calls.
    # Call 1: start the export

    # This is a post request - no URL variables
    url1 = f"https://www.tucan.tu-darmstadt.de/scripts/mgrqispi.dll"

    # Because the API is very old, it wants FormData.
    # Luckily, we can just use a string - It's not super robust, but it will work

    payload1 = f'month=0&week=Y{year}W{calendar_week}&APPNAME=CampusNet&PRGNAME=SCHEDULER_EXPORT_START&ARGUMENTS=sessionno%2Cmenuid%2Cdate&sessionno={apisession.sessionNo}&menuid=000272&date=Y{year}W{calendar_week}'
    response1 = session.post(url1, data=payload1)

    filetransfer = re.search('href="/scripts/(filetransfer\.exe\?.*)"', response1.text).groups()[0]

    url2 = f'https://www.tucan.tu-darmstadt.de/scripts/{filetransfer}'
    print(f'url2: {url2}')

    response2 = session.get(url2)
    return response2

def download_schedule_month(year, calendar_month):
    # This api wants multiple calls.
    # Call 1: start the export

    # This is a post request - no URL variables
    url1 = f"https://www.tucan.tu-darmstadt.de/scripts/mgrqispi.dll"

    # Because the API is very old, it wants FormData.
    # Luckily, we can just use a string - It's not super robust, but it will work

    payload1 = f'month=Y{year}M{calendar_month}&week=0&APPNAME=CampusNet&PRGNAME=SCHEDULER_EXPORT_START&ARGUMENTS=sessionno%2Cmenuid%2Cdate&sessionno={apisession.sessionNo}&menuid=000272&date=Y{year}M{calendar_month}'
    response1 = session.post(url1, data=payload1)

    filetransfer = re.search('href="/scripts/(filetransfer\.exe\?.*)"', response1.text).groups()[0]

    url2 = f'https://www.tucan.tu-darmstadt.de/scripts/{filetransfer}'
    print(f'url2: {url2}')

    response2 = session.get(url2)
    return response2

def flushapi():
    session.close()
    session = None
    apisession = None
    return

def dumpcookies():
    print("Cookie Dump Below:")
    print(session.cookies.get_dict())
