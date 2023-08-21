import poplib, requests
import time

class EmailConf:
    def __init__(self):
        self.server = poplib.POP3_SSL('pop-mail.outlook.com', 995)

    def login(self, email, password):
        self.server.user(email)
        self.server.pass_(password)
        self.email = email
        self.password = password

    def relogin(self):
        self.server.user(self.email)
        self.server.pass_(self.password)

    def readLastMssg(self):
        numMails = self.server.stat()[0]
        while numMails == 0:
            time.sleep(1)
            self.server.quit()
            self.relogin()
            numMails = self.server.stat()[0]
            print(numMails, end=' ')
        print()
        txt = str(self.server.retr(numMails)[1])
        ind1 = txt.find('https://store.steampowered.com/account/newaccountverification?stoken=')
        ind2 = txt.find('creationid')
        txt = txt[ind1:txt[ind2:].find("'") + ind2]
        txt = txt.replace('=3D', '=')
        txt = txt.replace("=', b'", '')
        return txt

    def requestConf(self, url, proxy):
        proxy_list = {
            'https' : 'http://' + proxy
        }
        requests.get(url, proxies=proxy_list)
        print('Confirmed!')

    def confirm(self, login, password, proxy):
        try:
            self.login(login, password)
        except Exception:
            return False
        url = self.readLastMssg()
        self.requestConf(url, proxy)
        return True

    def __del__(self):
        #self.server.quit()
        pass

