import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import os


class GraphicsData:
    def __init__(self, output_dir="image-graphic"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        sns.set(style="whitegrid")
        
    def gerar_graficos(self, df_final):

        sns.set(style="whitegrid")

        df_final["DATA_OBITO"] = df_final["DATA_OBITO"].astype(str)
        plt.figure(figsize=(10, 6))

        bar_width = 0.4
        x = range(len(df_final))

        plt.bar([p - bar_width/2 for p in x], df_final["OBITOS"], width=bar_width, label="Óbitos Confirmados", color="tomato")
        plt.bar([p + bar_width/2 for p in x], df_final["CONFIRMADOS"], width=bar_width, label="Casos Confirmados", color="steelblue")

        plt.xlabel("Mês")
        plt.ylabel("Quantidade")
        plt.title("Óbitos e Casos Confirmados de COVID-19 por Mês")
        plt.xticks(x, df_final["DATA_OBITO"])
        plt.legend()
        plt.yscale("log")
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y):,}'))
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/covid19_obitos_e_casos.png")
        plt.close()
        
        
