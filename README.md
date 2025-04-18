# Project Overview

This repository contains a collection of Python scripts and a Jupyter notebook to perform common bioinformatics data‑handling tasks. Each script is self‑contained and executable from the command line, covering:

- **Task 1**: FASTQ and FASTA processing, and genomic coordinate annotation
- **Task 2**: Coverage summary by GC‐content bins
- **Task 3**: Variant annotation via Ensembl REST API

For a deep dive into my approach & commented logic, see `test.ipynb`, which includes all functions for Task 1 and Task 2.

---

## Directory Structure

```
DFCI_Code/
├── fastq_stats.py            # Task 1: FASTQ summary
├── fasta_top10.py            # Task 1: FASTA top‐10 frequent sequences
├── gtf_annotate.py           # Task 1: Coordinate → gene annotation
├── gc_bin_coverage.py        # Task 2: Mean coverage by GC bins
├── variant_annotate.py       # Task 3: Ensembl variant annotation
├── test.ipynb                # Jupyter notebook with commented implementations
├── sql-and-cloud.ipynb       # Answers to cloud computing and sql questions.
├── sample_files/             # Sample input data (ignored large files via .gitignore)
│   ├── fastq/                # Example FASTQ files
│   ├── fasta/                # Example FASTA file
│   ├── gtf/                  # hg19_annotations.gtf (ignored)
│   └── annotate/             # coordinates_to_annotate.txt
└── .gitignore                # Ignores large reference data
```

---


## Usage

Navigate to the root folder and invoke each script with Python.

### Task 1: FASTQ Summary

```bash
python3 fastq_stats.py <fastq_root_directory> --min <min_length>
```

- `<fastq_root_directory>`: root to recursively search for `.fastq`/`.fq` files
- `--min`: minimum sequence length (default: 30)

Example:
```bash
python3 fastq_stats.py sample_files/fastq --min 30
```

### Task 1: FASTA Top‑10

```bash
python3 fasta_top10.py sample_files/fasta/sample.fasta
```

Outputs the ten most frequent sequences with counts.

### Task 1: GTF Annotation

```bash
python3 gtf_annotate.py \
  sample_files/gtf/hg19_annotations.gtf \
  sample_files/annotate/coordinates_to_annotate.txt \
  coordinates_annotated.tsv
```

Generates `coordinates_annotated.tsv` with `chrom`, `pos`, and overlapping `gene`.

### Task 2: GC Content Binning

```bash
python3 gc_bin_coverage.py Example.hs_intervals.txt
```

Prints mean target coverage per GC bin (0–10%, …, 90–100%).

### Task 3: Variant Annotation

```bash
python3 variant_annotate.py variants.txt variants_annotated.tsv
```

- `variants.txt`: one variant ID per line (e.g. `rs56116432`)
- `variants_annotated.tsv`: output with allele, location, transcript consequences, gene symbols

Your Ensembl REST API queries respect rate limits—adjust `--delay` if needed.

---

## Understanding My Approach

All core functions and detailed comments are included in **`test.ipynb`**. If you want to see how each routine was developed and the reasoning behind edge‑case handling, please open that notebook in Jupyter Lab:

```bash
jupyter lab test.ipynb
```

---

## Git & Data Management

- **Large reference files** (e.g. `hg19_annotations.gtf`) are excluded by `.gitignore`.

