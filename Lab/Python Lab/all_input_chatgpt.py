
import re
import base64

# ==========================
# Message Models (5-bit encoding)
# ==========================
MsgModel1 = "abcdefghijklmnopqrstuvwxyz,\n /#*"
msg_map1 = {c: f"{i:05b}" for i, c in enumerate(MsgModel1)}
msg_rev1 = {v: k for k, v in msg_map1.items()}

MsgModel2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.?!@"
msg_map2 = {c: f"{i:05b}" for i, c in enumerate(MsgModel2)}
msg_rev2 = {v: k for k, v in msg_map2.items()}

MsgModel3 = "0123456789-_=&%+;'()[]{}\"|:\\<^~>"
msg_map3 = {c: f"{i:05b}" for i, c in enumerate(MsgModel3)}
msg_rev3 = {v: k for k, v in msg_map3.items()}

# ==========================
# Link Models (6-bit and 4-bit)
# ==========================
linkModel1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/"
map6 = {c: f"{i:06b}" for i, c in enumerate(linkModel1)}
rev_map6 = {v: k for k, v in map6.items()}

linkModel2 = "<>|.:-_$&+,;=%~?*"
map4 = {c: f"{i:04b}" for i, c in enumerate(linkModel2)}
rev_map4 = {v: k for k, v in map4.items()}

# ==========================
# URL Pattern Dictionary
# ==========================
URL_PATTERNS = {
    'https://': '§H§', 'http://': '§h§', 'www.': '§W§', '.com': '§C§', '.org': '§O§',
    '.net': '§N§', '.jpg': '§J§', '.png': '§P§', '.mp4': '§M§', '.gif': '§G§',
    '.webm': '§V§', '.pdf': '§D§', 'product/': '§1§', 'image/': '§2§', 'video/': '§3§',
    'chat/': '§4§', 'person/': '§5§', 'post/': '§6§',
}
PATTERN_REV = {v: k for k, v in URL_PATTERNS.items()}

PATTERN_MAP = {
    '§H§': 'µ', '§h§': '¶', '§W§': '·', '§C§': '¸', '§O§': '¹', '§N§': 'º',
    '§J§': '»', '§P§': '¼', '§M§': '½', '§G§': '¾', '§V§': '¿', '§D§': 'À',
    '§1§': 'Á', '§2§': 'Â', '§3§': 'Ã', '§4§': 'Ä', '§5§': 'Å', '§6§': 'Æ',
}
PATTERN_REV_MAP = {v: k for k, v in PATTERN_MAP.items()}
PATTERN_ID_TO_MARKER = list(PATTERN_MAP.keys())

# ==========================
# Message Compression & Decompression
# ==========================
def compress_message(msg):
    bits = ""
    for c in msg:
        if c in msg_map1: bits += msg_map1[c]
        elif c in msg_map2: bits += msg_map1['#'] + msg_map2[c]
        elif c in msg_map3: bits += msg_map1['*'] + msg_map3[c]
        else:
            utf8_bytes = c.encode('utf-8')
            bits += "11111"
            bits += f"{len(utf8_bytes):08b}"
            for byte in utf8_bytes: bits += f"{byte:08b}"
    return bits

def decompress_message(bits):
    i = 0
    result = ""
    while i < len(bits):
        if i + 5 > len(bits): break
        block5 = bits[i:i+5]
        if block5 == "11111":
            i += 5
            if i + 8 > len(bits): break
            byte_count = int(bits[i:i+8], 2)
            i += 8
            if i + byte_count * 8 > len(bits): break
            utf8_bytes = bytearray()
            for _ in range(byte_count):
                utf8_bytes.append(int(bits[i:i+8], 2))
                i += 8
            try: result += utf8_bytes.decode('utf-8')
            except: pass
        else:
            ch = msg_rev1.get(block5)
            i += 5
            if ch == '#':
                if i + 5 > len(bits): break
                result += msg_rev2.get(bits[i:i+5], '')
                i += 5
            elif ch == '*':
                if i + 5 > len(bits): break
                result += msg_rev3.get(bits[i:i+5], '')
                i += 5
            else: result += ch or ''
    return result

