from jira import JIRA, JIRAError
from .models import User_jira, JiraIssues
from django.shortcuts import get_object_or_404
import re
from nltk import word_tokenize
from nltk import RSLPStemmer


# Ver A key de API para ser usdo no lugar do usuário
class MesaJira:

    def __init__(self):
        self.user = get_object_or_404(User_jira, login="vinicius.oliveira@mesainc.com.br")
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

        try:
            cards = jira.search_issues(
                'project = \"' + projeto_name + '\" AND Sprint = ' + sprint + ' AND status in ("Para Iniciar", "Impedimento/Pausa") AND type in (Historia,Melhoria,Ajuste,Refatoração,Hotfix) ORDER BY type DESC')
        except JIRAError:
            print("Deu erro pegando os dados da squad")
            print("Sprint com ID {} não existe ou você não tem permissão de visualização.".format(sprint))
            cards = []

        return cards

    def get_dev_data(self, projeto, dev):
        jira = self.get_jira_connection(projeto.url)
        dev_id = dev.id_jira
        query = 'assignee = ' + dev_id + ' AND status in (Done,"Desenv Concluido") order by created DESC'
        cards = jira.search_issues(query, maxResults=500)

        return cards

    def debugIssue(self, projeto):
        jira = self.get_jira_connection(projeto.url)

        ts = jira.issue('TS-1288')
        # print(ts.fields.customfield_10083)
        arquivo = open('issue.txt', 'w+', encoding='utf-8')
        texto = arquivo.readlines()
        for k in ts.fields.__dict__:
            print("Name: {} |Value: {}".format(k, ts.fields.__dict__[k]))
            if ts.fields.__dict__[k]:
                texto.append("\nName: {} |Value: {}".format(k, ts.fields.__dict__[k]))
        arquivo.writelines(texto)
        arquivo.close()

    def limpar_texto(self, texto):

        # Remover links
        texto_sem_links = re.sub('http://\S+|https://\S+', '', texto)

        # Tokenize o texto
        texto_tokenizado = word_tokenize(texto_sem_links)

        # Remover stopwords
        stopwords = ['a', 'à', 'adeus', 'agora', 'aí', 'ainda', 'além', 'algo', 'alguém', 'algum', 'alguma', 'algumas',
                     'alguns', 'ali', 'ampla', 'amplas', 'amplo', 'amplos', 'ano', 'anos', 'ante', 'antes', 'ao', 'aos',
                     'apenas', 'apoio', 'após', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aqui', 'aquilo', 'área',
                     'as',
                     'às',
                     'assim', 'até', 'atrás', 'através', 'baixo', 'bastante', 'bem', 'boa', 'boas', 'bom', 'bons',
                     'breve',
                     'cá', 'cada', 'catorze', 'cedo', 'cento', 'certamente', 'certeza', 'cima', 'cinco', 'coisa',
                     'coisas',
                     'com', 'como', 'conselho', 'contra', 'contudo', 'custa', 'da', 'dá', 'dão', 'daquela', 'daquelas',
                     'daquele', 'daqueles', 'dar', 'das', 'de', 'debaixo', 'dela', 'delas', 'dele', 'deles', 'demais',
                     'dentro',
                     'depois', 'desde', 'dessa', 'dessas', 'desse', 'desses', 'desta', 'destas', 'deste', 'destes',
                     'deve',
                     'devem', 'devendo', 'dever', 'deverá', 'deverão', 'deveria', 'deveriam', 'devia', 'deviam', 'dez',
                     'dezanove', 'dezasseis', 'dezassete', 'dezoito', 'dia', 'diante', 'disse', 'disso', 'disto',
                     'dito',
                     'diz',
                     'dizem', 'dizer', 'do', 'dois', 'dos', 'doze', 'duas', 'dúvida', 'e', 'é', 'ela', 'elas', 'ele',
                     'eles',
                     'em', 'embora', 'enquanto', 'entre', 'era', 'eram', 'éramos', 'és', 'essa', 'essas', 'esse',
                     'esses',
                     'esta', 'está', 'estamos', 'estão', 'estar', 'estas', 'estás', 'estava', 'estavam', 'estávamos',
                     'este',
                     'esteja', 'estejam', 'estejamos', 'estes', 'esteve', 'estive', 'estivemos', 'estiver', 'estivera',
                     'estiveram', 'estivéramos', 'estiverem', 'estivermos', 'estivesse', 'estivessem', 'estivéssemos',
                     'estiveste', 'estivestes', 'estou', 'etc', 'eu', 'exemplo', 'faço', 'falta', 'favor', 'faz',
                     'fazeis',
                     'fazem', 'fazemos', 'fazendo', 'fazer', 'fazes', 'feita', 'feitas', 'feito', 'feitos', 'fez',
                     'fim',
                     'final', 'foi', 'fomos', 'for', 'fora', 'foram', 'fôramos', 'forem', 'forma', 'formos', 'fosse',
                     'fossem',
                     'fôssemos', 'foste', 'fostes', 'fui', 'geral', 'grande', 'grandes', 'grupo', 'há', 'haja', 'hajam',
                     'hajamos', 'hão', 'havemos', 'havia', 'hei', 'hoje', 'hora', 'horas', 'houve', 'houvemos',
                     'houver',
                     'haver', 'houvera', 'houverá', 'houveram', 'houvéramos', 'houverão', 'houverei', 'houverem',
                     'houveremos',
                     'houveria', 'houveriam', 'houveríamos', 'houvermos', 'houvesse', 'houvessem', 'houvéssemos',
                     'isso',
                     'isto', 'já', 'la', 'lá', 'lado', 'lhe', 'lhes', 'lo', 'local', 'logo', 'longe', 'lugar', 'maior',
                     'maioria', 'mais', 'mal', 'mas', 'máximo', 'me', 'meio', 'menor', 'menos', 'mês', 'meses', 'mesma',
                     'mesmas', 'mesmo', 'mesmos', 'meu', 'meus', 'mil', 'minha', 'minhas', 'momento', 'muita', 'muitas',
                     'muito', 'muitos', 'na', 'nada', 'não', 'naquela', 'naquelas', 'naquele', 'naqueles', 'nas', 'nem',
                     'nenhum', 'nenhuma', 'nessa', 'nessas', 'nesse', 'nesses', 'nesta', 'nestas', 'neste', 'nestes',
                     'ninguém',
                     'nível', 'no', 'noite', 'nome', 'nos', 'nós', 'nossa', 'nossas', 'nosso', 'nossos', 'nova',
                     'novas',
                     'nove', 'novo', 'novos', 'num', 'numa', 'número', 'nunca', 'o', 'obra', 'obrigada', 'obrigado',
                     'oitava',
                     'oitavo', 'oito', 'onde', 'ontem', 'onze', 'os', 'ou', 'outra', 'outras', 'outro', 'outros',
                     'para',
                     'parece', 'parte', 'partir', 'paucas', 'pela', 'pelas', 'pelo', 'pelos', 'pequena', 'pequenas',
                     'pequeno',
                     'pequenos', 'per', 'perante', 'perto', 'pode', 'pude', 'pôde', 'podem', 'podendo', 'poder',
                     'poderia',
                     'poderiam', 'podia', 'podiam', 'põe', 'põem', 'pois', 'ponto', 'pontos', 'por', 'porém', 'porque',
                     'porquê', 'posição', 'possível', 'possivelmente', 'posso', 'pouca', 'poucas', 'pouco', 'poucos',
                     'primeira', 'primeiras', 'primeiro', 'primeiros', 'própria', 'próprias', 'próprio', 'próprios',
                     'próxima',
                     'próximas', 'próximo', 'próximos', 'pude', 'puderam', 'quais', 'quáis', 'qual', 'quando', 'quanto',
                     'quantos', 'quarta', 'quarto', 'quatro', 'que', 'quê', 'quem', 'quer', 'quereis', 'querem',
                     'queremas',
                     'queres', 'quero', 'questão', 'quinta', 'quinto', 'quinze', 'relação', 'sabe', 'sabem', 'são',
                     'se',
                     'segunda', 'segundo', 'sei', 'seis', 'seja', 'sejam', 'sejamos', 'sem', 'sempre', 'sendo', 'ser',
                     'será',
                     'serão', 'serei', 'seremos', 'seria', 'seriam', 'seríamos', 'sete', 'sétima', 'sétimo', 'seu',
                     'seus',
                     'sexta', 'sexto', 'si', 'sido', 'sim', 'sistema', 'só', 'sob', 'sobre', 'sois', 'somos', 'sou',
                     'sua',
                     'suas', 'tal', 'talvez', 'também', 'tampouco', 'tanta', 'tantas', 'tanto', 'tão', 'tarde', 'te',
                     'tem',
                     'tém', 'têm', 'temos', 'tendes', 'tendo', 'tenha', 'tenham', 'tenhamos', 'tenho', 'tens', 'ter',
                     'terá',
                     'terão', 'terceira', 'terceiro', 'terei', 'teremos', 'teria', 'teriam', 'teríamos', 'teu', 'teus',
                     'teve',
                     'ti', 'tido', 'tinha', 'tinham', 'tínhamos', 'tive', 'tivemos', 'tiver', 'tivera', 'tiveram',
                     'tivéramos',
                     'tiverem', 'tivermos', 'tivesse', 'tivessem', 'tivéssemos', 'tiveste', 'tivestes', 'toda', 'todas',
                     'todavia', 'todo', 'todos', 'trabalho', 'três', 'treze', 'tu', 'tua', 'tuas', 'tudo', 'última',
                     'últimas',
                     'último', 'últimos', 'um', 'uma', 'umas', 'uns', 'vai', 'vais', 'vão', 'vários', 'vem', 'vêm',
                     'vendo',
                     'vens', 'ver', 'vez', 'vezes', 'viagem', 'vindo', 'vinte', 'vir', 'você', 'vocês', 'vos', 'vós',
                     'vossa',
                     'vossas', 'vosso', 'vossos', 'zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', '!',
                     '"',
                     '#',
                     '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[',
                     '\\',
                     ']', '^', '`', '{', '|', '}', '~']

        texto_sem_stopwords = [p for p in texto_tokenizado if p not in stopwords]

        # Stemizar o texto
        stemmer = RSLPStemmer()
        texto_stemmizado = [stemmer.stem(p) for p in texto_sem_stopwords]

        return texto_stemmizado
        # print(texto_sem_stopwords)
        # lista_de_acentos = []
        # for c in acentos:
        #     if c not in stopwords:
        #         lista_de_acentos.append(c)

        # print(lista_de_acentos)
        # print(len(acentos))
        # print(len(lista_de_acentos))

    def cadastrar_issue(self, jiraIssue):
        print("\n\n")
        try:
            # print(jiraIssue.key)
            return get_object_or_404(JiraIssues, key=jiraIssue.key)

        except Exception:
            try:
                # print(jiraIssue.key)
                key = jiraIssue.key
                if not key:
                    key = "No Key"
            except Exception:
                key = "No Key"
                print("Key Problem")

            try:
                # print(jiraIssue.fields.summary)
                title = " ".join(self.limpar_texto(jiraIssue.fields.summary))
                if not title:
                    title = "No Title"
            except Exception:
                title = "No Title"
                print("Title Problem")

            try:
                if jiraIssue.fields.description:
                    descricao_limpa = " ".join(self.limpar_texto(jiraIssue.fields.description))
                    description = descricao_limpa

                elif hasattr(jiraIssue.fields, "customfield_10083") and jiraIssue.fields.customfield_10083:
                    descricao_limpa = " ".join(self.limpar_texto(jiraIssue.fields.customfield_10083))
                    description = descricao_limpa
                elif hasattr(jiraIssue.fields, "customfield_10084") and jiraIssue.fields.customfield_10084:
                    descricao_limpa = " ".join(self.limpar_texto(jiraIssue.fields.customfield_10084))
                    description = descricao_limpa
                else:
                    description = "No Description"

            except Exception:
                description = "No Description"
                print("Description Problem")

            try:
                # print(jiraIssue.fields.customfield_10029)
                feature = jiraIssue.fields.customfield_10029.value
                if not feature:
                    feature = "No Feature"
            except Exception:
                feature = "No Feature"
                print("Feature Problem")

            try:
                # print(jiraIssue.fields.priority)
                prioridade = jiraIssue.fields.priority
                if not prioridade:
                    prioridade = "No Priority"
            except Exception:
                prioridade = "No Priority"
                print("Priority Problem")

            try:
                # print(jiraIssue.fields.customfield_10029)
                plataforma = jiraIssue.fields.customfield_10029.value
                if not plataforma:
                    plataforma = "No Platform"
            except Exception:
                plataforma = "No Platform"
                print("Platform Problem")


            try:
                # print(jiraIssue.fields.customfield_10026)
                storyPoint = jiraIssue.fields.customfield_10026
                if not storyPoint:
                    storyPoint = 0
            except Exception:
                storyPoint = 0
                print("Story Point Problem")

            issue = JiraIssues(key=key,
                               title=title,
                               description=description,
                               feature=feature,
                               storyPoint=storyPoint,
                               prioridade=prioridade,
                               plataforma=plataforma,
                               dev=None)
            issue.save()
            return issue

