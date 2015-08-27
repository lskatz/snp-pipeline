#!/usr/bin/env python2.7

import argparse
from snppipeline import __version__
from snppipeline import snppipeline
from snppipeline import utils

#==============================================================================
# Command line driver
#==============================================================================
if __name__ == '__main__':

    def minConsFreq(value):
        fvalue = float(value)
        if fvalue <= 0.5 or fvalue > 1:
            raise argparse.ArgumentTypeError("Minimum consensus frequency must be > 0.5 and <= 1.0")
        return fvalue

    def minConsStrdBias(value):
        fvalue = float(value)
        if fvalue < 0.0 or fvalue > 0.5:
            raise argparse.ArgumentTypeError("Minimum consensus strand bias must be >= 0.0 and <= 0.5")
        return fvalue

    parser = argparse.ArgumentParser(description="""Call the consensus base for a sample at the specified positions 
                                                    where SNPs were previously called in any of the samples.  Generates 
                                                    a single-sequence fasta file with one base per specified position.""",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    help = dict()
    help['allPileupFile']  = """Relative or absolute path to the genome-wide pileup file for this sample."""
    help['force']          = """Force processing even when result file already exists and is newer than inputs."""
    help['snpListFile']    = """Relative or absolute path to the SNP list file across all samples."""
    help['output']         = """Output file. Relative or absolute path to the consensus fasta file for this sample."""
    help['minBaseQual']    = """Mimimum base quality score to count a read. All other snp filters take effect after the low-quality reads are discarded."""
    help['minConsFreq']    = """Consensus frequency. Mimimum fraction of high-quality reads supporting the consensus to make a call."""
    help['minConsStrdDpth']= """Consensus strand depth. Minimum number of high-quality reads supporting the consensus which must be present on both the
                                forward and reverse strands to make a call."""
    help['minConsStrdBias']= """Strand bias. Minimum fraction of the high-quality consensus-supporting reads which must be present on both the
                                forward and reverse strands to make a call. The numerator of this fraction is the number of high-quality
                                consensus-supporting reads on one strand.  The denominator is the total number of high-quality consensus-supporting 
                                reads on both strands combined."""
    help['verbose']        = """Verbose message level (0=no info, 5=lots)"""

    parser.add_argument(                          dest='allPileupFile',  type=str,                                                        help=help['allPileupFile'])
    parser.add_argument('-f', '--force',          dest='forceFlag',      action='store_true',                                             help=help['force'])
    parser.add_argument('-l', '--snpListFile',    dest='snpListFile',    type=str,            default='snplist.txt',      metavar='FILE', help=help['snpListFile'])
    parser.add_argument('-o', '--output',         dest='consensusFile',  type=str,            default='consensus.fasta',  metavar='FILE', help=help['output'])
    parser.add_argument('-q', '--minBaseQual',    dest='minBaseQual',    type=int,            default=0,                  metavar='INT',  help=help['minBaseQual'])
    parser.add_argument('-c', '--minConsFreq',    dest='minConsFreq',    type=minConsFreq,    default=0.60,               metavar='FREQ', help=help['minConsFreq'])
    parser.add_argument('-d', '--minConsStrdDpth',dest='minConsStrdDpth',type=int,            default=0,                  metavar='INT',  help=help['minConsStrdDpth'])
    parser.add_argument('-b', '--minConsStrdBias',dest='minConsStrdBias',type=minConsStrdBias,default=0,                  metavar='FREQ', help=help['minConsStrdBias'])
    parser.add_argument('-v', '--verbose',        dest='verbose',        type=int,            default=1,                  metavar='0..5', help=help['verbose'])
    parser.add_argument('--version', action='version', version='%(prog)s version ' + __version__)
    args_dict = vars(parser.parse_args())

    utils.set_logging_verbosity(args_dict)
    snppipeline.set_logging_verbosity(args_dict)
    snppipeline.call_consensus(args_dict)
