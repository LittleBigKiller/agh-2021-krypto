# Kod napisany w języku python
# Jest to modyfikacja DES'a wydłużająca klucz do 128 bitów i wiadomość do 64 bitów.
# Wszystkie permutacje musiały zostać odpowiednio zmienione
# Zmienia się głównie funkcjaF - dobór bitów "początkowego i końcowego" stał się znacznie bardziej skomplikowany, dobór bitów "środkowych" również
# S-Boxy zostały wymienione na nowe, szyfr nadal ma 16 rund

import textwrap

PC1 = [4, 121, 12, 113, 20, 105, 28, 97, 5, 89, 13, 81, 21, 73, 29, 65, 37, 122, 45, 114, 53, 106, 61, 98, 6, 90, 14, 82,
       22, 74, 30, 66, 38, 123, 46, 115, 54, 107, 62, 99, 7, 91, 15, 83, 23, 75, 31, 67, 39, 124, 47, 116, 55, 108, 63,
       100, 36, 127, 44, 119, 52, 111, 60, 103, 3, 95, 11, 87, 19, 79, 27, 71, 35, 126, 43, 118, 51, 110, 59, 102, 2, 94,
       10, 86, 18, 78, 26, 70, 34, 125, 42, 117, 50, 109, 58, 101, 1, 93, 9, 85, 17, 77, 25, 69, 33, 92, 41, 84, 49, 76, 57, 68]


def apply_PC1(pc1_table, key128):
    key112 = ""
    for index in pc1_table:
        key112 += key128[index-1]
    return key112


def split_reduced_key_in_half(key112):
    key_half = len(key112)//2
    left_keys, right_keys = key112[:key_half], key112[key_half:]

    return left_keys, right_keys


def circular_left_shift(bits, numberofbits):
    shiftedbits = bits[numberofbits:] + bits[:numberofbits]
    return shiftedbits


PC2 = [32, 70, 29, 73, 36, 67, 50, 80, 42, 57, 46, 61, 53, 59, 34, 84, 56, 71, 39, 62, 49, 77, 44, 66, 48, 79, 33, 75, 45, 68, 51, 60, 40, 82, 30, 64, 55, 72, 47, 63, 37, 83, 31, 76, 52, 69, 41, 58,
       2, 97, 13, 108, 20, 87, 27, 93, 7, 103, 16, 111, 8, 86, 26, 96, 4, 107, 12, 101, 19, 89, 23, 104, 10, 100, 21, 105, 6, 95, 15, 112, 28, 90, 3, 109, 5, 102, 1, 98, 24, 106, 11, 92, 17, 85, 14, 88]


def apply_PC2(pc2_table, key56):
    key48 = ""
    for index in pc2_table:
        key48 += key56[index-1]
    return key48


ROUND_SHIFTS = [1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1]


def generate_keys(key128):
    round_keys = list()
    key112 = apply_PC1(PC1, key128)
    left56, right56 = split_reduced_key_in_half(key112)
    for i in range(16):
        left56 = circular_left_shift(left56, ROUND_SHIFTS[i])
        right56 = circular_left_shift(right56, ROUND_SHIFTS[i])
        round_keys.append(apply_PC2(PC2, left56 + right56))

    return round_keys


EXPANSION_TABLE = [1, 64, 32, 33, 31, 34, 30, 35, 29, 36, 28, 37, 29, 36, 28, 37, 27, 38, 26, 39, 25, 40, 24, 41, 25, 40, 24, 41, 23, 42, 22, 43, 21, 44, 20, 45, 21, 44, 20, 45, 19, 46, 18, 47,
                   17, 48, 16, 49, 17, 48, 16, 49, 15, 50, 14, 51, 13, 52, 12, 53, 13, 52, 12, 53, 11, 54, 10, 55, 9, 56, 8, 57, 9, 56, 8, 57, 7, 58, 6, 59, 5, 60, 4, 61, 5, 60, 4, 61, 3, 62, 2, 63, 1, 64, 32, 33]


def apply_Expansion(expansion_table, bits64):
    """ Rozszerza 64-bitowy blok do 96 bitów, używając zadanego schematu"""
    bits96 = ""
    for index in expansion_table:
        bits96 += bits64[index-1]
    return bits96


def XOR(bits1, bits2):
    # ciągi muszą być równej długości
    xor_result = ""
    for index in range(len(bits1)):
        if bits1[index] == bits2[index]:
            xor_result += '0'
        else:
            xor_result += '1'
    return xor_result


