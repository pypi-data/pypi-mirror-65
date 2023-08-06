#!/usr/bin/env python
"""
Genome modeling
"""


class Genome:
    """
    Genome with single chromosome
    """
    def __init__(self, name, seq=""):
        """Genome name and sequence"""
        self.name = name
        self.seq = seq.upper()

    def __str__(self):
        return "%s: %d bp" % (self.name, len(self))

    def __len__(self):
        return len(self.seq)

    @staticmethod
    def revcompl(dna):
        """
        Reverse Complement given DNA sequence
        :return: str
        """
        complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
        return "".join([complement[base] for base in reversed(dna)])

    @staticmethod
    def gc(dna):
        """Compute GC-content of any DNA sequence"""
        ngc = dna.count('G') + dna.count('C')
        return float(ngc) / len(dna)

    def set_genome(self, ffa):
        """Set genome sequence from Fasta file"""
        seq = ""
        for line in open(ffa):
            if line.startswith(">"):
                continue
            seq += line.rstrip()
        self.seq = seq.upper()

    def len(self):
        """Get genome length"""
        return len(self.seq)

    def gc_content(self):
        """Compute whole genome GC-content"""
        if len(self) <= 0:
            return None
        ngc = self.seq.count('G') + self.seq.count('C')
        return float(ngc) / len(self)

    def gc_by_window(self, window=10):
        """Compute GC-content by given window size"""
        gcli = []
        for i in range(0, int(len(self) / window)):
            dna = self.seq[(i * window):((i + 1) * window)]
            gcli.append(Genome.gc(dna))
        return gcli

    def find_all(self, sub):
        """Generator of matched index for given subsequence"""
        start = 0
        while True:
            start = self.seq.find(sub, start)
            if start == -1:
                return
            yield start
            start += len(sub)  # use start += 1 to find overlapping matches

    def amplicon(self, fwd, rev):
        """
        Compute amplicon for given primer pair
        Return None if any primer's occurrence not equal to 1
        """
        revrc = Genome.revcompl(rev)
        fwdli = list(self.find_all(fwd))
        revli = list(self.find_all(revrc))
        if len(fwdli) != 1 or len(revli) != 1:
            return None
        fstart, rstart = fwdli[0], revli[0]
        rend = rstart + len(revrc)
        return fstart, rend

    def ivs_to_bed(self, ivs, name="iv", rgb='255,0,0'):
        """
        Convert sorted intervals [(s, e), ..] to BED12
        """
        assert len(ivs) >= 1
        start = ivs[0][0]
        end = ivs[-1][1]
        nblocks = len(ivs)
        lenblocks = [e[1] - e[0] for e in ivs]
        sblocks = [e[0] - start for e in ivs]
        return (self.name, start, end, name, 0, '+',
                start, end, rgb,
                nblocks,
                ",".join(map(str, lenblocks)),
                ",".join(map(str, sblocks)))

    def amplicon_bed(self, fwd, rev, name, rgb):
        """
        Make BED12 for amplicon by primer pair (fwd, rev)
        """
        ival = self.amplicon(fwd, rev)
        assert ival is not None
        exons = [
            (ival[0], ival[0] + len(fwd)),
            (ival[1] - len(rev), ival[1])]
        return self.ivs_to_bed(exons, name, rgb)

    def basefreq(self):
        return {b: self.seq.count(b) for b in 'ACGTN'}
