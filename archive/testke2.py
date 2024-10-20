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
        child2 = parent2[:crossover_point] + parent1[:crossover_point:]
        
        # Ensure no duplicates in children
        if len(set(child1)) != len(child1) or len(child1) != 6:
            child1 = parent1
        if len(set(child2)) != len(child2) or len(child2) != 6:
            child2 = parent2
        
        return child1, child2

    def swap_mutation(self, chromosome: List[int]) -> List[int]:
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(6), 2)
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        return chromosome

    def run(self) -> Tuple[List[int], int]:
        best_fitness = -1
        best_individual = None

        for generation in range(self.generations):
            fitness_values = [self.fitness_function(ind) for ind in self.population]
            
            current_best_fitness = max(fitness_values)
            current_best_individual = self.population[fitness_values.index(current_best_fitness)]
            
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best_individual
            
            print(f"Generasi {generation}: Fitness Terbaik = {current_best_fitness}")
            
            new_population = []
            for _ in range(self.population_size // 2):
                parent1 = self.roulette_wheel_selection(fitness_values)
                parent2 = self.roulette_wheel_selection(fitness_values)
                
                child1, child2 = self.one_point_crossover(parent1, parent2)
                
                child1 = self.swap_mutation(child1)
                child2 = self.swap_mutation(child2)
                
                new_population.extend([child1, child2])
            
            self.population = new_population
        
        return best_individual, best_fitness

class GeneticAlgorithmExplanation:
    def __init__(self, ga: GeneticAlgorithm):
        self.ga = ga

    def explain_gen_design(self):
        return "Gen terdiri dari 6 angka yang masing-masing merepresentasikan indeks mahasiswa dalam daftar mahasiswa. " \
               "Tiga angka pertama adalah tim cerdas, dan tiga angka terakhir adalah tim tangkas."

    def explain_fitness_calculation(self, chromosome: List[int]):
        fitness = self.ga.fitness_function(chromosome)
        return f"Fitness dihitung dengan mengalikan nilai cerdas dari tiga mahasiswa pertama dan nilai tangkas dari tiga mahasiswa terakhir. " \
               f"Contoh perhitungan untuk kromosom {chromosome}: Fitness = {fitness}"

    def explain_selection_technique(self):
        example_fitness_values = [self.ga.fitness_function(ind) for ind in self.ga.population]
        selected_individual = self.ga.roulette_wheel_selection(example_fitness_values)
        return "Teknik seleksi yang digunakan adalah roulette wheel selection. " \
            "Setiap individu dipilih berdasarkan probabilitas yang sebanding dengan nilai fitnessnya. " \
            f"Contoh hasil seleksi: individu dengan kromosom {selected_individual} dipilih dari populasi."

    def explain_crossover_technique(self, parent1: List[int], parent2: List[int]):
        child1, child2 = self.ga.one_point_crossover(parent1, parent2)
        return f"Teknik crossover yang digunakan adalah one-point crossover. " \
               f"Contoh hasil crossover untuk parent1 {parent1} dan parent2 {parent2}: child1 = {child1}, child2 = {child2}"

    def explain_mutation_technique(self, chromosome: List[int]):
        mutated_chromosome = self.ga.swap_mutation(chromosome)
        return f"Teknik mutasi yang digunakan adalah swap mutation. " \
               f"Contoh hasil mutasi untuk kromosom {chromosome}: mutated_chromosome = {mutated_chromosome}"

    def explain_best_individual(self, best_individual: List[int], generation: int):
        tim_cerdas = best_individual[:3]
        tim_tangkas = best_individual[3:]
        return f"Kromosom terbaik adalah {best_individual} yang ditemukan pada generasi ke-{generation}. " \
               f"Tim Kecerdasan: {', '.join(self.ga.mahasiswa[i].nama for i in tim_cerdas)}, " \
               f"Tim Ketangkasan: {', '.join(self.ga.mahasiswa[i].nama for i in tim_tangkas)}"

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
GENERATIONS = 10
MUTATION_RATE = 0.1

# Jalankan algoritma GA
ga = GeneticAlgorithm(mahasiswa, POPULATION_SIZE, GENERATIONS, MUTATION_RATE)
best_individual, best_fitness = ga.run()

# Inisialisasi kelas penjelasan
ga_explanation = GeneticAlgorithmExplanation(ga)

# Tampilkan hasil
tim_cerdas = best_individual[:3]
tim_tangkas = best_individual[3:]
print(f"Tim Kecerdasan: {', '.join(mahasiswa[i].nama for i in tim_cerdas)}")
print(f"Tim Ketangkasan: {', '.join(mahasiswa[i].nama for i in tim_tangkas)}")
print(f"Fitness Terbaik: {best_fitness}")

# Jawab pertanyaan
print("\nJawaban Pertanyaan:")
print("1. Jelaskan rancangan gen yang Anda buat beserta maknanya.")
print(ga_explanation.explain_gen_design())

print("\n2. Jelaskan perhitungan fitness yang anda gunakan – potongan kode programnya – dan contoh hasil perhitungan fitness untuk satu kromosom/individu.")
example_chromosome = ga.population[0]
print(ga_explanation.explain_fitness_calculation(example_chromosome))

print("\n3. Jelaskan teknik seleksi yang anda gunakan – potongan kode programnya – dan contoh hasil seleksinya.")
print(ga_explanation.explain_selection_technique())

print("\n4. Jelaskan teknik crossover yang anda gunakan – potongan kode programnya – dan contoh hasil crossovernya.")
parent1 = ga.population[0]
parent2 = ga.population[1]
print(ga_explanation.explain_crossover_technique(parent1, parent2))

print("\n5. Jelaskan teknik mutasi yang anda gunakan – potongan kode programnya – dan contoh hasil mutasinya.")
print(ga_explanation.explain_mutation_technique(example_chromosome))

print("\n6. Jelaskan kromosom/individu terbaik yang Anda dapatkan sebagai solusi permasalahan dan sebutkan solusi tersebut anda dapatkan pada generasi ke berapa.")
print(ga_explanation.explain_best_individual(best_individual, GENERATIONS))