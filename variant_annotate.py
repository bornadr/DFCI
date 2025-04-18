## my logic for this task is to read a list of variant IDs from a file, then for each ID:
## 1) Query the Ensembl REST API’s /variation/human endpoint to get back a JSON containing allele strings,
##genomic mappings, and transcript_consequences.
## 2) From the first mapping, extract the chromosome and position.
## 3) Loop over each transcript_consequence entry then pulling out transcript_id, gene_symbol, and the list of consequence_terms (joined by commas).
## 4) Write a TSV row per transcript consequence and catch errors. 
## 5) Include a short delay between API calls to for rate limits.



#!/usr/bin/env python3
import argparse
import requests
import time

API_BASE = "https://rest.ensembl.org"

def get_variant_info(vid):
    url = f"{API_BASE}/variation/human/{vid}"
    headers = {"Accept": "application/json"}
    r = requests.get(url, headers=headers)
    if not r.ok:
        r.raise_for_status()
    return r.json()

def parse_and_write(vid, data, fout):
    """
    flatten the JSON response and write one line per transcript consequence.
    """
    allele = data.get("allele_string", "")
    mappings = data.get("mappings", [])
    # pick first mapping for location
    if mappings:
        mapping = mappings[0]
        chrom = mapping.get("seq_region_name", "")
        pos   = mapping.get("start", "")
    else:
        chrom = pos = ""
    tcs = data.get("transcript_consequences", [])
    if not tcs:
        fout.write(f"{vid}\t{allele}\t{chrom}\t{pos}\t\t\t\n")
    else:
        for tc in tcs:
            tid = tc.get("transcript_id", "")
            gene = tc.get("gene_symbol", "")
            cons = ",".join(tc.get("consequence_terms", []))
            fout.write(f"{vid}\t{allele}\t{chrom}\t{pos}\t{tid}\t{gene}\t{cons}\n")

def main():
    p = argparse.ArgumentParser(description="Annotate variants via Ensembl REST API")
    p.add_argument("variants", help="Input file with one variant ID per line")
    p.add_argument("output",   help="TSV output file")
    p.add_argument("--delay", type=float, default=0.2,
                   help="Seconds to wait between API calls (to respect rate limits)")
    args = p.parse_args()

    with open(args.variants) as fin, open(args.output, 'w') as fout:
        # header
        fout.write("variant_id\tallele\tchrom\tpos\ttranscript_id\tgene_symbol\tconsequences\n")
        for line in fin:
            vid = line.strip()
            if not vid:
                continue
            try:
                data = get_variant_info(vid)
                parse_and_write(vid, data, fout)
            except Exception as e:
                # write an empty record with error note
                fout.write(f"{vid}\tERROR\t\t\t\t\t{e}\n")
            time.sleep(args.delay)

if __name__ == "__main__":
    main()

