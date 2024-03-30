import numpy as np
import math
import os
from sys import exit
import random
import copy
from math import ceil

class Library():
    def __init__(self,id_liv,n_livros,tempo_signup,livros_dia,livros):
        self.id_liv = id_liv
        # Number of books in the library
        self.n_livros = n_livros
        # Time it takes to sign up
        self.tempo_signup = tempo_signup
        # Number of books it can sign up per day
        self.livros_dia = livros_dia
        # Array with all book IDs
        self.livros = livros
        
    def __str__(self):
        # Convert all attributes to strings and concatenate them for representation
        return (self.n_livros + self.tempo_signup + self.livros_dia +  self.livros)

''' UTILS '''    
# Map the user's option to the corresponding filename 
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
        # If the option is invalid, print an error message and return "err"
        print("error reading option\n")
        return "err"
    return filename

# Determine the suffix for the final filename based on the option
def nome_ficheiro_final(op):
    if op==1:
        # Tabu Search
        nomefinal = "_TS_out.txt"
    elif op==2:
        # Simulated Annealing
        nomefinal = "_SA_out.txt"
    elif op==3:
        # Hill Climbing
        nomefinal = "_HC_out.txt"
    elif op==4:
        # Genetic Algorithm
        nomefinal = "_GA_out.txt"
    elif op==5:
        # Iterated Local Search
        nomefinal = "_ILS_out.txt"
    return nomefinal

# Verification that the user wants to leave the program
def verify_exit():
    check = ''
    print("\nAre you sure you want to exit? (Y/N): ")
    while True:
        check = input().lower()

        if check == 'y':
            # Exit the program
            exit()
        elif check == 'n':
            # Exit the loop
            menu()
            break
        else:
            print("\nInvalid Input, please try again")

# Creates an output file with the final solution.
def create_file(res, filename, scores, deadline, op):
    dict_sol = {}
    evaluate_solution(res[0], scores, deadline, dict_sol)
    nm = nome_ficheiro_final(op)
    out = os.path.basename(filename).replace(".txt", nm)

    # Define the folder path
    file_path = os.path.join("results", out)

    # Ensure that the directory structure exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write the file
    with open(file_path, 'w') as fileout:
        fileout.write(str(len(res[0])))
        fileout.write("\n")
        for lib in res[0]:
            try:
                fileout.write(str(lib.id_liv) + " " + str(len(dict_sol.get(lib.id_liv))) + "\n")
            except TypeError:
                fileout.write(str(lib.id_liv))
            try:
                for book in dict_sol.get(lib.id_liv):
                    fileout.write(str(book) + " ")
            except TypeError:
                fileout.write(" Assigned after deadline is over ")
            fileout.write("\n")

# Generate initial solution by scoring each library and sorting them based on their scores in descending order
def initial_solution(libs,book_scores):
    lib_scores = [(lib, library_score(lib,book_scores,libs,[1,1,1])) for lib in libs]
    sorted_libs = sorted(lib_scores, key=lambda x: x[1], reverse=True)
    sorted_libs = [lib for lib, _ in sorted_libs]
    return sorted_libs

# Generate neighboring solutions by applying a random strategy
def generate_neighbors(libs, book_scores):
    random_numbers = [random.randint(0, 2) for _ in range(3)]
    lib_scores = [(lib, library_score(lib,book_scores,libs,random_numbers)) for lib in libs]
    sorted_libs = sorted(lib_scores, key=lambda x: x[1], reverse=True)
    sorted_libs = [lib for lib, _ in sorted_libs]
    return sorted_libs

# Calculate a priority score for a given library based on its characteristics and scores  
def library_score(library,book_scores,libs,weights):
    max_throughput = max(library.livros_dia for library in libs)
    max_signup_time = max(library.tempo_signup for library in libs)

    unique_books_score = sum(book_scores[book_id-1] for book_id in set(library.livros))
    
    normalized_throughput = library.livros_dia / max_throughput
    
    normalized_signup_time = 1 - (library.tempo_signup / max_signup_time)
    weight_signup_time = weights[0]
    weight_throughput = weights[1]
    weight_books_score = weights[2]
    
    library_priority_score = (weight_signup_time * normalized_signup_time +
                            weight_throughput * normalized_throughput +
                            weight_books_score * unique_books_score)
    
    return library_priority_score

