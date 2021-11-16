# Created by HashTable159

import numpy as np
import time

from objective import ObjFunc

class GA:
    def __init__(
        self,
        parameters_num = None,
        bits = 8,
        population_num = 400, 
        generation = 1600, 
        crossover_prob = 0.9, 
        mutation_prob = 0.03, 
        k = 3,
        lower_bounds = [],
        upper_bounds = [],
    ):

        self.bits = bits
        self.chromosome_length = bits*parameters_num
        self.population_num = population_num
        self.generation = generation
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.k = int(k)
        self.obj_func = ObjFunc()
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds

    def getPopulation(self):
        population = np.empty((0, self.chromosome_length))
        for _ in range(self.population_num):
            #constraints
            while True:
                rand_chromosome = np.random.randint(2, size=(self.chromosome_length))

                # Parameter lists from result
                rand_param = self.obj_func.result(self.decode(rand_chromosome)[0])
                
                print("Constraints Begin!!!")
                print(rand_param)

                if(
                    # Enter constraints here!!!
                    # If no constrains set as True
                    True
                ):
                    break

            population = np.vstack([population, rand_chromosome])
        return population

    def decimal(self, binary):
        decimal_result = 0

        for index, bit in enumerate(binary):
            decimal_result += bit*2**(len(binary)-index-1)

        return decimal_result

    def objtive_function(self, parameters):
        return round(self.obj_func.function(parameters), 6)

    def decode(self, binary):

        decode = []
        for i in range(len(self.lower_bounds)):
            decode.append(round(self.lower_bounds[i] + self.decimal(binary[self.bits*i:self.bits*(i+1)])*((self.upper_bounds[i] - self.lower_bounds[i])/(2**self.bits - 1)), 6))

        return decode, self.objtive_function(decode)

    def binary_swap(self, bit):
        if bit == 0:
            return 1
        else:
            return 0

    def select_parents(self, population):
        winner_parents = np.empty((2, self.chromosome_length))
        
        for i in range(2):
            selected_parents = np.empty((self.k, self.chromosome_length))

            for j in range(self.k):
                rand_num = np.random.randint(len(population))
                selected_parents[j] = population[rand_num]
            
            obj_value = np.empty((self.k, 1))
            for index, element in enumerate(selected_parents):
                obj_value[index] = self.decode(element)[1]

            winner_parents[i] = selected_parents[np.argmin(obj_value)]

        return winner_parents

    def crossover(self, parents):
        rand_crossover_prob = np.random.rand()

        if rand_crossover_prob < self.crossover_prob:
            section_1 = np.random.randint(self.chromosome_length)
            while section_1 == self.chromosome_length-1:
                section_1 = np.random.randint(self.chromosome_length)

            section_2 = np.random.randint(self.chromosome_length)
            while section_2 <= section_1:
                section_2 = np.random.randint(self.chromosome_length)

            for index, _ in enumerate(parents[0]):
                if section_1 <= index <= section_2:
                    parents[0][index], parents[1][index] = parents[1][index], parents[0][index]

            return parents

        return parents

    def mutation(self, childs):
        for index, _ in enumerate(childs[0]):
            rand_mutation_prob = np.random.rand()

            if rand_mutation_prob < self.mutation_prob:
                childs[0][index] = self.binary_swap(childs[0][index])

        for index, _ in enumerate(childs[1]):
            rand_mutation_prob = np.random.rand()

            if rand_mutation_prob < self.mutation_prob:
                childs[1][index] = self.binary_swap(childs[1][index])    
        
        return childs
    
    def run(self):
        count = 0
        pool_of_generation = self.getPopulation()
        best_of_generation = np.empty((0, 2))
        best_of_all_stack = np.empty((0, 2))
        best_of_all = np.empty((0, 2))
        start_time = time.time()
        stack_plot = []

        print("First generation")
        for index, element in enumerate(pool_of_generation):
            print(f"LINE\t{index+1}\tf={self.decode(element)[1]}")

        for gen in range(self.generation):
            new_population = np.empty((0, self.chromosome_length))

            for _ in range(int(self.population_num/2)):
                #constraints
                while True:
                    parents = self.select_parents(pool_of_generation)
                    childs = self.crossover(parents)
                    mutated_childs = self.mutation(childs)

                    # Parameter lists from result
                    # You must change decode_1 and decode_2 as the same constraints
                    decode_1 = self.obj_func.result(self.decode(mutated_childs[0])[0])
                    decode_2 = self.obj_func.result(self.decode(mutated_childs[1])[0])
                    
                    if(
                        # Enter constraints here!!!
                        # If no constrains set as True
                        True
                    ):
                        break

                new_population = np.vstack([new_population, mutated_childs])
            
            pool_of_generation = new_population
            count = gen+1

            print()
            print(f"Generation #{gen+1}")
            for index, element in enumerate(new_population):
                print(f"LINE\t{index+1}\tf={self.decode(element)[1]}")
                best_of_all_stack = np.vstack([best_of_all_stack, self.decode(element)])

            best_of_generation_stack = np.empty((0, 1))
            for index, element in enumerate(new_population):
                best_of_generation_stack = np.vstack([best_of_generation_stack, self.decode(element)[1]])
            
            best_of_generation = self.decode(new_population[np.argmin(best_of_generation_stack)])
            stack_plot.append(best_of_generation[1])

        best_of_all_find = np.empty((0, 1))
        for item in best_of_all_stack:
            best_of_all_find = np.vstack([best_of_all_find, item[1]])
        best_of_all = best_of_all_stack[np.argmin(best_of_all_find)]

        end_time = time.time()
        execution_time = end_time - start_time

        result_generation = self.obj_func.result(best_of_generation[0])
        result_all = self.obj_func.result(best_of_all[0])

        print()
        print(f"Execution_time:\t{round(execution_time, 2)} sec, @Generation: {count}")
        print(f"BEST_OF:\t\tPARAMETERS:\t\t\tOBJ_VALUE:")
        print(f"Generation\t\t{best_of_generation[0]}\t\t{best_of_generation[1]}")
        print(f"All_time\t\t{best_of_all[0]}\t\t{best_of_all[1]}")
        print()
        print(f"Generation\t\t{best_of_generation[0]}: {result_generation}")
        print()
        print(f"All_time\t\t{best_of_all[0]}: {result_all}")

        return best_of_generation[0], result_generation, best_of_all[0], result_all