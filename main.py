"""Sistema de controle de qualidade e armazenamento de peças."""

from math import isfinite


PESO_MINIMO = 95
PESO_MAXIMO = 105
COMPRIMENTO_MINIMO = 10
COMPRIMENTO_MAXIMO = 20
CORES_PERMITIDAS = {"azul", "verde"}
CAPACIDADE_CAIXA = 10


def ler_id(pecas):
    """Lê um ID inteiro positivo que não pertença a uma peça cadastrada."""
    while True:
        entrada = input("ID da peça: ").strip()

        if not entrada.isdigit() or int(entrada) <= 0:
            print("O ID deve ser um número inteiro positivo.")
            continue

        identificador = int(entrada)
        id_ja_cadastrado = any(
            peca["id"] == identificador for peca in pecas
        )

        if id_ja_cadastrado:
            print("Já existe uma peça cadastrada com esse ID.")
            continue

        return identificador


def ler_numero_positivo(mensagem):
    """Lê um número positivo, aceitando ponto ou vírgula decimal."""
    while True:
        entrada = input(mensagem).strip().replace(",", ".")

        try:
            numero = float(entrada)
        except ValueError:
            print("Digite um valor numérico válido.")
            continue

        if not isfinite(numero) or numero <= 0:
            print("O valor deve ser maior que zero.")
            continue

        return numero


def ler_cor():
    """Lê uma cor não vazia e a padroniza em letras minúsculas."""
    while True:
        cor = input("Cor da peça: ").strip().lower()

        if cor:
            return cor

        print("A cor não pode ficar vazia.")


def avaliar_peca(peso, cor, comprimento):
    """Retorna todos os motivos que tornam uma peça inadequada."""
    motivos = []

    if not PESO_MINIMO <= peso <= PESO_MAXIMO:
        motivos.append("Peso fora do padrão (permitido: 95 g a 105 g)")

    if cor not in CORES_PERMITIDAS:
        motivos.append("Cor inválida (permitidas: azul ou verde)")

    if not COMPRIMENTO_MINIMO <= comprimento <= COMPRIMENTO_MAXIMO:
        motivos.append(
            "Comprimento fora do padrão (permitido: 10 cm a 20 cm)"
        )

    return motivos


def armazenar_peca_aprovada(peca, caixa_atual, caixas_fechadas):
    """Armazena uma peça aprovada e fecha a caixa ao atingir o limite."""
    numero_caixa = len(caixas_fechadas) + 1
    peca["caixa"] = numero_caixa
    peca["situacao_caixa"] = "ABERTA"
    caixa_atual.append(peca)

    print(
        f"Peça armazenada na caixa {numero_caixa} "
        f"({len(caixa_atual)}/{CAPACIDADE_CAIXA})."
    )

    if len(caixa_atual) == CAPACIDADE_CAIXA:
        for peca_armazenada in caixa_atual:
            peca_armazenada["situacao_caixa"] = "FECHADA"

        caixas_fechadas.append(caixa_atual.copy())
        caixa_atual.clear()
        print(f"Caixa {numero_caixa} finalizada.")


def cadastrar_peca(
    pecas,
    historico_reprovadas,
    caixa_atual,
    caixas_fechadas,
):
    """Avalia uma peça e cadastra somente quando ela for aprovada."""
    print("\n===== CADASTRO DE PEÇA =====")
    identificador = ler_id(pecas)
    peso = ler_numero_positivo("Peso em gramas: ")
    cor = ler_cor()
    comprimento = ler_numero_positivo("Comprimento em centímetros: ")

    motivos = avaliar_peca(peso, cor, comprimento)
    status = "REPROVADA" if motivos else "APROVADA"

    peca = {
        "id": identificador,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento,
        "status": status,
        "motivos": motivos,
        "caixa": None,
        "situacao_caixa": None,
    }
    if status == "REPROVADA":
        historico_reprovadas.append(peca)
        print(
            f"\nPeça {identificador} REPROVADA. "
            "O cadastro não foi realizado."
        )
        print("Motivos da reprovação:")
        for motivo in motivos:
            print(f"- {motivo}")
        return

    pecas.append(peca)
    print(f"\nPeça {identificador} cadastrada e APROVADA.")
    armazenar_peca_aprovada(peca, caixa_atual, caixas_fechadas)


