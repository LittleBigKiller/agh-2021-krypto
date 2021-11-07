# UWAGA - W kodzie znajdują się elementy niezaimplementowanej
# funkcjonalności - obsługi znaków specjalnych.
# O ile kodowanie ITA2 pozwala na ich obsługę, nie byłem w stanie
# znaleźć informacji odnośnie tego jak sama maszyna je obsługiwała.
# Ponieważ pełna obsługa znaków specjalnych znacznie i w mojej opinii
# niepotrzebnie komplikowałaby kod demonstracyjny,
# postanowiłem jej nie dokańczać ~ JD


import copy

# definicje rotorów odpowiednich grup, każdy innej długości,
# normalnie kombinacje 0 i 1 były konfigurowane przez użytkowników
# jednak na potrzeby prezentacji zostały wygenerowane losowo i są statyczne

# rotory psi
rotor_psi1  = '0110100100111100010010010111010001011111011'
rotor_psi2  = '10101101011100001100101011001001100011011101001'
rotor_psi3  = '111110110111110001110011001001001010011111001100010'
rotor_psi4  = '11010110111001100011111110011101011010001001011100111'
rotor_psi5  = '10000001000101001010110001010111110111110111100100011010111'

rotor_psi_list  = [rotor_psi1, rotor_psi2, rotor_psi3, rotor_psi4, rotor_psi5]

# rotory 
rotor_mu1   = '0010110100111110010010011011000110000'
rotor_mu2   = '0011110011101000001011011100100001011010000101001011101111101'

rotor_mu_list   = [rotor_mu1, rotor_mu2]

# rotory chi obracały się z każdą literą
rotor_chi1  = '00010001010110110010110011001101011011001'
rotor_chi2  = '0001011011111100111000111101100'
rotor_chi3  = '01000111101101010101010110000'
rotor_chi4  = '01111100011000001000010001'
rotor_chi5  = '01001100010000010110111'

rotor_chi_list  = [rotor_chi1, rotor_chi2, rotor_chi3, rotor_chi4, rotor_chi5]

# Zmienna przechowująca ilość możliwych ustawień danych rotorów w grupach
rotor_psi_len   = [43, 47, 51, 53, 59]
rotor_mu_len    = [37, 61]
rotor_chi_len   = [41, 31, 29, 26, 23]

# Tworzenie zmiennych przechowujących aktualne ustawienia rotorów konkretnych grup
# Utworzone "losowe" ustawienie na potrzeby demonstracji
rotor_psi_curr_setup    = [6, 4, 4, 5, 1]
rotor_mu_curr_setup     = [2, 3]
rotor_chi_curr_setup    = [1, 7, 4, 8, 6]

# Tworzenie zmiennych przechowujących pierwotne ustawienia rotorów konkretnych grup
rotor_psi_init_setup    = [0, 0, 3, 0, 0]
rotor_mu_init_setup     = [0, 0]
rotor_chi_init_setup    = [0, 0, 1, 0, 0]

# pomocniczy słownik do mapowania kodów ita2 na litery
ita2_to_letter = {
    '00000': '@', # zastąpienie znaku NULL na potrzeby prezentacji
    '11111': '#', # zastąpienie znaku ZMIANA TRYBU NA LITEROWY na potrzeby prezentacji
    '00010': '<', # zastąpienie znaku CR na potrzeby prezentacji
    '01000': '>', # zastąpienie znaku LF na potrzeby prezentacji
    '00100': ' ',   '11101': 'Q',   '11001': 'W',  
    '10000': 'E',   '01010': 'R',   '00001': 'T',   '10101': 'Y',   '11100': 'U',
    '01100': 'I',   '00011': 'O',   '01101': 'P',   '11000': 'A',   '10100': 'S',
    '10010': 'D',   '10110': 'F',   '01011': 'G',   '00101': 'H',   '11010': 'J',
    '11110': 'K',   '01001': 'L',   '10001': 'Z',   '10111': 'X',   '01110': 'C',
    '01111': 'V',   '10011': 'B',   '00110': 'N',   '00111': 'M',
    '11011': '%' # zastąpienie znaku ZMIANA TRYBU NA SYMBOLOWY na potrzeby prezentacji
}

# [NIEUŻYWANY] pomocniczy słownik do mapowania kodów ita2 na znaki
ita2_to_special = {
    '00010': '\r',  '01000': '\n',  '00100': ' ',   '11101': '1',   '11001': '2',
    '10000': '3',   '01010': '4',   '00001': '5',   '10101': '6',   '11100': '7',
    '01100': '8',   '00011': '9',   '01101': '0',   '11000': '-',   '10100': '\'',
    '10010': '$',   '10110': '!',   '01011': '&',   '00101': '#',   '11010': '£', 
    '11110': '(',   '01001': ')',   '10001': '+',   '10111': '/',   '01110': ':',  
    '01111': '=',   '10011': '?',   '00110': ',',   '00111': '.',   '11111': '_LS'
}

# lista znaków dozwolonych, z której korzysta funkcja czyszcząca tekst
allowed_chars = list('\r\n QWERTYUIOPASDFGHJKLZXCVBNM') # [OGRANICZENIE FUNKCJONALNOŚCI]
# allowed_chars = list('\r\n QWERTYUIOPASDFGHJKLZXCVBNM1234567890-\'$!&#£()+/:=?,.')

# pomocniczy słownik do mapowania liter na kody ita2 (odwrócony słownik ita2_to_letter)
letter_to_ita2 = {value : key for (key, value) in ita2_to_letter.items()}

