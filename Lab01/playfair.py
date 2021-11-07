import copy
import numpy as np

# funkcja pomocnicza, która zamienia nam string na listę znaków spełniających zasady
# tworzenia klucza - unikalne, J zostaje zamienione na I, kolejność zostaje zachowana
def process_key(string):
    unique = []
    # iterujemy po znakach w stringu
    for char in string:
        # jeśli znak to 'J' zamień je na 'I'
        if char == 'J':
            char = 'I'
        # jeśli znak jeszcze nie wystąpił oraz jest literą
        if (char not in unique) and (char.isalpha()):
            # dodaj go do listy unikalnych znaków
            unique.append(char)

    # zwróć klucz
    return unique

# funkcja pomocniczna przetwarzająca string na pary liter
# przygotowane do szyfrowania/deszyfrowania
def process_text(string):
    # zmienna przechowująca wszystkie pary
    all_pairs = []
    # aktualnie budowana para
    curr_pair = []
    # iterujemy po znakach w stringu
    for char in string:
        # pozbywamy się litery 'J', zamieniamy ją na 'I'
        if char == 'J':
            char = 'I'
        # jeśli znak jest literą
        if char.isalpha():
            # jeśli w aktualnie budowanej parze jest jedna litera
            if len(curr_pair) == 1:
                # sprawdzamy, czy litera się powtarza (taka para jest nieszyfrowalna)
                if char == curr_pair[0]:
                    # jeżeli tak, to dopisujemy 'X' do pary
                    curr_pair.append('X')
                    # dodajemy ją do listy gotowych par
                    all_pairs.append(copy.copy(curr_pair))
                    # a naszą aktualną literę umieszczamy w nowej parze
                    curr_pair = []
                    curr_pair.append(char)
                    # i przechodzimy do następnej litery
                    continue
            # dopisujemy naszą literę do aktualnie budowanej pary
            curr_pair.append(char)
            # jeśli nasza para ma długość 2 (jest pełna)
            if len(curr_pair) == 2:
                # dodajemy ją do listy gotowych par
                all_pairs.append(copy.copy(curr_pair))
                # opróżniamy roboczą parę
                curr_pair = []

    # kiedy już sprawdzimy wszystkie litery, sprawdzamy czy była ich parzysta ilość
    # (przez sprawdzenie czy nie została nam niedokończona para)
    if len(curr_pair) == 1:
        # jeżeli tak, to dodajemy do niej 'X'
        curr_pair.append('X')
        # a następnie dodajemy ją do listy gotowych par
        all_pairs.append(copy.copy(curr_pair))
        
    # zwracamy listę gotowych par
    return all_pairs

# funkcja pomocnicza do tworzenia siatki szyfrowania na podstawie klucza
def create_grid(key):
    # alfabet bez litery J
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    # tworzymy roboczą kopię tablicy klucza
    used = copy.deepcopy(key)
    # tworzymy pustą tablicę o 5 rzędach
    grid = [ [], [], [], [], [] ]
    # licznik aktualnej pozycji w kluczu
    key_ctr = 0
    # licznik aktualnej pozycji w alfabecie
    alph_ctr = 0

    # licznik rzędów
    for row in range(5):
        # licznik kolumn
        for _ in range(5):
            # jeżeli jeszcze nie wpisaliśmy wszystkich liter z klucza
            if key_ctr < len(key):
                # dopisujemy do aktualnego rzędu aktualną literę z klucza
                grid[row].append(used[key_ctr])
                # inkrementujemy licznik klucza
                key_ctr += 1
            else:
                # jeżeli wszystkie litery z klucza są już wpisane
                # przesuwamy licznik alfabetu aż trafimy na literę
                # jeszcze nie dodaną do siatki
                while alphabet[alph_ctr] in used:
                    alph_ctr += 1
                # dopisujemy literę alfabetu do siatki i listy zużytych liter
                grid[row].append(alphabet[alph_ctr])
                used.append(alphabet[alph_ctr])

    # zwracamy siatkę jako obiekt klasy array z biblioteki numpy
    return np.array(grid)