# ==========================
# Link Simplification & De-simplification
# ==========================
def simplify_links_enhanced(input_str):
    links = [l.strip() for l in input_str.strip().splitlines() if l.strip()]
    if not links: return ""
    processed_links = []
    for link in links:
        processed = link
        for pattern, marker in sorted(URL_PATTERNS.items(), key=lambda x: -len(x[0])):
            processed = processed.replace(pattern, PATTERN_MAP[marker])
        processed_links.append(processed)
    domain_dict, order = {}, []
    for link in processed_links:
        proto_marker = ""
        if link.startswith('µ'):
            proto_marker = 'µ'
            link = link[1:]
        elif link.startswith('¶'):
            proto_marker = '¶'
            link = link[1:]
        domain, path = link.split('/', 1) if '/' in link else (link, "")
        group_key = (domain, proto_marker)
        if group_key not in domain_dict:
            order.append(group_key)
            domain_dict[group_key] = []
        domain_dict[group_key].append(path)
    res = []
    for domain, proto_marker in order:
        paths = domain_dict[(domain, proto_marker)]
        if not paths or all(p == "" for p in paths):
            res.append(f"{proto_marker}{domain}<>")
            continue
        lcp = longest_common_prefix(paths)
        sfx = [p[len(lcp):] for p in paths]
        path_part = f"/{lcp}" if lcp else ""
        res.append(f"{proto_marker}{domain}{path_part}<{'|'.join(sfx)}>")
    return "".join(res)

def longest_common_prefix(strs):
    if not strs: return ""
    min_s, max_s = min(strs), max(strs)
    for i, c in enumerate(min_s):
        if c != max_s[i]: return min_s[:i]
    return min_s

def desimplify_links(simplified):
    if not simplified.strip(): return ""
    groups = re.findall(r'([^<>]*?)<([^>]*)>', simplified)
    output_links = []
    for domain_part, inner in groups:
        proto = ""
        if domain_part.startswith("µ"):
            proto = "https://"
            domain_part = domain_part[1:]
        elif domain_part.startswith("¶"):
            proto = "http://"
            domain_part = domain_part[1:]
        domain, pre = domain_part.split("/", 1) if "/" in domain_part else (domain_part, "")
        for char, marker in PATTERN_REV_MAP.items():
            pattern = PATTERN_REV[marker]
            domain = domain.replace(char, pattern)
            pre = pre.replace(char, pattern)
        if not inner and not pre:
            output_links.append(f"{proto}{domain}")
            continue
        paths = inner.split("|") if inner else [""]
        for p in paths:
            for char, marker in PATTERN_REV_MAP.items():
                p = p.replace(char, PATTERN_REV[marker])
            full_path = f"{pre}{p}" if pre and p else pre or p
            link = f"{proto}{domain}" + (f"/{full_path}" if full_path else "")
            if proto: link = proto + link[len(proto):].replace('//', '/')
            output_links.append(link)
    return "\n".join(output_links)

# ==========================
# Link Compression & Decompression
# ==========================
def compress_link(s):
    bits = ""
    SPECIAL_MARKER = "111110"
    SPECIAL_CHAR_FLAG = "11111"
    for c in s:
        if c in PATTERN_REV_MAP:
            pattern_id = PATTERN_ID_TO_MARKER.index(PATTERN_REV_MAP[c])
            bits += SPECIAL_MARKER + f"{pattern_id:05b}"
        elif c in map6: bits += map6[c]
        elif c in map4: bits += SPECIAL_MARKER + SPECIAL_CHAR_FLAG + map4[c]
        else:
            utf8_bytes = c.encode('utf-8')
            bits += "11111111" + f"{len(utf8_bytes):08b}"
            for byte in utf8_bytes: bits += f"{byte:08b}"
    return bits