# Evaluate the quality/score of a solution based on signed up libraries and read books.
def evaluate_solution(libs, scores, dias_total,dict_sol={}):
    if isinstance(libs, Library):
        libs = [libs]
    
    books_read = set()
    current_score = 0
    signed_up_libs = []
    
    ordered_books_all = {}
    
    for lib in libs:
        time_spent = calc_time(signed_up_libs)
        signed_up_libs.append(lib)
        
        if dias_total < (lib.tempo_signup + time_spent):
            # No time left to sign up more libraries
            break 
        
        if lib not in ordered_books_all:
            ordered_books_all[lib] = order_books(lib, scores)
        
        ordered_books = ordered_books_all[lib]
        
        dias_ativos = dias_total - (lib.tempo_signup + time_spent)
        total_livros = min(dias_ativos * lib.livros_dia, lib.n_livros - 1)
        book_out = []
        for book in ordered_books[:total_livros]:
            if book not in books_read:
                current_score += scores[book]
                books_read.add(book)
            book_out.append(book)
        dict_sol.update({lib.id_liv : book_out})
                
    return current_score

# Order the books in a library based on their scores.                    
def order_books(lib,scores):
    ordered_books = sorted(lib.livros, key=lambda book_id: scores[book_id], reverse=True)
    return ordered_books

# Calculate the total signup time required for a list of libraries.
def calc_time(libs):
    tempo = 0
    for lib in libs:
        tempo += lib.tempo_signup
    return tempo

''' TABU SEARCH ''' 
# Perform Tabu Search algorithm to find the best solution for library scheduling.                   
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
            break  

        current_solution = max(neighbors, key=lambda x: evaluate_solution(x, scores, dias_total))

        temp = evaluate_solution(current_solution, scores, dias_total)

        print("Score Attempt: " + str(temp))

        if temp > evaluate_solution(best_solution, scores, dias_total):
            best_solution = current_solution
            solution_score = temp

        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    return best_solution,solution_score

''' SIMULATED ANNEALING '''
# Perform Simulated Annealing algorithm to find the best solution for library scheduling.  
def Sim_annealing(nlib,lib,scores,deadline,Tmax,Tmin):
    best_solution=select_random_config(lib, deadline, nlib)
    best_cost=evaluate_solution(best_solution, scores, deadline)
    while(Tmax > Tmin):
        neighbor=get_neighbors_sa(lib,best_solution,deadline)
        new_cost=evaluate_solution(neighbor, scores, deadline)
        dif=new_cost - best_cost
        if(dif > 0):
            best_cost = new_cost
            best_solution = neighbor
        elif(math.exp(dif/Tmax)>random.random()):
            best_cost = new_cost
            best_solution = neighbor
        Tmax=Tmax*0.98
    return best_solution,best_cost

# Selects a random configuration of libraries that can be signed up before the deadline.
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

# Generates neighboring solutions for Simulated Annealing algorithm.       
def get_neighbors_sa(todas_lib,lib_sol,deadline):
    rand=random.random()
    if(0.2>rand):
        random.shuffle(lib_sol)
    elif(0.6>rand):
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

''' LOCAL SEARCH '''    
# Perform Iterated Local Search algorithm to find the best solution for library scheduling. 
def iterated_local_search(libs, scores, dias_total, max_iterations=50,perturbation_levels=3):
    current_solution = initial_solution(libs, scores)
    best_solution = current_solution
    best_score = evaluate_solution(current_solution, scores, dias_total)
    
    for i in range(max_iterations):
        current_solution, current_score = tabu_search(libs, scores, dias_total,5,30)
        for level in range(1, perturbation_levels + 1):
            perturbed_solution = perturb_solution(current_solution, level)
            perturbed_solution, perturbed_score = tabu_search(libs, scores, dias_total, 5, 30)
            
            if perturbed_score > best_score:
                best_solution = perturbed_solution
                best_score = perturbed_score
    return best_solution, best_score

# Perturbs the solution based on the perturbation level.
def perturb_solution(solution,level):
    perturbed_solution = solution.copy()
    num_libs = len(solution)
    if num_libs >= 2:
        if level == 1:
            id1, id2 = random.sample(range(num_libs), 2)
            perturbed_solution[id1], perturbed_solution[id2] = perturbed_solution[id2], perturbed_solution[id1]
        elif level == 2:
            subset_size = num_libs//3
            indices_to_swap = random.sample(range(num_libs), subset_size)
            if len(indices_to_swap) % 2 == 0:  
                for i in range(0, len(indices_to_swap), 2):
                    id1, id2 = indices_to_swap[i], indices_to_swap[i + 1]
                    perturbed_solution[id1], perturbed_solution[id2] = perturbed_solution[id2], perturbed_solution[id1]
        elif level == 3:
            random.shuffle(perturbed_solution)
    return perturbed_solution