# [NIEUŻYWANY] pomocniczy słownik do mapowania znaków na kody ita2 (odwrócony słownik ita2_to_special)
special_to_ita2 = {value : key for (key, value) in ita2_to_special.items()}

# funkcja pomocnicza do "XORowania" znaków "1" i "0"
def xor_mock_binary(bit0, bit1):
    # Jeżeli "bity" są identyczne zwróć "0"
    if bit0 == bit1:
        return '0'
    # w przeciwnym razie zwróć "1"
    else:
        return '1'

# funkcja pomocnicza czyszcząca tekst ze znaków nieobsługiwanych przez maszynę
def sanitize_text(string):
    # zmienna przechowująca "przygotowany" tekst
    sanitized = ''
    # iterujemy po każdej literze stringa
    for char in string.upper():
        # jeśli znak jest alfanumeryczny
        if char in allowed_chars:
            # dodajemy go do naszego stringa zatwierdzonych znaków
            sanitized += char

    return sanitized

# funkcja odpowiadająca za obrót rotorów
def shift_rotors(psi, mu, chi):
    # rotory chi zawsze się obracają
    for i in range(len(chi)):
        chi[i] += 1
        chi[i] %= rotor_chi_len[i]
    
    # rotor mu1 zawsze się obraca
    mu[0] += 1
    mu[0] %= rotor_mu_len[0]

    # rotor mu2 obraca się tylko jeśli mu1 jest ustawiony na wartość '1'
    if rotor_mu1[mu[0]] == '1':
        mu[1] += 1
        mu[1] %= rotor_mu_len[1]

    # rotory psi obracają się tylko jeśli mu2 jest ustawiony na wartość '1'
    if rotor_mu2[mu[1]] == '1':
        for i in range(len(psi)):
            psi[i] += 1
            psi[i] %= rotor_psi_len[i]
    
    return (psi, mu, chi)

# funkcja pomagająca wykonać XORowanie z kluczem danego znaku w ITA2
def xor_ita2(code, psi, mu, chi):
    res_code = ''
    # bit po bicie XOrujemy z odpowiednimi rotorami
    for i in range(len(code)):
        res = xor_mock_binary(code[i], rotor_chi_list[i][chi[i]])
        res = xor_mock_binary(res, rotor_psi_list[i][psi[i]])
        res_code += res

    # obracamy rotory po wykonaniu pracy na danym znaku
    psi, mu, chi = shift_rotors(psi, mu, chi)

    return (res_code, psi, mu, chi)

# funkcja szyfrująca (deszyfrowanie przez ponowne szyfrowanie z tymi samymi parametrami)
def encrypt(string, psi, mu, chi):
    # zmienna przechowująca tekst zaszyfrowany
    cyphertext = ''
    for char in string:
        # zamieniamy literę na jej kod ITA2
        ita = letter_to_ita2[char]
        # wykonujemy XORowanie z naszym 'kluczem' (odpowiednio ustawione rotory)
        ita, psi, mu, chi = xor_ita2(ita, psi, mu, chi)
        # dopisujemy wynik w postaci czytelnej (na potrzeby demonstracji) do cyphertextu
        cyphertext += ita2_to_letter[ita]
    return cyphertext

# obsługa wejścia
if __name__ == '__main__':
    # ============================================================== #
    # V # ODKOMENTOWYWAĆ NA WŁASNĄ ODPOWIEDZIALNOŚĆ - MĘCZĄCE!!! # V #
    # ============================================================== #

    # # pobranie od użytkownika pierwotnych ustawień rotorów
    # for i in range(len(rotor_psi_curr_setup)):
    #     rotor_psi_curr_setup[i] = int(input(f"Podaj ustawienie rotora psi{i+1} (liczba w zakresie 0-{rotor_psi_len[i]}): "))

    # for i in range(len(rotor_mu_curr_setup)):
    #     rotor_mu_curr_setup[i] = int(input(f"Podaj ustawienie rotora mu{i+1} (liczba w zakresie 0-{rotor_mu_len[i]}): "))

    # for i in range(len(rotor_chi_curr_setup)):
    #     rotor_chi_curr_setup[i] = int(input(f"Podaj ustawienie rotora chi{i+1} (liczba w zakresie 0-{rotor_chi_len[i]}): "))
    
    # ============================================================== #
    # ^ # ODKOMENTOWYWAĆ NA WŁASNĄ ODPOWIEDZIALNOŚĆ - MĘCZĄCE!!! # ^ #
    # ============================================================== #

    rotor_psi_init_setup = copy.deepcopy(rotor_psi_curr_setup)
    rotor_mu_init_setup = copy.deepcopy(rotor_mu_curr_setup)
    rotor_chi_init_setup = copy.deepcopy(rotor_chi_curr_setup)

    # pobranie od użytkownika plaintextu i przygotowanie go do pracy
    plaintext = input('Podaj plaintext (litery, bez cyfr): ')
    print(f'Plaintext: {plaintext}')
    san_pt = sanitize_text(plaintext)
    
    print(f'Przygotowany plaintext: {san_pt}')

    cyphertext = encrypt(san_pt, rotor_psi_curr_setup, rotor_mu_curr_setup, rotor_chi_curr_setup)

    print(f'Cyphertext: {cyphertext}')

    decrypted = encrypt(cyphertext, rotor_psi_init_setup, rotor_mu_init_setup, rotor_chi_init_setup)

    print(f'Decrypted: {decrypted}')