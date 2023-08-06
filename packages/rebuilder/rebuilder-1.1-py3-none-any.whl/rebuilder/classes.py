from Bio.PDB.Model import Model
from Bio.PDB.Chain import Chain
from Bio.PDB.NeighborSearch import NeighborSearch
from Bio import pairwise2


class DerivedModel(Model):
    def add(self, other):
        other.set_parent(self)
        self.child_list.append(other)

    def has_clashes_with(self, moving):
        backbone = {"CA", "C1\'", "P"}
        moving_atoms = moving.backbone_atoms()
        model_atoms = [atom for atom in self.get_iterator() if atom.id in backbone]
        ns = NeighborSearch(model_atoms)
        clashes = 0
        for atom in moving_atoms:
            clashes += bool(ns.search(atom.coord, 2))
        if clashes/len(moving_atoms) >= 0.03:
            return True
        else:
            return False

    # def save_to_mmcif(self, out_name):
    #     """Saves a model using the given output name in the cwd"""
    #     io = MMCIFIO()
    #     io.set_structure(self)
    #     try:
    #         io.save(out_name + ".cif")
    #         print(out_name + ".cif saved")
    #     except:
    #         sys.stderr.write("Couldn't save models to current working directory. "
    #                          "Make sure you have permission to write files")


class DerivedChain(Chain):
    superimposed = False
    protein_dict = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
                    'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N',
                    'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W',
                    'ALA': 'A', 'VAL': 'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M',
                    'UNK': 'X'}
    dna_dict = {'DA': 'A', 'DC': 'C', 'DG': 'G', 'DT': 'T'}
    rna_dict = {'A': 'A', 'C': 'C', 'G': 'G', 'U': 'U'}

    def get_sequence(self):
        sequence = ""
        first_residue = self.get_list()[0].resname.strip()
        if first_residue not in self.protein_dict:
            if "D" in first_residue:
                for res in self:
                    if res.id[0] == " ":
                        sequence += self.dna_dict[res.resname.strip()]
                        dna = True
            else:
                for res in self:
                    if res.id[0] == " ":
                        sequence += self.rna_dict[res.resname.strip()]
                        dna = False
        else:
            for res in self:
                if res.id[0] == " ":
                    sequence += self.protein_dict[res.resname]
                    dna = False
        return sequence, dna
    # def has_homology(self, unique_chains):
    #     cutoff = 0.95
    #     homologue_dict = {}
    #     sequence1 = self.get_sequence()
    #     for chain in unique_chains:
    #         sequence2 = chain.get_sequence()
    #         alignment = pairwise2.align.globalxx(sequence1, sequence2)[0]
    #         align_score = alignment[2]
    #         align_length = (len(alignment[0]))
    #         cutoff_chain = align_score / align_length
    #         if cutoff_chain > cutoff:
    #             homologue_dict[chain] = cutoff_chain
    #     if homologue_dict:
    #         homologue = max(homologue_dict, key=homologue_dict.get)
    #         return homologue
    #     else:
    #         return False

    def search_fasta_dict(self, fasta_dict, verbose):
        fasta = fasta_dict
        sequence1, dna = self.get_sequence()
        score_dict = {}
        cutoff = 0.6
        if fasta:
            for fasta_id, fasta_sequence in fasta_dict.items():
                if dna:
                    if (len(fasta_sequence)/2) % 2 == 0:
                        one_chain_only = int(len(fasta_sequence) / 2)
                    else:
                        one_chain_only = int((len(fasta_sequence) / 2) + 1)
                    sequence2 = fasta_sequence[0:one_chain_only]
                else:
                    sequence2 = fasta_sequence
                alignment = pairwise2.align.globalxx(sequence1, sequence2)[0]
                align_score = alignment[2]
                align_length = (len(alignment[0]))
                cutoff_fasta = align_score / align_length
                if cutoff_fasta > cutoff:
                    score_dict[fasta_id] = cutoff_fasta
            if score_dict:
                character = max(score_dict, key=score_dict.get)
                if verbose:
                    print("Fasta sequence with id {} shows high similarity to current chain"
                          .format([key for key, value in score_dict.items()]))
                return character
            else:
                if verbose:
                    print("None of the fasta sequences inputted shows high similarity to current chain's sequence")
                return None
        else:
            if verbose:
                print("No fasta file inputted.")
            return False

    def backbone_atoms(self):
        backbone = {"CA", "C1\'", "P"}
        return [atom for atom in self.get_iterator() if atom.id in backbone]