def decompress_link(bits):
    i = 0
    out = ""
    SPECIAL_MARKER = "111110"
    SPECIAL_CHAR_FLAG = "11111"
    UTF8_MARKER = "11111111"
    while i < len(bits):
        # FIX: Using a robust if/elif/else structure to prevent misinterpretation
        if i + 8 <= len(bits) and bits[i:i+8] == UTF8_MARKER:
            i += 8
            if i + 8 > len(bits): break
            byte_count = int(bits[i:i+8], 2)
            i += 8
            if i + byte_count * 8 > len(bits): break
            utf8_bytes = bytearray()
            for _ in range(byte_count):
                utf8_bytes.append(int(bits[i:i+8], 2))
                i += 8
            try: out += utf8_bytes.decode('utf-8')
            except: pass
        elif i + 6 <= len(bits) and bits[i:i+6] == SPECIAL_MARKER:
            i += 6
            if i + 5 > len(bits): break
            next_5 = bits[i:i+5]
            i += 5
            if next_5 == SPECIAL_CHAR_FLAG:
                if i + 4 > len(bits): break
                out += rev_map4.get(bits[i:i+4], '')
                i += 4
            else:
                pattern_id = int(next_5, 2)
                if pattern_id < len(PATTERN_ID_TO_MARKER):
                    out += PATTERN_MAP[PATTERN_ID_TO_MARKER[pattern_id]]
        elif i + 6 <= len(bits):
            code = bits[i:i+6]
            out += rev_map6.get(code, '')
            i += 6
        else:
            break
    return out

# ==========================
# Main Execution & Display (No changes needed below this line)
# ==========================
# Inputs
inputMessage = """Hi, how are you? this my image and video, and this is my link, আমি 🙂 achi,,
🎉 Testing emoji!"""
inputImageURL = """http://okk.com
https://google.com/product/image/pic1.jpg
https://facebook.com/product/chat/pic22.jpg
https://google.com/product/image/pic2.jpg
https://linkedin.com/person/pic_2.mp4
https://google.com/product/image/pic3.png
https://facebook.com/product/post/pic14.jpg
https://web.linkedin.com/person/pic1.mp4
http://mywebsite.com/s/fdee23sd
sub.yourwebsite.com/fsdfasdfasdf
https://example.org/documents/report.pdf
https://cdn.example.io/assets/video/intro.webm"""
inputVideoURL = """
https://gemini.google.com/app/83d82e8c10ec2247
https://chat.deepseek.com/a/chat/s/704475c5-46ba-47a8-95aa-2f8bc2c6355b
"""

# Run Compression
print("╔" + "═" * 100 + "╗")
print("║" + " " * 28 + "🚀 ENHANCED BLE COMPRESSION SYSTEM 🚀" + " " * 30 + "║")
print("║" + " " * 18 + "✨ Pattern dictionary | Unicode support | Optimized encoding ✨" + " " * 19 + "║")
print("╚" + "═" * 100 + "╝")

compressed_msg_bits = compress_message(inputMessage.strip())
simplifyImageLinks = simplify_links_enhanced(inputImageURL)
simplifyVideoLinks = simplify_links_enhanced(inputVideoURL)
compressed_bits_image = compress_link(simplifyImageLinks)
compressed_bits_video = compress_link(simplifyVideoLinks)

# Display Results
def calc_stats(name, original, simplified, compressed_bits):
    o_bytes_stripped = len(original.strip().encode('utf-8'))
    o_bits = o_bytes_stripped * 8
    s_bytes = len(simplified.encode('utf-8'))
    s_bits = s_bytes * 8
    c_bits = len(compressed_bits)
    c_bytes = (c_bits + 7) // 8
    reduction_final = ((o_bits - c_bits) / o_bits * 100) if o_bits > 0 else 0
    return {'name': name, 'o_bits': o_bits, 's_bits': s_bits, 'c_bits': c_bits, 'o_bytes': o_bytes_stripped, 'c_bytes': c_bytes, 'red_f': reduction_final}

msg_stats = calc_stats("Message", inputMessage, inputMessage, compressed_msg_bits)
img_stats = calc_stats("Image URLs", inputImageURL, simplifyImageLinks, compressed_bits_image)
vid_stats = calc_stats("Video URLs", inputVideoURL, simplifyVideoLinks, compressed_bits_video)

