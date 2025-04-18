# gc_bin_coverage.py
#!/usr/bin/env python3
import csv, argparse

def main():
    p = argparse.ArgumentParser(description="Mean coverage by GC bins")
    p.add_argument("intervals", help="HS intervals TSV with %gc & mean_coverage cols")
    args = p.parse_args()

    # define 10 GC bins
    labels = [f"{i*10}-{(i+1)*10}%" for i in range(10)]
    stats  = {lbl:[0.0,0] for lbl in labels}

    with open(args.intervals) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            gc_str  = row['%gc'].strip()
            cov_str = row['mean_coverage'].strip()
            if not gc_str or not cov_str:
                continue
            gc  = float(gc_str)
            cov = float(cov_str)
            idx = min(int(gc*10), 9)
            lbl = labels[idx]
            stats[lbl][0] += cov
            stats[lbl][1] += 1

    print("GC_bin\tmean_target_coverage")
    for lbl in labels:
        total, count = stats[lbl]
        if count:
            print(f"{lbl}\t{total/count:.2f}")

if __name__=="__main__":
    main()
