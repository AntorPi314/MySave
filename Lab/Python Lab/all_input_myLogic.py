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

# Pre-compiled regex
LINK_PATTERN = re.compile(r'([^<>]+)<([^>]*)>')

# ==========================
# Inputs
# ==========================
inputMessage = """
Hi, how are you? this my image and video, and this is my link,  achi,, sflfas fjsadlf sadfljasdlfjasd fasjdlfasdj fasldfjasdlfjsd ffsdjl
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
# Message Compression / Decompression (OPTIMIZED)
# ==========================
def compress_message(msg):
    """Optimized with pre-cached escape sequences and list concatenation"""
    bits = []
    escape_hash = msg_map1['#']
    escape_star = msg_map1['*']
    
    for c in msg:
        if c in msg_map1:
            bits.append(msg_map1[c])
        elif c in msg_map2:
            bits.append(escape_hash)
            bits.append(msg_map2[c])
        elif c in msg_map3:
            bits.append(escape_star)
            bits.append(msg_map3[c])
        else:
            return None  # out-of-model char
    return ''.join(bits)

def decompress_message(bits):
    """Optimized with list building and bounds checking"""
    result = []
    i = 0
    bits_len = len(bits)
    
    while i < bits_len:
        if i + 5 > bits_len:
            break
        
        block = bits[i:i+5]
        ch = msg_rev1.get(block)
        
        if ch == '#':
            if i + 10 <= bits_len:
                result.append(msg_rev2.get(bits[i+5:i+10], ''))
                i += 10
            else:
                break
        elif ch == '*':
            if i + 10 <= bits_len:
                result.append(msg_rev3.get(bits[i+5:i+10], ''))
                i += 10
            else:
                break
        else:
            result.append(ch or '')
            i += 5
    
    return ''.join(result)

# ==========================
# Helper: Longest Common Prefix (OPTIMIZED)
# ==========================
def longest_common_prefix(strs):
    """Optimized with early exit and zip"""
    if not strs:
        return ""
    if len(strs) == 1:
        return strs[0]
    
    prefix = []
    for chars in zip(*strs):
        if len(set(chars)) == 1:
            prefix.append(chars[0])
        else:
            break
    return ''.join(prefix)

# ==========================
# Simplify Links (OPTIMIZED)
# ==========================
def simplify_links(input_str):
    """Optimized with str.partition and reduced string operations"""
    links = [l.strip() for l in input_str.strip().splitlines() if l.strip()]
    domain_dict = {}
    order = []
    
    for link in links:
        # Efficient protocol handling
        if link.startswith("https://"):
            proto, rest = "https://", link[8:]
        elif link.startswith("http://"):
            proto, rest = "http://", link[7:]
        else:
            proto, rest = "https://", link
        
        # Use partition for single-pass split
        domain, _, path = rest.partition('/')
        
        if domain not in domain_dict:
            order.append(domain)
            domain_dict[domain] = []
        domain_dict[domain].append((path, proto))
    
    # Build result
    res = []
    for domain in order:
        pp = domain_dict[domain]
        paths = [p for p, _ in pp]
        protos = [pr for _, pr in pp]
        
        # Handle empty paths
        if not paths or all(not p for p in paths):
            proto_marker = "h:" if any(pr == "http://" for pr in protos) else ""
            res.append(f"{proto_marker}{domain}<>")
            continue
        
        # Find common prefix
        lcp = longest_common_prefix(paths)
        if lcp:
            sfx = [p[len(lcp):] for p in paths]
            res.append(f"{domain}/{lcp}<{'|'.join(sfx)}>")
        else:
            res.append(f"{domain}<{'|'.join(paths)}>")
    
    return ''.join(res)

# ==========================
# Compress / Decompress Links (OPTIMIZED)
# ==========================
def compress_link(s):
    """Optimized with list building"""
    bits = []
    for c in s:
        if c in map6:
            bits.append(map6[c])
        elif c in map4:
            bits.append("*")
            bits.append(map4[c])
        else:
            raise ValueError(f"Character '{c}' not supported in link model")
    return ''.join(bits)

def decompress_link(bits):
    """Optimized with reduced string slicing"""
    out = []
    i = 0
    bits_len = len(bits)
    
    while i < bits_len:
        if bits[i] == "*":
            if i + 5 <= bits_len:
                out.append(rev_map4.get(bits[i+1:i+5], ""))
                i += 5
            else:
                break
        else:
            if i + 6 <= bits_len:
                out.append(rev_map6.get(bits[i:i+6], ""))
                i += 6
            else:
                break
    
    return ''.join(out)

# ==========================
# De-Simplify Links (OPTIMIZED)
# ==========================
def desimplify_links(simplified):
    """Optimized with pre-compiled regex and reduced string ops"""
    groups = LINK_PATTERN.findall(simplified)
    output_links = []
    
    for domain, inner in groups:
        proto = "https://"
        if domain.startswith("h:"):
            domain = domain[2:]
            proto = "http://"
        
        # Use partition for efficiency
        domain_part, sep, pre = domain.partition("/")
        if sep:
            pre += "/"
        else:
            pre = ""
            domain_part = domain
        
        if not inner.strip():
            output_links.append(f"{proto}{domain_part}")
            continue
        
        parts = inner.split("|")
        for p in parts:
            # Build link with minimal operations
            if pre:
                link = f"{proto}{domain_part}/{pre}{p}"
            else:
                link = f"{proto}{domain_part}/{p}"
            # Fix double slashes
            link = link.replace("//", "/").replace(":/", "://")
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





def build_payload(message, image_urls, video_urls):
    """Build payload with new marker system"""
    payload = []
    
    # Handle message
    if message and message.strip():
        msg_bits = compress_message(message)
        if msg_bits is not None:
            # Successfully compressed - NO marker
            payload.append(msg_bits)
        else:
            # Unicode/emoji - add [u> marker
            payload.append("[u>" + message)
    
    # Handle images
    if image_urls and image_urls.strip():
        simplified = simplify_links(image_urls)
        compressed = compress_link(simplified)
        payload.append("[m>" + compressed)
    
    # Handle videos
    if video_urls and video_urls.strip():
        simplified = simplify_links(video_urls)
        compressed = compress_link(simplified)
        payload.append("[v>" + compressed)
    
    return ''.join(payload)

def parse_payload(payload):
    """Parse payload with new markers"""
    result = {"message": "", "imageUrls": "", "videoUrls": ""}
    
    if not payload:
        return result
    
    idx = 0
    
    # Check for message
    if payload.startswith("[u>"):
        # Unicode message
        idx = 3
        next_marker = find_next_marker(payload, idx)
        if next_marker != -1:
            result["message"] = payload[idx:next_marker]
            idx = next_marker
        else:
            result["message"] = payload[idx:]
            return result
    elif payload.startswith("[m>") or payload.startswith("[v>"):
        pass  # No message
    else:
        # Compressed message
        next_marker = find_next_marker(payload, idx)
        if next_marker != -1:
            result["message"] = decompress_message(payload[idx:next_marker])
            idx = next_marker
        else:
            result["message"] = decompress_message(payload[idx:])
            return result
    
    # Check for images
    if idx < len(payload) and payload[idx:].startswith("[m>"):
        idx += 3
        next_marker = find_next_marker(payload, idx)
        if next_marker != -1:
            compressed = payload[idx:next_marker]
            simplified = decompress_link(compressed)
            result["imageUrls"] = desimplify_links(simplified)
            idx = next_marker
        else:
            compressed = payload[idx:]
            simplified = decompress_link(compressed)
            result["imageUrls"] = desimplify_links(simplified)
            return result
    
    # Check for videos
    if idx < len(payload) and payload[idx:].startswith("[v>"):
        idx += 3
        compressed = payload[idx:]
        simplified = decompress_link(compressed)
        result["videoUrls"] = desimplify_links(simplified)
    
    return result

def find_next_marker(s, start_idx):
    """Find next [m> or [v> marker"""
    pos_m = s.find("[m>", start_idx)
    pos_v = s.find("[v>", start_idx)
    
    if pos_m == -1:
        return pos_v
    if pos_v == -1:
        return pos_m
    return min(pos_m, pos_v)

# Test the new system
print("\n=== Testing New Payload System ===")
payload = build_payload(inputMessage, inputImageURL, inputVideoURL)
print(f"Final Payload Length: {len(payload)} characters")
print(f"Final Payload Bits: {len(payload) * 8} bits")

parsed = parse_payload(payload)
print("\n=== Parsed Result ===")
print("Message:", parsed["message"][:50], "...")
print("Images:", parsed["imageUrls"][:100], "...")
print("Videos:", parsed["videoUrls"][:100], "...")