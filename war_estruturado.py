"""
War Estruturado - Tema 1
Arquivo: war_estruturado.py

Mini-jogo em Python que simula territórios com exércitos e ataques (versão textual).
Feito para envio no GitHub como solução do desafio.

Como executar:
    python3 war_estruturado.py

Descrição resumida:
- Representa territórios como dicionário com dono e número de exércitos.
- Permite dois jogadores (modo alternado) atacarem territórios adversários.
- Usa rolagem de dados simples para decidir resultados dos ataques.
- Termina quando um jogador controla todos os territórios.
"""

import random
import textwrap

# === CONFIGURAÇÃO INICIAL (pode alterar) ===
TERRITORIOS_INICIAIS = {
    "Brasil": {"jogador": "Alice", "exercitos": 5},
    "Argentina": {"jogador": "Bob", "exercitos": 4},
    "Chile": {"jogador": "Alice", "exercitos": 3},
    "Uruguai": {"jogador": "Bob", "exercitos": 2},
    "Peru": {"jogador": "Alice", "exercitos": 2},
    "Paraguai": {"jogador": "Bob", "exercitos": 1},
}

# === FUNÇÕES DO JOGO ===

def mostrar_territorios(territorios):
    """Mostra o estado atual dos territórios de forma organizada."""
    print("\n" + "=" * 30)
    print(" ESTADO ATUAL DOS TERRITÓRIOS ")
    print("=" * 30)
    for nome, info in territorios.items():
        print(f"- {nome:10} | {info['exercitos']:2} exércitos | dono: {info['jogador']}")
    print("=" * 30 + "\n")

def validar_territorio(nome, territorios):
    """Normaliza e valida se o território existe."""
    nome_formatado = nome.strip().title()
    if nome_formatado in territorios:
        return nome_formatado
    return None

def rolar_dado(n=1):
    """Rola n dados de 6 faces e retorna uma lista de resultados."""
    return [random.randint(1, 6) for _ in range(n)]

def simular_batalha(atacante_exercitos, defensor_exercitos):
    """
    Simula uma batalha simples baseada em comparações de rolagem.
    Retorna (perda_atacante, perda_defensor).
    Regras simples:
        - atacante rola 1 dado, defensor rola 1 dado
        - maior valor vence; empate favorece a defesa
        - perdedor perde 1 exército
    """
    ataque = rolar_dado(1)[0]
    defesa = rolar_dado(1)[0]
    if ataque > defesa:
        return (0, 1)
    else:
        return (1, 0)

def atacar(territorios, origem, destino):
    """Executa o ataque de origem para destino, atualizando a estrutura."""
    origem = origem
    destino = destino

    jogador_origem = territorios[origem]["jogador"]
    jogador_destino = territorios[destino]["jogador"]

    if jogador_origem == jogador_destino:
        return "Você não pode atacar um território seu."

    if territorios[origem]["exercitos"] <= 1:
        return "Não há exércitos suficientes para atacar (é preciso deixar 1 no território)."

    perda_atacante, perda_defensor = simular_batalha(territorios[origem]["exercitos"],
                                                    territorios[destino]["exercitos"])

    territorios[origem]["exercitos"] -= perda_atacante
    territorios[destino]["exercitos"] -= perda_defensor

    mensagem = f"{jogador_origem} atacou {destino} ({jogador_destino})!\n"
    mensagem += f"Dano: atacante perdeu {perda_atacante}, defensor perdeu {perda_defensor}.\n"

    if territorios[destino]["exercitos"] <= 0:
        territorios[destino]["jogador"] = jogador_origem
        # mover 1 exército do atacante para o território conquistado
        territorios[destino]["exercitos"] = 1
        territorios[origem]["exercitos"] = max(1, territorios[origem]["exercitos"] - 1)
        mensagem += f"Território {destino} conquistado por {jogador_origem}!\n"

    return mensagem

