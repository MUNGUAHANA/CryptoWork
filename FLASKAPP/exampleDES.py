# Définition des tables de permutation et de substitution
InitialPermutationTable = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8
]

FinalPermutationTable = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29
]

ExpansionPermutationTable = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

StraightPermutationTable = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]
def xor(a, b):
    
    ans = ""

    for i in range(len(a)):

        if a[i] == b[i]:

            ans = ans + "0"

        else:

            ans = ans + "1"

    return ans

def permute(n_bits, in_bytes, table):
    """Permute les bits d'un bloc d'entrée."""
    out_bytes = bytearray(n_bits // 8)
    for i in range(n_bits):
        out_byte_idx, out_bit_idx = i // 8, i % 8
        in_byte_idx, in_bit_idx = table[i] // 8, table[i] % 8
        out_bytes[out_byte_idx] |= (in_bytes[in_byte_idx] >> (7 - in_bit_idx)) & (1 << (7 - out_bit_idx))
    return out_bytes


def split(n_bits, n_bytes, in_bytes):
    """Divise un bloc d'entrée en deux blocs."""
    left_bytes = in_bytes[:n_bytes]
    right_bytes = in_bytes[n_bytes:]
    return left_bytes, right_bytes


def combine(n_bytes, n_bits, left_bytes, right_bytes):
    """Combine deux blocs en un seul."""
    out_bytes = bytearray(n_bits // 8)
    for i in range(n_bytes):
        out_bytes[i * 2] = left_bytes[i]
        out_bytes[i * 2 + 1] = right_bytes[i]
    return out_bytes


def xor_bytes(b1, b2):
    """Effectue un XOR bit à bit entre deux blocs d'octets."""
    return bytearray(a ^ b for a, b in zip(b1, b2))


def function(in_bytes, round_key):
    """Fonction interne du round DES."""
    expanded_bytes = permute(32, in_bytes, ExpansionPermutationTable)
    xor_bytes = xor_bytes(expanded_bytes, round_key)
    substituted_bytes = substitute(xor_bytes, SubstitutionTables)
    return permute(32, substituted_bytes, StraightPermutationTable)


def substitute(in_bytes, tables):
    """Applique les tables de substitution."""
    out_bytes = bytearray(4)
    for i in range(4):
        row = (in_bytes[i * 2] >> 1) | (in_bytes[i * 2 + 1] << 3)
        col = in_bytes[i * 2] & 1 | (in_bytes[i * 2 + 1] >> 5)
        out_bytes[i] = tables[i][row][col]
    return out_bytes


def Cipher(plain_block, round_keys, cipher_block):
    """Chiffre un bloc de 64 bits avec DES."""
    in_block = permute(64, plain_block, InitialPermutationTable)
    left_block, right_block = split(32, 4, in_block)
    for round in range(16):
        mixer(left_block, right_block, round_keys[round])
        if round != 15:
            swapper(left_block, right_block)
    out_block = combine(32, 64, left_block, right_block)
    return permute(64, out_block, FinalPermutationTable)


def mixer(left_block, right_block, round_key):
    """Fonction de mixage du round DES."""
    right_copy = right_block.copy()
    t2 = function(right_copy, round_key)
    left_block[:] = xor_bytes(left_block, t2)


def swapper(left_block, right_block):
    """Échange les blocs gauche et droit."""
    left_block, right_block = right_block, left_block


def encrypt(message, round_keys):
    """Chiffre un message avec DES."""
    message_bytes = message.encode('utf-8')
    padded_bytes = pad_message(message_bytes)
    cipher_blocks = []
    for i in range(0, len(padded_bytes), 8):
        block = padded_bytes[i:i + 8]
        cipher_block = Cipher(block, round_keys, bytearray(8))
        cipher_blocks.append(cipher_block)
