from jira import JIRA


# Ver A key de API para ser usdo no lugar do usuário
class MesaJira:

    def __init__(self, access_file):
        self.jira = None
        access = open(access_file, mode='r', encoding='utf-8')
        self.server = access.readline().replace("\n", "")
        self.user = access.readline().replace("\n", "")
        self.token = access.readline().replace("\n", "")
        access.close()

    def get_jira_connection(self):
        self.jira = JIRA(
            server=self.server,
            basic_auth=(self.user, self.token),

        )
        return self.jira
