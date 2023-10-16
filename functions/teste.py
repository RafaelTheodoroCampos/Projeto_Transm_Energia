
from tabelas import tabela36_pvc


if __name__ == "__main__":
    tabela = tabela36_pvc
    if tabela:
        print("Importação bem-sucedida!")
        print(tabela)  # Isso imprimirá o conteúdo do JSON na saída padrão
    else:
        print("Falha na importação.")
