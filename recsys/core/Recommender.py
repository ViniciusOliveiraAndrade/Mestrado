import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix


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
                possuidado.append(1 if experiencia in tabela_dev[dev] else 0)
                # else:
                #     possuidado.append(0)
            dados.append(possuidado)

        dados_transpostos = list(map(list, zip(*dados)))

        tabela = pd.DataFrame(data=dados_transpostos, index=todas_experiencias, columns=todos_devs)
        return tabela



    def recomendar_dev_para_projeto(self,projeto, listaDevs):
        print(self.gerar_tabela_dev(listaDevs))
        tabela = self.gerar_tabela_dev(listaDevs)