def fortificar(territorios, origem, destino, quantidade):
    """
    Move exércitos entre territórios do mesmo jogador.
    Não permite deixar menos de 1 exército no território de origem.
    """
    origem = origem
    destino = destino
    if territorios[origem]["jogador"] != territorios[destino]["jogador"]:
        return "Só é possível fortificar entre territórios do mesmo jogador."
    if quantidade < 1:
        return "Quantidade inválida (deve ser >= 1)."
    if territorios[origem]["exercitos"] - quantidade < 1:
        return "Movimento inválido: deve permanecer pelo menos 1 exército no território de origem."
    territorios[origem]["exercitos"] -= quantidade
    territorios[destino]["exercitos"] += quantidade
    return f"{quantidade} exército(s) movido(s) de {origem} para {destino}."

def verificar_vitoria(territorios):
    """Retorna True se todos os territórios pertencem ao mesmo jogador."""
    donos = [info["jogador"] for info in territorios.values()]
    return all(dono == donos[0] for dono in donos)

def escolher_acao(jogador, territorios):
    """
    Pergunta ao jogador qual ação ele deseja:
    - atacar
    - fortificar (mover exércitos)
    - passar
    """
    print(f"Vez de {jogador}. Escolha uma ação:")
    print("1 - Atacar")
    print("2 - Fortificar (mover exércitos)")
    print("3 - Passar")
    escolha = input("Opção (1/2/3): ").strip()
    return escolha

def jogo_loop(territorios, jogadores):
    """Loop principal do jogo."""
    rodada = 1
    while True:
        print("\n" + "#" * 40)
        print(f"         RODADA {rodada}")
        print("#" * 40)
        for jogador in jogadores:
            if verificar_vitoria(territorios):
                vencedor = territorios[next(iter(territorios))]["jogador"]
                print(f"\n🏆 {vencedor} venceu o jogo! Todos os territórios foram conquistados.")
                return

            mostrar_territorios(territorios)
            acao = escolher_acao(jogador, territorios)

            if acao == "1":  # Atacar
                origem = input("Território de origem: ").title()
                destino = input("Território a atacar: ").title()
                origem_v = validar_territorio(origem, territorios)
                destino_v = validar_territorio(destino, territorios)
                if not origem_v or not destino_v:
                    print("Território inválido. Tente novamente.")
                    continue
                if territorios[origem_v]["jogador"] != jogador:
                    print("Você só pode atacar a partir de um território que é seu.")
                    continue
                resultado = atacar(territorios, origem_v, destino_v)
                print(resultado)

            elif acao == "2":  # Fortificar
                origem = input("Território de origem: ").title()
                destino = input("Território destino: ").title()
                origem_v = validar_territorio(origem, territorios)
                destino_v = validar_territorio(destino, territorios)
                if not origem_v or not destino_v:
                    print("Território inválido. Tente novamente.")
                    continue
                if territorios[origem_v]["jogador"] != jogador:
                    print("Você só pode mover exércitos entre territórios seus.")
                    continue
                try:
                    quantidade = int(input("Quantos exércitos mover? ").strip())
                except ValueError:
                    print("Número inválido.")
                    continue
                resultado = fortificar(territorios, origem_v, destino_v, quantidade)
                print(resultado)

            elif acao == "3":
                print(f"{jogador} passou a vez.")

            else:
                print("Opção inválida. Passe a vez.")
        rodada += 1

def criar_readme_text():
    """Retorna um texto curto que pode ser usado como parte de um README."""
    readme = textwrap.dedent("""
    # War Estruturado - Tema 1

    Projeto para o desafio "War Estruturado" (Tema 1).

    ## Como executar
    1. Tenha Python 3 instalado.
    2. Rode no terminal:
       ```
       python3 war_estruturado.py
       ```

    ## Arquivos
    - `war_estruturado.py`: código fonte do mini-jogo.

    ## Descrição
    - Representa territórios com dono e número de exércitos (dicionário).
    - Permite ações: atacar, fortificar (mover exércitos) e passar.
    - Usa rolagem de dados simples para resolução de batalhas.
    """)
    return readme

def main():
    print("Iniciando War Estruturado (versão textual).")
    territorios = {k: v.copy() for k, v in TERRITORIOS_INICIAIS.items()}
    jogadores = sorted(list({info["jogador"] for info in territorios.values()}))
    print(f"Jogadores: {', '.join(jogadores)}")
    jogo_loop(territorios, jogadores)

if __name__ == "__main__":
    main()