''' HILL CLIMBING '''      
# Perform Hill Climbing algorithm to find the best solution for library scheduling.       
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

''' GENETIC ALGORITHM '''
# Selection of Parents for Genetic Algorithm
def selection(population):
    g1 = random.sample(population, 3)
    parent1 = sorted(g1, key=lambda x: x[1], reverse=True)[0]

    rest = [x for x in population if x not in g1]
    g2 = random.sample(rest, 3)
    parent2 = sorted(g2, key=lambda x: x[1], reverse=True)[0]

    return parent1, parent2

# Performs Crossover Operation for Genetic Algorithm
def crossover(p1, p2, libraries):
    crossover_point = random.randint(1, len(p1) - 1)
    child = []

    child.extend(p1[:crossover_point])
    child.extend(p2[crossover_point:])

    child = list(set(child))

    while len(child) < len(libraries):
        lib = random.choice(libraries)
        if lib not in child:
            child.append(lib)

    return child

# Performs mutation Operation for Genetic Algorithm in the whole population
def mutate_population(population, libraries, scores, mutation_prob, population_variation, deadline):
    for solution in population:
        lib_list = None
        if random.random() < mutation_prob:
            lib_list = mutate_solution(solution[0], libraries, population_variation)
        if lib_list is not None:
            solution = (lib_list, evaluate_solution(lib_list, scores, deadline))

# Performs mutation Operation for Genetic Algorithm in a specific solution
def mutate_solution(solution, libraries, mutation_no):
    solution_indices = [libraries.index(lib) for lib in solution]
    
    uniques = set(solution_indices)
    if -1 in uniques:
        uniques.remove(-1)
    old_lib_indices = random.sample(list(uniques), ceil(mutation_no * len(uniques)))

    new_solution_indices = copy.deepcopy(solution_indices)
    
    for i in old_lib_indices:
        old_lib_index = solution_indices.index(i)

        day = old_lib_index

        first_part = new_solution_indices[:day]
        old_lib = libraries[i]
        second_part = list(filter(lambda a: a != -1, new_solution_indices[day + old_lib.tempo_signup:]))
        remaining_days = len(new_solution_indices) - (len(first_part) + len(second_part))

        new_lib = random.choice(libraries)
        checked = {new_lib}
        n = len(libraries)
        while (libraries.index(new_lib) in new_solution_indices or new_lib.tempo_signup > remaining_days) and len(checked) < n:
            new_lib = random.choice(libraries)
            checked.add(new_lib)

        new_solution_indices = first_part

        if libraries.index(new_lib) not in new_solution_indices and new_lib.tempo_signup <= remaining_days:
            for _ in range(new_lib.tempo_signup):
                new_solution_indices.append(libraries.index(new_lib))

        new_solution_indices.extend(second_part)

        while len(new_solution_indices) < len(solution_indices):
            new_solution_indices.append(-1)

    new_solution = [libraries[idx] for idx in new_solution_indices]

    return new_solution

# Perform Genetic algorithm to find the best solution for library scheduling.       
def genetic_algorithm(deadline, scores, libraries): 
    print("\n------------------------------------------\n")
    print("Please, insert the population size. (Recommended size is 10)\n")
    population_size = input("Population Size: ")

    print("\nPlease, insert the number of generations - iterations that the genetic_algorithm algorithm will run for. (Recommended value is 10)\n")
    num_generations = input("Number of generations: ")

    print("\nPlease, insert a mutation rate - probability of mutation for each gene. (Recommended value is 0.05)\n")
    mutation_prob = input("(From 0 to 1) Mutation rate: ")

    print("\nPlease, insert value for Population Variation. (Recommended value is 0.01)\n")
    population_variation = input("(From 0 to 1) Population Variation: ")

    print("\n------------------------------------------\n")

    if population_size.isdigit() and num_generations.isdigit() and mutation_prob.replace('.', '', 1).isdigit() and population_variation.replace('.', '', 1).isdigit():        
        population_size = int(population_size)
        num_generations = int(num_generations)
        mutation_prob = float(mutation_prob)
        population_variation = float(population_variation)

        initial_sol = initial_solution(libraries, scores)
        solution = (initial_sol, evaluate_solution(initial_sol, scores, deadline))

        population = [solution]

        for i in range(population_size - 1):  
            new_solution = mutate_solution(solution[0], libraries, population_variation)  
            solution_score = evaluate_solution(new_solution, scores, deadline)
            population.append((new_solution, solution_score))

        for generation in range(num_generations):
            new_population = []
            for p in range(len(population)):
                parent1, parent2 = selection(population)
                child = crossover(parent1[0], parent2[0], libraries)
                new_population.append((child, evaluate_solution(child, scores, deadline)))

            new_population.extend(population)
            mutate_population(new_population, libraries, scores, mutation_prob, population_variation, deadline)
            new_population = sorted(new_population, key=lambda x: x[1], reverse=True)[:len(population)]

            population = []
            for s in new_population:
                if s in population:  
                    best = sorted(new_population, key=lambda x: x[1], reverse=True)[0]  
                    new_solution = mutate_solution(best[0], libraries, 0.1)  
                    population.append((new_solution, evaluate_solution(new_solution, scores, deadline)))  
                else:  
                    population.append(s)

            best = max(population, key=lambda x: x[1])
            print("Score Attempt:", best[1])

        return max(population, key=lambda x: x[1]) 
    else:
            print("One or more values inserted are not valid. Please try again.")