SBOX = [
    # Box-1
    [
        [13, 6, 0, 10, 14, 3, 11, 5, 7, 1, 9, 4, 2, 8, 12, 15],
        [0, 5, 10, 3, 7, 9, 12, 15, 11, 2, 6, 13, 8, 14, 1, 4],
        [8, 3, 5, 9, 11, 12, 6, 10, 1, 13, 2, 14, 4, 7, 15, 0],
        [7, 0, 9, 5, 12, 6, 10, 3, 8, 11, 15, 2, 1, 13, 4, 14]
    ],
    # Box-2
    [
        [9, 14, 5, 0, 12, 7, 6, 11, 2, 4, 15, 3, 1, 10, 8, 13],
        [15, 2, 3, 9, 6, 12, 8, 5, 1, 13, 4, 10, 11, 7, 14, 0],
        [5, 11, 9, 6, 10, 1, 0, 12, 14, 8, 2, 15, 7, 4, 13, 3],
        [10, 5, 0, 12, 13, 2, 7, 9, 4, 3, 11, 6, 14, 8, 1, 15]
    ],
    # Box-3
    [
        [8, 2, 4, 11, 7, 12, 13, 1, 5, 15, 3, 6, 14, 9, 0, 10],
        [1, 15, 11, 12, 14, 5, 8, 2, 10, 6, 4, 3, 9, 0, 7, 13],
        [7, 14, 10, 5, 12, 2, 1, 11, 0, 3, 15, 8, 9, 4, 6, 13],
        [12, 2, 5, 11, 3, 14, 15, 4, 7, 8, 9, 6, 0, 13, 10, 1]
    ],
    # Box-4
    [
        [15, 4, 12, 11, 5, 8, 2, 1, 10, 9, 6, 0, 3, 14, 13, 7],
        [9, 14, 10, 1, 12, 2, 7, 4, 3, 0, 15, 6, 5, 11, 8, 13],
        [4, 8, 2, 5, 14, 3, 1, 15, 13, 7, 11, 12, 0, 9, 6, 10],
        [14, 2, 7, 12, 11, 5, 4, 9, 8, 13, 1, 10, 6, 0, 15, 3]
    ],
    # Box-5
    [
        [9, 14, 0, 13, 15, 3, 5, 8, 6, 11, 10, 7, 1, 4, 12, 2],
        [6, 8, 9, 3, 10, 15, 0, 5, 1, 13, 7, 4, 12, 2, 11, 14],
        [14, 0, 3, 6, 5, 12, 9, 15, 8, 7, 13, 10, 11, 1, 2, 4],
        [3, 5, 4, 10, 9, 0, 15, 6, 13, 2, 14, 1, 7, 12, 8, 11]
    ],
    # Box-6
    [
        [11, 5, 7, 14, 4, 3, 13, 0, 8, 6, 2, 9, 15, 10, 1, 12],
        [8, 3, 11, 0, 14, 13, 1, 6, 5, 9, 12, 7, 2, 4, 15, 10],
        [6, 11, 13, 1, 10, 4, 0, 7, 3, 12, 8, 2, 5, 15, 14, 9],
        [13, 8, 0, 6, 7, 1, 14, 11, 10, 15, 5, 9, 12, 2, 3, 4]

    ],
    # Box-7
    [
        [12, 3, 2, 14, 15, 0, 5, 9, 7, 10, 4, 1, 8, 13, 11, 6],
        [2, 9, 5, 0, 8, 6, 15, 10, 14, 7, 3, 12, 13, 11, 4, 1],
        [6, 8, 15, 2, 12, 5, 3, 14, 10, 1, 9, 4, 7, 11, 0, 13],
        [1, 6, 10, 5, 7, 9, 12, 3, 13, 8, 0, 15, 14, 2, 11, 4]
    ],
    # Box-8
    [
        [11, 6, 5, 3, 0, 9, 12, 15, 13, 8, 10, 4, 7, 14, 1, 2],
        [8, 5, 3, 15, 13, 10, 6, 0, 2, 14, 12, 9, 1, 4, 11, 7],
        [2, 9, 14, 0, 11, 6, 5, 12, 4, 7, 3, 10, 8, 13, 15, 1],
        [7, 12, 0, 5, 14, 3, 9, 10, 1, 11, 15, 6, 4, 8, 2, 13]
    ]
]


