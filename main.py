from registr import RegisterSteam
from email_confirm import EmailConf

if __name__ == '__main__':
    f = open('email.txt', 'r')
    f_ind = open('last_conf_mail.txt', 'r')
    data = f.read().splitlines()
    ind = int(f_ind.read())
    f_ind.close()
    for i in range(ind + 1, len(data)):
        user = data[i]
        user = user.split(':')
        login = user[0]
        password = user[1]
        checkValid = EmailConf()
        f_ind = open('last_conf_mail.txt', 'w')
        f_ind.write(str(i))
        f_ind.close()
        try:
            checkValid.login(login, password)
        except Exception:
            continue
        autoReg = RegisterSteam(login, password)
        try:
            autoReg.new_register()
            autoReg.clear()
        except Exception as error:
            autoReg.clear()
            print(error, "error!\nskipped to next")

