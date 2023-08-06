from eukcc.eukcc import eukcc
fasta = "proteins.faa"
fasta = "/hps/nobackup2/production/metagenomics/saary/markergenes/eukcc/testdata/GCA_000208865.2._100000.fna"
config = "/homes/saary/data/databases/eukcheck"

info = eukcc(fasta, config,
        threads = 3,
           isprotein = False)
