from django.db import models
from django.core.exceptions import ValidationError
import os
from Bio import SeqIO, AlignIO
from Bio.Align import PairwiseAligner
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from django.core.exceptions import ObjectDoesNotExist
import subprocess
# Create your models here.


class ReferenceProtein(models.Model):
    protein_id = models.CharField(max_length=100, unique=True)
    fasta_file = models.FileField(upload_to="proteins/")    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    selected_as_main_ref = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.fasta_file.name.endswith(".fasta") or self.fasta_file.name.endswith(".fa"):
            raise ValidationError("The file must be a fasta file.")       
        
        

        if self.selected_as_main_ref:
        # Deselect all other main reference proteins
            ReferenceProtein.objects.filter(selected_as_main_ref=True).update(selected_as_main_ref=False)
        super().save(*args, **kwargs)
        self.generate_sap_address()

    def generate_sap_address(self):
        if not self.selected_as_main_ref:
            try:
                main_ref = ReferenceProtein.objects.get(selected_as_main_ref=True)
            except ObjectDoesNotExist:
                sap_address = self.protein_id
            with open(self.fasta_file.path, "r") as qf:
                query_seq = SeqIO.read(qf, "fasta").seq


        
            with open(main_ref.fasta_file.path, "r") as rf:
                ref_seq = SeqIO.read(rf, "fasta").seq
            # Perform alignment between main reference and new sequence
            input_file = "input.fasta"
            self.combined_fasta(main_ref.fasta_file.path, self.fasta_file.path, input_file)

            output_file = "aligned.fasta"
            self.run_clustalo(input_file, output_file)

            aligned_sequences = list(SeqIO.parse(output_file, "fasta"))
            aligned_ref_seq = str(aligned_sequences[0].seq)  # First sequence (reference)
            aligned_query_seq = str(aligned_sequences[1].seq)     
            
            sap_addresses = self.generate_addresses(aligned_ref_seq, aligned_query_seq, ref_seq_id=main_ref.protein_id)

            if sap_addresses:
                for sap in sap_addresses:
                    SAPAddress.objects.create(protein=self, sap_address= sap)


    # def find_saps(self, alignment):
    #     saps=[]
    #     num_sequences = len(alignment)
    #     alignment_length = alignment.get_alignment_length()

    #     # Loop over each position in the alignment
    #     for i in range(alignment_length):
    #         # Get the set of amino acids at the current position
    #         position_amino_acids = set(record.seq[i] for record in alignment)

    #         # If there's more than one unique amino acid at this position, it's a polymorphic site (SAP)
    #         if len(position_amino_acids) > 1:
    #             saps.append((i + 1, position_amino_acids))  # 1-based index for positions

    #     return saps
    
    def generate_addresses(self, ref_seq, query_seq, ref_seq_id):
        saps = []
    
        alignment_length = len(ref_seq)  # Length of the aligned sequences
        
        for i in range(alignment_length):
            # Get the amino acid in the reference sequence at the current position
            ref_aa = ref_seq[i]
            query_aa = query_seq[i]
            
            # If there's a polymorphism at this position, generate an SAP address
            if ref_aa != query_aa and query_aa != '-':  # Ignore gaps ('-')
                saps.append(f"{ref_seq_id}:{i+1}{ref_aa}>{query_aa}")
        
        return saps
    
    def run_clustalo(self, input_file, output_file):
        cmd = [
            "clustalo",              # Clustal Omega command
            "-i", input_file,        # Input file
            "-o", output_file,       # Output file for alignment
            "--auto",                # Automatically set parameters
            "-v",                    # Verbose output
            "--force"                # Overwrite output if it exists
        ]
        subprocess.run(cmd, check=True)

    def combined_fasta(self, file1, file2, output_file):
        with open(output_file, 'w') as outfile:
        # Open and write the contents of the first file
            with open(file1, 'r') as f1:
                outfile.write(f1.read())
            
            # Open and write the contents of the second file
            with open(file2, 'r') as f2:
                outfile.write(f2.read())
    

class SAPAddress(models.Model):
    protein = models.ForeignKey(ReferenceProtein, related_name="sap_addresses", on_delete=models.CASCADE)
    sap_address = models.CharField(max_length=100)    

    def __str__(self):
        return f"{self.protein.protein_id}"