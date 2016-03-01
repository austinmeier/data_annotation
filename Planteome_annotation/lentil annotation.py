import time


GRIN =open('/Users/meiera/Documents/Jaiswal/TO/test_folder/lentil_GRIN_germplasm_annotation/descriptor_query.csv')




lentil_grin ={
'"PEMV"':'TO:xxxxxxx',
'"SEEDWGT"':'TO:xxxxxxx',
'"HYPOCOTCOL"':'TO:xxxxxxx',
'"PODPIG"':'TO:xxxxxxx',
'"PODSHED"':'TO:xxxxxxx',
'"SEEDSPOD"':'TO:xxxxxxx',
'"HGTLOWPOD"':'TO:xxxxxxx',
'"PODMAT"':'TO:xxxxxxx',
'"FLOWERSPED"':'TO:xxxxxxx',
'"PODSPED"':'TO:xxxxxxx',
'"PLANT_HEIGHT"':'TO:xxxxxxx',
'"PLANTHABIT"':'TO:xxxxxxx',
'"PODSHATTER"':'TO:xxxxxxx',
'"DAYSFLOWER"':'TO:xxxxxxx',
'"PLANTSIZE"':'TO:xxxxxxx',
'"FLOGRDCOL"':'TO:xxxxxxx',
'"PODLENGTH"':'TO:xxxxxxx',
'"PODWIDTH"':'TO:xxxxxxx',
'"SEEDSIZE"':'TO:xxxxxxx',
'"SEEDPROD"':'TO:xxxxxxx',
'"SEEDPAT"':'TO:xxxxxxx',
'"SEEDPATCOL"':'TO:xxxxxxx',
'"SEEDGRDCOL"':'TO:xxxxxxx',
'"ANTHRAC"':'TO:xxxxxxx',
'"COTYLCOLOR"':'TO:xxxxxxx',
'"PSBMV"':'TO:xxxxxxx',
'"PLANT_WIDTH"':'TO:xxxxxxx',
'"MINERAL_K"':'TO:xxxxxxx',
'"MINERAL_MG"':'TO:xxxxxxx',
'"MINERAL_MN"':'TO:xxxxxxx',
'"MINERAL_S"':'TO:xxxxxxx',
'"PROTEIN"':'TO:xxxxxxx',
'"MINERAL_CU"':'TO:xxxxxxx',
'"MINERAL_P"':'TO:xxxxxxx',
'"MINERAL_ZN"':'TO:xxxxxxx',
'"MINERAL_FE"':'TO:xxxxxxx',
'"MINERAL_CA"':'TO:xxxxxxx',
'"LODGING"':'TO:xxxxxxx',
'"PODDROP"':'TO:xxxxxxx',
'"SHATTERING"':'TO:xxxxxxx'
}



lentil_grin ={
"PEMV":'TO:xxxxxxx',
"SEEDWGT":'TO:xxxxxxx',
"HYPOCOTCOL":'TO:xxxxxxx',
"PODPIG":'TO:xxxxxxx',
"PODSHED":'TO:xxxxxxx',
"SEEDSPOD":'TO:xxxxxxx',
"HGTLOWPOD":'TO:xxxxxxx',
"PODMAT":'TO:xxxxxxx',
"FLOWERSPED":'TO:xxxxxxx',
"PODSPED":'TO:xxxxxxx',
"PLANT_HEIGHT":'TO:xxxxxxx',
"PLANTHABIT":'TO:xxxxxxx',
"PODSHATTER":'TO:xxxxxxx',
"DAYSFLOWER":'TO:xxxxxxx',
"PLANTSIZE":'TO:xxxxxxx',
"FLOGRDCOL":'TO:xxxxxxx',
"PODLENGTH":'TO:xxxxxxx',
"PODWIDTH":'TO:xxxxxxx',
"SEEDSIZE":'TO:xxxxxxx',
"SEEDPROD":'TO:xxxxxxx',
"SEEDPAT":'TO:xxxxxxx',
"SEEDPATCOL":'TO:xxxxxxx',
"SEEDGRDCOL":'TO:xxxxxxx',
"ANTHRAC":'TO:xxxxxxx',
"COTYLCOLOR":'TO:xxxxxxx',
"PSBMV":'TO:xxxxxxx',
"PLANT_WIDTH":'TO:xxxxxxx',
"MINERAL_K":'TO:xxxxxxx',
"MINERAL_MG":'TO:xxxxxxx',
"MINERAL_MN":'TO:xxxxxxx',
"MINERAL_S":'TO:xxxxxxx',
"PROTEIN":'TO:xxxxxxx',
"MINERAL_CU":'TO:xxxxxxx',
"MINERAL_P":'TO:xxxxxxx',
"MINERAL_ZN":'TO:xxxxxxx',
"MINERAL_FE":'TO:xxxxxxx',
"MINERAL_CA":'TO:xxxxxxx',
"LODGING":'TO:xxxxxxx',
"PODDROP":'TO:xxxxxxx',
"SHATTERING":'TO:xxxxxxx'
}




#go through every line in the grin.xls converted to .csv  and print the appropriate gaf2 formatted line
outfile= "/Users/meiera/Documents/Jaiswal/TO/test_folder/GRIN_germpaslm_annotation/lentil_trait_annotation.tsv"
OUTWRITE = open(outfile,"w")

date=str(time.strftime('%m%d%Y'))

GRIN.seek(00)
for line in GRIN:
	l= line.split(",")
	trait=l[3].replace('"','')
	trait2=lentil_grin[trait]
	country= l[8].replace(" ","_").replace('"','')
	phenotype = l[2].replace(" ","_").replace('"','')
	OUTWRITE.write ("GRIN\t"+					#column1  OUTWRITE.write
			(l[1]).replace('"','')+"\t"+						#column2
			(l[6]).replace('"','')+"\t"+						#column3
			"\t" +								#column4
			lentil_grin[l[3].replace('"','')]+"\t"+				#column5
			"\t"+	                            #column6  pubmed ID??
			"IAGP\t"+							#column7
			"from_country(%s)"%(country)+"\t"+	#column8
			"T\t"+								#column11
			str(l[1].replace('"',''))+"\t"+						#column10
			str(l[6].replace('"',''))+"\t"+						#column11
			"germplasm\t"+						#column12
			"taxon:xxxx\t"+						#column13
			date+"\t"+							#column14
			"austin_meier\t"+					#column15
			"has_phenotype_score(%s)"%(phenotype)+
			"\n")




OUTWRITE.close()





