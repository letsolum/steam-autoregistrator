import poplib, requests
import time

class Pop3Server:
    def __init__(self):
        self.server = poplib.POP3_SSL('pop-mail.outlook.com', 995)

    def getServer(self):
        return self.server
class EmailConf:

    def __init__(self):
        self.mediator = Pop3Server()
        self.server = self.mediator.getServer()

    def login(self, email, password):
        self.server.user(email)
        self.server.pass_(password)
        self.email = email
        self.password = password

    def relogin(self):
        self.mediator = Pop3Server()
        self.server = self.mediator.getServer()
        self.server.user(self.email)
        self.server.pass_(self.password)

    def __extractUrl(self, txt):
        ind1 = txt.find('https://store.steampowered.com/account/newaccountverification?stoken=')
        ind2 = txt.find('creationid')
        txt = txt[ind1:txt[ind2:].find("'") + ind2]
        txt = txt.replace('=3D', '=')
        txt = txt.replace("=', b'", '')
        return txt
    def readLastMssg(self):
        numMails = self.server.stat()[0]
        cnt = 0
        while numMails == 0:
            time.sleep(0.5)
            cnt += 1
            if (cnt >= 25):
                raise Exception("Too long captcha solving or wrong email")
            self.server.quit()
            self.relogin()
            numMails = self.server.stat()[0]
        txt = str(self.server.retr(numMails)[1])
        txt = self.__extractUrl(txt)
        while len(txt) < 10:
            time.sleep(0.5)
            cnt += 1
            if (cnt >= 25):
                raise Exception("Too long captcha solving or wrong email")
            self.server.quit()
            self.relogin()
            numMails = self.server.stat()[0]
            txt = str(self.server.retr(numMails)[1])
            txt = self.__extractUrl(txt)
        return txt

    def requestConf(self, url, proxy):
        proxy_list = {
            'https' : 'http://' + proxy
        }
        print(proxy, url)
        requests.get(url, proxies=proxy_list)
        print('Confirmed!')

    def confirm(self, login, password, proxy):
        try:
            self.login(login, password)
        except Exception:
            print(Exception, "Not logged!")
            return False
        try:
            url = self.readLastMssg()
        except Exception as error:
            print(error, "Not read!")
            return False
        try:
            self.requestConf(url, proxy)
        except Exception:
            print(Exception, "Not requested")
            return False
        return True

