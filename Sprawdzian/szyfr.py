# Schemat permutacji z kompresją
import textwrap
PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44,
       36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]


def apply_PC1(pc1_table, keys_64bits):
    keys_56bits = ""
    for index in pc1_table:
        keys_56bits += keys_64bits[index-1]
    return keys_56bits


# Test
keys_64bits = "0001001100110100010101110111100110011011101111001101111111110001"
keys_56bits = apply_PC1(PC1, keys_64bits)
# Poprawne wyjście: 11110000110011001010101011110101010101100110011110001111
print('Klucz DES zredukowany do 56 bitów:', keys_56bits)


def split56bits_in_half(keys_56bits):
    left_keys, right_keys = keys_56bits[:28], keys_56bits[28:]
    return left_keys, right_keys


left56, right56 = split56bits_in_half(keys_56bits)

print('Lewa strona:  ', left56)
print('Prawa strona: ', right56)


def circular_left_shift(bits, numberofbits):
    shiftedbits = bits[numberofbits:] + bits[:numberofbits]
    return shiftedbits


print("Lewa połowa klucza po przesunięciu:  ", circular_left_shift(left56, 1))
print("Prawa połowa klucza po przesunięciu: ", circular_left_shift(right56, 2))

PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]


def apply_PC2(pc2_table, keys_56bits):
    keys_48bits = ""
    for index in pc2_table:
        keys_48bits += keys_56bits[index-1]
    return keys_48bits


# Test
left_half = "1111000011001100101010101111"
right_half = "0101010101100110011110001111"

subkey = apply_PC2(PC2, left_half + right_half)

print("Przykładowy klucz podrundy: ", subkey)


round_shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def generate_keys(key_64bits):
    round_keys = list()
    # wykonaj operacje jak w diagramie powyżej
    key56 = apply_PC1(PC1, key_64bits)
    left28, right28 = split56bits_in_half(key56)
    for i in range(16):
        left28 = circular_left_shift(left28, round_shifts[i])
        right28 = circular_left_shift(right28, round_shifts[i])
        round_keys.append(apply_PC2(PC2, left28 + right28))

    return round_keys


# test
key_64bits = "0001001100110100010101110111100110011011101111001101111111110001"

subkeys = generate_keys(key_64bits)

print("Lista 16 podkluczy: ")
print("\n".join(subkeys))


strangekey1 = '1111111011111110111111101111111011111110111111101111111011111110'
strangekey2 = '1110000011100000111000001110000011110001111100011111000111110001'

print("Strange list 1: ")
print("\n".join(generate_keys(strangekey1)))
print()
print("Strange list 2: ")
print("\n".join(generate_keys(strangekey2)))


EXPANSION_TABLE = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]


def apply_Expansion(expansion_table, bits32):
    """ Rozszerza 32-bitowy blok do 48 bitów, używając zadanego schematu"""
    bits48 = ""
    for index in expansion_table:
        bits48 += bits32[index-1]
    return bits48


# test
bits32 = '11110000101010101111000010101010'
out_bits48 = apply_Expansion(EXPANSION_TABLE, bits32)
print("Rozszerzony blok wiadomości: ", out_bits48)
# 011110100001010101010101011110100001010101010101


def XOR(bits1, bits2):
    # ciągi muszą być równej długości
    xor_result = ""
    for index in range(len(bits1)):
        if bits1[index] == bits2[index]:
            xor_result += '0'
        else:
            xor_result += '1'
    return xor_result


bits1 = '1100'
bits2 = '1010'
print(XOR(bits1, bits2))
# output: '0110'

SBOX = [
    # Box-1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # Box-2

    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],

    # Box-3

    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]

    ],

    # Box-4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],

    # Box-5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # Box-6

    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]

    ],
    # Box-7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # Box-8

    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]

]


# znowu trochę funkcji pomoczniczych do działań na Sboxach.

# podział wiadomości na 6-bitowe porcje 48/6 = 8

