#!/usr/bin/env python3

import sys

def toBinary(text, model):
    bit_length = (len(model)-1).bit_length()
    binary = ''
    for ch in text:
        index = model.index(ch)
        binary += format(index, f'0{bit_length}b')
    return binary, bit_length

def toASCII(bitstring):
    """
    Converts a bitstring into bytes.
    Uses a 1-byte header that stores the number of valid bits 
    in the *last* data byte (1-8).
    A header of '0' signifies an empty string (0 bits).
    """
    bit_len = len(bitstring)
    
    # Handle the empty string case
    if bit_len == 0:
        return bytes([0]) # Header '0' means 0 bits, 0 data bytes.

    # Calculate number of valid bits in the last byte
    valid_bits_last_byte = bit_len % 8
    if valid_bits_last_byte == 0:
        valid_bits_last_byte = 8 # A full byte has 8 valid bits
        
    # Create the 1-byte header
    header = bytes([valid_bits_last_byte])
    
    # Pad the bitstring to a full number of bytes
    padded_len = ((bit_len + 7) // 8) * 8
    bitstring_padded = bitstring.ljust(padded_len, '0')
    
    # Convert padded bitstring to bytes
    # Ensure at least 1 byte is written if padded_len is 0 (though bit_len > 0)
    byte_count = max(1, padded_len // 8)
    num_bytes = int(bitstring_padded, 2).to_bytes(byte_count, 'big')
    
    return header + num_bytes


def fromASCII(data):
    """
    Recovers the original bitstring from bytes created by toASCII.
    Reads the 1-byte header to determine how many bits from the
    last byte are valid.
    """
    if not data:
        return "" # Handle empty data

    valid_bits_last_byte = data[0]
    
    # Handle empty string case (header '0', no data bytes)
    if valid_bits_last_byte == 0:
        if len(data) == 1:
            return ""
        else:
            # Error: header is 0, but data follows. Treat as empty.
            print("Warning: Header is 0 but data is present. Decoding as empty.", file=sys.stderr)
            return "" 
    
    # Check for invalid header (must be 1-8)
    if valid_bits_last_byte < 1 or valid_bits_last_byte > 8:
        print(f"Error: Invalid header byte {valid_bits_last_byte}", file=sys.stderr)
        return "[DECODE_ERROR:INVALID_HEADER]"
        
    bit_bytes = data[1:]
    total_data_bytes = len(bit_bytes)
    
    if total_data_bytes == 0:
        # Error: Header says 1-8 bits, but no data bytes follow
        print(f"Error: Header byte {valid_bits_last_byte} but no data", file=sys.stderr)
        return "[DECODE_ERROR:MISSING_DATA]"

    # Calculate the total bit length
    # All bytes *except* the last one are full (8 bits)
    # The last byte has 'valid_bits_last_byte' bits
    bit_len = (total_data_bytes - 1) * 8 + valid_bits_last_byte
    
    # Convert bytes to padded bitstring
    bitstring_padded = bin(int.from_bytes(bit_bytes, 'big'))[2:].zfill(total_data_bytes * 8)
    
    # Return the unpadded bitstring by taking the correct length
    return bitstring_padded[:bit_len]

def fromBinary(bitstring, bit_len, model1, model2, model3, m1_map):
    model1_inv_map = {i: char for i, char in enumerate(model1)}
    model2_inv_map = {i: char for i, char in enumerate(model2)}
    model3_inv_map = {i: char for i, char in enumerate(model3)}
    
    marker_to_m2_bits = format(m1_map['#'], f'0{bit_len}b')
    marker_to_m3_bits = format(m1_map['*'], f'0{bit_len}b')

    recovered_text = ""
    i = 0
    current_mode = 1
    
    while i < len(bitstring):
        if i + bit_len > len(bitstring):
            break
            
        chunk = bitstring[i : i + bit_len]
        i += bit_len
        
        if current_mode == 1:
            if chunk == marker_to_m2_bits:
                current_mode = 2
            elif chunk == marker_to_m3_bits:
                current_mode = 3
            else:
                index = int(chunk, 2)
                recovered_text += model1_inv_map.get(index, '?')
        
        elif current_mode == 2:
            index = int(chunk, 2)
            recovered_text += model2_inv_map.get(index, '?')
            current_mode = 1
            
        elif current_mode == 3:
            index = int(chunk, 2)
            recovered_text += model3_inv_map.get(index, '?')
            current_mode = 1
            
    return recovered_text


# ==========================================================
# Main Compression & Decompression Script
# ==========================================================

MsgModel1 = "abcdefghijklmnopqrstuvwxyz,\n /#*"
MsgModel2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.?!@#*"
MsgModel3 = "0123456789-_=&%+;'()[]{}\"|:\\<^~>"

BIT_LENGTH = 5

model1_map = {char: i for i, char in enumerate(MsgModel1)}
model2_map = {char: i for i, char in enumerate(MsgModel2)}
model3_map = {char: i for i, char in enumerate(MsgModel3)}

marker_to_m2 = format(model1_map['#'], f'0{BIT_LENGTH}b')
marker_to_m3 = format(model1_map['*'], f'0{BIT_LENGTH}b')

inputMessage = """
hi, A1 ok
how are you""".strip()



compressed_bitstring = ""
compression_possible = True
failing_char = ''
# Define payLoad with a default (it will be overwritten)
payLoad = b"" 

# --- Calculate and print Input stats first ---
input_chars = len(inputMessage)
# Estimate input bits as standard ASCII/UTF-8 bytes * 8
input_bytes_utf8 = len(inputMessage.encode('utf-8'))
print(f'Input ({input_chars} / {input_bytes_utf8 * 8}): "{inputMessage}"')


for char in inputMessage:
    if char in model1_map:
        index = model1_map[char]
        compressed_bitstring += format(index, f'0{BIT_LENGTH}b')
    
    elif char in model2_map:
        compressed_bitstring += marker_to_m2
        index = model2_map[char]
        compressed_bitstring += format(index, f'0{BIT_LENGTH}b')

    elif char in model3_map:
        compressed_bitstring += marker_to_m3
        index = model3_map[char]
        compressed_bitstring += format(index, f'0{BIT_LENGTH}b')
        
    else:
        # === MODIFIED 1 ===
        # Set the fallback payload with [u> prefix
        payLoad = f"[u>{inputMessage}".encode('utf-8')
        # ==================
        compression_possible = False
        failing_char = char
        break

if compression_possible:
    # First, generate the compressed payload
    compressed_payLoad = toASCII(compressed_bitstring)
    compressed_payload_bytes = len(compressed_payLoad)
    
    # Now, check if it's actually smaller than the original UTF-8
    if compressed_payload_bytes > input_bytes_utf8:
        # It's not. Fall back to uncompressed UTF-8.
        # === MODIFIED 2 ===
        payLoad = f"[u>{inputMessage}".encode('utf-8')
        # ==================
        payload_bytes = len(payLoad)
        print(f"Compression inefficient ({compressed_payload_bytes} bytes > {input_bytes_utf8} bytes). Using fallback.")
        print(f"Payload (UTF-8) ({payload_bytes} / {payload_bytes * 8}): {payLoad}")
    else:
        # It is. Use the compressed version. (NO [u> prefix)
        payLoad = compressed_payLoad
        payload_bytes = len(payLoad)
        print(f"Payload ({payload_bytes} / {payload_bytes * 8}): (Note: Payload not shown as bytes. "
              f"Original bits: {len(compressed_bitstring)}. "
              f"Byte count includes 1-byte length header + data padded to 8 bits.)")
        
        # --- Example of Decompression ---
        print("\n--- Decompression Check ---")
        try:
            recovered_bitstring = fromASCII(payLoad)
            recovered_text = fromBinary(recovered_bitstring, BIT_LENGTH, MsgModel1, MsgModel2, MsgModel3, model1_map)
            print(f'Recovered: "{recovered_text}"')
            if recovered_text == inputMessage:
                print("Success: Decompressed text matches input.")
            else:
                print("Error: Decompressed text does not match input.")
        except Exception as e:
            print(f"Decompression failed with error: {e}")
        # ------------------------------


else:
    # This block runs if compression_possible was set to False in the loop
    payload_bytes = len(payLoad) # payLoad was already set in the loop
    
    print(f"Compression Failed. Character '{failing_char}' not in model.")
    print(f"Payload (UTF-8) ({payload_bytes} / {payload_bytes * 8}): {payLoad}")



    