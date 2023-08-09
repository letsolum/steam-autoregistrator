from registr import RegisterSteam
import time

if __name__ == '__main__':
    f = open('email.txt', 'r')
    data = f.read().splitlines()
    data = data[6:]
    for user in data:
        user = user.split(':')
        login = user[0]
        password = user[1]
        autoReg = RegisterSteam(login, password)
        try:
            autoReg.new_register()
        except Exception as error:
            print(error, "error!\nskipped to next")
        #break
        time.sleep(1000000)

