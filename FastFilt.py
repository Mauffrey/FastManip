#!/usr/bin/python3

import sys

try:
    from Bio import SeqIO
except ModuleNotFoundError:
    sys.exit("\nBiopython not installed\n")

parameters = ["length_max", "length_min", "seq_present", "seq_absent"]


def check_arg():
    if len(sys.argv) != 4:
        print("\nWrong number of arguments\n")
        return False
    elif sys.argv[1] not in parameters:
        print(f"\n{sys.argv[1]} parameter not valid\n")
        return False
    else:
        if sys.argv[1] in ["length_max", "length_min"]:
            try:
                int(sys.argv[2])
                return True
            except ValueError:
                print("\nlength_max, length_min: Value must be an integer\n")
                return False
        else:
            return True


def check_extension():
    extension = sys.argv[3].split(".")[-1]
    if extension in ["fa", "fna", "fasta"]:
        return "fasta"
    elif extension in ["fq", "fastq"]:
        return "fastq"
    else:
        sys.exit("\nIncorrect file format. File should end in .fq, .fastq, .fa, .fna or .fasta.\n")


def seq_filter(file_ext):
    param = sys.argv[1]
    value = sys.argv[2]
    fast_sequences = SeqIO.parse(sys.argv[3], file_ext)
    seq_output = []

    if param == "length_max":
        for seq in fast_sequences:
            if len(seq.seq) <= int(value):
                seq_output.append(seq)

    elif param == "length_min":
        for seq in fast_sequences:
            if len(seq.seq) >= int(value):
                seq_output.append(seq)

    elif param == "seq_present":
        for seq in fast_sequences:
            if value in seq.seq:
                seq_output.append(seq)

    elif param == "seq_absent":
        for seq in fast_sequences:
            if value not in seq.seq:
                seq_output.append(seq)

    with open(f"{sys.argv[3]}_out.{file_ext}", "w") as output:
        SeqIO.write(seq_output, output, file_ext)


if __name__ == "__main__":
    if check_arg():
        seq_type = check_extension()
        seq_filter(seq_type)
    else:
        sys.exit("\n#####################################\n"
                 "########## FastSplit.py ############\n"
                 "#####################################\n"
                 "\nFilter fasta/fastq file based on chosen parameter\n\n"
                 "Usage: FastSplit.py [parameter] [value] [file]\n\n"
                 "Parameters are:\n"
                 "length_max = maximum length of contigs\n"
                 "length_min = minimum length of contigs\n"
                 "seq_present = contigs containing the sequence (or base)\n"
                 "seq_absent = contigs not containing the sequence (or base)\n\n")
