import re

# Duly note: This requires the Username to be above the Password since otherwise, Password will also match the username
def read_env():
    file = open('.env', 'r').read()
    username = re.search('Username=(.*)(\r\n|\r|\n)', file).groups()[0]
    password = re.search('Password=(.*)', file).groups()[0]

    return {'username': username, 'password': password}

def check_env():
    file = open('.env', 'r').read()
    username = re.search('Username=(.*)(\r\n|\r|\n)', file).groups()[0]
    password = re.search('Username=(.*)', file).groups()[0]

    return username and password
