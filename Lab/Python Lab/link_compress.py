import re

# ==========================
# Models
# ==========================
linkModel1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/*"
linkModel2 = "<>|-._:$&+,;=%~?"

map6 = {c: f"{i:06b}" for i, c in enumerate(linkModel1)}
rev_map6 = {v: k for k, v in map6.items()}

map4 = {c: f"{i:04b}" for i, c in enumerate(linkModel2)}
rev_map4 = {v: k for k, v in map4.items()}

# ==========================
# Input Links
# ==========================
inputLinks = """

https://google.com/product/image/pic1.jpg
https://facebook.com/product/chat/pic22.jpg
https://google.com/product/image/pic2.jpg
https://linkedin.com/person/vid2.mp4
https://google.com/product/image/pic3.png
https://facebook.com/product/post/pic14.jpg
https://web.linkedin.com/person/vid1.mp4
mywebsite.com/s/fdee23sd
sub.yourwebsite.com/fsdfasdfasdf

"""

# ==========================
# Helper: Longest Common Prefix
# ==========================
def longest_common_prefix(strs):
    if not strs:
        return ""
    min_len = min(len(s) for s in strs)
    prefix = ""
    for i in range(min_len):
        char = strs[0][i]
        if all(s[i] == char for s in strs):
            prefix += char
        else:
            break
    return prefix

# ==========================
# Simplify Links
# ==========================
def simplify_links(input_str):
    links = [l.strip() for l in input_str.strip().splitlines() if l.strip()]
    domain_dict = {}

    for link in links:
        # Remove scheme
        if link.startswith("https://"):
            url = link[8:]
        elif link.startswith("http://"):
            url = link[7:]
        else:
            url = link

        # Split domain / path
        if '/' in url:
            domain, path = url.split('/', 1)
        else:
            domain, path = url, ""

        domain_dict.setdefault(domain, []).append(path)

    # Build simplified string
    result = ""
    for domain, paths in domain_dict.items():
        if not paths or all(p == "" for p in paths):
            result += domain
            continue
        # Find longest common prefix of paths
        lcp = longest_common_prefix(paths)
        suffixes = [p[len(lcp):] for p in paths]
        if lcp:
            result += f"{domain}/{lcp}<{ '|'.join(suffixes) }>"
        else:
            result += f"{domain}<{ '|'.join(paths) }>"
    return result

simplifyLinks = simplify_links(inputLinks)

# ==========================
# Compression / Decompression
# ==========================
def compress_link(s):
    bits = ""
    for c in s:
        if c in map6:
            bits += map6[c]
        elif c in map4:
            bits += "*" + map4[c]
        else:
            raise ValueError(f"Character '{c}' not in any model")
    return bits

def decompress_link(bits):
    i = 0
    result = ""
    while i < len(bits):
        if bits[i] == "*":
            code = bits[i+1:i+5]
            result += rev_map4[code]
            i += 5
        else:
            code = bits[i:i+6]
            result += rev_map6[code]
            i += 6
    return result

# ==========================
# Recover full links
# ==========================
def recover_links(s):
    pattern = r'([^<>]+)(<[^<>]+>)?'
    matches = re.findall(pattern, s)
    links = []
    for base, group in matches:
        base = base.strip()
        if not base:
            continue
        if group:
            items = group[1:-1].split('|')
            for item in items:
                if base.endswith('/') or item.startswith('/'):
                    links.append(f"{base}{item}")
                else:
                    links.append(f"{base}/{item}")
        else:
            links.append(base)
    return links

# ==========================
# Convert bits to ASCII string
# ==========================
def bits_to_ascii(bits):
    # Pad bits to multiple of 8
    extra = (8 - len(bits)%8) % 8
    bits += "0"*extra
    chars = [chr(int(bits[i:i+8],2)) for i in range(0,len(bits),8)]
    return "".join(chars)

# ==========================
# Run
# ==========================
compressed_bits = compress_link(simplifyLinks)
decompressed = decompress_link(compressed_bits)
recovery_successful = decompressed == simplifyLinks

original_bits_len = len(inputLinks.strip())*8
simplified_bits_len = len(simplifyLinks)*8
compressed_bits_len = len(compressed_bits)

print("Simplified Links:\n", simplifyLinks)
print("\nBits before simplifyLinks (inputLinks):", original_bits_len, f"(Char > {original_bits_len/8})")
print("Bits after simplifyLinks:", simplified_bits_len, f"(Char > {simplified_bits_len/8})")
print("Bits after compression:", compressed_bits_len, f"(Char > {compressed_bits_len/8})")
print("Recovery successful:", recovery_successful)

if recovery_successful:
    recovered_links = recover_links(decompressed)
    print("\nRecovered full links:")
    for link in recovered_links:
        print(link)

    ascii_str = bits_to_ascii(compressed_bits)
    print("\nCompressed bits as ASCII string:\n", ascii_str)
