#!/usr/local/anaconda3/bin/python3

# create gaf file from predotar output

import sys
import datetime
import sys

import pandas as pd

usage_statement= "usage: <path>/predotar2gaf.py <input type> <predotar input> <gaf destination> <options>\nexample: ./predotar2gaf.py -p first500.fasta_predotar_results first500.gaf"

#check to make sure there is a specified infile, and outfile
if len(sys.argv) != 4:
	print(len(sys.argv))
	print("Error:  This script requires 3 arguments, the input type, an input file, and output file.\n%s" %(usage_statement))
	quit()

#read arguments
print(sys.argv[0])
predotar_output = sys.argv[2]
OUTGAF= sys.argv[3]

# These are filled in based on the mode.  different pubmed ID, and relationship name.
ref = None
relationship = None
header_check = None
separator = None

if sys.argv[1] == '-p':
	mode = 'predotar'
	ref = 'PMID:15174128'
	relationship = 'has_predotar_score({})'
	header_check = ['Seq', 'Mit', 'Plast', 'ER', 'None', 'Prediction']
	separator = '\t'
	skiprows = 5

elif sys.argv[1] == '-t':
	mode = 'targetP'
	ref = 'PMID:17446895'
	relationship = 'has_targetP_score({})'
	header_check = ['Name', 'Len', 'cTP', 'mTP', 'SP', 'other', 'Loc', 'RC']
	separator = '\s+'
	skiprows = 6


else:
	print('Error: script only allows for 2 modes: \n-p for Predotar\n-t for targetP ')
	quit()


# global vars
LOW_THRESH = 0.5
HIGH_THRESH = 1.0

# Ontology translation
IDs = {
	'mit':"GO:0005739",
	'plast':"GO:0009536",
	'er':"GO:0005783",
	'none':"GO:0005575"
}

skipped_lines = []

def generate_gaf_line(row, gaf_list):
	"""
	This function takes a row of predotar data, and an output list and appends a dictionary with 16 keys, one for each column in a gaf file for each score over HIGH_THRESH

	The resulting list is transformed into a df at the end of main().

	1. DB - PlanteomeGene
	2. DB_ID - gene name/id
	3. Object Symbol = gene name/id
	4. Qualifier = N/A
	5. GO_ID = plastid (GO:0009536), mitrochondria (GO:0005739), ER (GO:0005783), cellular component (GO:0005575)
	6. DB:ref (predotar- PMID:15174128, targetP - PMID:17446895 )
	7. Evidence code (RCA or IEA)
	8. with/from - N/A
	9. Aspect - "C"  (for cellular component in GO)
	10. Name: gene name/id
	11. Synonym: gene name/id
	12. Obj_type: gene
	13. Taxon = NCBITaxon:4530
	14. Date = today
	15. Assigned_by- Planteome:Austin_Meier
	16. Annotation_extension - has_predotar_score() or has_TargetP_score()
	17. Gene_Product_Form_ID - use original transcript ID (eg- Os01t0101500-00)
	"""

	transcript = row[0]

	scores = {}

	if mode == 'predotar':  # look for the predotar header names
		scores['mit'] = float(row['Mit'])
		scores['plast'] = float(row['Plast'])
		scores['er'] = float(row['ER'])
		scores['none'] = float(row['None'])
	elif mode == 'targetP':  # look for the targetP header names
		scores['mit'] = float(row['mTP'])
		scores['plast'] = float(row['cTP'])
		scores['er'] = float(row['SP'])
		scores['none'] = float(row['other'])

	for loc,score in scores.items():
		# for each location and its respective score, generate a gaf line dictionary for each with a score higher than threshold
		if round(score,1) >= LOW_THRESH:
			gene_name = transcript.split('-')[0].replace('t','g')
			evidence_code = 'IEA'
			if score > HIGH_THRESH:
				evidence_code = 'RCA'
		
			gaf_line_dict = {
				'DB':'PlanteomeGene',
				'DB_ID':gene_name, 
				'Symbol':gene_name,
				'Qualifier':'',
				'GO_ID':IDs[loc],
				'DB:ref':ref,
				'evidence_code':evidence_code,
				'with_from':'',
				'Aspect':'C',
				'Name':gene_name,
				'Synonym':gene_name,
				'Obj_type':'gene',
				'Taxon':'NCBITaxon:4530',
				'Date': datetime.datetime.now().date(),
				'Assigned_by':'Planteome:Austin_Meier',
				'Annotation_extension':relationship.format(score),
				'Gene_Product_Form_ID':transcript
			}

			gaf_list.append(gaf_line_dict)
		else:
			skipped_lines.append(transcript)
			print('Skipping gene: {}'.format(transcript))


def main():
	# Read in predotar output, and make a dataframe from it.
	# There are 5 lines at the beginning of the file that won't be used.  Remove those, and load in data as a pandas dataframe

	df = pd.read_csv(predotar_output, sep=separator, skiprows=skiprows, skipfooter=2)
	print(df.shape)

	df.dropna(how='any', inplace=True)
	print(df.shape)

	if list(df) != header_check:
		print('ERROR: headers do not match expected predotar output headers\nExpected headers: {}'.format(header_check))
		exit()

	outlist1 =[]
	for index, row in df.iterrows():
		generate_gaf_line(row, outlist1)

	# Turn the list of gaf_line_dictionaries into a dataframe for printing.
	COLUMN_NAMES = ['DB','DB_ID', 'Symbol','Qualifier','GO_ID','DB:ref','evidence_code','with_from','Aspect','Name','Synonym','Obj_type','Taxon','Date','Assigned_by','Annotation_extension','Gene_Product_Form_ID']
	out_gaf_df = pd.DataFrame(outlist1, columns=COLUMN_NAMES)
	gaf_header = '!gaf-version: 2.0\n'
	with open(OUTGAF, 'w') as f:
		f.write(gaf_header)
	with open(OUTGAF, 'a') as f:
		out_gaf_df.to_csv(f, sep='\t', header=False, index=False)
	print("Finished.\n{} lines were skipped: No subcellular location score exceeds threshold of: {}".format(len(skipped_lines),LOW_THRESH))

if __name__ == '__main__':
	main()

