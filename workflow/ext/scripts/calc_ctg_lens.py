import argparse
import os

def main(args): # A FastA file
    # Extract contig lengths and report i) the entire list and ii) a summary
    seq_lens = []
    ctg = ''
    out = "%s,%s," % (args.sp, args.asm)
    # if getsize(fa):  # Handle empty FastAs
    with open(args.fa, 'r') as f_in, open(args.f_len, 'w') as f_out:
        for line in f_in:
            if '>' in line:
                s = len(ctg)
                seq_lens.append(s)
                f_out.write(args.sp + ',' + args.asm + ',' + str(s) + '\n')
                ctg = ''
            else:
                ctg += line.strip()
    out += "%d,%d,%.2f" % (len(seq_lens), sum(seq_lens), float(sum(seq_lens) / len(seq_lens)))
    with open(args.f_summ, 'w') as f_out:
        f_out.write(out + '\n')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sp", help="Sample name")
    parser.add_argument("asm", help="Assembler name")
    parser.add_argument("fa", help="Contig file")
    parser.add_argument("f_summ", help="Assembly size summary file")
    parser.add_argument("f_len", help="Contig length file")
    args = parser.parse_args()
    main(args)
