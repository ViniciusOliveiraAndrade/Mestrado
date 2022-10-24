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

        cards = jira.search_issues('project = \"'+projeto_name+'\" AND Sprint = '+sprint+' AND status in ("Para Iniciar", "Impedimento/Pausa") AND type in (Historia,Melhoria,Ajuste,Refatoração,Hotfix) ORDER BY type DESC')


        # debug dos cards
        # for card in cards:
        #     print(card)

        # debug dos issue
        # ts = jira.issue('TS-658')
        # for key in ts.__dict__:
        #     # print("Name: {} |Value: {}".format(key, ts.__dict__[key]))
        #     print(ts.key)
        #     # print(ts.)

        # debug dos issue fields
        # ts = jira.issue('TS-658')
        # arquivo = open('issue.txt', 'w+')
        # texto = arquivo.readlines()
        # for k in ts.fields.__dict__:
        #     print("Name: {} |Value: {}".format(k, ts.fields.__dict__[k]))
        #     if ts.fields.__dict__[k]:
        #         texto.append("\nName: {} |Value: {}".format(k, ts.fields.__dict__[k]))
        # arquivo.writelines(texto)
        # arquivo.close()


        return cards