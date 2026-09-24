"""Testes automáticos do sistema de controle de peças."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main


def criar_peca(
    identificador,
    status="APROVADA",
    motivos=None,
    caixa=None,
    situacao_caixa=None,
):
    """Cria uma peça de teste com a mesma estrutura usada no programa."""
    return {
        "id": identificador,
        "peso": 100.0,
        "cor": "azul",
        "comprimento": 15.0,
        "status": status,
        "motivos": motivos or [],
        "caixa": caixa,
        "situacao_caixa": situacao_caixa,
    }


class TesteAvaliacao(unittest.TestCase):
    """Testa os critérios obrigatórios de qualidade."""

    def test_aprova_valores_minimos(self):
        motivos = main.avaliar_peca(95, "azul", 10)
        self.assertEqual(motivos, [])

    def test_aprova_valores_maximos(self):
        motivos = main.avaliar_peca(105, "verde", 20)
        self.assertEqual(motivos, [])

    def test_reprova_por_todos_os_criterios(self):
        motivos = main.avaliar_peca(110, "vermelha", 25)
        self.assertEqual(len(motivos), 3)
        self.assertTrue(any("Peso" in motivo for motivo in motivos))
        self.assertTrue(any("Cor" in motivo for motivo in motivos))
        self.assertTrue(any("Comprimento" in motivo for motivo in motivos))


class TesteCadastro(unittest.TestCase):
    """Testa a separação entre cadastro e histórico de reprovações."""

    def test_reprovada_nao_bloqueia_reutilizacao_do_id(self):
        pecas = []
        historico_reprovadas = []
        caixa_atual = []
        caixas_fechadas = []

        with patch(
            "builtins.input",
            side_effect=["1", "100", "azul", "21"],
        ):
            with redirect_stdout(io.StringIO()):
                main.cadastrar_peca(
                    pecas,
                    historico_reprovadas,
                    caixa_atual,
                    caixas_fechadas,
                )

        self.assertEqual(pecas, [])
        self.assertEqual(len(historico_reprovadas), 1)

        with patch(
            "builtins.input",
            side_effect=["1", "100", "azul", "15"],
        ):
            with redirect_stdout(io.StringIO()):
                main.cadastrar_peca(
                    pecas,
                    historico_reprovadas,
                    caixa_atual,
                    caixas_fechadas,
                )

        self.assertEqual(len(pecas), 1)
        self.assertEqual(pecas[0]["id"], 1)
        self.assertEqual(pecas[0]["status"], "APROVADA")


class TesteCaixas(unittest.TestCase):
    """Testa o armazenamento e o fechamento automático das caixas."""

    def test_fecha_caixa_com_dez_pecas(self):
        caixa_atual = []
        caixas_fechadas = []

        with redirect_stdout(io.StringIO()):
            for identificador in range(1, 11):
                peca = criar_peca(identificador)
                main.armazenar_peca_aprovada(
                    peca,
                    caixa_atual,
                    caixas_fechadas,
                )

        self.assertEqual(caixa_atual, [])
        self.assertEqual(len(caixas_fechadas), 1)
        self.assertEqual(len(caixas_fechadas[0]), 10)
        self.assertTrue(
            all(
                peca["situacao_caixa"] == "FECHADA"
                for peca in caixas_fechadas[0]
            )
        )


class TesteRelatorio(unittest.TestCase):
    """Testa a consolidação dos motivos de reprovação."""

    def test_conta_motivos_repetidos(self):
        motivo_peso = "Peso fora do padrão"
        motivo_cor = "Cor inválida"
        pecas = [
            criar_peca(1, "REPROVADA", [motivo_peso, motivo_cor]),
            criar_peca(2, "REPROVADA", [motivo_peso]),
        ]

        contagem = main.contar_motivos_reprovacao(pecas)

        self.assertEqual(contagem[motivo_peso], 2)
        self.assertEqual(contagem[motivo_cor], 1)


class TesteRemocao(unittest.TestCase):
    """Testa a confirmação e o cancelamento da remoção."""

    def test_remove_peca_confirmada_da_caixa_aberta(self):
        peca = criar_peca(1, caixa=1, situacao_caixa="ABERTA")
        pecas = [peca]
        caixa_atual = [peca]

        with patch("builtins.input", side_effect=["1", "s"]):
            with redirect_stdout(io.StringIO()):
                main.remover_peca(pecas, caixa_atual)

        self.assertEqual(pecas, [])
        self.assertEqual(caixa_atual, [])

    def test_mantem_peca_quando_remocao_e_cancelada(self):
        peca = criar_peca(1, caixa=1, situacao_caixa="ABERTA")
        pecas = [peca]
        caixa_atual = [peca]

        with patch("builtins.input", side_effect=["1", "n"]):
            with redirect_stdout(io.StringIO()):
                main.remover_peca(pecas, caixa_atual)

        self.assertEqual(pecas, [peca])
        self.assertEqual(caixa_atual, [peca])


if __name__ == "__main__":
    unittest.main()