# podział wiadomości na 12-bitowe porcje 96/12 = 8
def split96bits_in_12bits(XOR_96bits):
    """Podział bloku 96-bitowego na 12-bitowe porcje"""
    list_of_12bits = textwrap.wrap(XOR_96bits, 12)
    return list_of_12bits


def get_2first_and_4last_bit_xor(bits12):
    """Pobierz pierwsze 2 i ostatni 4 bity z 12-bitowego łańcucha bitów
        XORuj pierwsze 2 z 3 i 4 od końca, wynik tego XORuj z ostatnimi dwoma
        i zwróć wynikową liczbę"""
    twobits = XOR(bits12[:2], bits12[-4:-2])
    twobits = XOR(twobits, bits12[-2:])
    return twobits


def get_four_from_almost_middle_six_bits(bits12):
    """Pobierz środkowe 6 bitów (3-8) z 12-bitowego łańcucha bitów
        zwróć 1 bit, wynik XORowania 2 i 3 z 4 i 5 oraz 6 bit"""
    fourbits = bits12[2] + XOR(bits12[3:5], bits12[5:7]) + bits12[8]
    return fourbits


def binary_to_decimal(binarybits):
    """ Konwersja łańcucha bitów do wartości dzięsiętnej """
    decimal = int(binarybits, 2)
    return decimal


def decimal_to_binary(decimal):
    """ Konwersja wartości dziesiętnej do 4-bitowego łańcucha bitów """
    binary4bits = bin(decimal)[2:].zfill(4)
    return binary4bits


def sbox_lookup(sboxcount, first_last, middle4):
    """ Dostęp do odpowiedniej wartości odpowiedniego sboxa"""
    d_first_last = binary_to_decimal(first_last)
    d_middle = binary_to_decimal(middle4)
    sbox_value = SBOX[sboxcount][d_first_last][d_middle]
    return decimal_to_binary(sbox_value)


PERMUTATION_TABLE = [16, 57, 7, 36, 20, 43, 21, 54, 29, 38, 12, 62, 28, 45, 17, 51, 1, 41, 15, 35, 23, 59, 26, 64, 5, 46, 18, 56, 31,
                     40, 10, 34, 2, 42, 8, 63, 24, 50, 14, 37, 32, 58, 27, 55, 3, 47, 9, 33, 19, 49, 13, 60, 30, 44, 6, 61, 22, 53, 11, 52, 4, 39, 25, 48]


def apply_sbox_permutation(permutation_table, sboxes_output):
    """ Scalony efekt użycia Sboksów poddawany jest zdefiniowanej permutacji"""
    permuted64bits = ""
    for index in permutation_table:
        permuted64bits += sboxes_output[index-1]
    return permuted64bits


def functionF(pre64bits, key96bits):
    final64bits = ''
    ext96 = apply_Expansion(EXPANSION_TABLE, pre64bits)
    xored = XOR(ext96, key96bits)
    split_list = split96bits_in_12bits(xored)

    res_list = []
    for i in range(8):
        fl = get_2first_and_4last_bit_xor(split_list[i])
        m4 = get_four_from_almost_middle_six_bits(split_list[i])
        res_list.append(sbox_lookup(i, fl, m4) +
                        XOR(sbox_lookup(7 - i, fl, m4), sbox_lookup(i, fl, m4)))

    jres = "".join(res_list)
    final64bits = apply_sbox_permutation(PERMUTATION_TABLE, jres)

    return final64bits


INITIAL_PERMUTATION_TABLE = ['58 ', '50 ', '42 ', '34 ', '26 ', '18 ', '10 ', '2',
                             '60 ', '52 ', '44 ', '36 ', '28 ', '20 ', '12 ', '4',
                             '62 ', '54 ', '46 ', '38 ', '30 ', '22 ', '14 ', '6',
                             '64 ', '56 ', '48 ', '40 ', '32 ', '24 ', '16 ', '8',
                             '57 ', '49 ', '41 ', '33 ', '25 ', '17 ', ' 9 ', '1',
                             '59 ', '51 ', '43 ', '35 ', '27 ', '19 ', '11 ', '3',
                             '61 ', '53 ', '45 ', '37 ', '29 ', '21 ', '13 ', '5',
                             '63 ', '55 ', '47 ', '39 ', '31 ', '23 ', '15 ', '7',
                             '122', '114', '106', '98', '90', '82', '74', '66',
                             '124', '116', '108', '100', '92', '84', '76', '68',
                             '126', '118', '110', '102', '94', '86', '78', '70',
                             '128', '120', '112', '104', '96', '88', '80', '72',
                             '121', '113', '105', '97', '89', '81', '73', '65',
                             '123', '115', '107', '99', '91', '83', '75', '67',
                             '125', '117', '109', '101', '93', '85', '77', '69',
                             '127', '119', '111', '103', '95', '87', '79', '71']


