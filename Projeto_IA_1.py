import numpy as np

class Library():
    def __init__(self,n_livros,tempo_signup,livros_dia,livros):
        self.n_livros = n_livros
        self.tempo_signup = tempo_signup
        self.livros_dia = livros_dia
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
    filename = ler_opcao(op)
    print(filename + "\n")
    
    

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
  