def exibir_peca(peca):
    """Exibe todas as informações armazenadas de uma peça."""
    print(f"\nPEÇA {peca['id']} - {peca['status']}")
    print(f"Peso: {peca['peso']:g} g")
    print(f"Cor: {peca['cor']}")
    print(f"Comprimento: {peca['comprimento']:g} cm")

    if peca["status"] == "APROVADA":
        print(f"Caixa: {peca['caixa']}")
        print(f"Situação da caixa: {peca['situacao_caixa'].lower()}")
    else:
        print("Motivos da reprovação:")
        for motivo in peca["motivos"]:
            print(f"- {motivo}")


def listar_pecas(pecas, historico_reprovadas):
    """Lista peças cadastradas e o histórico separado de reprovações."""
    if not pecas and not historico_reprovadas:
        print("\nNenhuma inspeção foi realizada.")
        return

    while True:
        print("\n===== LISTAGEM DE PEÇAS =====")
        print("1. Listar todos os resultados de inspeção")
        print("2. Listar peças cadastradas e aprovadas")
        print("3. Listar histórico de reprovações")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            return

        if opcao == "1":
            pecas_selecionadas = pecas + historico_reprovadas
            titulo = "RESULTADOS DE INSPEÇÃO"
        elif opcao == "2":
            pecas_selecionadas = pecas
            titulo = "PEÇAS CADASTRADAS E APROVADAS"
        elif opcao == "3":
            pecas_selecionadas = historico_reprovadas
            titulo = "HISTÓRICO DE REPROVAÇÕES"
        else:
            print("Opção inválida. Escolha um número entre 0 e 3.")
            continue

        print(f"\n===== {titulo} =====")

        if not pecas_selecionadas:
            print("Nenhuma peça encontrada nessa categoria.")
            continue

        for peca in pecas_selecionadas:
            exibir_peca(peca)


def remover_peca(pecas, caixa_atual):
    """Remove uma peça cadastrada depois da confirmação do usuário."""
    if not pecas:
        print("\nNenhuma peça foi cadastrada.")
        return

    print("\n===== REMOÇÃO DE PEÇA =====")
    entrada = input("Digite o ID da peça ou 0 para cancelar: ").strip()

    if entrada == "0":
        print("Remoção cancelada.")
        return

    if not entrada.isdigit() or int(entrada) <= 0:
        print("ID inválido. Digite um número inteiro positivo.")
        return

    identificador = int(entrada)
    peca_encontrada = next(
        (peca for peca in pecas if peca["id"] == identificador),
        None,
    )

    if peca_encontrada is None:
        print(f"Nenhuma peça encontrada com o ID {identificador}.")
        return

    exibir_peca(peca_encontrada)

    while True:
        confirmacao = input("Confirmar remoção? (S/N): ").strip().lower()

        if confirmacao == "s":
            if peca_encontrada in caixa_atual:
                caixa_atual.remove(peca_encontrada)

            pecas.remove(peca_encontrada)
            print(f"Peça {identificador} removida com sucesso.")
            return

        if confirmacao == "n":
            print("Remoção cancelada.")
            return

        print("Resposta inválida. Digite S para confirmar ou N para cancelar.")


