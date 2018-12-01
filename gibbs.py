#!/usr/bin/python
""" Gibb's sampling method for finding motif l-mer in an array of sequences

Algorithm steps
1. Input: motif (l-mer, l = length of motif we are looking for) and an array of sequences (t=number of sequences)
2. Randomly select start positions in each sequence
3. Create an alignment matrix t x l from the best local alignment for each sequence
4. Create a profile matrix 4 x l with probabilities of each letter AGCT at each position
5. Take a single sequence and to find the motif within it use the matrix in 4 and starting at
starting position of sequence find probabilities of each and find the one that give the highest probability

"""

import sys
import argparse
import random
import pandas as pd

amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I',
               'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']

bases = ['A', 'G', 'C', 'T']


def score(s, seq):
    pass


def create_profile(sequences, is_protein):

    # Put sequences into a dataframe
    sequence_df = pd.DataFrame(sequences)
    print(sequence_df)

    profile_df = pd.DataFrame()
    if is_protein:
        profile_df = pd.DataFrame(columns=amino_acids)
    else:
        profile_df = pd.DataFrame(columns=bases)

    for letter in list(profile_df.columns.values):
        continue

def gibbs(l, sequences, is_protein):
    """ This function perform's gibbs sampling method for motif finding """
    # Randomly select start positions
    start_positions = [random.randint(0, len(x)-l) for x in sequences]
    print('Trying start positions ' + str(start_positions))
    profile = []
    best_score = 0

    # Randomly choose one of the t sequences
    t = len(sequences)
    r = random.randint(0, t-1)
    random_sequence = sequences[r]
    print("Random sequence at position " + str(r) + " = " + random_sequence)

    # Create a profile for rest of sequences
    profile = create_profile([seq for index, seq in enumerate(sequences) if index != r])
    print(profile)

    """ while i != last:  # repeat until nothing changes
        last = list(i)

        # iterate through every string
        for i in xrange(len(Seqs)):
        # compute the profile for the sequences except i
        P = profile_for([
            x[j: j + k] for q, (x, j) in enumerate(zip(Seqs, I))
            if q != i
        ])
        # find the place the profile matches best
        best = None
        for j in xrange(len(Seqs[i]) - k + 1):
            score = profile_score(P, Seqs[i][j: j + k])
        if score > best or best is None:
            best = score
        bestpos = j
        # update the ith position with the best
        I[i] = bestpos

    return I, [x[j: j + k] for x, j in zip(Seqs, I)]"""
    motifs = [1, 0, 9, 8, 1, 0, 0]
    return motifs


def main():
    args = parse_arguments()
    filename = args.f
    motif_length = int(args.l)
    is_protein = bool(args.p)

    # Check if file exists
    try:
        file = open(filename, 'r')
        print('Search for motif of length' + str(motif_length) + ' in sequences found in file ' + filename)
        if is_protein:
            print('Protein Sequences')
        else:
            print('DNA Sequences')

        # Read sequences into array
        sequences = [line.strip() for line in file]
        print(sequences)

        # Do validation if necessary

        # Make sure the sequences are all upper case
        for seq in sequences:
            seq = seq.upper()

        # Perform Gibb's Sampling
        motifs = gibbs(motif_length, sequences)

        # Output result
        output = open("motif_output.txt", "w+")
        i = 0
        for m in motifs:
            output.write(sequences[i][m:m+motif_length] + ', ' + str(m) + '\r\n')
            i = i + 1

        output.close()

    except FileNotFoundError:
        print('File Not Found Error: file does not exist in given directory, make sure to include the full path.')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Uses gibbs sampling method to find motifs in a set of sequences')
    parser.add_argument('-f', required=True,
                        help='the input filename of sequences, each sequence should be on a new line')
    parser.add_argument('-l', default=6,
                        help='the length of the motif you are searching for')
    parser.add_argument('-p', default=False,
                        help='true if these are protein sequences, defaults to false')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
