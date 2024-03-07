import numpy as np
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
    if(op==1):
        filename = "a_example.txt"
    elif(op==2):
        filename = "b_read_on.txt"
    elif(op==3):
        filename = "c_incunabula.txt"
    elif(op==4):
        filename = "d_tough_choices.txt"
    elif(op==5):
        filename = "e_so_many_books.txt"
    elif(op==6):
        filename = "f_libraries_of_the_world.txt"
    else:
        print("error reading option\n")
        return "err"
    return filename


def main(op):
    # Nome do ficheiro
    filename = ler_opcao(op)
    # Abertura do ficheiro
    file = open(filename,"r")
    # Numero total de livros | Numero total de livrarias | Limite de dias 
    nlivros,nlib,deadline=map(int,file.readline().split())
    # Array com todas as pontuações dos livros, o livro numero 3 tem pontuação de socre[2]
    scores=map(int,file.readline().split())
    # Lista com todas as livrarias, organizadas pela class criada acima
    lib = list()
    for i in range(nlib):
        nl,ts,ld=map(int,file.readline().split())
        idlivros=map(int,file.readline().split())
        lib.append(Library(nl,ts,ld,idlivros))
    print(lib[0].n_livros)
    # Fecha o ficheiro
    file.close()
    # Sai do programa (Por enquanto mete-se isto para nao voltar logo ao menu e ser mais facil ler o resultado)
    exit()
    
    

def menu():
    op = 0
    while(op!=7):
        print("------------------------------------------\n")
        print("|                                        |\n")
        print("|       Selecione os dados a ler         |\n")
        print("|                                        |\n")
        print("|    1- (A) Basic Example                |\n")
        print("|    2- (B) Read On                      |\n")
        print("|    3- (C) Incunabula                   |\n")
        print("|    4- (D) Tough Choices                |\n")
        print("|    5- (E) So Many Books                |\n")
        print("|    6- (F) Libraries of the World       |\n")
        print("|                                        |\n")
        print("|    7- Sair                             |\n")
        print("|                                        |\n")
        print("------------------------------------------\n")
        op = input("Opção: ")
        main(int(op))
menu()
  
