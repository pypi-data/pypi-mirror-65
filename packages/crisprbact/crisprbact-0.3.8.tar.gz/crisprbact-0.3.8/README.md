# CRISPRbact

**Tools to design and analyse CRISPRi experiments in bacteria.**

CRISPRbact currently contains an on-target activity prediction tool for the Streptococcus pyogenes dCas9 protein.
This tool takes as an input the sequence of a gene of interest and returns a list of possible target sequences with the predicted on-target activity. Predictions are made using a linear model fitted on data from a genome-wide CRISPRi screen performed in E. coli (Cui et al. Nature Communications, 2018). The model predicts the ability of dCas9 to block the RNA polymerase when targeting the non-template strand (i.e. the coding strand) of a target gene.

## Getting Started

### Installation

For the moment, you can install this package only via PyPI

#### PyPI

```console
$ pip install crisprbact
$ crisprbact --help
```

```
Usage: crisprbact [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose
  --help         Show this message and exit.

Commands:
  predict
```

### API

Using this library in your python code.

```python
from crisprbact import on_target_predict

guide_rnas = on_target_predict("ACCACTGGCGTGCGCGTTACTCATCAGATGCTGTTCAATACCGATCAGGTTATCGAAGTGTTTGTGATTGTTTGCCGCGCGCGTGGCGAAGGCCCGTGATGAAGGAAAAGTTTTGCGCTATGTTGGCAATATTGATGAAG")

for guide_rna in guide_rnas:
    print(guide_rna)

```

_output :_

```
{'target': 'TCATCACGGGCCTTCGCCACGCGCG', 'guide': 'TCATCACGGGCCTTCGCCAC', 'start': 82, 'stop': 102, 'pam': 80, 'ori': '-', 'target_id': 1, 'pred': -0.4719254873780802, 'off_targets_per_seed': []}
{'target': 'CATCACGGGCCTTCGCCACGCGCGC', 'guide': 'CATCACGGGCCTTCGCCACG', 'start': 81, 'stop': 101, 'pam': 79, 'ori': '-', 'target_id': 2, 'pred': 1.0491308060379676, 'off_targets_per_seed': []}
{'target': 'CGCGCGCGGCAAACAATCACAAACA', 'guide': 'CGCGCGCGGCAAACAATCAC', 'start': 63, 'stop': 83, 'pam': 61, 'ori': '-', 'target_id': 3, 'pred': -0.9021152826078697, 'off_targets_per_seed': []}
{'target': 'CCTGATCGGTATTGAACAGCATCTG', 'guide': 'CCTGATCGGTATTGAACAGC', 'start': 29, 'stop': 49, 'pam': 27, 'ori': '-', 'target_id': 4, 'pred': 0.23853258873311955, 'off_targets_per_seed': []}
```

### Command line interface

#### Predict guide RNAs activity

Input the sequence of a target gene and this script will output candidate guide RNAs for the S. pyogenes dCas9 with predicted on-target activity.

```console
$ crisprbact predict --help
```

```
Usage: crisprbact predict [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  from-seq  Outputs candidate guide RNAs for the S.
  from-str  Outputs candidate guide RNAs for the S.
```

##### From a string sequence:

The target input sequence can be a simple string.

```console
$ crisprbact predict from-str --help
```

```
Usage: cli.py predict from-str [OPTIONS] [OUTPUT_FILE]

  Outputs candidate guide RNAs for the S. pyogenes dCas9 with predicted on-
  target activity from a target gene.

  [OUTPUT_FILE] file where the candidate guide RNAs are saved. Default =
  "stdout"

Options:
  -t, --target TEXT               Sequence file to target  [required]
  -s, --off-target-sequence FILENAME
                                  Sequence in which you want to find off-
                                  targets
  -w, --off-target-sequence-format [fasta|gb|genbank]
                                  Sequence in which you want to find off-
                                  targets format  [default: genbank]
  --help                          Show this message and exit.

```

```console
$ crisprbact predict from-str -t ACCACTGGCGTGCGCGTTACTCATCAGATGCTGTTCAATACCGATCAGGTTATCGAAGTGTTTGTGATTGTTTGCCGCGCGCGTGGCGAAGGCCCGTGATGAAGGAAAAGTTTTGCGCTATGTTGGCAATATTGATGAAG guide-rnas.tsv
```

output file `guide-rnas.tsv` :

No `seq_id` is defined since it is from a simple string.

