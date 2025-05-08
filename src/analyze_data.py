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