def split48bits_in_6bits(XOR_48bits):
    """Podział bloku 48-bitowego na 6-bitowe porcje """
    list_of_6bits = textwrap.wrap(XOR_48bits, 6)
    return list_of_6bits


def get_first_and_last_bit(bits6):
    """Pobierz pierwszy i ostatni bit z 6-bitowego łańcucha bitów"""
    twobits = bits6[0] + bits6[-1]
    return twobits


def get_middle_four_bit(bits6):
    """Pobierz środkowe 4 bity z z 6-bitowego łańcucha bitów"""
    fourbits = bits6[1:5]
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


# Test
bits48 = '011110100001010101010101011110100001010101010101'
sixbitslist = split48bits_in_6bits(bits48)
print("Blok podzielony na 6-bitowe porcje:", sixbitslist)
bits6 = sixbitslist[0]
first_last = get_first_and_last_bit(bits6)  # '10' -> 2
print("Liczba z pierwszego i ostatniego bitu: ", first_last)
middle4 = get_middle_four_bit(bits6)  # '0000' -> 0
print("Liczba z środkowych 4 bitów:", middle4)

sboxcount = 1
result = sbox_lookup(sboxcount, first_last, middle4)
print("4-bitowa wartość z s-box", result)


SBOX_PERMUTATION_TABLE = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
                     2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]


def apply_sbox_permutation(permutation_table, sboxes_output):
    """ Scalony efekt użycia Sboksów poddawany jest zdefiniowanej permutacji"""
    permuted32bits = ""
    for index in permutation_table:
        permuted32bits += sboxes_output[index-1]
    return permuted32bits


def functionF(pre32bits, key48bits):
    # uzupełnij kod funkcji zgodnie z diagramem powyżej
    final32bits = ''
    ext48 = apply_Expansion(EXPANSION_TABLE, pre32bits)
    xored = XOR(ext48, key48bits)
    split_list = split48bits_in_6bits(xored)

    res_list = []
    for i in range(8):
        fl = get_first_and_last_bit(split_list[i])
        m4 = get_middle_four_bit(split_list[i])
        res_list.append(sbox_lookup(i, fl, m4))

    jres = "".join(res_list)
    final32bits = apply_sbox_permutation(SBOX_PERMUTATION_TABLE, jres)

    return final32bits


# test
bits32 = '11110000101010101111000010101010'
key48bits = '110010110011110110001011000011100001011111110101'
print("Wynik aplikowania F(): ", functionF(bits32, key48bits))


INITIAL_PERMUTATION_TABLE = ['58 ', '50 ', '42 ', '34 ', '26 ', '18 ', '10 ', '2',
                             '60 ', '52 ', '44 ', '36 ', '28 ', '20 ', '12 ', '4',
                             '62 ', '54 ', '46 ', '38 ', '30 ', '22 ', '14 ', '6',
                             '64 ', '56 ', '48 ', '40 ', '32 ', '24 ', '16 ', '8',
                             '57 ', '49 ', '41 ', '33 ', '25 ', '17 ', '9 ', '1',
                             '59 ', '51 ', '43 ', '35 ', '27 ', '19 ', '11 ', '3',
                             '61 ', '53 ', '45 ', '37 ', '29 ', '21 ', '13 ', '5',
                             '63 ', '55 ', '47 ', '39 ', '31 ', '23 ', '15 ', '7']


def apply_permutation(P_TABLE, PLAINTEXT):
    permutated_M = ""
    for index in P_TABLE:
        permutated_M += PLAINTEXT[int(index)-1]
    return permutated_M


# Test
block = "0100000101110100011101000110000101100011011010110010000100100001"
print("Binarna postać tekstu jawnego: ", block)
permuted_block = apply_permutation(INITIAL_PERMUTATION_TABLE, block)
print("Blok po początkowej permutacji:", permuted_block)


def split64bits_in_half(binarybits):
    return binarybits[:32], binarybits[32:]


L0, R0 = split64bits_in_half(permuted_block)
print("Blok po podziale: ", L0, R0)


