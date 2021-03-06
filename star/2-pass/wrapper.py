__author__ = "Dohoon Lee"
__copyright__ = "Copyright 2018, Dohoon Lee"
__email__ = "dohlee.bioinfo@gmail.com"
__license__ = "MIT"


from snakemake.shell import shell

# Extract log.
log = snakemake.log_fmt_shell(stdout=False, stderr=True)

def optionify_input(parameter, option):
    """Return optionified parameter."""
    try:
        param = str(snakemake.input[parameter])
        if param:
            return option + ' ' + str(snakemake.input[parameter])
        else:
            return ''
    except AttributeError:
        return ''

def optionify_params(parameter, option):
    """Return optionified parameter."""
    try:
        param = str(snakemake.params[parameter])
        if param:
            return option + ' ' + str(snakemake.params[parameter])
        else:
            return ''
    except AttributeError:
        return ''

# Extract required inputs.
reads = snakemake.input.reads
if isinstance(reads, str):
    reads = [reads]
assert len(reads) in [1, 2], "Currently star/2-pass wrapper only supports single-sample analysis."
star_index = snakemake.input.star_index

# Extract required outputs.
output_sorted_bam = snakemake.output[0]
output_prefix = output_sorted_bam[:-10]  # Strip tailing 'sorted.bam'.

# Extract parameters.
# Extract optional parameters.
extra = snakemake.params.get('extra', '')
# If gzipped reads are given, but user did not specify readFilesCommand option,
# kindly add the option.
read_files_command = '--readFilesCommand cat'
if reads[0].endswith('.gz') and '--readFilesCommand' not in extra:
    read_files_command = '--readFilesCommand zcat'
sjdb_gtf_file = optionify_params('sjdb_gtf_file', '--sjdbGTFfile')
sjdb_overhang = optionify_params('sjdb_overhang', '--sjdbOverhang')
sjdb_gtf_chr_prefix = optionify_params('sjdb_gtf_chr_prefix', '--sjdbGTFchrPrefix')
sjdb_gtf_tag_exon_parent_transcript = optionify_params('sjdb_gtf_tag_exon_parent_transcript', '--sjdbGTFtagExonParentTranscript')

# rename {output_prefix}Aligned.sortedByCoord.out.bam into {output_prefix}.sorted.bam
rename_command = '&& mv {prefix}Aligned.sortedByCoord.out.bam {prefix}sorted.bam'.format(prefix=output_prefix)

# Execute shell command.
shell(
    "("
    "STAR "
    "--runMode alignReads "
    "--twopassMode Basic "
    "--runThreadN {snakemake.threads} "
    "--readFilesIn {reads} "
    "--genomeDir {star_index} "
    "--outFileNamePrefix {output_prefix} "
    "--outSAMtype BAM SortedByCoordinate "
    "{read_files_command} "
    "{extra} "
    "{sjdb_gtf_file} "
    "{sjdb_overhang} "
    "{sjdb_gtf_chr_prefix} "
    "{sjdb_gtf_tag_exon_parent_transcript} "
    "{rename_command} "
    ") "
    "{log}"
)
