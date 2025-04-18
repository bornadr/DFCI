# fastq_stats.py
#!/usr/bin/env python3
import os
import argparse

def find_fastq_files(root):
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith(('.fastq','.fq')):
                yield os.path.join(dirpath, fn)

def calc_pct_long_reads(path, min_len):
    total = over = 0
    with open(path) as f:
        while True:
            header = f.readline()
            if not header:
                break
            seq = f.readline().strip()
            f.readline(); f.readline()
            total += 1
            if len(seq) > min_len:
                over += 1
    pct = (over/total*100) if total else 0
    return total, over, pct

def main():
    p = argparse.ArgumentParser(description="FASTQ length stats")
    p.add_argument("root", help="Directory to search")
    p.add_argument("--min", type=int, default=30, help="Min length threshold")
    args = p.parse_args()

    for fq in find_fastq_files(args.root):
        total, over, pct = calc_pct_long_reads(fq, args.min)
        print(f"{fq}\t{pct:.2f}% ({over}/{total}) reads > {args.min} nt")

if __name__=="__main__":
    main()
