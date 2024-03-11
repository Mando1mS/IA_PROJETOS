import numpy as np
import os
from sys import exit

class Library():
    def __init__(self,n_livros,tempo_signup,livros_dia,livros):
        # Numero de livros na livraria
        self.n_livros = n_livros
        # Tempo que demora a registar
        self.tempo_signup = tempo_signup
        # Quantos livros por dia consegue registar
        self.livros_dia = livros_dia
        # Array com todos os IDs dos livros
        self.livros = livros
        
        
def ler_opcao(op):
    if op == 1:
        filename = os.path.join("task_files/", "a_example.txt")
    elif op == 2:
        filename = os.path.join("task_files/", "b_read_on.txt")
    elif op == 3:
        filename = os.path.join("task_files/", "c_incunabula.txt")
    elif op == 4:
        filename = os.path.join("task_files/", "d_tough_choices.txt")
    elif op == 5:
        filename = os.path.join("task_files/", "e_so_many_books.txt")
    elif op == 6:
        filename = os.path.join("task_files/", "f_libraries_of_the_world.txt")
    else:
        print("error reading option\n")
        return "err"
    return filename

def verify_exit():
    check = ''

    print("\nAre you sure you want to exit? (Y/N): ")

    while True:
        check = input().lower()

        if check == 'y':
            exit()
        elif check == 'n':
            menu()
            break
        else:
            print("\nInvalid Input, please try again")
            
def melhor_lib_dr(scores,lib,dias_restantes):
    max=0
    for lb in lib:
        currindex=0
        acc=0
        for i in range(dias_restantes):
            for j in range(lb.livros_dia):
                if(currindex <= lb.n_livros):
                    acc=acc+scores[lb.livros[currindex]]
                    currindex=+1
        if(acc>max):
            max=acc
    return max
                
                
                
                
            

def main(fileop, op):
    # Nome do ficheiro
    filename = ler_opcao(fileop)
    # Abertura do ficheiro
    file = open(filename, "r")

    # Numero total de livros | Numero total de livrarias | Limite de dias
    nlivros, nlib, deadline = map(int, file.readline().split())
    # Array com todas as pontuações dos livros, o livro numero 3 tem pontuação de socre[2]
    scores =list(map(int, file.readline().split()))

    # Lista com todas as livrarias, organizadas pela class criada acima
    lib = list()
    for i in range(nlib):
        nl, ts, ld = list(map(int, file.readline().split()))
        idlivros =list( map(int, file.readline().split()))
        lib.append(Library(nl, ts, ld, idlivros))
    res=melhor_lib_dr(scores, lib, deadline)
    print("Max: "+ str(res) + "\n")
    # Resultado com base na escolha do utilizador
    if op == 1:
        print(nlivros)
    elif op == 2:
        print(nlib)
    elif op == 3:
        print(deadline)
    else:
        print(lib[0].n_livros) # Solução errada tendo em conta o que é pedido, mas falta ser implementada

    # Fecha o ficheiro
    file.close()
    # Sai do programa (Por enquanto mete-se isto para nao voltar logo ao menu e ser mais facil ler o resultado)
    exit()

def search_options(fileop):
    while True:
        print("------------------------------------------\n")
        print("|                                        |\n")
        print("|       What info do you want to         |\n")
        print("|       retrieve from this file?         |\n")
        print("|________________________________________|\n")
        print("|                                        |\n")
        print("|       1- Number of dierent books       |\n")
        print("|       2- Number of libraries           |\n")
        print("|       3- Limit number of days          |\n")
        print("|       4- Maximized total score         |\n")
        print("|          of scanned books              |\n")
        print("|________________________________________|\n")
        print("|                                        |\n")
        print("|             [B] - Go back              |\n")
        print("|               [E] - Exit               |\n")
        print("|                                        |\n")
        print("------------------------------------------\n")
        
        op = input("Opção: ")
        
        if op.isdigit() and 1 <= int(op) <= 4:
            main(int(fileop), int(op))
            break
        elif op.lower() == 'e':
            verify_exit()
        elif op.lower() == 'b':
            menu()
            break
        else:
            print("Invalid option. Please choose a valid option (1-7).")

def menu():
    while True:
        print("------------------------------------------\n")
        print("|                                        |\n")
        print("|   Please select a file from the list   |\n")
        print("|________________________________________|\n")
        print("|                                        |\n")
        print("|    1- (A) Basic Example                |\n")
        print("|    2- (B) Read On                      |\n")
        print("|    3- (C) Incunabula                   |\n")
        print("|    4- (D) Tough Choices                |\n")
        print("|    5- (E) So Many Books                |\n")
        print("|    6- (F) Libraries of the World       |\n")
        print("|________________________________________|\n")
        print("|                                        |\n")
        print("|               [E] - Exit               |\n")
        print("|                                        |\n")
        print("------------------------------------------\n")
        
        fileop = input("Opção: ")
        
        if fileop.isdigit() and 1 <= int(fileop) <= 6:
            search_options(int(fileop))
            break
        elif fileop.lower() == 'e':
            verify_exit()
        else:
            print("Invalid option. Please choose a valid option.")
        
menu()
  
