#!/usr/bin/env python3

import sys
import re # Added for desimplify_links

def toASCII(bitstring):
    """
    Converts a bitstring into a byte payload using the new logic.
    The payload format is:
    [1 byte: valid_bits_in_last_byte] + [N bytes: data]
    """
    bit_len = len(bitstring)
    
    # কেস ১: যদি ইনপুট স্ট্রিং খালি থাকে
    if bit_len == 0:
        # হেডার 0 মানে এটি একটি খালি স্ট্রিং
        return bytes([0])

    # কেস ২: ইনপুটে ডেটা আছে
    
    # কতগুলো প্যাডিং বিট দরকার?
    padding_bits = (8 - (bit_len % 8)) % 8
    
    # শেষ বাইটে কতগুলো আসল (valid) বিট আছে?
    lastByte_firstValidBits = 8 - padding_bits
    
    padded_len = bit_len + padding_bits
    bitstring_padded = bitstring.ljust(padded_len, '0')
    
    # প্যাডেড স্ট্রিংকে বাইটে রূপান্তর করুন
    num_bytes = int(bitstring_padded, 2).to_bytes(padded_len // 8, 'big')
    
    # 1-বাইটের হেডার (যেখানে 1-8 পর্যন্ত মান থাকতে পারে)
    header = bytes([lastByte_firstValidBits])
    
    return header + num_bytes

def fromASCII(payload):
    """
    Reverses the new toASCII process.
    Reads the 1-byte header (valid_bits_in_last_byte)
    and extracts the exact bitstring.
    """
    if not payload:
        return ""
        
    # হেডার (শেষ বাইটে কতগুলো আসল বিট আছে)
    lastByte_firstValidBits = payload[0]
    num_bytes = payload[1:]
    
    # কেস ১: হেডার 0 মানে এটি একটি খালি স্ট্রিং ছিল
    if lastByte_firstValidBits == 0:
        return ""
        
    # কেস ২: ডেটা আছে
    if not num_bytes:
        return ""
        
    padded_len = len(num_bytes) * 8
    num = int.from_bytes(num_bytes, 'big')
    bitstring_padded = format(num, f'0{padded_len}b')
    
    # কতগুলো প্যাডিং বিট ছিল তা হিসাব করুন
    padding_bits = 8 - lastByte_firstValidBits
    
    # আসল বিটের দৈর্ঘ্য
    original_bit_len = padded_len - padding_bits
    
    # আসল বিটস্ট্রিং ফেরত দিন
    return bitstring_padded[:original_bit_len]

# ==========================================================
# Helper Functions (Copied from all_input_compress.py)
# ==========================================================

def longest_common_prefix(strs):
    """
    Helper function for simplify_links.
    Finds the longest common prefix string amongst a sequence of strings.
    """
    if not strs:
        return ""
    min_len = min(len(s) for s in strs)
    prefix = ""
    for i in range(min_len):
        ch = strs[0][i]
        if all(s[i] == ch for s in strs):
            prefix += ch
        else:
            break
    return prefix

def simplify_links(input_str):
    """
    Simplifies a block of text links into a compact, single-line string.
    Groups by domain and uses LCP (Longest Common Prefix) for paths.
    """
    links = [l.strip() for l in input_str.strip().splitlines() if l.strip()]
    domain_dict, order = {}, []
    for link in links:
        proto = ""
        if link.startswith("https://"):
            proto, link = "https://", link[8:]
        elif link.startswith("http://"):
            proto, link = "http://", link[7:]
        
        if '/' in link:
            domain, path = link.split('/', 1)
        else:
            domain, path = link, ""
            
        if domain not in domain_dict:
            order.append(domain)
            domain_dict[domain] = []
        domain_dict[domain].append((path, proto))
    
    res = []
    for domain in order:
        pp = domain_dict[domain]
        paths = [p for p, _ in pp]
        protos = [pr for _, pr in pp]
        
        # Check for http:// prefix (h:)
        proto_marker = "h:" if any(p.startswith("http://") for p in protos) else ""

        if not paths or all(p == "" for p in paths):
            res.append(f"{proto_marker}{domain}<>")
            continue
            
        lcp = longest_common_prefix(paths)
        sfx = [p[len(lcp):] for p in paths]
        
        if lcp:
            # যদি একটি মাত্র লিঙ্ক থাকে, sfx = [''] হবে
            # এটি "domain/path<>" তৈরি করবে
            res.append(f"{proto_marker}{domain}/{lcp}<{ '|'.join(sfx) }>")
        else:
            res.append(f"{proto_marker}{domain}<{ '|'.join(paths) }>")
            
    return "".join(res)

# --- [FIXED] desimplify_links Function ---
def desimplify_links(simplified):
    """
    (Copied from all_input_compress.py and FIXED)
    Convert simplified link string back to multi-line https:// links.
    """
    groups = re.findall(r'([^<>]+)<([^>]*)>', simplified)
    output_links = []
    # 'domain' কে 'domain_part' নাম দেওয়া হলো বোঝার সুবিধার জন্য
    for domain_part, inner in groups:
        proto = "https://"
        if domain_part.startswith("h:"):
            domain_part = domain_part[2:]
            proto = "http://"
        
        # কেস ১: <> এর ভেতর খালি (e.g., "h:okk.com<>" or "domain/path/file.mp4<>")
        if not inner.strip():
            # সম্পূর্ণ domain_part-টিই লিঙ্ক
            link = f"{proto}{domain_part}"
            link = link.replace(":/", "://") # http:// র জন্য
            output_links.append(link)
            continue

        # কেস ২: <> এর ভেতর suffix আছে (e.g., "google.com/product/pic<1.jpg|2.jpg>")
        # এখন domain_part কে ডোমেইন এবং পাথ-এ ভাগ করুন
        if "/" in domain_part:
            domain, pre = domain_part.split("/", 1)
            if pre:
                pre += "/"
        else:
            domain, pre = domain_part, ""
            
        parts = inner.split("|")
        for p in parts:
            link = f"{proto}{domain}/{pre}{p}".replace("//", "/")
            link = link.replace(":/", "://")
            output_links.append(link)
    return "\n".join(output_links)


# ==========================================================
# Main Compression Script
# ==========================================================

# --- Define Models (Must match all_input_compress.py) ---
linkModel1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345<>|./*"
linkModel2 = "6789:-_$&+,;=%~?"

# --- Define Bit Lengths ---
BIT_LENGTH_M1 = 6
BIT_LENGTH_M2 = 4

# --- Create lookup maps (For Compression) ---
model1_map = {char: i for i, char in enumerate(linkModel1)}
model2_map = {char: i for i, char in enumerate(linkModel2)}

# --- NEW: Create reverse lookup maps (For Decompression) ---
rev_model1_map = {format(i, f'0{BIT_LENGTH_M1}b'): char for char, i in model1_map.items()}
rev_model2_map = {format(i, f'0{BIT_LENGTH_M2}b'): char for char, i in model2_map.items()}

# --- Define the marker ---
try:
    marker_to_m2_bits = format(model1_map['*'], f'0{BIT_LENGTH_M1}b')
except KeyError:
    print("Error: Marker '*' not found in linkModel1. Exiting.", file=sys.stderr)
    sys.exit(1)


# --- (Copied as requested) Decompression Maps & Function ---
rev_map6 = {f"{i:06b}": c for i, c in enumerate(linkModel1)}
rev_map4 = {f"{i:04b}": c for i, c in enumerate(linkModel2)}

def decompress_link(bits):
    """
    Decompress function from all_input_compress.py.
    (Not used by this script's main logic)
    """
    i, out = 0, ""
    while i < len(bits):
        if bits[i] == "*":
            out += rev_map4.get(bits[i+1:i+5], "")
            i += 5
        else:
            out += rev_map6.get(bits[i:i+6], "")
            i += 6
    return out
# --- End of copied decompression functions ---

# --- NEW: Decompressor for *this* script's logic ---
def decompress_bitstring(bitstring):
    """
    Reverses this script's compression loop (model1 + model2 w/ marker).
    """
    result = ""
    i = 0
    while i < len(bitstring):
        # Check if we have enough bits for a model1 char
        if i + BIT_LENGTH_M1 > len(bitstring):
            break # Not enough bits left
            
        bits_m1 = bitstring[i : i + BIT_LENGTH_M1]
        
        if bits_m1 == marker_to_m2_bits:
            # It's a marker, switch to model 2
            i += BIT_LENGTH_M1
            
            # Check if we have enough bits for a model2 char
            if i + BIT_LENGTH_M2 > len(bitstring):
                break # Not enough bits left
                
            bits_m2 = bitstring[i : i + BIT_LENGTH_M2]
            char = rev_model2_map.get(bits_m2, '?') # '?' on error
            result += char
            i += BIT_LENGTH_M2
            
        else:
            # It's a standard model 1 char
            char = rev_model1_map.get(bits_m1, '?') # '?' on error
            result += char
            i += BIT_LENGTH_M1
            
    return result


# --- Define Input Data ---
inputImageURL = """http://okk.com
https://google.com/product/image/pic1.jpg
https://facebook.com/product/chat/pic22.jpg
https://google.com/product/image/pic2.jpg
https://linkedin.com/person/pic_2.png
https://google.com/product/image/pic3.png
https://facebook.com/product/post/pic14.jpg
https://web.linkedin.com/person/pic1.png
http://mywebsite.com/s/fdee23sd
sub.yourwebsite.com/fsdfasdfasdf
https://example.org/documents/report.png
https://cdn.example.io/assets/video/intro.webm"""

# --- *** NEW STEP: Simplify links before compressing *** ---
print("--- Simplifying Links ---")
simplified_ImageURL = simplify_links(inputImageURL)
print(f"Simplified Image URLs: {simplified_ImageURL}")
print("-------------------------")

# Combine *simplified* inputs and strip whitespace
inputMessage = simplified_ImageURL.strip()


# --- Initialize variables ---
compressed_bitstring = ""
compression_possible = True
failing_char = ''
payLoad = b""

# --- Calculate and print Input stats first ---
input_chars = len(inputMessage)
input_bytes_utf8 = len(inputMessage.encode('utf-8'))
print(f'Input ({input_chars} chars / {input_bytes_utf8} bytes): "{inputMessage}"')


# --- Compression Loop (Same as before) ---
for char in inputMessage:
    if char in model1_map:
        index = model1_map[char]
        compressed_bitstring += format(index, f'0{BIT_LENGTH_M1}b')
    elif char in model2_map:
        compressed_bitstring += marker_to_m2_bits
        index = model2_map[char]
        compressed_bitstring += format(index, f'0{BIT_LENGTH_M2}b')
    else:
        payLoad = f"[m>{inputMessage}".encode('utf-8')
        compression_possible = False
        failing_char = char
        break # Exit the loop

# --- Post-Loop Logic (Efficiency check removed) ---
if compression_possible:
    # এই ফাংশনটি এখন আপনার নতুন লজিক ব্যবহার করবে
    compressed_payLoad = toASCII(compressed_bitstring)
    
    # ALWAYS use the compressed version, regardless of efficiency.
    # Add the [m> prefix.
    payLoad = b"[m>" + compressed_payLoad
    payload_bytes = len(payLoad)
    
    print(f"Compression successful.")
    print(f"Payload ({payload_bytes} bytes / {payload_bytes * 8} bits): "
          f"(Original bits: {len(compressed_bitstring)}. "
          # হেডারটি এখন 'valid_bits_in_last_byte'
          f"Byte count includes 1-byte length header + data padded to 8 bits + 3-byte prefix.)")
    print(f"Payload (bytes): {payLoad}")

else:
    # This block runs if compression_possible was False
    payload_bytes = len(payLoad) # payLoad was already set in the loop
    
    print(f"Compression Failed. Character '{failing_char}' not in model.")
    print(f"Payload (UTF-8) ({payload_bytes} bytes / {payload_bytes * 8} bits): {payLoad}")


# ==========================================================
# NEW: Decompression & De-simplification Test
# ==========================================================
print("\n=== Decompression & De-simplification Test ===")

if compression_possible:
    print("Payload was compressed. Reversing process...")
    
    # 1. Remove [m> prefix
    if not payLoad.startswith(b'[m>'):
        print("Error: Payload missing [m> prefix.")
        # Handle error or exit if needed
        compressed_data = payLoad
    else:
        compressed_data = payLoad[3:]
    
    # 2. Decompress from bytes -> bitstring
    # এই ফাংশনটি এখন আপনার নতুন লজিক ব্যবহার করবে
    recovered_bitstring = fromASCII(compressed_data)
    print(f"Recovered bitstring (len {len(recovered_bitstring)})")

    # 3. Decompress from bitstring -> simplified string
    recovered_simplified_string = decompress_bitstring(recovered_bitstring)
    print(f"Recovered simplified string: {recovered_simplified_string}")

    # 4. De-simplify string -> final links
    # এই ফাংশনটি এখন ফিক্সড লজিক ব্যবহার করবে
    final_links = desimplify_links(recovered_simplified_string)
    print("\n--- Final Recovered Links ---")
    print(final_links)
    
    # 5. Check if recovered string matches original simplified string
    if recovered_simplified_string == inputMessage:
        print("\nVerification: SUCCESS. Recovered string matches simplified input.")
    else:
        print("\nVerification: FAILED. Recovered string does not match.")
        print(f"Expected: {inputMessage}")
        print(f"Got: {recovered_simplified_string}")

else:
    print("Payload was not compressed (fallback UTF-8). Skipping decompression test.")
    print(f"Original Simplified Input: {inputMessage}")