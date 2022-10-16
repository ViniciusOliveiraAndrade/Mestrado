import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

from django.contrib.staticfiles import finders


class Recommender:

    def __init__(self):
        pass

    def gerar_tabela_dev(self, devs):

        tabela_dev = {}
        todas_experiencias = []
        todos_devs = []
        dados = []

        for dev in devs:
            lista_experiencia = []
            for experiencia in dev.experiencia_set.all():
                lista_experiencia.append(experiencia.exp)
                if experiencia.exp not in todas_experiencias:
                    todas_experiencias.append(experiencia.exp)
            tabela_dev[dev.name] = lista_experiencia
            if dev.name not in todos_devs:
                todos_devs.append(dev.name)

        # print("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.")
        # print(tabela_dev)
        # print("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.")

        for dev in todos_devs:
            possuidado = []
            for experiencia in todas_experiencias:
                # if experiencia in tabela_dev[dev]:
                possuidado.append(float(1) if experiencia in tabela_dev[dev] else float(0))
                # else:
                #     possuidado.append(0)
            dados.append(possuidado)

        # dados_transpostos = list(map(list, zip(*dados)))
        dados_transpostos = dados

        tabela = pd.DataFrame(data=dados_transpostos, index=todos_devs, columns=todas_experiencias)
        return tabela



    def recomendar_dev_para_projeto(self,projeto, listaDevs):
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
            if dev["qt"]>0:
                devs_recomendados.append(dev)

        devs_recomendados = sorted(devs_recomendados, key=lambda d: d['qt'], reverse=True)

        # print(devs_recomendados)
        return devs_recomendados


    def recomendar_dev_para_JiraIssue(self,issue, listaDevs):

        # Filtragem ranqueada v1

        devs_recomendados = []
        devs_e_experiencia = {}

        for dev in listaDevs:
            lista_experiencia = []
            for experiencia in dev.experiencia_set.all():
                lista_experiencia.append(experiencia.exp)
            devs_e_experiencia[dev.id] = lista_experiencia

        for key in devs_e_experiencia:
            dev = {"id": key, "qt": 0}
            for experiencia in issue.experiencia_set.all():
                    if experiencia.exp in devs_e_experiencia[key]:
                        dev["qt"] += 1
            if dev["qt"]>0:
                devs_recomendados.append(dev)

        devs_recomendados = sorted(devs_recomendados, key=lambda d: d['qt'], reverse=True)

        # print(devs_recomendados)
        return devs_recomendados