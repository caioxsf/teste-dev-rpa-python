from src.graphics import GraphicsData
import pandas as pd
import os
import concurrent.futures

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
                df = pd.read_excel(path, engine="openpyxl")
                
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
        df_casos = self.dataframes.get("casos")

        df_obitos["DATA_OBITO"] = pd.to_datetime(df_obitos["DATA_OBITO"], dayfirst=True)
        df_casos["DATA"] = pd.to_datetime(df_casos["DATA"], dayfirst=True)

        obitos_grouped = df_obitos.groupby(df_obitos["DATA_OBITO"].dt.to_period("M")).size().reset_index(name="OBITOS")
        casos_grouped = df_casos.groupby(df_casos["DATA"].dt.to_period("M"))["CONFIRMADOS"].sum().reset_index()
        casos_grouped = casos_grouped.rename(columns={"DATA": "DATA_OBITO"})

        df_final = pd.merge(obitos_grouped, casos_grouped, on="DATA_OBITO", how="outer")
        df_final["OBITOS"] = df_final["OBITOS"].fillna(0).astype(int)
        df_final["CONFIRMADOS"] = df_final["CONFIRMADOS"].fillna(0).astype(int)
        df_final = df_final[df_final["DATA_OBITO"].dt.month <= 7]

        graphics_data.gerar_graficos(df_final)