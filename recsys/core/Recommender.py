import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from django.shortcuts import get_object_or_404

from .models import JiraIssues, Recommendation
from .MJira import MesaJira


class Recommender:

    def __init__(self):
        pass

    def gerar_tabela_issue(self, issues, devs):

        colunas = ['key', 'texto']
        linhas = []
        dados = []

        todas_issues = []
        todas_issues.extend(issues)

        todas_issues_dos_devs = []
        for dev in devs:
            for issue_dev in dev.jiraissues_set.all():
                todas_issues_dos_devs.append(issue_dev)
        todas_issues.extend(todas_issues_dos_devs)

        for count, issue in enumerate(todas_issues):
            linhas.append(count)
            dados.append([issue.key, issue.title + " " + issue.description + " " + issue.feature])

        tabela = pd.DataFrame(data=dados, index=linhas, columns=colunas)

        return tabela

    def recomendar_dev_para_projeto(self, projeto, listaDevs):
        """
        print(self.gerar_tabela_dev(listaDevs))
        tabela = self.gerar_tabela_dev(listaDevs)

        lista_de_desejo = []
        for exp in projeto.experiencia_set.all():
            lista_de_desejo.append(exp.exp)

        # criou o sparse da tabela
        tabela_sparse = csr_matrix(tabela)

        # predição por visinhos mais proximo não supervisionado
        model = NearestNeighbors(algorithm='brute')
        model.fit(tabela_sparse)

        # distancia, sugestao = model.kneighbors(np.array(lista_de_desejo).reshape(-1, 1))

        """

        """
        # Filtragem e raqueamento
        devs_recomendados = {}
        devs_e_experiencia = {}


        for dev in listaDevs:
            lista_experiencia = []
            for experiencia in dev.experiencia_set.all():
                lista_experiencia.append(experiencia.exp)
            devs_e_experiencia[dev.name] = lista_experiencia

        for experiencia in projeto.experiencia_set.all():

            for key in devs_e_experiencia:
                if experiencia.exp in devs_e_experiencia[key]:
                    if key in devs_recomendados:
                        devs_recomendados[key]=devs_recomendados[key]+1
                    else:
                        devs_recomendados[key]=1

        print(devs_recomendados)
        """

        # Filtragem ranqueada v2

        devs_recomendados = []
        devs_e_experiencia = {}

        for dev in listaDevs:
            lista_experiencia = []
            for experiencia in dev.experiencia_set.all():
                lista_experiencia.append(experiencia.exp)
            devs_e_experiencia[dev.id] = lista_experiencia

        for key in devs_e_experiencia:
            dev = {"id": key, "qt": 0}
            for experiencia in projeto.experiencia_set.all():
                if experiencia.exp in devs_e_experiencia[key]:
                    dev["qt"] += 1
            if dev["qt"] > 0:
                devs_recomendados.append(dev)

        devs_recomendados = sorted(devs_recomendados, key=lambda d: d['qt'], reverse=True)

        # print(devs_recomendados)
        return devs_recomendados

    def recomendar_dev_para_JiraIssue(self, issues, listaDevs):
        issues_recomendadas = {}
        devs_recomendados = {}
        mesa_jira = MesaJira()

        issues_cadastradas = []
        for issue in issues:
            issue_cadastrada = mesa_jira.cadastrar_issue(issue)
            issues_cadastradas.append(issue_cadastrada)

        tabela = self.gerar_tabela_issue(issues_cadastradas, listaDevs)



        def get_recomendation(key, tabela):
            tfidf = TfidfVectorizer()
            tfidf_matrix = tfidf.fit_transform(tabela['texto'])

            cosine_sim = linear_kernel(tfidf_matrix)

            indices = pd.Series(tabela.index, index=tabela['key']).drop_duplicates()
            idx = indices[key]

            sim_score = enumerate(cosine_sim[idx])
            sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)
            sim_score = sim_score[1:4]
            sim_index = [i[0] for i in sim_score]
            return tabela['key'].iloc[sim_index].tolist()


        # filtrando as issuas semelhantes
        for i in issues_cadastradas:
            issues_semelhantes_recomendadas = get_recomendation(i.key, tabela)
            issues_semelhantes = JiraIssues.objects.filter(key__in=issues_semelhantes_recomendadas)

            issues_recomendadas[i.key] = []
            for semelhante in issues_semelhantes:
                if semelhante.plataforma == i.plataforma:
                    issues_recomendadas[i.key].append(semelhante)
        print(issues_recomendadas)

        for i in issues_recomendadas:
            devs_recomendados[i] = []
            for issue_recomendado in issues_recomendadas[i]:
                if issue_recomendado.dev and issue_recomendado.dev not in devs_recomendados[i]:
                    devs_recomendados[i].append(issue_recomendado.dev)
        print(devs_recomendados)
