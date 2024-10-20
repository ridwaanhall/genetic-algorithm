import random
import numpy as np

# Student class to represent each student's intelligence (C) and dexterity (T) values
class Student:
    def __init__(self, name, C, T):
        self.name = name
        self.C = C  # Intelligence value
        self.T = T  # Dexterity value

# Team class to calculate the total strength based on the members' intelligence or dexterity
class Team:
    def __init__(self, members):
        self.members = members  # List of Student objects

    def calculate_strength(self, is_intelligence=True):
        # Calculate the strength as the product of C values (intelligence) or T values (dexterity)
        strength = 1
        for member in self.members:
            strength *= member.C if is_intelligence else member.T
        return strength

# Genetic Algorithm class to solve the optimization problem
class GeneticAlgorithm:
    def __init__(self, students, population_size=100, generations=1000, mutation_rate=0.1):
        self.students = students  # List of Student objects
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()

    def initialize_population(self):
        # Randomly create initial population of team compositions
        population = []
        for _ in range(self.population_size):
            # Randomly select 6 students: 3 for the intelligence team and 3 for the dexterity team
            individuals = random.sample(self.students, 6)
            intelligence_team = Team(individuals[:3])
            dexterity_team = Team(individuals[3:])
            population.append((intelligence_team, dexterity_team))
        return population

    def fitness_function(self, intelligence_team, dexterity_team):
        # Fitness is the sum of intelligence team strength and dexterity team strength
        intelligence_strength = intelligence_team.calculate_strength(is_intelligence=True)
        dexterity_strength = dexterity_team.calculate_strength(is_intelligence=False)
        return intelligence_strength + dexterity_strength

    def selection(self):
        # Select top individuals based on fitness score using roulette wheel selection
        fitness_scores = [self.fitness_function(int_team, dex_team) for int_team, dex_team in self.population]
        total_fitness = sum(fitness_scores)
        probabilities = [fitness / total_fitness for fitness in fitness_scores]
        selected_indices = np.random.choice(range(self.population_size), size=self.population_size, p=probabilities)
        return [self.population[i] for i in selected_indices]

    def crossover(self, parent1, parent2):
        # Single-point crossover between two parents
        intelligence_team1, dexterity_team1 = parent1
        intelligence_team2, dexterity_team2 = parent2
        crossover_point = random.randint(1, 2)
        child1_intelligence = intelligence_team1.members[:crossover_point] + intelligence_team2.members[crossover_point:]
        child2_intelligence = intelligence_team2.members[:crossover_point] + intelligence_team1.members[crossover_point:]
        child1_dexterity = dexterity_team1.members[:crossover_point] + dexterity_team2.members[crossover_point:]
        child2_dexterity = dexterity_team2.members[:crossover_point] + dexterity_team1.members[crossover_point:]
        return (Team(child1_intelligence), Team(child1_dexterity)), (Team(child2_intelligence), Team(child2_dexterity))

    def mutate(self, individual):
        # Randomly mutate by swapping one member in the team with another random student
        intelligence_team, dexterity_team = individual
        if random.random() < self.mutation_rate:
            all_students = intelligence_team.members + dexterity_team.members
            new_student = random.choice([s for s in self.students if s not in all_students])
            mutate_team = random.choice([intelligence_team, dexterity_team])
            mutate_team.members[random.randint(0, 2)] = new_student
        return individual

    def run(self):
        # Main loop to evolve the population over generations
        for generation in range(self.generations):
            new_population = []
            selected_population = self.selection()

            # Crossover and mutation
            for i in range(0, self.population_size, 2):
                parent1 = selected_population[i]
                parent2 = selected_population[(i+1) % self.population_size]
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(child1))
                new_population.append(self.mutate(child2))

            self.population = new_population

            # Find the best individual in the current generation
            best_individual = max(self.population, key=lambda ind: self.fitness_function(ind[0], ind[1]))
            best_fitness = self.fitness_function(best_individual[0], best_individual[1])

            print(f"Generation {generation+1}, Best Fitness: {best_fitness}")

        # Return the best individual found
        best_individual = max(self.population, key=lambda ind: self.fitness_function(ind[0], ind[1]))
        return best_individual

# Define students (from the provided data)
students = [
    ("Arya", 11, 60),
    ("Alana", 70, 32),
    ("Zayn", 101, 101),
    ("Kaelan", 99, 103),
    ("Ziva", 103, 10),
    ("Mikael", 16, 100),
    ("Nayla", 20, 64),
    ("Freya", 54, 85),
    ("Naufal", 100, 3),
    ("Damar", 40, 23),
    ("Kiara", 74, 19),
]

# Initialize and run the genetic algorithm
ga = GeneticAlgorithm(students, population_size=50, generations=10, mutation_rate=0.1)
best_intelligence_team, best_dexterity_team = ga.run()

# Output the best solution found
print("Best Intelligence Team:", [student.name for student in best_intelligence_team.members])
print("Best Dexterity Team:", [student.name for student in best_dexterity_team.members])
