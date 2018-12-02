# Gibbs Sampling Method for Motif Finding

This command line program searches for a motif of length l in a set of sequences. It uses
the gibb's sampling method to locate the most likely motifs.

## Get started

### Installation

Run the commands below to clone the repository and install package dependencies.

```
git clone https://github.com/jperilla/gibbs_motif_finding.git
cd gibbs_motif_finding
pip install -r requirements.txt
```
---

### Running
####`gibbs.py`
Run gibbs.py to locate sequences of length l in a set of sequences in your input file.
This code requires python 3 to run.

To run from teh command line:

```
python gibbs.py -l 6 -f inputfile.txt
```
 
`-l`: defines the l-mer, or size of teh motif you are searching for   

`-f`: required parameter that gives the filename of the input file of the sequences to be searched

`-p`: set to True if these are protein sequences, otherwise DNA sequences, default is False

---

## The Algorithm

This program uses the Gibb's sampling method to find the optimal starting positions

1. Input: motif (l-mer, l = length of motif we are looking for) and an array of sequences (t=number of sequences)
2. Randomly choose starting positions within each sequence
3. Randomly choose one of the t sequences
4. Create an alignment matrix t x l with the rest of t-1 sequences
5. Create a profile matrix 4 x l (or 20 x l) with probabilities of each letter AGCT (or amino acids) at each position
6. Take the random matrix you chose in step 3 and find the best probability based on the profile and set that starting position to the new starting position
7. Repeat from step 3 until the list of starting positions does not change