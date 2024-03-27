import numpy as np
import os
from sys import exit
import random
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
        
    def __str__(self):
            return (self.n_livros + self.tempo_signup + self.livros_dia +  self.livros)

            
        
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
    maxi=0
    for lb in lib:
        currindex=0
        acc=0
        temp = dias_restantes - lb.tempo_signup
        if(temp>=0):
            for i in range(temp):
                if(currindex >lb.n_livros-1):
                    break
                for j in range(lb.livros_dia):
                    if(currindex <= lb.n_livros-1):
                        acc=acc+scores[lb.livros[currindex]]
                        currindex=currindex+1
                    else:
                        break
            if(acc>maxi):
                maxi=acc
                reslib=lb
    res = [maxi,reslib]
    return res
                

def reset_score(lib,scores,dias_restantes):
    tmp = dias_restantes - lib.tempo_signup
    currindex=0
    for i in range(tmp):
        if(currindex>lib.n_livros-1):
            break
        for j in range(lib.livros_dia):
            if(currindex <= lib.n_livros-1):
                scores[lib.livros[currindex]]=0
                currindex=currindex+1
            else:
                break

def tabu_search(libs, scores, dias_total, tabu_size=10, iterations=100):
    current_solution = initial_solution(libs, scores)
    best_solution = current_solution
    tabu_list = []
    solution_score = evaluate_solution(current_solution, scores, dias_total)
    
    for i in range(iterations):
        neighbors = []
        for i in range(10):
            neighbors.append(generate_neighbors(libs, scores))
        neighbors = [n for n in neighbors if n not in tabu_list]

        if not neighbors:
            break  # No new neighbors to explore

        current_solution = max(neighbors, key=lambda x: evaluate_solution(x, scores, dias_total))
        temp = evaluate_solution(current_solution, scores, dias_total)
        if temp > evaluate_solution(best_solution, scores, dias_total):
            best_solution = current_solution
            solution_score = temp
            
        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    return (best_solution,solution_score)

def initial_solution(libs,book_scores):

    lib_scores = [(lib, library_score(lib,book_scores,libs,[1,1,1])) for lib in libs]
    
    sorted_libs = sorted(lib_scores, key=lambda x: x[1], reverse=True)
    
    sorted_libs = [lib for lib, _ in sorted_libs]
    
    return sorted_libs

def generate_neighbors(libs, book_scores):
    random_numbers = [random.randint(0, 2) for _ in range(3)]
    
    lib_scores = [(lib, library_score(lib,book_scores,libs,random_numbers)) for lib in libs]
    
    sorted_libs = sorted(lib_scores, key=lambda x: x[1], reverse=True)
    
    sorted_libs = [lib for lib, _ in sorted_libs]
    
    return sorted_libs
    

def library_score(library,book_scores,libs,weights):

    
    max_throughput = max(library.livros_dia for library in libs)
    max_signup_time = max(library.tempo_signup for library in libs)

    unique_books_score = sum(book_scores[book_id-1] for book_id in set(library.livros))
    
    # Normalize the library's throughput (you might need to adjust the normalization based on your dataset)
    normalized_throughput = library.livros_dia / max_throughput
    
    # Normalize the library's signup time (you might need to adjust the normalization based on your dataset)
    normalized_signup_time = 1 - (library.tempo_signup / max_signup_time)
    
    # Adjust these weights based on their importance to your strategy
    weight_signup_time = weights[0]
    weight_throughput = weights[1]
    weight_books_score = weights[2]
    
    # Composite score calculation
    library_priority_score = (weight_signup_time * normalized_signup_time +
                            weight_throughput * normalized_throughput +
                            weight_books_score * unique_books_score)
    
    return library_priority_score

def evaluate_solution(libs, scores, dias_total):
    if isinstance(libs, Library):
        libs = [libs]
        
    books_read = []
    current_score = 0
    signed_up_libs = []
    for lib in libs:
        time_spent = calc_time(signed_up_libs)
        signed_up_libs.append(lib)

        if(dias_total >= (lib.tempo_signup + time_spent)):
            ordered_books = order_books(lib,scores)
            dias_ativos = dias_total - (lib.tempo_signup + time_spent)
            total_livros = dias_ativos * lib.livros_dia
            if (total_livros-1)>lib.n_livros:
                total_livros = lib.n_livros
            else:
                total_livros = total_livros-1
            for i in range(total_livros):
                
                #print(ordered_books[i])
                #print(scores[ordered_books[i]-1])
                #print("---------")
                #print(len(scores))
                #print(total_livros)
                book = ordered_books[i]
                if(book not in books_read):
                    current_score += scores[book]
                    books_read.append(book)
                else:
                    continue
    return current_score
                    
def hill_climbing(libraries, book_scores, deadline):
    current_solution = initial_solution(libraries, book_scores)
    current_score = evaluate_solution(current_solution, book_scores, deadline)
    
    while True:
        neighbors = generate_neighbors(current_solution, book_scores)
        best_neighbor = max(neighbors, key=lambda neighbor: evaluate_solution(neighbor, book_scores, deadline))
        neighbor_score = evaluate_solution(best_neighbor, book_scores, deadline)
        
        if neighbor_score <= current_score:
            break  # Local maximum reached
        
        current_solution = best_neighbor
        current_score = neighbor_score
    
    return current_solution, current_score