def listar_caixas_fechadas(caixas_fechadas):
    """Exibe as caixas que atingiram a capacidade máxima."""
    print("\n===== CAIXAS FECHADAS =====")

    if not caixas_fechadas:
        print("Nenhuma caixa foi fechada.")
        return

    for numero_caixa, caixa in enumerate(caixas_fechadas, start=1):
        ids = ", ".join(str(peca["id"]) for peca in caixa)
        print(f"\nCaixa {numero_caixa} - FECHADA")
        print(f"Quantidade: {len(caixa)}/{CAPACIDADE_CAIXA}")
        print(f"Peças: {ids}")


def contar_motivos_reprovacao(pecas_reprovadas):
    """Conta quantas vezes cada motivo de reprovação foi registrado."""
    contagem = {}

    for peca in pecas_reprovadas:
        for motivo in peca["motivos"]:
            contagem[motivo] = contagem.get(motivo, 0) + 1

    return contagem


def gerar_relatorio(
    pecas,
    historico_reprovadas,
    caixa_atual,
    caixas_fechadas,
):
    """Exibe peças cadastradas e o histórico separado de reprovações."""
    pecas_aprovadas = pecas
    pecas_reprovadas = historico_reprovadas
    quantidade_caixas = len(caixas_fechadas)

    if caixa_atual:
        quantidade_caixas += 1

    print("\n===== RELATÓRIO FINAL =====")
    print(
        f"Total de peças inspecionadas: "
        f"{len(pecas_aprovadas) + len(pecas_reprovadas)}"
    )
    print(f"Total de peças cadastradas: {len(pecas_aprovadas)}")
    print(f"Total de peças aprovadas: {len(pecas_aprovadas)}")
    print(f"Total de inspeções reprovadas: {len(pecas_reprovadas)}")
    print(f"Quantidade de caixas utilizadas: {quantidade_caixas}")
    print(f"Quantidade de caixas finalizadas: {len(caixas_fechadas)}")

    if caixa_atual:
        print(
            f"Ocupação da caixa atual: "
            f"{len(caixa_atual)}/{CAPACIDADE_CAIXA}"
        )

    print("\n===== MOTIVOS DE REPROVAÇÃO =====")
    contagem_motivos = contar_motivos_reprovacao(pecas_reprovadas)

    if contagem_motivos:
        for motivo, quantidade in contagem_motivos.items():
            print(f"- {motivo}: {quantidade}")
    else:
        print("Nenhuma reprovação registrada.")

    print("\n===== PEÇAS APROVADAS =====")

    if pecas_aprovadas:
        for peca in pecas_aprovadas:
            exibir_peca(peca)
    else:
        print("Nenhuma peça aprovada.")

    print("\n===== HISTÓRICO DE REPROVAÇÕES =====")

    if pecas_reprovadas:
        for peca in pecas_reprovadas:
            exibir_peca(peca)
    else:
        print("Nenhuma inspeção reprovada.")


def exibir_menu():
    """Exibe as opções disponíveis no menu principal."""
    print("\n===== CONTROLE DE PEÇAS =====")
    print("1. Cadastrar nova peça")
    print("2. Listar peças e histórico de reprovações")
    print("3. Remover peça cadastrada")
    print("4. Listar caixas fechadas")
    print("5. Gerar relatório final")
    print("0. Sair")


def main():
    """Mantém o programa em execução até o usuário escolher sair."""
    pecas = []
    historico_reprovadas = []
    caixa_atual = []
    caixas_fechadas = []

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Programa encerrado.")
            break

        if opcao == "1":
            cadastrar_peca(
                pecas,
                historico_reprovadas,
                caixa_atual,
                caixas_fechadas,
            )
        elif opcao == "2":
            listar_pecas(pecas, historico_reprovadas)
        elif opcao == "3":
            remover_peca(pecas, caixa_atual)
        elif opcao == "4":
            listar_caixas_fechadas(caixas_fechadas)
        elif opcao == "5":
            gerar_relatorio(
                pecas,
                historico_reprovadas,
                caixa_atual,
                caixas_fechadas,
            )
        else:
            print("Opção inválida. Escolha um número entre 0 e 5.")


if __name__ == "__main__":
    main()
