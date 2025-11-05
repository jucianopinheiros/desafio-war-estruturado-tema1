# 💥 Desafio War Estruturado
# 🏫 Faculdade Estácio
# 👨‍🎓 Aluno: Francisco Juciano Pinheiro
# 📚 Disciplina: Estrutura de Dados - Turma 9001
# 📅 Tema 1

import random
import time

# ----------------------------------------
# Funções principais
# ----------------------------------------

def criar_jogadores():
    print("=== Configuração de Jogadores ===")
    j1 = input("Nome do Jogador 1: ").strip() or "Jogador 1"
    j2 = input("Nome do Jogador 2: ").strip() or "Jogador 2"
    return {"nome": j1, "exercitos": 10}, {"nome": j2, "exercitos": 10}

def rolar_dado():
    """Retorna um valor aleatório entre 1 e 6 (simulação de dado)."""
    return random.randint(1, 6)

def batalha(jogador1, jogador2):
    print("\n=== Iniciando Batalha ===")
    time.sleep(1)
    d1 = rolar_dado()
    d2 = rolar_dado()

    print(f"{jogador1['nome']} tirou {d1}")
    print(f"{jogador2['nome']} tirou {d2}")

    if d1 > d2:
        jogador2["exercitos"] -= 1
        print(f"{jogador1['nome']} venceu a rodada! {jogador2['nome']} perdeu 1 exército.")
    elif d2 > d1:
        jogador1["exercitos"] -= 1
        print(f"{jogador2['nome']} venceu a rodada! {jogador1['nome']} perdeu 1 exército.")
    else:
        print("Empate! Nenhum exército perdido.")

def mostrar_status(j1, j2):
    print("\n--- Situação Atual ---")
    print(f"{j1['nome']}: {j1['exercitos']} exércitos restantes")
    print(f"{j2['nome']}: {j2['exercitos']} exércitos restantes")
    print("----------------------")

def verificar_vencedor(j1, j2):
    if j1["exercitos"] <= 0:
        return j2
    elif j2["exercitos"] <= 0:
        return j1
    return None

# ----------------------------------------
# Função principal do jogo
# ----------------------------------------

def main():
    print("🎯 Bem-vindo ao Desafio War Estruturado 🎯")
    jogador1, jogador2 = criar_jogadores()

    while True:
        batalha(jogador1, jogador2)
        mostrar_status(jogador1, jogador2)

        vencedor = verificar_vencedor(jogador1, jogador2)
        if vencedor:
            print(f"\n🏆 {vencedor['nome']} conquistou a vitória!")
            break

        continuar = input("\nDeseja continuar a batalha? (s/n): ").lower()
        if continuar != "s":
            print("Batalha encerrada pelo jogador.")
            break

    print("\nFim do jogo. Obrigado por jogar!")

# ----------------------------------------
# Execução
# ----------------------------------------

if __name__ == "__main__":
    main()
