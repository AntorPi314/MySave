def toBinary(text, model):
    """
    Convert text to bit string according to the given model.
    model: string containing allowed characters in order.
    Returns: bit string, bits per character
    """
    bit_length = (len(model)-1).bit_length()  # minimum bits per char
    binary = ''
    for ch in text:
        index = model.index(ch)
        binary += format(index, f'0{bit_length}b')
    return binary, bit_length

def toASCII(bitstring):
    """
    Convert bitstring to ASCII bytes with 1-byte length metadata
    so original bit length can be restored.
    """
    bit_len = len(bitstring)
    # Pad to full bytes
    padded_len = ((bit_len + 7) // 8) * 8
    bitstring_padded = bitstring.ljust(padded_len, '0')
    # Convert to bytes
    num_bytes = int(bitstring_padded, 2).to_bytes(padded_len // 8, 'big')
    # Store bit length as first byte
    return bytes([bit_len]) + num_bytes


def fromASCII(data):
    """
    Convert ASCII bytes (with first byte = bit length) back to bitstring
    """
    bit_len = data[0]           # first byte = original bit length
    bit_bytes = data[1:]        # actual bytes
    # Convert bytes to full bit string
    bitstring_padded = bin(int.from_bytes(bit_bytes, 'big'))[2:].zfill(len(bit_bytes)*8)
    # Take only valid bits
    return bitstring_padded[:bit_len]


# =========================
# Example usage
# =========================

bits = "0011101000110101110011110000001111100001111000111001010"

# Convert to ASCII
ascii_bytes = toASCII(bits)
print("ASCII bytes:", ascii_bytes)
print("Total bytes:", len(ascii_bytes))

# Recover original bit string
recovered_bits = fromASCII(ascii_bytes)
print("Recovered bits:", recovered_bits)
print("Match:", recovered_bits == bits)