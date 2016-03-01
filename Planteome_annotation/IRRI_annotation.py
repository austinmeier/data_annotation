/local/cluster/bin/python2.7
########################################################################################
#			imports and usage statement
########################################################################################
import io
import sys
import re
import imp
import os

usage_statement = "usage: python2.7 Planteome_annotate.py <OG_datafile.tsv> <Trait_map.csv> <name and path of output directory>

#check the number of arguments
if len(sys.argv) !=4:
	print("Error: incorrect number of arguments")
	print(usage_statement)
	quit()

OG_datafile = sys.argv[1]
traitmap = sys.argv[2]
#outdir
if sys.argv[3].endswith('/'):
	outdir = sys.argv[3]
else: outdir = sys.argv[3]+'/'
#check if the outdirectory specified exists, if not, make it.
if not os.path.exists(sys.argv[3]):
	os.makedirs(sys.argv[3])



########################################################################################
#				format the traitmap to be used for translation
########################################################################################

TRAITS = open(traitmap, "r")

crop_traits = {}
for trait in TRAITS:
	line1 = line.strip('\n')
	line2 = line.split(',')
	crop_traits[line2[0]=line2[1]]


########################################################################################
#			creating dictionaries for each bubble in the Venn diagram
########################################################################################


########################################################################################
#			writing the GAF2 file
########################################################################################



date=str(time.strftime('%m%d%Y'))

OG_datafile_handle = open(OG_datafile)
OG_datafile_handle.seek(00)
for line in OG_datafile_handle:
	l= line.split(",")
	trait= lentil_traits[l[3].replace('"','')]
	country= l[8].replace(" ","_").replace('"','')
	phenotype = l[2].replace(" ","_").replace('"','')
	grin_id = lentil_PI[(l[1]).replace('"','')]
	OUTWRITE.write("GRIN\t"+					        #column1  OUTWRITE.write
			grin_id+"\t"+				                #column2
			call3()+"\t"+								#column3
			"\t" +								        #column4
			trait+"\t"+				                    #column5
			"GRIN\t"+	                                #column6  pubmed ID??
			"IDA\t"+							        #column7
			"from_country(%s)"%(country)+"\t"+	        #column8
			"T\t"+								        #column11
			call3()+"\t"+				                #column10
			str(l[1].replace('"',''))+"\t"+				#column11
			"germplasm\t"+						        #column12
			"taxon:362247\t"+						    #column13
			date+"\t"+							        #column14
			"austin_meier\t"+					        #column15
			"has_phenotype_score(%s)"%(phenotype)+ "\t" #column16
			"\n")

OG_datafile_handle.close()
OUTWRITE.close()