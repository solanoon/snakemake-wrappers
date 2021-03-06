from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider
HTTP = HTTPRemoteProvider()

rule all:
    input: 'test.sorted.bam.bai'

rule sambamba_sort:
    input:
        HTTP.remote('sgp1.digitaloceanspaces.com/dohlee-bioinfo/test-data/bam/test.bam')
    output:
        'test.sorted.bam'
    wrapper:
        'sambamba/sort'

rule sambamba_index:
    input:
        'test.sorted.bam'
    output:
        'test.sorted.bam.bai'
    wrapper:
        'sambamba/index'
