from jira import JIRA


# Ver A key de API para ser usdo no lugar do usuário
class MesaJira:

    def __init__(self, access_file):
        access = open(access_file, mode='r', encoding='utf-8')
        # with open(access_file, "r") as access:
        #     url = access.readlines()[0]
        # self.connection = None
        self.url = access.readline().replace("\n", "")
        self.user = access.readline().replace("\n", "")
        self.psd = access.readline().replace("\n", "")
        access.close()

    def get_jira_connection(self):
        print("URL:{}\nUser:{}\nPass:{}".format(self.url, self.user, self.psd))
