from jira import JIRA
from .models import User_jira
from django.shortcuts import get_object_or_404

# Ver A key de API para ser usdo no lugar do usuário
class MesaJira:


    def __init__(self):
        self.user = get_object_or_404(User_jira,login="vinicius.oliveira@mesainc.com.br")
        self.jira = None

    def get_jira_connection(self, host):
        self.jira = JIRA(
            server=host,
            basic_auth=(self.user.login, self.user.token),
        )
        return self.jira

    def get_squad_data(self, projeto, squad):
        jira = self.get_jira_connection(projeto.url)

        sprint = squad.sprint
        projeto_name = projeto.name

        # cards = jira.search_issues('project = \"'+projeto_name+'\" AND Sprint = '+sprint+' AND status in ("Para Iniciar", "Impedimento/Pausa") AND type in (Historia,Melhoria,Ajuste,Refatoração,Hotfix) ORDER BY type DESC')
        # for card in cards:
        #     print(card)

        ts = jira.issue('TS-658')

        # print(ts.__dict__)
        for key in ts.__dict__:
            print("Name: {} |Value: {}".format(key, ts.__dict__[key]))

        # return cards