from src.graphics import GraphicsData
import pandas as pd
import os
import concurrent.futures
from unidecode import unidecode

graphics_data = GraphicsData()

class AnalyzeData():
    def __init__(self,download_dir,files):
        self.download_dir = download_dir
        self.files = files
        self.dataframes = {}
        
    def load_data(self):
        
        def read_files(name, path):
            print(f"[{name}] Carregando dados...")
            
            if path.endswith(".csv"):
                df = pd.read_csv(path, sep=";")
            elif path.endswith(".xlsx"):
                df = pd.read_excel(path, engine="openpyxls")
                
            print(f"[{name}] Linhas carregadas: {len(df)}")
            return name, df
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.files)) as executor:
            futures = []
            for name, files in self.files.items():
                path = os.path.join(self.download_dir, files)
                futures.append(executor.submit(read_files, name, path))
                
            for future in concurrent.futures.as_completed(futures):
                name, df = future.result()
                self.dataframes[name] = df
                
    def cross_data(self):
        print("[CRUZAMENTO] Iniciando cruzamento de dados...")
        
        df_obitos = self.dataframes.get("obitos")
        df_contratacao = self.dataframes.get("contratacao")
        
        df_contratacao['VALOR'] = (df_contratacao['VALOR'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float))
        value_organ = df_contratacao.groupby('ORGAO_ENTIDADE')['VALOR'].sum()
        total_value = value_organ.sum()
        
        abreviacoes = {
            "Respirador purificador de ar tipo pecas semifacial filtrante classe PFF2 (N95)": "Respirador PFF2",
            "Mascara cirurgica descartavel com 3 camadas": "Máscara 3 camadas",
            "Mascaras, luvas, aventais e alcool": "Kit proteção",
            "Protetores Faciais": "Protetor facial",
            "oculos de Protecao": "Óculos",
            "Luvas para procedimentos e Gorros descartaveis": "Luvas e gorros",
            "Luvas e gorros": "Luvas e gorros",
            "Luvas": "Luvas",
            "Mascaras": "Máscaras",
            "Aventais": "Aventais",
            "Saco para obito": "Saco para óbito",
            "Fornecimento de cestas basicas as familias de estudantes matriculados na Rede Municipal de Ensino e Rede Parceira": "Cestas básicas",
            "Aquisicao de 5.000 (cinco mil) litros de alcool etilico 70% a serem usados pelos agentes da Guarda Civil Municipal de BH, o Centro Integrado de Operacões de Belo Horizonte – COP-BH e o Centro Integrado de Atencao a Mulher – CIAM, areas da SMSP que, juntamente com a GCMBH, estao atuando efetivamente para o bom funcionamento de nossa cidade e, ainda, para um melhor acolhimento dos cidadaos nesse periodo de restricões e contingenciamento.": "Álcool 70%",
            "Aquisicao de 10.000 (dez mil) unidades de mascaras cirurgicas, 3 camadas, para uso dos agentes da Guarda Civil Municipal de BH de forma preventiva contra  COVID 1, conforme orientado pela OMS.": "Máscara 3 camadas",
            "Aquisicao de 10.000 pares de luvas cirurgicas": "Luvas",
            "Aquisicao de colheres e marmitas descartaveis": "Marmitas",
            "Aquisicao de Respiradores categoria PFF2 contra agentes biologicos": "Respirador PFF2",
            "oculos de protecao": "Óculos",
            "Mascaras Cirurgicas com 3 camadas": "Máscara 3 camadas"
        }

        df_contratacao["OBJETO_NORMALIZADO"] = df_contratacao["OBJETO"].apply(lambda x: unidecode(str(x)).lower())
        abreviacoes_normalizadas = {
            unidecode(k).lower(): v for k, v in abreviacoes.items()
        }
        df_contratacao["OBJETO_ABREVIADO"] = df_contratacao["OBJETO_NORMALIZADO"].map(abreviacoes_normalizadas).fillna("Outros")
        value_object = df_contratacao.groupby("OBJETO_ABREVIADO")["VALOR"].sum()
        value_object = value_object.sort_values(ascending=False)
        
        graphics_data.contract_graphic_organ_value(value_organ, total_value)
        graphics_data.contract_graphic_object_items(value_object)