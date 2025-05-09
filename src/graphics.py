import matplotlib.pyplot as plt
import seaborn as sns
import os

class GraphicsData:
    def __init__(self, output_dir="image-graphics"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        sns.set(style="whitegrid")
        
    def contract_graphic_organ_value(self, value_organ, total_value):
        sns.set(style="whitegrid")
        plt.figure(figsize=(12, 8))

        bars = plt.barh(value_organ.index, value_organ.values, color=sns.color_palette("viridis", len(value_organ)))

        plt.xlabel(f'Valor Total (R$ {total_value:,.2f})', fontsize=12, color='gray')
        plt.ylabel('Órgão', fontsize=12)
        plt.title('Gastos Totais por Órgão Público', fontsize=16)

        for bar in bars:
            width = bar.get_width()
            plt.text(width + total_value * 0.01, bar.get_y() + bar.get_height() / 2,
                f'R$ {width:,.2f}', va='center', ha='left', fontsize=10, color='black')

        plt.grid(axis='x', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/gastos_totais_por_orgao_horizontal_com_total.png")
        plt.close()
        
    def contract_graphic_object_items(self, value_object):
        plt.figure(figsize=(15, 6))
        bars = plt.bar(value_object.index, value_object.values, color='skyblue')
        plt.ylim(bottom=0.01)
        
        plt.xlabel('Tipo de Item', fontsize=12)
        plt.title('Quantidade Gasta por Tipo de Item', fontsize=16)

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.01, f'R$ {height:,.2f}', 
                ha='center', va='bottom', fontsize=10, color='black')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.savefig(f"{self.output_dir}/quantidade_gasta_por_tipo_de_item.png")
        plt.close()
        
  
                
