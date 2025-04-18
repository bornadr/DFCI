# gtf_annotate.py
#!/usr/bin/env python3
import re, bisect, argparse

def build_gene_index(gtf_path):
    index = {}
    pat = re.compile(r'gene_name "([^"]+)"')
    with open(gtf_path) as g:
        for L in g:
            if L.startswith('#'): continue
            c,_,feat,s,e,_,_,_,attrs = L.split('\t',8)
            if feat!='gene': continue
            name = pat.search(attrs)
            gene = name.group(1) if name else "NA"
            index.setdefault(c,[]).append((int(s),int(e),gene))
    starts = {}
    for c,ivals in index.items():
        ivals.sort(key=lambda x:x[0])
        starts[c] = [iv[0] for iv in ivals]
    return index, starts

def annotate(coords, index, starts, out):
    with open(coords) as fin, open(out,'w') as fout:
        fout.write("chrom\tpos\tgene\n")
        for line in fin:
            chrom,pos = line.split()
            pos = int(pos)
            gene = "intergenic"
            if chrom in index:
                i = bisect.bisect_right(starts[chrom], pos)
                if i and index[chrom][i-1][1] >= pos:
                    gene = index[chrom][i-1][2]
            fout.write(f"{chrom}\t{pos}\t{gene}\n")

def main():
    p = argparse.ArgumentParser(description="Annotate coordinates via GTF")
    p.add_argument("gtf",   help="GTF annotation file")
    p.add_argument("coords",help="Coordinates file (chrom<TAB>pos)")
    p.add_argument("out",   help="Output TSV")
    args = p.parse_args()

    idx, sts = build_gene_index(args.gtf)
    annotate(args.coords, idx, sts, args.out)

if __name__=="__main__":
    main()
