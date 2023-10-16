
import unittest
import json


def importar_tabela_valores():
    with open('../data/tabela36_pvc.json', 'r') as arquivo:
        tabela_valores = json.load(arquivo)
    return tabela_valores


class TestImportacaoTabela(unittest.TestCase):
    def test_importacao_bem_sucedida(self):
        tabela = importar_tabela_valores()
        self.assertIsNotNone(tabela)


if __name__ == "__main__":
    unittest.main()
