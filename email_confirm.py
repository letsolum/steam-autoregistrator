import poplib, requests


class EmailConf:
    def __init__(self):
        self.server = poplib.POP3_SSL('pop-mail.outlook.com', '995')

    def login(self, email, password):
        self.server.user(email)
        self.server.pass_(password)

    def readLastMssg(self):
        numMails = len(self.server.list()[1])
        if numMails == 0:
            return False
        txt = str(self.server.retr(numMails)[1])
        ind1 = txt.find('https://store.steampowered.com/account/newaccountverification?stoken=')
        ind2 = txt.find('creationid')
        txt = txt[ind1:txt[ind2:].find("'") + ind2]
        txt = txt.replace('=3D', '=')
        txt = txt.replace("=', b'", '')
        return txt

    def requestConf(self, url):
        proxy_list = []
        with open('proxy.txt') as f:
            proxy_list = f.read().splitlines()
        proxy_list = {
            'https' : 'http://' + proxy_list[0].split(' ')[0]
        }
        requests.get(url, proxies=proxy_list)
        print('Confirmed!')

    def confirm(self, login, password):
        self.login(login, password)
        url = self.readLastMssg()
        self.requestConf(url)

    def __del__(self):
        self.server.quit()
