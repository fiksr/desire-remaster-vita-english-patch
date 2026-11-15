#!/usr/bin/env python3
"""
DESIRE remaster ver. (PS Vita) - English Translation Patcher
Title ID: PCSG00959

This tool injects translated scenario scripts and localized UI textures into
the game's data.psarc archive. Requires a legally dumped original data.psarc.
Zero external dependencies required (uses standard library only).
"""

import struct
import zlib
import os
import sys
import time


def find_data_psarc():
    candidates = [
        "data.psarc",
        "data/data.psarc",
        "PCSG00959/data/data.psarc",
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.getsize(c) > 100_000_000:
            return c
    return None


def patch_psarc(input_psarc_path, output_psarc_path, patch_dir):
    print("=" * 65)
    print("  DESIRE remaster ver. (PS Vita) - English Translation Patcher")
    print("  Title ID: PCSG00959")
    print("=" * 65)
    print(f"\n[+] Input archive:  {input_psarc_path}")
    print(f"[+] Output archive: {output_psarc_path}")
    print(f"[+] Patch folder:   {patch_dir}")

    if not os.path.exists(input_psarc_path):
        print(f"\n[!] Error: Input archive '{input_psarc_path}' not found!")
        sys.exit(1)

    t0 = time.time()
    with open(input_psarc_path, "rb") as f_in:
        header = f_in.read(32)
        magic, ver_maj, ver_min, compression_type, toc_size, entry_size, num_entries, block_size, flags = struct.unpack(">4sHH4sIIIII", header)
        if magic != b"PSAR":
            print("[!] Error: File is not a valid PSARC archive.")
            sys.exit(1)
        if compression_type != b"zlib":
            print(f"[!] Error: Expected zlib compression, got {compression_type}.")
            sys.exit(1)

        print(f"[+] Reading archive TOC: {num_entries} entries, block size {block_size} bytes...")

        entries = []
        for i in range(num_entries):
            e_bytes = f_in.read(entry_size)
            name_hash = e_bytes[:16]
            zblock_idx, = struct.unpack(">I", e_bytes[16:20])
            uncomp_size = int.from_bytes(e_bytes[20:25], "big")
            offset = int.from_bytes(e_bytes[25:30], "big")
            entries.append({
                "index": i,
                "name_hash": name_hash,
                "zblock_idx": zblock_idx,
                "uncomp_size": uncomp_size,
                "offset": offset,
            })

        entries_len = entry_size * num_entries
        zblock_table_len = toc_size - entries_len
        zblock_bytes = f_in.read(zblock_table_len)
        num_zblocks = zblock_table_len // 2
        zblocks = list(struct.unpack(f">{num_zblocks}H", zblock_bytes))

        zb_start = entries[0]["zblock_idx"]
        next_zb = entries[1]["zblock_idx"]
        e_zblocks = zblocks[zb_start:next_zb]
        f_in.seek(entries[0]["offset"])
        manifest_bytes = bytearray()
        for zb in e_zblocks:
            sz = zb if zb != 0 else block_size
            chunk = f_in.read(sz)
            if zb != 0:
                manifest_bytes.extend(zlib.decompress(chunk))
            else:
                manifest_bytes.extend(chunk)

        manifest_lines = [l.strip() for l in manifest_bytes.decode('utf-8', errors='ignore').split('\n') if l.strip()]
        name_to_index = {manifest_lines[i]: i + 1 for i in range(len(manifest_lines))}

        replacements = {}
        for root, dirs, files in os.walk(patch_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, patch_dir).replace("\\", "/")
                if rel_path in name_to_index:
                    replacements[name_to_index[rel_path]] = full_path

        print(f"[+] Found {len(replacements)} matching files in patch folder to inject.")

        new_entries = []
        new_zblocks = []
        temp_data_path = output_psarc_path + ".tmp"

        with open(temp_data_path, "wb") as f_data_tmp:
            curr_data_offset = 0

            for i in range(num_entries):
                ent = entries[i]
                zb_start = ent["zblock_idx"]
                next_zb = entries[i + 1]["zblock_idx"] if i + 1 < num_entries else num_zblocks
                new_zb_start = len(new_zblocks)

                if i in replacements:
                    with open(replacements[i], "rb") as f_rep:
                        raw_data = f_rep.read()
                    uncomp_size = len(raw_data)
                    num_b = (uncomp_size + block_size - 1) // block_size if uncomp_size > 0 else 1

                    for b in range(num_b):
                        chunk = raw_data[b * block_size : (b + 1) * block_size]
                        if len(chunk) == 0:
                            comp = b""
                            zb_val = 0
                        else:
                            comp = zlib.compress(chunk, level=6)
                            if len(comp) >= len(chunk):
                                comp = chunk
                                zb_val = len(chunk) if len(chunk) < block_size else 0
                            else:
                                zb_val = len(comp)
                        f_data_tmp.write(comp)
                        new_zblocks.append(zb_val)

                    new_entries.append({
                        "name_hash": ent["name_hash"],
                        "zblock_idx": new_zb_start,
                        "uncomp_size": uncomp_size,
                        "rel_offset": curr_data_offset,
                    })
                    curr_data_offset += sum(
                        (new_zblocks[new_zb_start + b] if new_zblocks[new_zb_start + b] != 0 else block_size)
                        for b in range(num_b)
                    ) if uncomp_size > 0 else 0
                else:
                    orig_zblocks = zblocks[zb_start:next_zb]
                    total_bytes = sum((zb if zb != 0 else block_size) for zb in orig_zblocks)
                    if ent["uncomp_size"] == 0 and len(orig_zblocks) == 1 and orig_zblocks[0] == 0:
                        total_bytes = 0

                    f_in.seek(ent["offset"])
                    remaining = total_bytes
                    while remaining > 0:
                        buf = f_in.read(min(remaining, 4 * 1024 * 1024))
                        if not buf:
                            break
                        f_data_tmp.write(buf)
                        remaining -= len(buf)

                    new_zblocks.extend(orig_zblocks)
                    new_entries.append({
                        "name_hash": ent["name_hash"],
                        "zblock_idx": new_zb_start,
                        "uncomp_size": ent["uncomp_size"],
                        "rel_offset": curr_data_offset,
                    })
                    curr_data_offset += total_bytes

                if (i + 1) % 1000 == 0 or i + 1 == num_entries:
                    pct = ((i + 1) / num_entries) * 100
                    print(f"\r[+] Packing archive: {i+1}/{num_entries} ({pct:.1f}%)", end="", flush=True)

        print("\n[+] Writing final PSARC headers and combining payload...")
        new_toc_size = 32 + (num_entries * entry_size) + (len(new_zblocks) * 2)

        with open(output_psarc_path, "wb") as f_out:
            new_header = struct.pack(">4sHH4sIIIII", magic, ver_maj, ver_min, compression_type, new_toc_size, entry_size, num_entries, block_size, flags)
            f_out.write(new_header)

            for ne in new_entries:
                abs_offset = new_toc_size + ne["rel_offset"]
                f_out.write(ne["name_hash"])
                f_out.write(struct.pack(">I", ne["zblock_idx"]))
                f_out.write(ne["uncomp_size"].to_bytes(5, "big"))
                f_out.write(abs_offset.to_bytes(5, "big"))

            f_out.write(struct.pack(f">{len(new_zblocks)}H", *new_zblocks))

            with open(temp_data_path, "rb") as f_tmp:
                while True:
                    buf = f_tmp.read(8 * 1024 * 1024)
                    if not buf:
                        break
                    f_out.write(buf)

        if os.path.exists(temp_data_path):
            os.remove(temp_data_path)

    print(f"[+] SUCCESS! Patched archive written to: {output_psarc_path} ({time.time()-t0:.1f}s)")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    patch_dir = os.path.join(script_dir, "patch_files")

    if not os.path.exists(patch_dir):
        print("[!] Error: 'patch_files' directory not found next to patcher.py!")
        sys.exit(1)

    if len(sys.argv) >= 2:
        in_psarc = sys.argv[1]
    else:
        in_psarc = find_data_psarc()

    if not in_psarc or not os.path.exists(in_psarc):
        print("[!] Could not find 'data.psarc'!")
        print("    Please place your decrypted 'data.psarc' in this folder and run again.")
        sys.exit(1)

    out_psarc = sys.argv[2] if len(sys.argv) >= 3 else "data_patched.psarc"
    patch_psarc(in_psarc, out_psarc, patch_dir)


if __name__ == "__main__":
    main()
