import argparse
import logging
import os
from pkg_resources import resource_filename
import sys

import numpy as np
import pysam

import medaka.common
import medaka.datastore
import medaka.features
import medaka.labels
import medaka.methdaka
import medaka.prediction
import medaka.rle
import medaka.smolecule
import medaka.stitch
import medaka.training
import medaka.variant
import medaka.vcf


# TODO: should revisit this
# commented models are deprecated and remove from repo
model_store = resource_filename(__package__, 'data')
allowed_models = [
    ## r9 consensus
    # 'r941_min_fast_g303',
    # 'r941_min_high_g303',
    'r941_min_high_g330',
    'r941_min_high_g344',
    'r941_min_high_g351',
    # 'r941_prom_fast_g303',
    # 'r941_prom_high_g303',
    'r941_prom_high_g330',
    'r941_prom_high_g344',
    'r941_prom_high_g351',
    ## rle consensus
    'r941_min_high_g340_rle',
    ## r10 consensus
    # 'r10_min_high_g303',
    # 'r10_min_high_g340',
    'r103_min_high_g345',
    ## snp and variant
    # 'r941_prom_snp_g303',
    # 'r941_prom_variant_g303',
    'r941_prom_snp_g322',
    'r941_prom_variant_g322',
    'r103_prom_snp_g3210',
    'r103_prom_variant_g3210',
]
default_consensus_model = 'r941_min_high_g351'
default_snp_model = 'r941_prom_snp_g322'
default_variant_model = 'r941_prom_variant_g322'
for m in (default_consensus_model, default_snp_model, default_variant_model):
    if m not in allowed_models:
        raise ValueError(
            "'{}' is listed as a default model but is not an allowed model.".format(
                m))
model_dict = {
    k:os.path.join(model_store, '{}_model.hdf5'.format(k))
    for k in allowed_models
}


class ResolveModel(argparse.Action):
    """Resolve model filename or ID into filename"""
    def __init__(self, option_strings, dest, default=None, required=False, help='Model file.'):
        super().__init__(
            option_strings, dest, nargs=1, default=default, required=required,
            help='{} {{{}}}'.format(help, ', '.join(allowed_models))
        )

    def __call__(self, parser, namespace, values, option_string=None):
        val = values[0]
        if not os.path.exists(val):
            # try lookup
            try:
                val = model_dict[val]
            except:
                raise RuntimeError(
                    "Filepath for '--{}' argument does not exist and is not a known model ID ({})".format(
                        self.dest, val)
                )
            #TODO: verify the file is a model?
        setattr(namespace, self.dest, val)


class CheckBam(argparse.Action):
    """Check a bam is a bam."""

    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.exists(values):
            raise RuntimeError(
                "Filepath for '--{}' argument does not exist ({})".format(
                    self.dest, values)
            )
        try:
            with pysam.AlignmentFile(values) as bam:
                # just to check its a bam
                _ = bam.references
        except Exception:
            raise IOError('The bam {} could not be read.'.format(values))
        setattr(namespace, self.dest, values)

    @staticmethod
    def count_read_groups(fname):
        """Count the number of read groups (RG tag) defined in bam header.

        :param fname: bam file name.

        :returns: number of read groups.
        """
        with pysam.AlignmentFile(fname) as bam:
            # As of 13/12/19 pypi still has no wheel for pysam v0.15.3 so we
            # pinned to v0.15.2. However bioconda's v0.15.2 package
            # conflicts with the libdeflate they have so we are forced
            # to use newer versions. Newer versions however have a
            # different API, sigh...
            try:
                header_dict = bam.header.as_dict()
            except AttributeError:
                header_dict = bam.header
            if 'RG' not in header_dict:
                return 0
            else:
                return len(header_dict['RG'])



class CheckIsBed(argparse.Action):
    """Check if --region option is a bed file."""

    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) == 1 and os.path.exists(values[0]):
            # parse bed file
            regions = []
            for chrom, start, stop in medaka.common.yield_from_bed(values[0]):
                regions.append('{}:{}-{}'.format(chrom, start, stop))
            setattr(namespace, self.dest, regions)
        else:
            setattr(namespace, self.dest, values)


