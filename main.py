from src.download import run_threads
from src.analyze_data import AnalyzeData
import os

DOWNLOAD_DIR = os.path.join(os.getcwd(), "data")

files = {
    "obitos": "obitos-confirmados-covid-19.csv",
    "casos": "XLSX_Painel_2020.xlsx"
}

def main():
    run_threads()
    analyze = AnalyzeData(DOWNLOAD_DIR, files)
    analyze.load_data()
    analyze.cross_data()
    
if __name__ == "__main__":
    main()