def order_books(lib,scores):
    ordered_books = sorted(lib.livros, key=lambda book_id: scores[book_id], reverse=True)
    return ordered_books

def calc_time(libs):
    tempo = 0
    for lib in libs:
        tempo += lib.tempo_signup
    return tempo

def Sim_annealing(lib,scores,deadline,Tmax,Tmin):
    return 0

def select_random_config(lib,deadline,nlib):
    currday=0
    deck = list(range(0, nlib))
    random.shuffle(deck)
    res=list()
    for i in range(nlib):
        num = deck.pop()
        if(currday + lib[num].tempo_signup < deadline):
            currday=currday+lib[num].tempo_signup
            res.append(lib[num])
    return res
        

def main(fileop, op,iterations,tabuSize):
    # Nome do ficheiro
    filename = ler_opcao(fileop)
    # Abertura do ficheiro
    file = open(filename, "r")

    # Numero total de livros | Numero total de livrarias | Limite de dias
    nlivros, nlib, deadline = map(int, file.readline().split())
    # Array com todas as pontuações dos livros, o livro numero 3 tem pontuação de score[2]
    scores =list(map(int, file.readline().split()))
   
    # Lista com todas as livrarias, organizadas pela class criada acima
    lib = list()
    for i in range(nlib):
        nl, ts, ld = list(map(int, file.readline().split()))
        idlivros =list( map(int, file.readline().split()))
        lib.append(Library(nl, ts, ld, idlivros))

    res=melhor_lib_dr(scores, lib, deadline)
    
    # Resultado com base na escolha do utilizador

    if op == 1: #tabu_seacrh
        final_solution, solution_score = tabu_search(lib, scores, deadline, tabuSize, iterations)
        print('\n--------------------------------\n')
        #print("Final Solution:", final_solution)
        print("Solution Score:", solution_score)

    elif op == 2: #Sim_annealing
        Tmax=nlib*2
        Tmin=0
        res=select_random_config(lib, deadline, nlib)
        total_usados = 0
        for i in range(len(res)):
            total_usados = total_usados + res[i].tempo_signup
            print("lib: " + str(res[i].n_livros) + " Tempo para dar signup " + str(res[i].tempo_signup) + "\n")
            print("Deadline: " + str(deadline)+ "\n")
            print("usados: " + str(total_usados)+ "\n")
            #res=Sim_annealing(lib,scores,deadline,Tmax,Tmin)

    elif op == 3: #hill_climbing
        # Call hill climbing algorithm
        final_solution, solution_score = hill_climbing(lib, scores, deadline)
        
        # Output the result
        print('\n--------------------------------\n')
        #print("Final Solution:", final_solution)
        print("Solution Score:", solution_score)

    elif op == 4: #genetic
        #implement code here
        print(deadline)
    
    elif op == 5: #Other
        #implement code here
        print(deadline)

    # Fecha o ficheiro
    file.close()
    # Sai do programa (Por enquanto mete-se isto para nao voltar logo ao menu e ser mais facil ler o resultado)
    exit()

def tabu_search_menu(fileop):
    while True:
        print("------------------------------------------\n")
        print("|                                        |\n")
        print("|     Insert the number of iterations    |\n")
        print("|          for the tabu search.          |\n")
        print("|________________________________________|\n")

        op = input("Número de Iterações: ")

        print("------------------------------------------\n")
        print("|                                        |\n")
        print("|        Now insert the tabu size.       |\n")
        print("|________________________________________|\n")
        
        op2 = input("Tabu Size: ")

        if op.isdigit() :
            main(int(fileop), 1, int(op), int(op2))
            break
        else:
            print("Invalid option. Please choose a valid option.")
        

def total_score_menu(fileop):
    while True:
        print("------------------------------------------\n")
        print("|                                        |\n")
        print("|        What method do you want         |\n")
        print("|     to use to find the total score?    |\n")
        print("|________________________________________|\n")
        print("|                                        |\n")
        print("|       1- Tabu Search                   |\n")
        print("|       2- Simulated Annealing           |\n")
        print("|       3- Hill Climbing                 |\n")
        print("|       4- Genetic Algorithm             |\n")
        print("|       5- Other                         |\n")
        print("|________________________________________|\n")
        print("|                                        |\n")
        print("|             [B] - Go back              |\n")
        print("|               [E] - Exit               |\n")
        print("|                                        |\n")
        print("------------------------------------------\n")
        
        op = input("Opção: ")
        
        if op.isdigit() and 1 == int(op):
            tabu_search_menu(fileop)
            break
        if op.isdigit() and 2 == int(op):
            main(int(fileop),int(op),0,0)
            break
        if op.isdigit() and 3 == int(op):
            main(int(fileop),int(op),0,0)
            break
        if op.isdigit() and 4 == int(op):
            #implement code here
            break
        if op.isdigit() and 5 == int(op):
            #implement code here
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
            total_score_menu(int(fileop))
            break
        elif fileop.lower() == 'e':
            verify_exit()
        else:
            print("Invalid option. Please choose a valid option.")
        
menu()