def _log_level():
    """Parser to set logging level and acquire software version/commit"""

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)

    #parser.add_argument('--version', action='version', version=get_version())

    modify_log_level = parser.add_mutually_exclusive_group()
    modify_log_level.add_argument('--debug', action='store_const',
        dest='log_level', const=logging.DEBUG, default=logging.INFO,
        help='Verbose logging of debug information.')
    modify_log_level.add_argument('--quiet', action='store_const',
        dest='log_level', const=logging.WARNING, default=logging.INFO,
        help='Minimal logging; warnings only).')

    return parser


def _model_arg():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
    parser.add_argument('--model', action=ResolveModel, default=model_dict[default_consensus_model],
            help='Model definition, default is equivalent to {}.'.format(default_consensus_model))
    parser.add_argument('--allow_cudnn', dest='allow_cudnn', default=True, action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--disable_cudnn', dest='allow_cudnn', default=False, action='store_false',
            help='Disable use of cuDNN model layers.')
    return parser


def _chunking_feature_args(batch_size=100, chunk_len=10000, chunk_ovlp=1000):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
    parser.add_argument('--batch_size', type=int, default=batch_size, help='Inference batch size.')
    parser.add_argument('--regions', default=None, action=CheckIsBed, nargs='+',
                        help='Genomic regions to analyse, or a bed file.')
    parser.add_argument('--chunk_len', type=int, default=chunk_len, help='Chunk length of samples.')
    parser.add_argument('--chunk_ovlp', type=int, default=chunk_ovlp, help='Overlap of chunks.')
    return parser


def print_model_path(args):
    print(os.path.abspath(args.model))


def is_rle_encoder(args):
    rle_encoders = [medaka.features.HardRLEFeatureEncoder]
    model = medaka.datastore.DataStore(args.model)
    encoder = model.get_meta('feature_encoder')
    is_rle = any((isinstance(encoder, x) for x in rle_encoders))
    print(is_rle)


def print_all_models(args):
    print('Available:', ', '.join(allowed_models))
    print('Default consensus: ', default_consensus_model)
    print('Default SNP: ', default_snp_model)
    print('Default variant: ', default_variant_model)


def fastrle(args):
    import libmedaka
    libmedaka.lib.fastrle(args.input.encode())


class StoreDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        """Converts 'key1=value1 key2=value1a,value2a' to a dictionary.

        List values are supported, as are simple type conversions.
        """
        str_to_type = {
            'None': None,
            'True': True, 'False': False,
            'true': True, 'false': False,
            'TRUE': True, 'FALSE': False}

        def _str_to_numeric(x):
            if not isinstance(x, str):
                return x
            try:
                return int(x)
            except:
                try:
                    return float(x)
                except:
                    return x

        my_dict = {}
        for kv in values:
            key, value = kv.split("=")
            list_like = ',' in value
            value = str_to_type.get(value, value)
            if value is not None:
                if list_like:
                    value = [_str_to_numeric(str_to_type.get(x,x))
                        for x in value.split(',')]
                else:
                    value = _str_to_numeric(value)
            my_dict[key] = value
        setattr(namespace, self.dest, my_dict)


