#!/usr/bin/python
""" Gibb's sampling method for finding motif l-mer in an array of sequences

Algorithm steps
1. Input: motif (l-mer, l = length of motif we are looking for) and an array of sequences (t=number of sequences)
2. Randomly choose starting positions within each sequence
3. Randomly choose one of the t sequences
4. Create an alignment matrix t x l with the rest of t-1 sequences
5. Create a profile matrix 4 x l (or 20 x l) with probabilities of each letter AGCT (or amino acids) at each position
6. Take the random matrix you chose in step 3 and find the best probability based on the profile and set that starting position to the new starting position
7. Repeat from step 3 until the list of starting positions does not change

"""
import time
import argparse
import random
import pandas as pd
import numpy as np
import logging

amino_acids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I',
               'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
bases = ['A', 'G', 'C', 'T']
logging.basicConfig(filename='./logs/gibbs.log', level=logging.DEBUG, format='%(asctime)s %(message)s')


def calculate_consensus_score(sequences, s, l, is_protein):
    """ This function computes the consensus score of the set of lmers in the sequences start at
    positions s """
    """ This function creates a profile of the l-mers at the starting positions s"""

    # Put lmers into a matrix
    lmer_matrix = np.char.asarray([list(x[s[index]:s[index] + l]) for index, x in enumerate(sequences)])

    # Initialize profile based on type of sequences
    letters = amino_acids if is_protein else bases

    # Create profile matrix
    consensus_score = 0
    for i in range(0, np.size(lmer_matrix, 1)):
        max_count = 0
        for letter in letters:
            letter_count = list(lmer_matrix[:, i]).count(letter)
            if letter_count > max_count:
                max_count = letter_count
        consensus_score += max_count

    logging.info(" - Consensus Score = " + str(consensus_score))

    return consensus_score


def create_profile(sequences, s, l, is_protein):
    """ This function creates a profile of the l-mers at the starting positions s"""
    logging.info(" - Sequences = " + str(sequences))
    logging.info(" - Starting positions = " + str(s))

    # Put lmers into a matrix
    lmer_matrix = np.char.asarray([list(x[s[index]:s[index]+l]) for index, x in enumerate(sequences)])

    logging.info(" - Profile matrix = ")
    logging.info(lmer_matrix)

    # Initialize profile based on type of sequences
    if is_protein:
        profile_df = pd.DataFrame(columns=amino_acids)
    else:
        profile_df = pd.DataFrame(columns=bases)

    num_sequences = len(sequences)

    # Create profile matrix
    for i in range(0, np.size(lmer_matrix, 1)):
        for letter in list(profile_df.columns.values):
            letter_count = list(lmer_matrix[:, i]).count(letter)
            logging.info(letter_count)
            profile_df.at[i, letter] = letter_count / num_sequences

    logging.info(" - Profile = ")
    logging.info(profile_df)

    return profile_df


def get_best_probability(lmer, profile):
    """ This function computes the probability that this lmer will be generated by this profile """
    total_probability = 1
    pos = 0
    for letter in lmer:
        total_probability *= profile.at[pos, letter]
        pos += 1

    return total_probability


def gibbs(l, sequences, is_protein):
    """ This function perform's gibbs sampling method for motif finding """
    # Randomly select start positions
    logging.info("Step 1. Randomly choose starting positions")
    start_positions = [random.randint(0, len(x)-l) for x in sequences]
    logging.info('Trying start positions ' + str(start_positions))

    # Repeat these steps until we cannot import the score
    consensus_score = calculate_consensus_score(sequences, start_positions, l, is_protein)
    last_score = 0
    while consensus_score > last_score:
        last_score = consensus_score

        # Randomly choose one of the t sequences
        t = len(sequences)
        chosen_sequence_index = random.randint(0, t-1)
        random_sequence = sequences[chosen_sequence_index]
        logging.info("Step 2. Random sequence at position " + str(chosen_sequence_index) + " = " + random_sequence)

        # Create a profile for rest of sequences
        logging.info("Step 3. Profile creation from t-1 sequences and random start positions")
        profile = create_profile([seq for index, seq in enumerate(sequences) if index != chosen_sequence_index],
                                 [pos for index, pos in enumerate(start_positions) if index != chosen_sequence_index],
                                 l, is_protein)

        # Calculate probabilities at each position in chosen sequence
        prob_distribution = list()
        logging.info("Step 4. Find probabilities of all positions of chosen sequence to find the best")

        for pos in range(0, len(random_sequence)-l):
            score = get_best_probability(random_sequence[pos:pos+l], profile)
            if score > 0:
                prob_distribution.append((score, pos))

        logging.info(prob_distribution)

        if len(prob_distribution) > 0:
            # Calculate probability distribution
            best_score = 0
            best_start = start_positions[chosen_sequence_index]
            logging.info(" - Current start position = " + str(best_start))
            min_prob = min([score for score, pos in prob_distribution])
            logging.info("Min prob = " + str(min_prob))
            prob_distribution = [(score/min_prob, pos) for score, pos in prob_distribution]
            logging.info(prob_distribution)
            total_score = sum([score for score, pos in prob_distribution])
            logging.info("Total prob = " + str(total_score))
            prob_distribution = [(score/total_score, pos) for score, pos in prob_distribution]
            logging.info(prob_distribution)
            for score, pos in prob_distribution:
                if score > best_score:
                    best_score = score
                    best_start = pos

            # Update the new starting position
            logging.info(" - New best start position = " + str(best_start))
            start_positions[chosen_sequence_index] = best_start

            # Calculate a new consensus score
            consensus_score = calculate_consensus_score(sequences, start_positions, l, is_protein)

    print("Consensus Score = " + str(consensus_score))
    print("Optimal starting positions")
    print(start_positions)
    logging.info("Optimal starting positions")
    logging.info(start_positions)

    return start_positions


def import_from_fasta(file):
    from Bio import SeqIO
    fasta_sequences = SeqIO.parse(file, 'fasta')
    return [str(fasta_seq.seq) for fasta_seq in fasta_sequences]


def main():
    args = parse_arguments()
    filename = args.f
    motif_length = int(args.l)
    is_protein = bool(args.p)

    # Check if file exists
    try:
        file = open(filename, 'r')
        logging.info('STARTING NEW MOTIF SEARCH')
        logging.info('Search for motif of length ' + str(motif_length) + ' in sequences found in file ' + filename)
        if is_protein:
            logging.info('Protein Sequences')
        else:
            logging.info('DNA Sequences')

        # Read sequences into array
        if filename.endswith('fasta'):
            sequences = import_from_fasta(file)
        else:
            sequences = [line.strip() for line in file]

        # Make sure the sequences are all upper case
        sequences = [seq.upper() for seq in sequences]
        print("Number of sequences = " + str(len(sequences)))
        logging.info("Number of sequences = " + str(len(sequences)))

        # Perform Gibb's Sampling
        motifs = gibbs(motif_length, sequences, is_protein)

        # Output result
        output = open("motif_output.txt", "w+")
        i = 0
        for m in motifs:
            output.write(sequences[i][m:m+motif_length] + ', ' + str(m) + '\r\n')
            i = i + 1

        output.close()

    except FileNotFoundError:
        logging.info('File Not Found Error: file does not exist in given directory, '
                     'make sure to include the full path.')


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
    start_time = time.time()
    main()
    elapsed_time = time.time() - start_time
    msg = "Running time = " + str(elapsed_time * 1000) + "ms"
    logging.info(msg)
    print(msg)

