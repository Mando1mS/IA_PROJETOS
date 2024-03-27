import numpy as np
import math
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
    print("temp: ",solution_score)
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
        print("temp: ",temp)
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
'''
def evaluate_solution(libs, scores, dias_total):

    books_read = []
    current_score = 0
    signed_up_libs = []
    print("---------")
    for lib in libs:
        time_spent = calc_time(signed_up_libs)
        signed_up_libs.append(lib)

        print("tempo: ",(lib.tempo_signup + time_spent))
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
'''

def evaluate_solution(libs, scores, dias_total):
    books_read = set()
    current_score = 0
    signed_up_libs = []
    
    ordered_books_all = {}  # Store ordered books for all libraries
    
    for lib in libs:
        time_spent = calc_time(signed_up_libs)
        signed_up_libs.append(lib)
        
        if dias_total < (lib.tempo_signup + time_spent):
            break  # No time left to sign up more libraries
        
        if lib not in ordered_books_all:
            ordered_books_all[lib] = order_books(lib, scores)
        
        ordered_books = ordered_books_all[lib]
        
        dias_ativos = dias_total - (lib.tempo_signup + time_spent)
        total_livros = min(dias_ativos * lib.livros_dia, lib.n_livros - 1)
        
        for book in ordered_books[:total_livros]:
            if book not in books_read:
                current_score += scores[book]
                books_read.add(book)
                
    return current_score
                    


def order_books(lib,scores):
    ordered_books = sorted(lib.livros, key=lambda book_id: scores[book_id], reverse=True)
    return ordered_books

def calc_time(libs):
    tempo = 0
    for lib in libs:
        tempo += lib.tempo_signup
    return tempo

def Sim_annealing(nlib,lib,scores,deadline,Tmax,Tmin):
    best_solution=select_random_config(lib, deadline, nlib)
    best_cost=evaluate_solution(best_solution, scores, deadline)
    while(Tmax > Tmin):
        neighbor=get_neighbors_sa(lib,best_solution,deadline)
        new_cost=evaluate_solution(neighbor, scores, deadline)
        dif=new_cost - best_cost
        if(dif >= 0):
            best_cost = new_cost
            best_solution = neighbor
        elif(math.exp(dif/Tmax)>random.random()):
            best_cost = new_cost
            best_solution = neighbor
        Tmax=Tmax-1
    return best_cost

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
        
def get_neighbors_sa(todas_lib,lib_sol,deadline):
    if(0.5>random.random()):
        #print("Solucao len\n" + str(len(lib_sol))+"\n")
        nums = list(range(0,len(lib_sol)))
        random.shuffle(nums)
        if nums:
            n1= nums.pop()
            n2= nums.pop()
            tmp= lib_sol[n2]
            lib_sol[n2]=lib_sol[n1]
            lib_sol[n1]=tmp
    else:
        visited_lib = []
        tam_original=len(lib_sol)
        nums = list(range(0,len(lib_sol)))
        random.shuffle(nums)
        n = nums.pop()
        rem=lib_sol[n]
        lib_sol.remove(lib_sol[n])
        tot=0
        for lb in lib_sol:
            tot=tot+lb.tempo_signup
            visited_lib.append(lb)
        tempolivre = deadline-tot-1
        while(1):
            if not nums:
                break
            else:
                nr=nums.pop()
                if((todas_lib[nr] not in visited_lib) and (todas_lib[nr].tempo_signup<=tempolivre)):
                    lib_sol.append(todas_lib[nr])
                    break
        if(len(lib_sol)!=tam_original):
            lib_sol.append(rem)
    return lib_sol
    


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

    #res=melhor_lib_dr(scores, lib, deadline)
    #Mete o valor dos livros ja usados a 0
    #reset_score(res[1],scores,deadline)
    #print("Max: "+ str(res[0]) + " Signup: " + str(res[1].tempo_signup)+" Scores atualizados"+ str(scores) +"\n")
    # Resultado com base na escolha do utilizador
    if op == 1:
        print(nlivros)
    elif op == 2:
        Tmax=nlib*4
        Tmin=0
        res = Sim_annealing(nlib,lib,scores,deadline,Tmax,Tmin)
        print("Custo final: " + str(res) + " \n")
        
        
    elif op == 3:
        print(deadline)
    elif op == 4:
        print(tabu_search(lib,scores,deadline,tabuSize,iterations))
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
            total_score_menu(fileop)
            break
        elif op.lower() == 'e':
            verify_exit()
        elif op.lower() == 'b':
            menu()
            break
        else:
            print("Invalid option. Please choose a valid option (1-7).")


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
        elif op.lower() == 'e':
            verify_exit()
        elif op.lower() == 'b':
            search_options()
            break
        else:
            print("Invalid option. Please choose a valid option (1-7).")



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
            main(int(fileop), 4,int(op),int(op2))
            break
        else:
            print("Invalid option. Please choose a valid option.")
        


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
  