def main():
    from medaka import __version__

    pymajor, pyminor = sys.version_info[0:2]
    if (pymajor < 3) or (pyminor not in {5, 6}):
        raise RuntimeError(
            '`medaka` is unsupported on your version of python, '
            'please use python 3.5 or python 3.6.')

    parser = argparse.ArgumentParser('medaka',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(title='subcommands', description='valid commands', help='additional help', dest='command')
    subparsers.required = True

    parser.add_argument('--version', action='version',
        version='%(prog)s {}'.format(__version__))

    # Compress bam file_ext
    rparser = subparsers.add_parser('compress_bam',
        help='Compress an alignment into RLE form. ',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    rparser.set_defaults(func=medaka.rle.compress_bam)
    rparser.add_argument('bam_input', help='Bam file to compress.')
    rparser.add_argument('bam_output', help='Output bam file.')
    rparser.add_argument('ref_fname',
                         help='Reference fasta file used for `bam_input`.')
    rparser.add_argument('--threads', type=int, default=1,
                         help='Number of threads for parallel execution.')
    rparser.add_argument('--regions', default=None, nargs='+', action=CheckIsBed,
                         help='Genomic regions to analyse, or .bed file.')

    rparser.add_argument(
        '--use_fast5_info', metavar='<fast5_dir> <index>', default=None,
        nargs=2, help=(
            'Root directory containing the fast5 files and .tsv file with '
            'columns filename and read_id.'))


    # Creation of feature files
    fparser = subparsers.add_parser('features',
        help='Create features for inference.',
        parents=[_log_level(), _chunking_feature_args()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    fparser.set_defaults(func=medaka.features.create_samples)
    fparser.add_argument('bam', help='Input alignments.', action=CheckBam)
    fparser.add_argument('output', help='Output features file.')
    fparser.add_argument('--truth', help='Bam of truth aligned to ref to create features for training.')
    fparser.add_argument('--truth_haplotag', help='Two-letter tag defining haplotype of alignments for polyploidy labels.')
    fparser.add_argument('--threads', type=int, default=1, help='Number of threads for parallel execution.')
    # TODO: enable other label schemes.
    fparser.add_argument('--label_scheme', default='HaploidLabelScheme', help='Labelling scheme.',
                         choices=sorted(medaka.labels.label_schemes))
    fparser.add_argument('--label_scheme_args', action=StoreDict, nargs='+',
        default=dict(), metavar="KEY1=VAL1 KEY2=VAL2a,VAL2b...",
        help="Label scheme key-word arguments.")
    fparser.add_argument('--feature_encoder', default='CountsFeatureEncoder',
        help='FeatureEncoder used to create the features.',
        choices=sorted(medaka.features.feature_encoders))
    fparser.add_argument('--feature_encoder_args', action=StoreDict, nargs='+',
        default=dict(), metavar="KEY1=VAL1 KEY2=VAL2a,VAL2b...",
        help="Feature encoder key-word arguments.")

    # Training program
    tparser = subparsers.add_parser('train',
        help='Train a model from features.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    tparser.set_defaults(func=medaka.training.train)
    tparser.add_argument('features', nargs='+', help='Paths to training data.')
    tparser.add_argument('--train_name', type=str, default='keras_train', help='Name for training run.')
    tparser.add_argument('--model', action=ResolveModel, help='Model definition and initial weights .hdf, or .yml with kwargs to build model.')
    tparser.add_argument('--epochs', type=int, default=5000, help='Maximum number of trainig epochs.')
    tparser.add_argument('--batch_size', type=int, default=100, help='Training batch size.')
    tparser.add_argument('--max_samples', type=int, default=np.inf, help='Only train on max_samples.')
    tparser.add_argument('--mini_epochs', type=int, default=1, help='Reduce fraction of data per epoch by this factor')
    tparser.add_argument('--seed', type=int, help='Seed for random batch shuffling.')
    tparser.add_argument('--threads_io', type=int, default=1, help='Number of threads for parallel IO.')
    tparser.add_argument('--device', type=int, default=0, help='GPU device to use.')
    tparser.add_argument('--optimizer', type=str, default='rmsprop', choices=['nadam','rmsprop'], help='Optimizer to use.')
    tparser.add_argument('--optim_args', action=StoreDict, default=None, nargs='+',
        metavar="KEY1=VAL1,KEY2=VAL2...", help="Optimizer key-word arguments.")

    vgrp = tparser.add_mutually_exclusive_group()
    vgrp.add_argument('--validation_split', type=float, default=0.2, help='Fraction of data to validate on.')
    vgrp.add_argument('--validation_features', nargs='+', default=None, help='Paths to validation data')

    # Consensus from bam input
    cparser = subparsers.add_parser('consensus',
        help='Run inference from a trained model and alignments.',
        parents=[_log_level(), _chunking_feature_args(), _model_arg()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    cparser.add_argument('bam', help='Input alignments.', action=CheckBam)
    cparser.set_defaults(func=medaka.prediction.predict)
    cparser.add_argument('output', help='Output file.')
    cparser.add_argument('--threads', type=int, default=1, help='Number of threads used by inference.')
    cparser.add_argument('--check_output', action='store_true', default=False,
            help='Verify integrity of output file after inference.')
    cparser.add_argument('--save_features', action='store_true', default=False,
            help='Save features with consensus probabilities.')
    tag_group = cparser.add_argument_group('filter tag', 'Filtering alignments by an integer valued tag.')
    tag_group.add_argument('--tag_name', type=str, help='Two-letter tag name.')
    tag_group.add_argument('--tag_value', type=int, help='Value of tag.')
    tag_group.add_argument('--tag_keep_missing', action='store_true', help='Keep alignments when tag is missing.')
    rg_group = cparser.add_argument_group('read group', 'Filtering alignments the read group (RG) tag, expected to be string value.')
    rg_group.add_argument('--RG', metavar='READGROUP', type=str, help='Read group to select.')


    # Consensus from single-molecules with subreads
    smparser = subparsers.add_parser('smolecule',
        help='Create consensus sequences from single-molecule reads.',
        parents=[_log_level(), _chunking_feature_args(batch_size=100, chunk_len=1000, chunk_ovlp=500), _model_arg()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    smparser.add_argument('fasta', nargs='+', help='Single-molecule reads, one file per read.')
    smparser.set_defaults(func=medaka.smolecule.main)
    smparser.add_argument('output', help='Output directory.')
    smparser.add_argument('--depth', type=int, default=3, help='Minimum subread count.')
    smparser.add_argument('--length', type=int, default=400, help='Minimum median subread length.')
    smparser.add_argument('--threads', type=int, default=1, help='Number of threads used by inference.')
    smparser.add_argument('--check_output', action='store_true', default=False,
            help='Verify integrity of output file after inference.')
    smparser.add_argument('--save_features', action='store_true', default=False,
            help='Save features with consensus probabilities.')

    # Consensus from features input
    cfparser = subparsers.add_parser('consensus_from_features',
        help='Run inference from a trained model on existing features.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    cfparser.add_argument('features', nargs='+', help='Pregenerated features (from medaka features).')
    cfparser.add_argument('--model', action=ResolveModel, default=default_consensus_model, help='Model definition.')

    # Compression of fasta/q to quality-RLE fastq
    rleparser = subparsers.add_parser('fastrle',
        help='Create run-length encoded fastq (lengths in quality track).',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    rleparser.set_defaults(func=fastrle)
    rleparser.add_argument('input', help='Input fasta/q. may be gzip compressed.')

    # Post-processing of consensus outputs
    sparser = subparsers.add_parser('stitch',
        help='Stitch together output from medaka consensus into final output.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    sparser.set_defaults(func=medaka.stitch.stitch)
    sparser.add_argument('inputs', nargs='+', help='Consensus .hdf files.')
    sparser.add_argument('output', help='Output .fasta.', default='consensus.fasta')
    sparser.add_argument('--regions', default=None, nargs='+', help='Limit stitching to these reference names')
    sparser.add_argument('--jobs', default=1, type=int, help='Number of worker processes to use.')

    var_parser = subparsers.add_parser('variant',
        help='Decode probabilities to VCF.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    var_parser.set_defaults(func=medaka.variant.variants_from_hdf)
    var_parser.add_argument('ref_fasta', help='Reference sequence .fasta file.')
    var_parser.add_argument('inputs', nargs='+', help='Consensus .hdf files.')
    var_parser.add_argument('output', help='Output .vcf.', default='medaka.vcf')
    var_parser.add_argument('--regions', default=None, nargs='+',
                         help='Limit variant calling to these reference names')
    var_parser.add_argument('--verbose', action='store_true',
                         help='Populate VCF info fields.')

    # TODO do we still need this?
    snp_parser = subparsers.add_parser('snp',
        help='Decode probabilities to SNPs.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    snp_parser.set_defaults(func=medaka.variant.snps_from_hdf)
    snp_parser.add_argument('ref_fasta', help='Reference sequence .fasta file.')
    snp_parser.add_argument('inputs', nargs='+', help='Consensus .hdf files.')
    snp_parser.add_argument('output', help='Output .vcf.', default='medaka.vcf')
    snp_parser.add_argument('--regions', default=None, nargs='+', help='Limit variant calling to these reference names')
    snp_parser.add_argument('--threshold', default=0.04, type=float,
                         help='Threshold for considering secondary calls. A value of 1 will result in haploid decoding.')
    snp_parser.add_argument('--ref_vcf', default=None, help='Reference vcf.')
    snp_parser.add_argument('--verbose', action='store_true',
                         help='Populate VCF info fields.')

    # Methylation
    methparser = subparsers.add_parser('methylation',
        help='methylation subcommand.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    methsubparsers = methparser.add_subparsers(
        title='methylation', description='valid methylation commands', help='additional help', dest='meth_command')

    hdf2samparser = methsubparsers.add_parser('guppy2sam',
        help='Convert Guppy .fast5 files with methylation calls to .sam file, output to stdout.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    hdf2samparser.set_defaults(func=medaka.methdaka.hdf_to_sam)
    hdf2samparser.add_argument('path', help='Input path for .fast5 files.')
    hdf2samparser.add_argument('--reference',
        help='.fasta containing reference sequence(s). If not given output will be unaligned sam.')
    hdf2samparser.add_argument('--workers', type=int, default=16, help='Number of alignment threads.')
    hdf2samparser.add_argument('--io_workers', type=int, default=4, help='Number of .fast5 reader processes.')
    hdf2samparser.add_argument('--recursive', action='store_true', help='Search for .fast5s recursively.')

    methcallparser = methsubparsers.add_parser('call',
        help='Call methylation from .bam file.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    methcallparser.set_defaults(func=medaka.methdaka.call_methylation)
    methcallparser.add_argument('bam', help='Input .bam file (via `medaka methylation guppy2sam`).')
    methcallparser.add_argument('reference', help='.fasta containing reference sequence(s).')
    methcallparser.add_argument('region', help='bam region to process (chrom:start-end).')
    methcallparser.add_argument('output', help='Output file name.')
    methcallparser.add_argument('--meth', default='cpg', choices=list(medaka.methdaka.MOTIFS.keys()), help='methylation type.')
    methcallparser.add_argument(
            '--filter', type=int, nargs=2, default=(64, 128),
            metavar=('upper', 'lower'), help='Upper (lower) score boundary to call canonical (methylated) base. Scores are in the range [0, 256].')
    rg_group = methcallparser.add_argument_group('read group', 'Filtering alignments the read group (RG) tag, expected to be string value.')
    rg_group.add_argument('--RG', metavar='READGROUP', type=str, help='Read group to select.')

    # Tools
    toolparser = subparsers.add_parser('tools',
        help='tools subcommand.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    toolsubparsers = toolparser.add_subparsers(title='tools', description='valid tool commands', help='additional help', dest='tool_command')

    # merge two haploid VCFs into a diploid VCF.
    h2dparser = toolsubparsers.add_parser('haploid2diploid',
        help='Merge two haploid VCFs into a diploid VCF.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    h2dparser.set_defaults(func=medaka.vcf.haploid2diploid)
    h2dparser.add_argument('vcf1', help='Input .vcf file.')
    h2dparser.add_argument('vcf2', help='Input .vcf file.')
    h2dparser.add_argument('ref_fasta', help='Reference .fasta file.')
    h2dparser.add_argument('vcfout', help='Output .vcf.')
    h2dparser.add_argument('--discard_phase', default=False,
                           action='store_true', help='output unphased diploid vcf')
    h2dparser.add_argument('--adjacent', action='store_true',
                         help=('Merge adjacent variants (i.e. variants with non-overlapping genomic ranges) instead' +
                               ' of just overlapping ones. If set to True, all runs of adjacent variants will be' +
                               ' merged including those which appear in just one of the input VCFs.'))

    # split a diploid VCF into two haploid VCFs.
    d2hparser = toolsubparsers.add_parser('diploid2haploid',
        help='Split a diploid VCF into two haploid VCFs.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    d2hparser.set_defaults(func=medaka.vcf.diploid2haploid)
    d2hparser.add_argument('vcf', help='Input .vcf file.')
    d2hparser.add_argument('--notrim', action='store_true',
                         help='Do not trim variant to minimal ref and alt and update pos.')

    # classify variants in a vcf writing new vcfs containing subs, indels etc.
    clparser = toolsubparsers.add_parser('classify_variants',
        help='Classify variants and write vcf for each type and subtype.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    clparser.set_defaults(func=medaka.vcf.classify_variants)
    clparser.add_argument('vcf', help='Input .vcf file.')
    clparser.add_argument('--replace_info', action='store_true',
                         help='Replace info tag (useful for visual inspection of types).')

    # convert a vcf to tsv
    tsvparser = toolsubparsers.add_parser('vcf2tsv',
        help='convert vcf to tsv, unpacking info and sample columns.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    tsvparser.set_defaults(func=medaka.vcf.vcf2tsv)
    tsvparser.add_argument('vcf', help='Input .vcf file.')

    # find homozygous and heterozygous regions in a VCF
    hzregparser = toolsubparsers.add_parser('homozygous_regions',
        help='Find homozygous regions from a diploid vcf.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    hzregparser.set_defaults(func=medaka.vcf.get_homozygous_regions)
    hzregparser.add_argument('vcf', help='Input .vcf file.')
    hzregparser.add_argument('region', help='Genomic region within which to find homozygous sub-regions.')
    hzregparser.add_argument('--min_len', type=int, default=1000,
                             help='Minimum region length.')
    hzregparser.add_argument('--suffix', help='Output suffix.', default='regions.txt')

    # resolve model and print full model file path to screen
    rmparser = toolsubparsers.add_parser('resolve_model',
        help='Resolve model and print full file path.',
        parents=[_log_level(), _model_arg()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    rmparser.set_defaults(func=print_model_path)

    # check if feature encoder is RLE
    rleparser = toolsubparsers.add_parser('is_rle_model',
        help='Check if a model is an RLE model.',
        parents=[_model_arg()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    rleparser.set_defaults(func=is_rle_encoder)

    # append RLE tags to a bam from hdf
    rlebamparser = toolsubparsers.add_parser('rlebam',
        description='Add RLE tags from HDF to bam. (input bam from stdin)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    rlebamparser.add_argument('read_index', help='Two column .tsv mapping read_ids to .hdf filepaths.')
    rlebamparser.add_argument('--workers', type=int, default=4, help='Number of worker processes.')
    rlebamparser.set_defaults(func=medaka.rle.rlebam)

    # print all model tags followed by default
    lmparser = toolsubparsers.add_parser('list_models',
        help='List all models.',
        parents=[_log_level(), _model_arg()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    lmparser.set_defaults(func=print_all_models)

    # write a bed file of regions spanned by a hdf feature / probs file.
    bdparser = toolsubparsers.add_parser('hdf_to_bed',
        help='Write a bed file of regions spanned by a hdf file.',
        parents=[_log_level()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    bdparser.set_defaults(func=medaka.variant.samples_to_bed)
    bdparser.add_argument('inputs', nargs='+',
                          help='Consensus .hdf files.')
    bdparser.add_argument('output', help='Output .bed.', default='medaka.bed')

    args = parser.parse_args()

    # https://github.com/tensorflow/tensorflow/issues/26691
    # we have local imports of tf generally, but this is pseudo global
    # however with tf1.14 tensorflow import time looks faster than previous
    # so we could/should stick to more standard imports
    import tensorflow as tf
    import absl.logging
    logging.root.removeHandler(absl.logging._absl_handler)
    absl.logging._warn_preinit_stderr = False

    logging.basicConfig(format='[%(asctime)s - %(name)s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
    logger = logging.getLogger(__package__)
    logger.setLevel(args.log_level)

    if args.command == 'tools' and not hasattr(args, 'func'):
        # display help if given `medaka tools (--help)`
        toolparser.print_help()
    elif args.command == 'methylation' and not hasattr(args, 'func'):
        methparser.print_help()
    else:
        # do some common argument validation here
        if hasattr(args, 'bam') and args.bam is not None:
            if hasattr(args, 'RG') and args.RG is not None:
                num_rg = CheckBam.count_read_groups(args.bam)
                if num_rg > 1 and args.RG:
                    raise RuntimeError(
                        'The bam {} contains more than one read group. '
                        'Please specify `--RG` to select which read group'
                        'to process'.format(values))
                else:
                    logger.info(
                        "Reads will be filtered to only those with RG tag: {}".format(args.RG))
        args.func(args)