INVERSE_PERMUTATION_TABLE = ['40 ', '8 ', '48 ', '16 ', '56 ', '24 ', '64 ', '32',
                             '39 ', '7 ', '47 ', '15 ', '55 ', '23 ', '63 ', '31',
                             '38 ', '6 ', '46 ', '14 ',  '54 ', '22 ', '62 ', '30',
                             '37 ', '5 ', '45 ', '13 ', '53 ', '21 ', '61 ', '29',
                             '36 ', '4 ', '44 ', '12 ', '52 ', '20 ', '60 ', '28',
                             '35 ', '3 ', '43 ', '11 ', '51 ', '19 ', '59 ', '27',
                             '34 ', '2 ', '42 ', '10 ', '50 ', '18 ', '58 ', '26',
                             '33 ', '1 ', '41 ', '9 ', '49 ', '17 ', '57 ', '25']


cipher = apply_permutation(INVERSE_PERMUTATION_TABLE, L0+R0)
print("Blok po finalnej permutacji:", cipher)


# 1. wygenerujmy klucze rundy
key_64bits = "0001001100110100010101110111100110011011101111001101111111110001"
roundkeys = generate_keys(key_64bits)
# Testowa wartości bloków
R = '11001100000000001100110011111111'
L = '11110000101010101111000010101010'

print("Blok wejściowy", L+R)
# Sieć Feistela - uzupełnij kod wg schematu powyżej, użyj podklucza z dowolnej rundy
L1 = R
R1 = XOR(L, functionF(R, roundkeys[0]))

print("Blok wyjściowy (szyfrogram)", L1+R1)
# Wykonaj operacje odwrotne w sieci Feistela - sprawdź czy szyfrowanie się odwróci
R = L1
L = XOR(R1, functionF(L1, roundkeys[0]))

print("Blok wyjściowy (tekst jawny)", L+R)


# Funkcje pomocnicze
def get_bin(x, n): return format(x, 'b').zfill(n)

# tablica znaków w tablicę kodów int


def intoIntArray(message: str):
    int_array = []
    mesg_array = list(message)
    for i in mesg_array:
        int_array.append(ord(i))
    return int_array

# tablica kodów int w tablice znaków


def intoCharArray(message: []):
    mesg_char = []
    for i in message:
        mesg_char.append(chr(i))
    return mesg_char


def intListToBinStr(message_list):
    binary = []
    for x in message_list:
        binary.append(get_bin(x, 8))
    binary_str = ""
    for x in binary:
        binary_str += x
    return binary_str


M = "Attack!!"
key = "EagleHasLanded"

plaintext = intListToBinStr(intoIntArray(M))
print("Plaintext (64 bits):", plaintext)
binary_key = intListToBinStr(intoIntArray(key))
print("Key (only 64 bits): ", binary_key[:64])

rkeys = generate_keys(binary_key)


def DES_encrypt(message, key):
    cipher = ""
    after_ip = apply_permutation(INITIAL_PERMUTATION_TABLE, message)
    L, R = split64bits_in_half(after_ip)
    for i in range(0, 16):
        L1 = R
        R1 = XOR(L, functionF(R, rkeys[i]))
        L = L1
        R = R1

    RL = R + L
    cipher = apply_permutation(INVERSE_PERMUTATION_TABLE, RL)

    return cipher


def DES_decrypt(message, key):
    cipher = ""
    after_fp = apply_permutation(INITIAL_PERMUTATION_TABLE, message)
    R, L = split64bits_in_half(after_fp)
    for i in range(15, -1, -1):
        R1 = L
        L1 = XOR(R, functionF(L, rkeys[i]))
        L = L1
        R = R1

    LR = L + R
    cipher = apply_permutation(INVERSE_PERMUTATION_TABLE, LR)

    return cipher


ciphertext = DES_encrypt(plaintext, binary_key[:64])
print("Ciphertext:         ", ciphertext)
encrypted = DES_decrypt(ciphertext, binary_key[:64])
print("Encrypted message:  ", encrypted)
print(XOR(plaintext, encrypted))
