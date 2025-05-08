import pandas as pd
import os
import concurrent.futures

class AnalyzeData():
    def __init__(self,download_dir,files):
        self.download_dir = download_dir
        self.files = files
        self.dataframes = {}
        
    def load_data(self):
        
        def read_files(name, path):
            print(f"[{name}] Carregando dados...")
            
            if path.endswith(".csv"):
                df = pd.read_csv(path, sep=";") # o sep=";" é pq os arquivos da segunda planilha tao separado por ;
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
        
        contract_object = df_contratacao.groupby('CONTRATADO').apply(lambda group: '\n'.join(f"- {obj} (R$ {valor:,.2f})" for obj, valor in zip(group['OBJETO'], group['VALOR'])))

        print(value_organ)
        print(contract_object)