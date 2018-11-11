""" Gibb's sampling method for finding motif l-mer in an array of sequences

Algorithm steps
1. Start with a motif (l-mer) and an array of sequences
2. Perform local alignment on each sequence with the l-mer (use code from the first programming project)
3. Create an alignment matrix t x l from the best local alignment for each sequence
4. Create a profile matrix 4 x l with probabilities of each letter AGCT at each position
5. Take a single sequence and to find the motif within it use the matrix in 4 and starting at
starting position of sequence find probabilities of each and find the one that give the highest probability

"""

def gibbs(motif, sequences):
    pass

motif = "ACCTGAA"
sequences = [""]