def apply_permutation(P_TABLE, PLAINTEXT):
    permutated_M = ""
    for index in P_TABLE:
        permutated_M += PLAINTEXT[int(index)-1]
    return permutated_M


def split_bits_in_half(binarybits):
    return binarybits[:len(binarybits)//2], binarybits[len(binarybits)//2:]


INVERSE_PERMUTATION_TABLE = ['40 ', '8 ', '48 ', '16 ', '56 ', '24 ', '64 ', '32',
                             '39 ', '7 ', '47 ', '15 ', '55 ', '23 ', '63 ', '31',
                             '38 ', '6 ', '46 ', '14 ', '54 ', '22 ', '62 ', '30',
                             '37 ', '5 ', '45 ', '13 ', '53 ', '21 ', '61 ', '29',
                             '36 ', '4 ', '44 ', '12 ', '52 ', '20 ', '60 ', '28',
                             '35 ', '3 ', '43 ', '11 ', '51 ', '19 ', '59 ', '27',
                             '34 ', '2 ', '42 ', '10 ', '50 ', '18 ', '58 ', '26',
                             '33 ', '1 ', '41 ', '9 ', '49 ', '17 ', '57 ', '25',
                             '104', '72', '112', '80', '120', '88', '128', '96',
                             '103', '71', '111', '79', '119', '87', '127', '95',
                             '102', '70', '110', '78', '118', '86', '126', '94',
                             '101', '69', '109', '77', '117', '85', '125', '93',
                             '100', '68', '108', '76', '116', '84', '124', '92',
                             '99', '67', '107', '75', '115', '83', '123', '91',
                             '98', '66', '106', '74', '114', '82', '122', '90',
                             '97', '65', '105', '73', '113', '81', '121', '89']

# Zamiana na binarne
def get_bin(x, n): return format(x, 'b').zfill(n)


# Tablica znaków w tablicę kodów int
def intoIntList(message: str):
    int_array = []
    mesg_array = list(message)
    for i in mesg_array:
        int_array.append(ord(i))
    return int_array


# Tablica kodów int w tablice znaków
def intoCharArray(message: []):
    mesg_char = []
    for i in message:
        mesg_char.append(chr(i))
    return mesg_char


# Tablica kodów int w "binarny" string
def intListToBinStr(message_list):
    binary = []
    for x in message_list:
        binary.append(get_bin(x, 8))
    binary_str = ""
    for x in binary:
        binary_str += x
    return binary_str


def encrypt(message, key):
    cipher = ""
    rkeys = generate_keys(binary_key)
    after_ip = apply_permutation(INITIAL_PERMUTATION_TABLE, message)
    L, R = split_bits_in_half(after_ip)
    for i in range(0, 16):
        L1 = R
        R1 = XOR(L, functionF(R, rkeys[i]))
        L = L1
        R = R1

    RL = R + L
    cipher = apply_permutation(INVERSE_PERMUTATION_TABLE, RL)

    return cipher


def decrypt(message, key):
    cipher = ""
    rkeys = generate_keys(binary_key)
    after_fp = apply_permutation(INITIAL_PERMUTATION_TABLE, message)
    R, L = split_bits_in_half(after_fp)
    for i in range(15, -1, -1):
        R1 = L
        L1 = XOR(R, functionF(L, rkeys[i]))
        L = L1
        R = R1

    LR = L + R
    cipher = apply_permutation(INVERSE_PERMUTATION_TABLE, LR)

    return cipher


if __name__ == '__main__':
    # Przykładowy program
    message = "2xKlucz2xProblem"
    key = "ZdecydowaniePrzekombinowalem"

    plaintext = intListToBinStr(intoIntList(message))
    print("Plaintext (128 bits):      ", plaintext)

    binary_key = intListToBinStr(intoIntList(key))
    print("Key (only 128 bits):       ", binary_key[:128])

    ciphertext = encrypt(plaintext, binary_key[:64])
    print("Ciphertext:                ", ciphertext)

    decrypted = decrypt(ciphertext, binary_key[:64])
    print("Decrypted message:         ", decrypted)

    print("XOR(Plaintext, Decrypted): ", XOR(plaintext, decrypted))

