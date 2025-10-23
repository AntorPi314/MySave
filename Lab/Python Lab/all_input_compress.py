import re

# ==========================
# Message Models (5-bit each)
# ==========================
MsgModel1 = "abcdefghijklmnopqrstuvwxyz,\n /#*"
MsgModel2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.?!@#*"
MsgModel3 = "0123456789-_=&%+;'()[]{}\"|:\\<^~>"

msg_map1 = {c: f"{i:05b}" for i, c in enumerate(MsgModel1)}
msg_rev1 = {v: k for k, v in msg_map1.items()}

msg_map2 = {c: f"{i:05b}" for i, c in enumerate(MsgModel2)}
msg_rev2 = {v: k for k, v in msg_map2.items()}

msg_map3 = {c: f"{i:05b}" for i, c in enumerate(MsgModel3)}
msg_rev3 = {v: k for k, v in msg_map3.items()}

# ==========================
# Link Models
# ==========================
linkModel1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/*"
linkModel2 = "<>|.:-_$&+,;=%~?"

map6 = {c: f"{i:06b}" for i, c in enumerate(linkModel1)}
rev_map6 = {v: k for k, v in map6.items()}

map4 = {c: f"{i:04b}" for i, c in enumerate(linkModel2)}
rev_map4 = {v: k for k, v in map4.items()}

# ==========================
# Inputs
# ==========================
inputMessage = """
Hi, how are you? this my image and video, and this is my link, আমি achi,,
"""

inputImageURL = """
http://okk.com
https://google.com/product/image/pic1.jpg
https://facebook.com/product/chat/pic22.jpg
https://google.com/product/image/pic2.jpg
https://linkedin.com/person/pic_2.mp4
https://google.com/product/image/pic3.png
https://facebook.com/product/post/pic14.jpg
https://web.linkedin.com/person/pic1.mp4
http://mywebsite.com/s/fdee23sd
sub.yourwebsite.com/fsdfasdfasdf
"""

inputVideoURL = """
https://google.com/product/vid/v1.jpg
https://facebook.com/product/chat/v22.jpg
https://google.com/product/vid/v2.jpg
https://linkedin.com/person/vid2.mp4
https://google.com/product/vid/vid3.png
https://facebook.com/product/post/vid14.jpg
https://web.linkedin.com/person/vid1.mp4
mywebsite.com/s/fdee23sd
sub.yourwebsite.com/fsdfasdfasdf
"""

# ==========================
# Message Compression / Decompression
# ==========================
def compress_message(msg):
    bits = ""
    for c in msg:
        if c in msg_map1:
            bits += msg_map1[c]
        elif c in msg_map2:
            bits += msg_map1['#'] + msg_map2[c]
        elif c in msg_map3:
            bits += msg_map1['*'] + msg_map3[c]
        else:
            return None  # out-of-model char (e.g., Bangla)
    return bits

def decompress_message(bits):
    i = 0
    result = ""
    while i < len(bits):
        block = bits[i:i+5]
        if len(block) < 5:
            break
        ch = msg_rev1.get(block)
        if ch == '#':
            i += 5
            result += msg_rev2.get(bits[i:i+5], '')
        elif ch == '*':
            i += 5
            result += msg_rev3.get(bits[i:i+5], '')
        else:
            result += ch or ''
        i += 5
    return result

# ==========================
# Helper: Longest Common Prefix
# ==========================
def longest_common_prefix(strs):
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

# ==========================
# Simplify Links
# ==========================
def simplify_links(input_str):
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
        if not paths or all(p == "" for p in paths):
            proto_marker = "h:" if any(p.startswith("http://") for p in protos) else ""
            res.append(f"{proto_marker}{domain}<>")
            continue
        lcp = longest_common_prefix(paths)
        sfx = [p[len(lcp):] for p in paths]
        if lcp:
            res.append(f"{domain}/{lcp}<{ '|'.join(sfx) }>")
        else:
            res.append(f"{domain}<{ '|'.join(paths) }>")
    return "".join(res)

# ==========================
# Compress / Decompress Links
# ==========================
def compress_link(s):
    bits = ""
    for c in s:
        if c in map6:
            bits += map6[c]
        elif c in map4:
            bits += "*" + map4[c]
        else:
            raise ValueError(f"Character '{c}' not supported in link model")
    return bits

def decompress_link(bits):
    i, out = 0, ""
    while i < len(bits):
        if bits[i] == "*":
            out += rev_map4.get(bits[i+1:i+5], "")
            i += 5
        else:
            out += rev_map6.get(bits[i:i+6], "")
            i += 6
    return out

# ==========================
# De-Simplify Links
# ==========================
def desimplify_links(simplified):
    """
    Convert simplified link string back to multi-line https:// links.
    """
    groups = re.findall(r'([^<>]+)<([^>]*)>', simplified)
    output_links = []
    for domain, inner in groups:
        proto = "https://"
        if domain.startswith("h:"):
            domain = domain[2:]
            proto = "http://"
        if "/" in domain:
            domain, pre = domain.split("/", 1)
            if pre:
                pre += "/"
        else:
            pre = ""
        if not inner.strip():
            output_links.append(f"{proto}{domain}")
            continue
        parts = inner.split("|")
        for p in parts:
            link = f"{proto}{domain}/{pre}{p}".replace("//", "/")
            link = link.replace(":/", "://")
            output_links.append(link)
    return "\n".join(output_links)

# ==========================
# Run Compression
# ==========================
msg_bits = compress_message(inputMessage)
if msg_bits is not None:
    msg_ok = (decompress_message(msg_bits) == inputMessage)
    compressed_msg_bits = msg_bits if msg_ok else None
else:
    compressed_msg_bits = None

simplifyImageLinks = simplify_links(inputImageURL)
simplifyVideoLinks = simplify_links(inputVideoURL)
compressed_bits_image = compress_link(simplifyImageLinks)
compressed_bits_video = compress_link(simplifyVideoLinks)

# ==========================
# Bit Comparison Table
# ==========================
def calc_bits(name, original, simplified, compressed_bits):
    o_bits = len(original.strip()) * 8
    s_bits = len(simplified.strip()) * 8
    c_bits = len(compressed_bits)
    o_chars = len(original.strip())
    s_chars = len(simplified.strip())
    c_chars = round(c_bits / 8)
    print(f"{name:<15} - {o_bits:5} bits  >  {s_bits:5} bits  >  {c_bits:5} bits    (Char - {o_chars} > {s_chars} > {c_chars})")

print("\n=== Bit Comparison Table ===")
calc_bits("inputMessage", inputMessage, inputMessage, compressed_msg_bits or "")
calc_bits("inputImageURL", inputImageURL, simplifyImageLinks, compressed_bits_image)
calc_bits("inputVideoURL", inputVideoURL, simplifyVideoLinks, compressed_bits_video)

total_input_bits = len(inputMessage.strip())*8 + len(inputImageURL.strip())*8 + len(inputVideoURL.strip())*8
total_simplified_bits = len(inputMessage.strip())*8 + len(simplifyImageLinks.strip())*8 + len(simplifyVideoLinks.strip())*8
total_compressed_bits = (len(compressed_msg_bits or inputMessage.strip())*8) + len(compressed_bits_image) + len(compressed_bits_video)
print(f"\n{'allReadyData':<15} - {total_input_bits:5} bits  >  {total_simplified_bits:5} bits  >  {total_compressed_bits:5} bits    (Char - {round(total_input_bits/8)} > {round(total_simplified_bits/8)} > {round(total_compressed_bits/8)})")

# ==========================
# Show Simplified Links
# ==========================
print("\n=== Simplified Image Links ===")
print(simplifyImageLinks)
print("\n=== Simplified Video Links ===")
print(simplifyVideoLinks)

# ==========================
# Reverse / Decode Test
# ==========================
rev_msg = decompress_message(compressed_msg_bits) if compressed_msg_bits else inputMessage
rev_img = decompress_link(compressed_bits_image)
rev_vid = decompress_link(compressed_bits_video)

print("\n=== Reverse Check (Decoded) ===")
print("Recovered Message:\n", rev_msg.strip())
print("\nRecovered Image Links:\n", rev_img.strip())
print("\nRecovered Video Links:\n", rev_vid.strip())

# ==========================
# De-Simplify Final Output
# ==========================
print("\n=== De-Simplify Output ===")

print("\ninputMessage >> ")
print(rev_msg.strip(), "\n")

print("inputImageURL >> ")
print(desimplify_links(rev_img), "\n")

print("inputVideoURL >> ")
print(desimplify_links(rev_vid))
