import os

from Bio import SeqIO


def gbed_gene_genbank(f_genbank):
    """
    Parse and generate BED file for genes in GenBank file
    """
    assert os.path.exists(f_genbank)
    with open(f_genbank, "r") as handle:
        for record in SeqIO.parse(handle, "genbank"):  # parser
            cid = record.id.split(".")[0]
            for feat in record.features:
                if feat.type == 'gene':
                    name = feat.qualifiers['gene'][0]
                    start = feat.location.start
                    end = feat.location.end
                    yield (cid, start, end, name, 0, '+',
                           start, end, '0,0,0', 1, end - start, 0)
