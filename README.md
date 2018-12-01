# Gibbs Sampling Method for Motif Finding

This command line program searches for a motif of length l in a set of sequences. It uses
the gibb's sampling method to locate the most likely motifs.

## Get started

### `gibbs.py`
Run gibbs.py to locate sequences of length l in a set of sequences in your input file.
This code requires python 3 to run.

To run from teh command line:

```
python gibbs.py -l 6 -f inputfile.txt
```
 
`-l`: defines the l-mer, or size of teh motif you are searching for   

`-f`: required parameter that gives the filename of the input file of the sequences to be searched

---