''' MAIN AND MENUS '''
# Main entry point of the program: reads input from a file, processes the data, and performs an optimization algorithm based on the user's choice.
def main(fileop, op,iterations,tabuSize):
    # Reads the file name and opens the corresponding file
    filename = ler_opcao(fileop)
    file = open(filename, "r")

    # Retrieves important information for the file
    nlivros, nlib, deadline = map(int, file.readline().split())
    scores =list(map(int, file.readline().split()))
    
    # Organizes all libraries using the class above
    lib = list()
    for i in range(nlib):
        nl, ts, ld = list(map(int, file.readline().split()))
        idlivros =list( map(int, file.readline().split()))
        lib.append(Library(i,nl, ts, ld, idlivros))

    # Reads the user's input
    if op == 1:
        final_solution = tabu_search(lib, scores, deadline, tabuSize, iterations)
        create_file(final_solution, filename, scores, deadline, op)
        print("------------------------------------------\n")
        print("Solution Score:", final_solution[1])

    elif op == 2:
        Tmax=nlib*10
        Tmin=1
        final_solution = Sim_annealing(nlib,lib,scores,deadline,Tmax,Tmin)
        create_file(final_solution, filename, scores, deadline,op)
        print("------------------------------------------\n")
        print("Solution Score:", str(final_solution[1]))

    elif op == 3:
        final_solution = hill_climbing(lib, scores, deadline)
        create_file(final_solution, filename, scores, deadline, op)
        print("------------------------------------------\n")
        print("Solution Score:", final_solution[1])
        
    elif op == 4:
        final_solution = genetic_algorithm(deadline, scores, lib)
        create_file(final_solution, filename, scores, deadline, op)
        print("------------------------------------------\n")
        print("Solution Score:", final_solution[1])

    elif op == 5:
        final_solution = iterated_local_search(lib, scores, deadline)
        create_file(final_solution, filename, scores, deadline, op)
        print("------------------------------------------\n")
        print("Solution Score:", str(final_solution[1]))

    # Closes the file
    file.close()

    # Go back to the main menu or exit program
    print('\n******************************************\n')
    print('[B] - Go back to main menu\n')
    print('[E] - Exit program\n')             
    while True:
        op = input("Option: ")
        if op.lower() == 'e':
            verify_exit()
        elif op.lower() == 'b':
            menu()
            break
        else:
            print("Invalid option. Please choose a valid one.")

# Displays a menu for configuring parameters for the tabu search algorithm.
def tabu_search_menu(fileop):
    while True:
        print("\nPlease, insert the number of iterations for the tabu search. (Recommended value is 100)\n")
        op = input("Number of iterations: ")

        print("\nPlease, insert the tabu size. (Recommended value is 20)\n")
        op2 = input("Tabu Size: ")

        if op.isdigit() & op2.isdigit():
            main(int(fileop), 1,int(op),int(op2))
            break
        else:
            print("One or more values inserted are not valid. Please try again.")

# Displays a menu for selecting the optimization algorithm to find the total score of the solution.
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
        
        op = input("Option: ")
        
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
            main(int(fileop),int(op),0,0)
            break
        if op.isdigit() and 5 == int(op):
            main(int(fileop),int(op),0,0)
            break
        elif op.lower() == 'e':
            verify_exit()
        elif op.lower() == 'b':
            menu()
            break
        else:
            print("Invalid option. Please choose a valid option (1-7).")

# This function displays the main menu, prompting the user to select a file.
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
