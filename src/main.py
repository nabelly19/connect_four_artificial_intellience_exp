from gui.controller import run_pygame

def main():
    print("\nEscolha o nível do agente:")
    print("1 - Iniciante")
    print("2 - Intermediário")
    print("3 - Profissional")
    choice = input("Digite 1/2/3: ")

    level_map = {"1": "iniciante", "2": "intermediario", "3": "profissional"}
    level = level_map.get(choice, "intermediario")
    
    run_pygame(level)

if __name__ == "__main__":
    main()
