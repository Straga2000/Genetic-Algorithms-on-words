from random import randint

class Letter:

    def __init__(self, length):

        self.frequency = []
        self.length = length

        for i in range(length):
            self.frequency.append(0)

        self.frequency_max = 0

    def update(self, val, pos):
        self.frequency[pos] += val

    def frequency_update(self):
        val = 0
        pos = 0
        for i in range(self.length):
            if self.frequency[i] > val:
                val = self.frequency[i]
                pos = i

        self.frequency_max = pos



class GrammarChecker:

    def __init__(self):

        self.was_filled = False

        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                         'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                         'u', 'v', 'w', 'x', 'y', 'z', ' ']

        self.alphabet_size = len(self.alphabet)

        self.alpha_dict = {}

        for i in range(self.alphabet_size):

            self.alpha_dict[self.alphabet[i]] = Letter(self.alphabet_size)

    def choose_letter(self, letter):

        return self.alphabet[self.alpha_dict[letter].frequency_max]

    def update_dictionary(self):
        for elem in self.alpha_dict:
            self.alpha_dict[elem].frequency_update()


class Evolution(GrammarChecker):
    def __init__(self, specimen):

        GrammarChecker.__init__(self)

        self.mutation_value = randint(0, 100)

        self.found = None

        self.specimen = list(specimen)
        self.population = []

        self.length = len(specimen)
        self.number_of_generations = 0

    def create_new_population(self):

        for i in range(self.length):
            word = self.create_random_individual(i)
            self.population.append(word)

    def create_random_individual(self, pos):

        word = []

        for i in range(self.length):
            letter = self.alphabet[(pos + i) % self.alphabet_size]
            word.append(letter)

        return word

    def create_new_individual(self, parent0, parent1, cnt):

        word = []

        for i in range(self.length):
            if (i * cnt) % 2:
                word.append(parent1[i])
            else:
                word.append(parent0[i])

        mutation = randint(0, 3)

        if mutation == 0:
            pos = randint(0, self.length - 1)

            if not self.was_filled:
                word[pos] = self.alphabet[self.get_mutation_value()]
            else:
                replacer = self.choose_letter(word[pos])
                self.alpha_dict[word[pos]].update(1, replacer)

        return word

    def get_mutation_value(self):
        self.mutation_value = (self.mutation_value + 1) % self.alphabet_size
        return self.mutation_value

    def compare_strings(self, src):

        score = 0

        for i in range(self.length):
            if src[i] == self.specimen[i]:
                score += 1

        return score

    def find_fittest_individuals(self):

        maxim_scores = (0, 0)
        maxim_position = (0, 0)

        for i in range(self.length):

            score = self.compare_strings(self.population[i])

            if score == self.length:
                self.found = self.population[i]

            elif i == 0:
                maxim_scores = (0, 0)

            elif score > maxim_scores[0]:
                maxim_scores = (score, maxim_scores[0])
                maxim_position = (i, maxim_position[0])

            elif maxim_scores[1] < score < maxim_scores[0]:
                maxim_scores = (maxim_scores[0], score)

        self.number_of_generations += 1

        return maxim_position

    def grow_population(self):

        pos = self.find_fittest_individuals()

        if self.found is None:
            parent0 = self.population[pos[0]]
            parent1 = self.population[pos[1]]

            print(parent0, parent1)

            self.population[0] = parent0
            self.population[1] = parent1

            for i in range(2, self.length):
                self.population[i] = self.create_new_individual(parent0, parent1, i)

evolve = Evolution("salutare tuturor si bine ati venit la emisiunea mea faimoasa astazi va voi prezenta cum se face o placinta de casa")
evolve.create_new_population()
while evolve.found is None:
    evolve.grow_population()

print(evolve.found, evolve.number_of_generations)