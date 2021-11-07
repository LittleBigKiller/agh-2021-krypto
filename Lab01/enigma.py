# kod enigmy opisujący działanie modelu komercyjnego "Enigma K (A27)" z roku 1927
# model ten posiadał 3 rotory i ustawialny reflektor

import copy

# pomocniczo zapisujemy sobie alfabet
alphabet    = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# zmienne opisujące aktualne i pierwotne ustawienie rotorów
# pierwotne ustawienie jest przechowywane w celach deszyfrowania
curr_rotor_setup = [0, 0, 0]
init_rotor_setup = [0, 0, 0]

# statyczny połączenia wejściowe określające pierwotną zamianę parami
# liter alfabetu na początku i na końcu procesu szyfrowania
entry_wiring = {
    "A": "Q", "B": "W", "C": "E", "D": "R", "E": "C",
    "F": "T", "G": "Z", "H": "U", "I": "O", "J": "S",
    "K": "Y", "L": "P", "M": "V", "N": "X", "O": "I",
    "P": "L", "Q": "A", "R": "D", "S": "J", "T": "F",
    "U": "H", "V": "M", "W": "B", "X": "N", "Y": "K",
    "Z": "G" }

# rotory to permutacje alfabetu wykorzystywane w procesie szyfrowania
rotor_IC    = "DMTWSILRUYQNKFEJCAZBPGXOHV"
rotor_IIC   = "HQZGPJTMOBLNCIFDYAWVEUSRKX"
rotor_IIIC  = "UQNTLSZFMREHDPXKIBVYGJCWOA"

# zmienna ułatwiająca nam pracę na rotorach (i określająca ich ułożenie)
rotors = [rotor_IC, rotor_IIC, rotor_IIIC]

# reflektor określa jak litery zostają zamienione w środkowej fazie szyfrowania,
# litery dobrane są parami, litera nie może zamienić się w samą siebie
reflector = {
    "A": "V", "B": "M", "C": "E", "D": "F", "E": "C",
    "F": "D", "G": "J", "H": "O", "I": "W", "J": "G",
    "K": "Q", "L": "P", "M": "B", "N": "U", "O": "H",
    "P": "L", "Q": "K", "R": "Z", "S": "Y", "T": "X",
    "U": "N", "V": "A", "W": "I", "X": "T", "Y": "S",
    "Z": "R" }

def turn_rotors(rotor_setup):
    # pierwszy rotor zawsze się przestawia
    rotor_setup[0] += 1
    # z powodów technicznych "zawijamy" wartość zmiennej
    rotor_setup[0] %= 26

    if rotor_setup[0] == 17:
        # jeżeli pierwszy rotor dotrze do pozycji "R" (w alfabecie), 
        # to przestawiamy rotor drugi
        rotor_setup[1] += 1
        # z powodów technicznych "zawijamy" wartość zmiennej
        rotor_setup[1] %= 26
        if rotor_setup[1] == 12:
            # jeżeli drugi rotor dotrze do pozycji "M" (w alfabecie), 
            # to przestawiamy rotor trzeci
            rotor_setup[2] += 1
            # z powodów technicznych "zawijamy" wartość zmiennej
            rotor_setup[2] %= 26
    
    return rotor_setup

def flip_entry(letter):
    # zwróć odpowiednią literę według podłączenia wejściowego
    return entry_wiring[letter]

def reflect(letter):
    # zwróć odpowiednią literę według podłączenia w reflektorze
    return reflector[letter]

# funkcja opisująca szyfrowanie każdej litery przez rotory przy "wchodzeniu",
# to jest przed odbiciem na reflektorze
def rotate_letter_entry(letter, rotor_setup):
    # litera po kolei przechodzi przez trzy rotory w kolejności 1, 2, 3
    # na każdym zostaje zamieniona zgodnie z ustawieniem rotora
    for i in range(len(rotors)):
        letter = rotors[i][(alphabet.index(letter) + rotor_setup[i]) % 26]
    return letter

# funkcja opisująca szyfrowanie każdej litery przez rotory przy "wchodzeniu",
# to jest po odbiciu na reflektorze
def rotate_letter_exit(letter, rotor_setup):
    # litera przechodzi przez trzy rotory w odwróconej kolejności - 3, 2, 1,
    # na każdym zostaje zamieniona zgodnie z ustawieniem rotora
    for i in range(len(rotors) - 1, -1, -1):
        letter = alphabet[(rotors[i].index(letter) - rotor_setup[i]) % 26]
    return letter

# sama funkcja opisująca proces szyfrowania/deszyfrowania litery
def encrypt(letter, rotor_setup):
    # litera zostaje zamieniona wg podłączenia wejściowego
    letter = flip_entry(letter)
    
    # litera przechodzi przez rotory w kolejności 1, 2, 3
    letter = rotate_letter_entry(letter, rotor_setup)

    # litera jest odbijana na reflektorze
    letter = reflect(letter)
    
    # litera przechodzi ponownie przez rotory,
    # tym razem w odwrotnej kolejności - 3, 2, 1
    letter = rotate_letter_exit(letter, rotor_setup)

    # litera zostaje ponownie zamieniona wg podłączenia wejściowego
    letter = flip_entry(letter)

    # zwrot zaszyfrowanej litery
    return letter

# kod wprowadzający
if __name__ == "__main__":
    # dla każdego rotora
    for i in range(len(rotors)):
        # pobieramy od użytkownika ustawienie początkowe
        curr_rotor_setup[i] = int(input(f"Podaj ustawienie rotora nr {i+1} (liczba w zakresie 0-25): "))

    # tworzymy kopię tablicy przechowującej ustawienia rotorów
    # będzie nam potrzebna do deszyfrowania
    init_rotor_setup = copy.deepcopy(curr_rotor_setup)
        
    # pobieramy od użytkownika plaintext do zaszyfrowania i zamieniamy na wielkie litery
    plaintext = input("plaintext (litery, bez znaków specjalnych i cyfr): ").upper()
    # pozbywamy się przerw między słowami
    plaintext = ''.join(plaintext.split())

    # zmienna przechowująca szyfrogram
    cyphertext = ""
    # dla każdej litery w plaintext
    for letter in plaintext: 
        # szyfrujemy ją na podstawie "aktualnego" ustawienia rotorów
        cyphertext += encrypt(letter, curr_rotor_setup)
        # po zaszyfrowaniu litery obracamy rotory
        curr_rotor_setup = turn_rotors(curr_rotor_setup)

    # wypisujemy szyfrogram
    print(f"Cyphertext: {cyphertext}")

    # zmienna przechowująca tekst odszyfrowany
    decodedtext = ""
    # dla każdej litery w szyfrogramie
    for letter in cyphertext:
        # w celu odszyfrowania należy każdą z liter ponownie "zaszyfrować"
        # zgodnie z "pierwotnym" ustawieniem rotorów, które kopiowaliśmy
        decodedtext += encrypt(letter, init_rotor_setup)
        # po odszyfrowaniu litery obracamy rotory
        init_rotor_setup = turn_rotors(init_rotor_setup)

    # wypisujemy zdekodowany tekst
    print(f"Decoded text: {decodedtext}")
    # powinien się pokryć z tekstem oryginalnym
    # (chociaż nie ma spacji i nie rozróżnia małych/wielkich liter)