import random
from typing import List, Tuple

class Mahasiswa:
    def __init__(self, nama: str, nilai_cerdas: int, nilai_tangkas: int):
        self.nama = nama
        self.nilai_cerdas = nilai_cerdas
        self.nilai_tangkas = nilai_tangkas

class GeneticAlgorithm:
    def __init__(self, mahasiswa: List[Mahasiswa], population_size: int, generations: int, mutation_rate: float):
        self.mahasiswa = mahasiswa
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()

    def fitness_function(self, chromosome: List[int]) -> int:
        if len(set(chromosome)) != len(chromosome):
            return 0
        
        a, b, c = chromosome[:3]
        x, y, z = chromosome[3:]
        
        team_cerdas = self.mahasiswa[a].nilai_cerdas * self.mahasiswa[b].nilai_cerdas * self.mahasiswa[c].nilai_cerdas
        team_tangkas = self.mahasiswa[x].nilai_tangkas * self.mahasiswa[y].nilai_tangkas * self.mahasiswa[z].nilai_tangkas
        
        return team_cerdas + team_tangkas

    def initialize_population(self) -> List[List[int]]:
        population = []
        for _ in range(self.population_size):
            chromosome = random.sample(range(len(self.mahasiswa)), 6)
            population.append(chromosome)
        return population

    def roulette_wheel_selection(self, fitness_values: List[int]) -> List[int]:
        total_fitness = sum(fitness_values)
        pick = random.uniform(0, total_fitness)
        current = 0
        for i, fitness in enumerate(fitness_values):
            current += fitness
            if current > pick:
                return self.population[i]

    def one_point_crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        crossover_point = random.randint(1, 5)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        
        if len(set(child1)) == len(child1) and len(set(child2)) == len(child2):
            return child1, child2
        else:
            return parent1, parent2

    def swap_mutation(self, chromosome: List[int]) -> List[int]:
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(6), 2)
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        return chromosome

    def run(self) -> Tuple[List[int], int]:
        for generation in range(self.generations):
            fitness_values = [self.fitness_function(ind) for ind in self.population]
            
            best_fitness = max(fitness_values)
            best_individual = self.population[fitness_values.index(best_fitness)]
            print(f"Generasi {generation}: Fitness Terbaik = {best_fitness}")
            
            new_population = []
            for _ in range(self.population_size // 2):
                parent1 = self.roulette_wheel_selection(fitness_values)
                parent2 = self.roulette_wheel_selection(fitness_values)
                
                child1, child2 = self.one_point_crossover(parent1, parent2)
                
                child1 = self.swap_mutation(child1)
                child2 = self.swap_mutation(child2)
                
                new_population.extend([child1, child2])
            
            self.population = new_population
        
        fitness_values = [self.fitness_function(ind) for ind in self.population]
        best_fitness = max(fitness_values)
        best_individual = self.population[fitness_values.index(best_fitness)]
        
        return best_individual, best_fitness

# Data mahasiswa
mahasiswa = [
    Mahasiswa("Arya", 11, 60),
    Mahasiswa("Alana", 70, 32),
    Mahasiswa("Zayn", 101, 101),
    Mahasiswa("Kaelan", 99, 103),
    Mahasiswa("Ziva", 103, 10),
    Mahasiswa("Mikael", 16, 100),
    Mahasiswa("Nayla", 20, 64),
    Mahasiswa("Freya", 54, 85),
    Mahasiswa("Naufal", 100, 3),
    Mahasiswa("Damar", 40, 23),
    Mahasiswa("Kiara", 74, 19),
]

# Inisialisasi parameter GA
POPULATION_SIZE = 100
GENERATIONS = 20
MUTATION_RATE = 0.1

# Jalankan algoritma GA
ga = GeneticAlgorithm(mahasiswa, POPULATION_SIZE, GENERATIONS, MUTATION_RATE)
best_individual, best_fitness = ga.run()

# Tampilkan hasil
tim_cerdas = best_individual[:3]
tim_tangkas = best_individual[3:]
print(f"Tim Kecerdasan: {', '.join(mahasiswa[i].nama for i in tim_cerdas)}")
print(f"Tim Ketangkasan: {', '.join(mahasiswa[i].nama for i in tim_tangkas)}")
print(f"Fitness Terbaik: {best_fitness}")
