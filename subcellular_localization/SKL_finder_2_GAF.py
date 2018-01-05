from Bio import SeqIO
import datetime
import pandas as pd

peptide_sequence_fasta = "/Users/meiera/Documents/Jaiswal/Planteome/black_box_project/IRGSP-1.0_predicted-protein_2017-08-04.fasta"  #this is just the predicted ones
OUTGAF = "/Users/meiera/Google Drive/Jaiswal/subcellular_localization_project/SKL.gaf"

def writegaf(id):
    gene_name = id.split('-')[0].replace('t','g')
    gaf_line = {
        'DB':'PlanteomeGene',
        'DB_ID':gene_name, 
        'Symbol':gene_name,
        'Qualifier':'',
        'GO_ID':'GO:0005777',
        'DB:ref':'PO_REF:xxxxx',
        'evidence_code':'ISS',
        'with_from':'',
        'Aspect':'C',
        'Name':gene_name,
        'Synonym':gene_name,
        'Obj_type':'gene',
        'Taxon':'NCBITaxon:4530',
        'Date': datetime.datetime.now().date(),
        'Assigned_by':'Planteome:Austin_Meier',
        'Annotation_extension':'',
        'Gene_Product_Form_ID':id
    }
    
    return(gaf_line)

def main():
    count = 0
    annotations = []
    for record in SeqIO.parse(peptide_sequence_fasta, "fasta"):
        last4 = record.seq[-4:]
        last3 = last4[:3]
        if last3 == "SKL":
            print(record.id)
            count += 1
            annotations.append(writegaf(record.id))

    with open(OUTGAF, 'w') as gaf:
        gaf.write('!gaf-version: 2.0\n')

    COLUMN_NAMES = ['DB','DB_ID', 'Symbol','Qualifier','GO_ID','DB:ref','evidence_code','with_from','Aspect','Name','Synonym','Obj_type','Taxon','Date','Assigned_by','Annotation_extension','Gene_Product_Form_ID']
    out_gaf_df = pd.DataFrame(annotations, columns=COLUMN_NAMES)

    with open(OUTGAF, 'a') as gaf:
        out_gaf_df.to_csv(gaf, sep='\t', header=False, index=False)
    

if __name__ == "__main__":
	main()