```
target	PAM position	prediction	seq_id
TCATCACGGGCCTTCGCCACGCGCG	80	-0.4719254873780802	N/A
CATCACGGGCCTTCGCCACGCGCGC	79	1.0491308060379676	N/A
CGCGCGCGGCAAACAATCACAAACA	61	-0.9021152826078697	N/A
CCTGATCGGTATTGAACAGCATCTG	27	0.23853258873311955	N/A
```

You can also pipe the results :

```console
$ crisprbact predict from-str -t ACCACTGGCGTGCGCGTTACTCATCAGATGCTGTTCAATACCGATCAGGTTATCGAAGTGTTTGTGATTGTTTGCCGCGCGCGTGGCGAAGGCCCGTGATGAAGGAAAAGTTTTGCGCTATGTTGGCAATATTGATGAAG | tail -n +2 | wc -l
```

##### From a sequence file

```console
$ crisprbact predict from-seq --help
```

```
Usage: cli.py predict from-seq [OPTIONS] [OUTPUT_FILE]

  Outputs candidate guide RNAs for the S. pyogenes dCas9 with predicted on-
  target activity from a target gene.

  [OUTPUT_FILE] file where the candidate guide RNAs are saved. Default =
  "stdout"

Options:
  -t, --target FILENAME           Sequence file to target  [required]
  -f, --seq-format [fasta|gb|genbank]
                                  Sequence file to target format  [default:
                                  fasta]
  -s, --off-target-sequence FILENAME
                                  Sequence in which you want to find off-
                                  targets
  -w, --off-target-sequence-format [fasta|gb|genbank]
                                  Sequence in which you want to find off-
                                  targets format  [default: genbank]
  --help                          Show this message and exit.
```

- Fasta file (could be a multifasta file)

```console
$ crisprbact predict from-seq -t /tmp/seq.fasta guide-rnas.tsv
```

- GenBank file

```console
$ crisprbact predict from-seq -t /tmp/seq.gb -f gb guide-rnas.tsv
```

- Off-targets

```console
predict from-seq -t data-test/sequence.fasta -s data-test/sequence.gb guide-rnas.tsv
```

##### Output file

```
target_id	target	PAM position	prediction	target_seq_id	seed_size	off_target_recid	off_target_start	off_target_end	off_target_pampos	off_target_strand	off_target_feat_type	off_target_feat_start	off_target_feat_end	off_target_feat_strand	off_target_locus_tag	off_target_gene	off_target_note	off_target_product	off_target_protein_id
1	TGATCCAGGCATTTTTTAGCTTCAT	835	0.47949500169043713	NC_017634.1:2547433-2548329	8	NC_017634.1	1388198	1388209	1388209	+
1	TGATCCAGGCATTTTTTAGCTTCAT	835	0.47949500169043713	NC_017634.1:2547433-2548329	8	NC_017634.1	2244514	2244525	2244525	+	CDS	2243562	2244720	-1	NRG857_10810		COG1174 ABC-type proline/glycine betaine transport systems, permease component	putative transport system permease	YP_006120510.1
1	TGATCCAGGCATTTTTTAGCTTCAT	835	0.47949500169043713	NC_017634.1:2547433-2548329	8	NC_017634.1	4160984	4160995	4160995	+	CDS	4160074	4161406	-1	NRG857_19625	hslU	COG1220 ATP-dependent protease HslVU (ClpYQ), ATPase subunit	ATP-dependent protease ATP-binding subunit HslU	YP_006122267.1
1	TGATCCAGGCATTTTTTAGCTTCAT	835	0.47949500169043713	NC_017634.1:2547433-2548329	8	NC_017634.1	4534189	4534200	4534200	+
1	TGATCCAGGCATTTTTTAGCTTCAT	835	0.47949500169043713	NC_017634.1:2547433-2548329	8	NC_017634.1	548804	548815	548804	-
1	TGATCCAGGCATTTTTTAGCTTCAT	835	0.47949500169043713	NC_017634.1:2547433-2548329	8	NC_017634.1	786462	786473	786462	-	CDS	785384	786470	1	NRG857_03580		COG2055 Malate/L-lactate dehydrogenases	hypothetical protein	YP_006119079.1

```

## Contributing

### Clone repo

```console
$ git clone https://gitlab.pasteur.fr/dbikard/crisprbact.git
```

### Create a virtualenv

```console
$ virtualenv -p python3.7 .venv
$ . .venv/bin/activate
$ pip install poetry
```

### Install crisprbact dependencies

```console
$ poetry install
```

### Install hooks

In order to run flake8 and black for each commit.

```console
$ pre-commit install
```
