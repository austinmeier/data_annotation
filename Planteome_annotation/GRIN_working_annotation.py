
import time


traitname= "alkalisprd	amylose	awntype	blast	brancolor	daysanthes	daysflower	hullcolor	kernellen	kernelwid	kernelwtr	plantht1	plantht2	planttype	protein"
traitname= traitname.split("\t")

GRIN =open('/Users/meiera/PycharmProjects/Planteome_Annotation/why_wont_this_work_copy.csv')




nsf_project_obs =[
("HULLED.SEED",26,"TO:0000734", "CO:xxxxxxx",2),
("amylose_content",27,"TO:0000196", "CO:xxxxxxx",2),
("alkalisprd",11,"TO:0000462","CO_320:0000107",1),
("amylose",12,"TO:0000196","CO_320:0000102",1),
("awntype",13,"TO:0002718","CO_320:0000015",1),
("blast",14,"TO:0000468","CO_320:0000176",1),
("brancolor",15,"TO:0000707","CO_320:0000115",1),
("daysanthes",16,"TO:0000344","CO_320:0000088",1),
("daysflower",17,"TO:0000344","CO_320:0000088",1),	#same trait as daysanthes
("hullcolor",18,"TO:0000264","CO_320:0000039",1),
("kernellen",19,"TO:0000734","CO_320:0000004",1),
("kernelwid",20,"TO:0000402","CO_320:0000005",1),
("kernelwtr",21,"TO:0000382","CO_320:0000100",1),
("plantht1",22,"TO:0000207","CO_320:0000076",1),
("plantht2",23,"TO:0000207","CO_320:0000076",1) , 	#same trait as plantht1
("planttype",24,"TO:0000427","CO_320:0000031",1),
("protein",25,"TO:0000138","CO_320:0000111",1)
]



def call6(l,ref):
	col6=[]
	if ref ==1:
		col6="NFS.PROJECT.OBS|PMID:21915109"
	elif ref==2:
		col6="PMID:20520727"
	return col6


## PMID: 20520727





#define a function to generate column 16's content based on presence or absence of values in the grin dataframe
#argument l = each line, with columns separated into a list
#argument p = the column number the phenotype scores are in (the original sheet column number)
def call816(l,p):
	col16 =[]
	country= l[6].replace(" ","_")					#remove spaces from the country name
	phenotype_score= l[p-1].strip('\n')				#takes user input for which column the phenotype scores are in (minus one because python)

	if phenotype_score == "" and country =="":		#if both country, and phenotype score are missing
		col16 =""
	elif phenotype_score =="": 						#if the previous if didn't catch it, we can assume both are not empty, so this checks to see if phenotype is missing
		col16 = "from_country(%s)"%(country)
	elif country=="":								#again, if the first if didn't catch, we assume both not empty, and check if country is empty
		col16="has_phenotype_score(%s)"%(phenotype_score)
	else:											#if all 3 above don't catch it, both are not empty, so print the whole thing.
		col16= "has_phenotype_score(%s)|from_country(%s)" %(phenotype_score,country)
	return str(col16)

def call16(l,p):
	col16 =""
	phenotype_score= l[p-1].strip('\n')
	if phenotype_score!="":
		col16="has_phenotype_score(%s)"%(phenotype_score)
	return col16


def call8(l,p):
	col8 =""
	country= l[6].replace(" ","_")
	if country !="":
		col8= "from_country(%s)"%(country)
	return col8

#go through every line in the grin.xls converted to .csv  and print the appropriate gaf2 formatted line

def main(grin,grout, traitID, colnum, ref):
	GRIN.seek(00)
	for line in grin:
		date=str(time.strftime('%m%d%Y'))
		l= line.split(",")
		if l[colnum-1]!="":
			grout.write ("GRIN\t"+						#column1
					str(l[9])+"\t"+						#column2
					str(l[5])+"\t"+						#column3
					"\t" +								#column4
					traitID+"\t"+						#column5
					call6(l,ref)+"\t"+					#column6
					"IAGP\t"+							#column7
					call8(l,colnum)+"\t"+				#column8
					"T\t"+								#column11
					str(l[5])+"\t"+						#column10
					str(l[7])+"\t"+						#column11
					"germplasm\t"+						#column12
					"taxon:4530\t"+						#column13
					date+"\t"+							#column14
					"austin_meier\t"+					#column15
					call16(l,colnum)+"\t"				#column16
					 "\n")



#write a GAF2 file for each trait
filenames=[]
for trait_tup in nsf_project_obs:
	#outfile= "/Users/meiera/Documents/Jaiswal/TO/test_folder/rice_staging/%s_trait_annotation.tsv" %(trait_tup[0])
	outfile= "/Users/meiera/PycharmProjects/Planteome_Annotation/finished_assoc_files/%s_trait_annotation.tsv" %(trait_tup[0])
	OUTWRITE = open(outfile,"w")
	main(GRIN,OUTWRITE,trait_tup[2],trait_tup[1],trait_tup[4])
	OUTWRITE.close()
	filenames.append(outfile)



#combine all files into one gaf2 file on the SVN
final_file= "/Users/meiera/Desktop/GRIN_working_annotation_py_outfile.txt"
#final_file=  "/Users/meiera/Documents/SVN/associations/to-associations/test_germplasm_TO/to_germplasm_rice.assoc"
with open(final_file,'w') as outfile:
	outfile.write("!gaf-version: 2.0\n")
	for fname in filenames:
		with open(fname) as infile:
			for line in infile:
				outfile.write(line)