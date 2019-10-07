import random
import operator
import math

from Models import MinSetGenerator, MinSetChecker


def get_unique(lst):
    """
    Get generator with unique values
    :param lst: list
    :return: generator
    """
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item


def get_list_with_unique_values(gen):
    """
    Get list with unique values
    :param gen: generator
    :return: list
    """
    return list(get_unique(sorted(gen, reverse=True)))


class GeneticAlgorithmBanknotes:
    """
    Genetic algorithm that finds a set with a minimal number of banknotes
    that the probability that 2 person have the same set of banknotes
    (same set of banknotes for two different random amounts of money uniformly distributed
    in the 'money_range') is exactly 'target'
    Attributes:
        params: parameters of model
            0: number of genes
            1: size of population
            2: number of elitism
            3: number of 'best sample'
            4: number of 'lucky few'
            5: number of child
            6: chance of mutation
            7: min value of each gene
            8: max value of each gene
        money_range: range of money
            0: min value of money
            1: max value of money
        target: target probability
    """

    def __init__(self, params, money_range, target):
        self.number_of_genes = params[0]
        self.size_population = params[1]
        self.number_elitism = params[2]
        self.best_sample = params[3]
        self.lucky_few = params[4]
        self.number_of_child = params[5]
        self.chance_of_mutation = params[6]
        self.gene_value_min = params[7]
        self.gene_value_max = params[8]
        self.money_min = money_range[0]
        self.money_max = money_range[1]
        self.target = target
        self.is_found = False  # True if solution is found
        self.eps = math.pow(10, -5)  # precision

    def fitness(self, individual):
        """
        Fitness function that returns 'abs(target - current_probability)'
        If fitness value is equal to 0, its individual is a solution
        :param individual: individual of population
        :return: fitness value of individual
        """
        result_all = []  # all possible sets with a minimal number of banknotes
        for i in range(self.money_min, self.money_max + 1):
            q, s = MinSetGenerator(self.number_of_genes, individual, i).generate()
            # if exists another set with a minimal number of banknotes - return bad fitness value (100)
            if MinSetChecker(self.number_of_genes, individual, i, q).is_exist_another_solution():
                return 100.0
            else:
                result_all.append(s)
        result_unique = get_list_with_unique_values(result_all)  # unique sets with a minimal number of banknotes
        probability = 0.0
        result_all_count = len(result_all)
        for item in result_unique:
            buff = result_all.count(item)
            up = buff * (buff - 1)
            down = result_all_count * (result_all_count - 1)
            probability += up / down
        probability = probability * 100
        return abs(self.target - probability)

    def generate_individual(self):
        """
        Generate individual of population with random genes
        :return: individual of population
        """
        # Gene with value 1 must exist in each individual of population
        individual = [1]
        # values of genes cannot be repeated
        individual.extend(random.sample(range(self.gene_value_min, self.gene_value_max), self.number_of_genes - 1))
        return individual

    def generate_first_population(self):
        """
        Generate population (set of individual)
        :return: population
        """
        population = []
        for i in range(0, self.size_population):
            population.append(self.generate_individual())
        return population

    def compute_population(self, population):
        """
        Sort individuals in population in ascending order due its fitness values
        :param population: population
        :return: sorted population
        """
        population_computed = {}
        values_computed = {}
        for i in range(0, self.size_population):
            population_computed[i] = population[i]
            values_computed[i] = self.fitness(population[i])
        values_sorted = sorted(values_computed.items(), key=operator.itemgetter(1))
        values_out = [v[1] for v in values_sorted]
        population_out = [population[v[0]] for v in values_sorted]
        return population_out, values_out

    def select_from_population(self, population_sorted):
        """
        Selector
        :param population_sorted: population
        :return: set of individuals of population
        """
        generation_next = []
        for i in range(self.best_sample):
            generation_next.append(population_sorted[i])
        for i in range(self.lucky_few):
            generation_next.append(random.choice(population_sorted))
        random.shuffle(generation_next)
        return generation_next

    def create_child(self, individual1, individual2):
        """
        Create child from parents
        :param individual1: first parent
        :param individual2: second parent
        :return: child (individual)
        """
        individual = [1]
        for i in range(1, self.number_of_genes):
            if int(100 * random.random()) < 50:
                individual.append(individual1[i])
            else:
                individual.append(individual2[i])
        return individual

    def create_children(self, breeders):
        """
        Crossover
        :param breeders: set of parents
        :return: population with their children
        """
        population_next = []
        for i in range(int(len(breeders) / 2)):
            for j in range(self.number_of_child):
                population_next.append(self.create_child(breeders[i], breeders[len(breeders) - 1 - i]))
        return population_next

    def mutate_individual(self, individual):
        """
        Mutate genes of individual
        :param individual: individual
        :return: mutated individual
        """
        s = {0, 1}  # genes don't have gene 0 (meaningless) or 1 (this value the first gene has)
        # Mutate all genes except the first (because it must have value 1)
        for i in range(1, self.number_of_genes):
            if random.random() * 100 < self.chance_of_mutation:
                value = self.gene_value_min + int((self.gene_value_max - self.gene_value_min) * random.random())
                # values of genes cannot be repeated
                while value in s:
                    value = self.gene_value_min + int((self.gene_value_max - self.gene_value_min) * random.random())
                individual[i] = value
                s.add(value)
            else:
                s.add(individual[i])
        return individual

    def mutate_population(self, population):
        """
        Mutate population
        :param population: population
        :return: mutated population
        """
        for i in range(len(population)):
            if random.random() * 100 < self.chance_of_mutation:
                population[i] = self.mutate_individual(population[i])
        return population

    def generate_population(self, generation_last):
        """
        Evolve population
        :param generation_last: last population
        :return: next population
        """
        population_sorted, values_sorted = self.compute_population(generation_last)
        # print sorted population and its fitness values
        print([population_sorted[i] for i in range(0, self.size_population)])
        print([values_sorted[i] for i in range(0, self.size_population)])
        # Stop when a solution is found
        if values_sorted[0] < self.eps:
            self.is_found = True
            print('Solution is found: ' + population_sorted[0])
            return [population_sorted[i] for i in range(0, self.size_population)]
        breeders_next = self.select_from_population(population_sorted)
        population_next = self.create_children(breeders_next)
        generation_next = self.mutate_population(population_next)
        # Elitism - the best individual in each population must survive
        generation_next.append(population_sorted[0])
        return generation_next

    def check(self):
        """
        Check parameters of genetic algorithm
        :return: True if OK, False if not
        """
        is_verify = True
        if self.size_population != \
                self.number_elitism + ((self.best_sample + self.lucky_few) / 2) * self.number_of_child:
            print("Check GA parameters: 'size_population' must be equal "
                  "'number_elitism + (('best_sample + lucky_few')) / 2) * number_of_child'")
            is_verify = False
        elif self.number_elitism >= self.size_population:
            print("Check GA parameters: 'number_elitism' must be less 'size_population'")
            is_verify = False
        elif self.chance_of_mutation > 100:
            print("Check GA parameters: 'chance_of_mutation' must be less or equal '100'")
            is_verify = False
        return is_verify

    def run(self):
        """
        Run calculation
        """
        if self.check():
            historic = [self.generate_first_population()]
            i = 0
            while not self.is_found:
                print('Generation: ' + str(i+1))
                historic.append(self.generate_population(historic[i]))
                i += 1


if __name__ == '__main__':
    GeneticAlgorithmBanknotes([5, 21, 1, 4, 4, 5, 60, 2, 99], [0, 99], 4.0).run()
