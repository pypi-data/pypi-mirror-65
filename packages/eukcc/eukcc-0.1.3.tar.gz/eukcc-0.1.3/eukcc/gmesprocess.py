import gffutils
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
import os
from pyfaidx import Fasta
codonsun = { 
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T', 
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',                  
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P', 
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R', 
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A', 
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G', 
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L', 
        'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_', 
        'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W', 
    } 

def mergeOverlaps(intervals):
    '''https://codereview.stackexchange.com/a/69249'''
    sorted_by_lower_bound = sorted(intervals, key=lambda tup: tup[0])
    merged = []

    for higher in sorted_by_lower_bound:
        if not merged:
            merged.append(higher)
        else:
            lower = merged[-1]
            # test for intersection between lower and higher:
            # we know via sorting that lower[0] <= higher[0]
            if higher[0] <= lower[1]:
                upper_bound = max(lower[1], higher[1])
                merged[-1] = [lower[0], upper_bound]  # replace by merged interval
            else:
                merged.append(higher)

    return(merged)

class peptide():
    def __init__(self, name):
        self.name = name
        self.dnaseq = ""
        #self.protseq = self.translate(self.dnaseq)
        self.strand = "."
        self.chrom = None
        self.start = None
        self.stop = None
        self.frags = []
    
    def translate(self, seq):
        return(seq)
    
    def collapseRanges(self):
        self.frags = mergeOverlaps(self.frags)
        
        
        
def reverse_complement(dna):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return ''.join([complement[base] for base in dna[::-1]])


class gmespostprocess():
    """
    A class to postprocess the genemark ES output.
    I reads the GTF file and extracts protein sequences
    It names the protein sequences and also creates a bed file
    indicating the locations of each peptide.
    """
    def __init__(self, gtf, fasta, faaoutfile = "f.faa", bedoutfile = "f.bed", tmpdir = "."):
        

        #self.proteins = self.readGTF(gtf)
        #self.fasta = self.readFasta(fasta)
        #self.extractDNA()
        ga = self.addTranscriptToGTF(gtf, os.path.join(tmpdir, "renamed.gtf"))
        #fa = self.removespacesfromfile(fasta, os.path.join(tmpdir, "renamed.fasta"))
        #ga = self.removespacesfromfile(gtf, os.path.join(tmpdir, "renamed.gtf"))
        
        db = gffutils.create_db(ga, ':memory:', merge_strategy="create_unique", keep_order=False)
        #2myFasta = Fasta(fa)

        for t in db.features_of_type('transcript', order_by='start'): 
            print(t.id)
            print(t)
            print(t.start)
            print( db.children(t.id))
            for c in db.children(t.id):
                print(c)
            for i in db.children(t.id, featuretype='CDS', order_by='start'): # or exon/intron
                print(i)
                seq = i.sequence(myFasta, use_strand=True)
                print(seq)
            break
    
    def removespacesfromfile(self, file, outfile, gtf = True):
        with open(outfile, "w") as of:
            with open(file) as f:
                for l in f:
                    l = l.replace(" ", "")
                    of.write(l)
        return(outfile)
        
    def addTranscriptToGTF(self, gtf, out, comment = "#"):
        return(out)
        # keep track of names
        names = {}
        i = 1
        # all proteins as list
        proteins = {}
        with open(out, "w") as of:
            with open(gtf) as f:
                for line in f:
                    # skip comment lines
                    if line.startswith(comment):
                        continue
                    l = line.split("\t")
                    name = "_".join(l[8].split())
                    if name not in names.keys():
                        names[name] = {'name': "t_{}".format(i),
                                       "p":[],
                                       "l": l}
                        i += 1
                    # save all feature locations in a list
                    names[name]['p'].append(int(l[3]))
                    names[name]['p'].append(int(l[4]))
                    
                    # write lines
                    line = line.replace(" ", "")
                    of.write(line)

            for n, v in names.items():
                #print(v['name2'], min(v['p']), max(v['p']))
                l = v['l']
                l[3] = str(min(v['p']))
                l[4] = str(max(v['p']))
                l[2] = 'transcript'
                l[7] = "."
                line = "\t".join(l)
                line = line.replace(" ", "")
                of.write(line)
        return(out)
                
        
    def readFasta(self, file):
        seqs = {}
        with open(file) as f:
            for line in f:
                if line.startswith(">"):
                    name = line.strip()
                    name = name.replace(">","")
                    seqs[name] = ""
                else:
                    seqs[name] += line.strip()
        return(seqs)
            
    
    def extractDNA(self):
        """
        get all DNA for each protein
        """
        j = 10
        for name, protein in self.proteins.items():
            # collapse coding sequences
            print("\n",name)
            # reverse order os frags if on reverse strand
            if protein.strand == "-":
                protein.frags.reverse()
                
            #protein.collapseRanges()
            for r in protein.frags:
                #print(r)
                ns = self.fasta[protein.chrom][r[0]-1:r[1]+1].upper()
                # reverse seq if needed
                if protein.strand == "-":
                    ns = self.fasta[protein.chrom][r[0]-1:r[1]].upper()
                    #print(ns)
                    ns = reverse_complement(ns)
                    #print(ns)
                # make exon a multiple of 3
                
                if (len(ns) % 3) != 0:
                    print("trimming", len(ns)/3)
                    ns = ns[:-(len(ns) % 3)]
                else:
                    print("no trimming")
                #print(ns)
                # concatenate seq
                #if  protein.dnaseq == "":
                protein.dnaseq += ns
            

            seq  = protein.dnaseq
            pseq = ""
            if len(seq)%3 == 0: 
                for i in range(0, len(seq), 3): 
                    codon = seq[i:i + 3] 
                    pseq+= codonsun[codon] 
            print("protein:", protein.name, protein.strand, protein.frags)
            #print(protein.dnaseq)
            print(pseq)
            
            j -= 1
            if j < 0:
                break
                
            
            
    
    def readGTF(self, gtf, sep = "\t", comment = "#", n = "peptide_"):
        # keep track of names
        names = {}
        i = 0
        # all proteins as list
        proteins = {}
        with open(gtf) as f:
            for line in f:
                # skip comment lines
                if line.startswith(comment):
                    continue
                # split lines
                l = (line.split(sep))
                # get entry type. keep coding seqs
                feature = l[2]
                if feature in ['CDS']:
                    start = int(l[3])
                    stop = int(l[4])
                    strand = l[6]
                    # determine the frame of the first codon
                    frame = l[7]
                    if frame != ".":
                        if strand == "+":
                            start = start + int(frame)
                        elif strand == "-":
                            start = start - 1
                            stop = stop - int(frame)
                            

                    # join whitespace to string
                    name = "_".join(l[8].split())
                    if name not in names.keys():
                        names[name] = "{}{}".format(n, i)
                        
                        proteins[name] = peptide(names[name])
                        proteins[name].chrom = l[0].strip()
                        proteins[name].strand = strand
                        i += 1
                    locs = [start, stop]
                    proteins[name].frags.append([min(locs), max(locs)])
        return(proteins)
                    
                    
                
                
                
        
        
if __name__ == "__main__":
    import sys
    gtf = sys.argv[1]
    fasta = sys.argv[2]
    # execute only if run as a script
    gmespostprocess(gtf, fasta)