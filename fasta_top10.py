# fasta_top10.py
#!/usr/bin/env python3
import argparse

def parse_fasta(path):
    counts = {}
    seq = ''
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if seq:
                    counts[seq] = counts.get(seq,0) + 1
                seq = ''
            else:
                seq += line
        if seq:
            counts[seq] = counts.get(seq,0) + 1
    return counts

def main():
    p = argparse.ArgumentParser(description="Top 10 most frequent FASTA sequences")
    p.add_argument("fasta", help="Input FASTA file")
    args = p.parse_args()

    counts = parse_fasta(args.fasta)
    top10 = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

    print("Count\tSequence")
    for seq, cnt in top10:
        print(f"{cnt}\t{seq}")

if __name__=="__main__":
    main()