print("\n┌" + "─" * 100 + "┐")
print("│" + " " * 38 + "📊 COMPRESSION RESULTS" + " " * 40 + "│")
print("├" + "─" * 100 + "┤")
print("│ Type          │ Original → Simplified → Compressed │ Bytes Saved │ Final Reduction │")
print("├" + "─" * 100 + "┤")
def print_stats_row(stats):
    print(f"│ {stats['name']:<13} │ {stats['o_bits']:,}b → {stats['s_bits']:,}b → {stats['c_bits']:,}b │ {stats['o_bytes'] - stats['c_bytes']:>11} │ {stats['red_f']:>15.1f}% │")
print_stats_row(msg_stats)
print_stats_row(img_stats)
print_stats_row(vid_stats)
print("├" + "─" * 100 + "┤")
total_o_bytes = msg_stats['o_bytes'] + img_stats['o_bytes'] + vid_stats['o_bytes']
total_c_bytes = msg_stats['c_bytes'] + img_stats['c_bytes'] + vid_stats['c_bytes']
total_o_bits = msg_stats['o_bits'] + img_stats['o_bits'] + vid_stats['o_bits']
total_s_bits = msg_stats['s_bits'] + img_stats['s_bits'] + vid_stats['s_bits']
total_c_bits = msg_stats['c_bits'] + img_stats['c_bits'] + vid_stats['c_bits']
total_saved = total_o_bytes - total_c_bytes
total_reduction = ((total_o_bits - total_c_bits) / total_o_bits * 100) if total_o_bits > 0 else 0
print(f"│ {'TOTAL':<13} │ {total_o_bits:>8,}b → {total_s_bits:>8,}b → {total_c_bits:>8,}b │ {total_saved:>11} │ {total_reduction:>14.1f}% │")
print("└" + "─" * 100 + "┘")

# Decompression Test
print("\n┌" + "─" * 100 + "┐")
print("│" + " " * 38 + "✅ DECOMPRESSION TEST" + " " * 41 + "│")
print("└" + "─" * 100 + "┘")
rev_msg = decompress_message(compressed_msg_bits)
rev_img_simplified = decompress_link(compressed_bits_image)
rev_vid_simplified = decompress_link(compressed_bits_video)
img_final = desimplify_links(rev_img_simplified)
vid_final = desimplify_links(rev_vid_simplified)
msg_match = rev_msg == inputMessage.strip()
img_match = img_final == inputImageURL.strip()
vid_match = vid_final == inputVideoURL.strip()
print(f"\n📝 Message: {'✅ PERFECT MATCH' if msg_match else '❌ MISMATCH'}")
print(f"🖼️  Image URLs: {'✅ PERFECT MATCH' if img_match else '❌ MISMATCH'}")
print(f"🎬 Video URLs: {'✅ PERFECT MATCH' if vid_match else '❌ MISMATCH'}")
if not img_match:
    print("\n⚠️  Image URLs mismatch Details:\n--- EXPECTED ---\n" + inputImageURL.strip() + "\n--- GOT ---\n" + img_final)
if not vid_match:
    print("\n⚠️  Video URLs mismatch Details:\n--- EXPECTED ---\n" + inputVideoURL.strip() + "\n--- GOT ---\n" + vid_final)
print("\n📤 Decoded Message:")
print(f"   {rev_msg[:100]}...")
print("\n📤 Decoded Image URLs (first 3):")
for line in img_final.split('\n')[:3]: print(f"   {line}")
print("\n📤 Decoded Video URLs (first 3):")
for line in vid_final.split('\n')[:3]: print(f"   {line}")

# Summary
print("\n" + "═" * 100)
if total_saved > 0:
    print(f"✅ SUCCESS: Compressed from {total_o_bytes} bytes to {total_c_bytes} bytes")
    print(f"🎉 Total Compression: {total_reduction:.1f}% | Saved {total_saved} bytes | Perfect for BLE!")
else:
    print(f"📊 Result: {total_reduction:.1f}% compression | Total size: {total_c_bytes} bytes")
print("═" * 100)