# funkcja szyfrująca
def encrypt(pairs, grid):
    # zmienna przechowująca szyfrogram
    encrypted = ""
    # dla każdej pary (przygotowany tekst)
    for pair in pairs:
        # korzystając z funkcji numpy znajdujemy koordynaty liter w siatce
        coords = []
        coords.append(list(np.argwhere(grid == pair[0])[0]))
        coords.append(list(np.argwhere(grid == pair[1])[0]))
        
        # sprawdzamy czy litery z pary są w tym samym rzędzie
        if coords[0][0] == coords[1][0]:
            # jeśli tak to zastępujemy je literami o 1 pozycję na prawo od nich
            encrypted += grid[coords[0][0]][(coords[0][1] + 1) % 5]
            encrypted += grid[coords[1][0]][(coords[1][1] + 1) % 5]
            encrypted += " "

        # jeżeli nie to sprawdzamy czy litery z pary są w tej samej kolumnie
        elif coords[0][1] == coords[1][1]:
            # jeśli tak to zastępujemy je literami o 1 pozycję w dół od nich
            encrypted += grid[(coords[0][0] + 1) % 5][coords[0][1]]
            encrypted += grid[(coords[1][0] + 1) % 5][coords[1][1]]
            encrypted += " "

        # w takim razie muszą tworzyć prostokąt
        else:
            # zamieniamy litery tak, aby litera została zastąpiona tą
            # z 'niezajętego' kąta prostokąta, ale w tym samym rzędzie
            encrypted += grid[coords[0][0]][coords[1][1]]
            encrypted += grid[coords[1][0]][coords[0][1]]
            encrypted += " "

    # zwracamy string zaszyfrowanych par
    return encrypted

# funkcja deszyfrująca
def decrypt(pairs, grid):
    decrypted = ""
    for pair in pairs:
        coords = []
        coords.append(list(np.argwhere(grid == pair[0])[0]))
        coords.append(list(np.argwhere(grid == pair[1])[0]))
        
        # sprawdzamy czy litery z pary są w tym samym rzędzie
        if coords[0][0] == coords[1][0]:
            # jeśli tak to zastępujemy je literami o 1 pozycję na lewo od nich
            # (odwrotność szyfrowania)
            decrypted += grid[coords[0][0]][(coords[0][1] - 1) % 5]
            decrypted += grid[coords[1][0]][(coords[1][1] - 1) % 5]
            decrypted += " "

        # jeżeli nie to sprawdzamy czy litery z pary są w tej samej kolumnie
        elif coords[0][1] == coords[1][1]:
            # jeśli tak to zastępujemy je literami o 1 pozycję w górę od nich
            # (odwrotność szyfrowania)
            decrypted += grid[(coords[0][0] - 1) % 5][coords[0][1]]
            decrypted += grid[(coords[1][0] - 1) % 5][coords[1][1]]
            decrypted += " "

        # w takim razie muszą tworzyć prostokąt
        else:
            # zamieniamy litery tak, aby litera została zastąpiona tą
            # z 'niezajętego' kąta prostokąta, ale w tym samym rzędzie
            # (tak samo jak w szyfrowaniu)
            decrypted += grid[coords[0][0]][coords[1][1]]
            decrypted += grid[coords[1][0]][coords[0][1]]
            decrypted += " "

    # zwracamy string zdeszyfrowanych par
    return decrypted

# obsługa wejścia
if __name__ == '__main__':
    # pobranie od użytkownika klucza i przygotowanie go do pracy
    key = input('Podaj klucz (litery, bez cyfr): ')
    key = process_key(key.upper())

    # utworzenie z klucza siatki szyfrowej
    pf_grid = create_grid(key)

    # pobranie od użytkownika plaintextu i przygotowanie go do pracy
    plaintext = input('Podaj plaintext (litery, bez cyfr): ').upper()
    print(f'Plaintext: {plaintext}')
    plaintext = process_text(plaintext)

    # zaszyfrowanie podanej wiadomości i pokazanie wyników
    cyphertext = encrypt(plaintext, pf_grid)
    print(f'Tekst zaszyfrowany: {cyphertext}')

    # przygotowanie szyfrogramu do rozszyfrowania
    to_decrypt = process_text(cyphertext)

    # zdeszyfrowanie szyfrogramu i pokazanie wyników
    decryptedtext = decrypt(to_decrypt, pf_grid)
    print(f'Tekst zdeszyfrowany: {decryptedtext}')
