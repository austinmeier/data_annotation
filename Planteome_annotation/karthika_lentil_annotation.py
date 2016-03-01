import time

#data from GRIN
KARTHIKA =open('/Users/meiera/Desktop/after_awk_lentil_annotation.tsv')

outfile= '/Users/meiera/Documents/SVN/associations/to-associations/test_lentil_TO/annotation_Lentil.tsv'
#used to be here Jaiswal/TO/test_folder/GRIN_germpaslm_annotation/lentil_trait_annotation.tsv
OUTWRITE = open(outfile,"w")
OUTWRITE.write("!gaf-version: 2.0\n")










coTrait_coVar={'CO_339:0000045':'CO_339:0000212','CO_339:0000054':'CO_339:0000217','CO_339:0000114':'CO_339:0000237','CO_339:0000078':'CO_339:0000225','CO_339:0000090':'CO_339:0000229','CO_339:0000012':'CO_339:0000201','CO_339:0000168':'CO_339:0000256'}



#go through every line in the grin.xls converted to .csv  and print the appropriate gaf2 formatted line


date=str(time.strftime('%m%d%Y'))

for line in KARTHIKA:
    l= line.split("\t")
    l[2]= l[2].strip("BMS_")
    l[1]=l[1].strip("-")
    l[9]=l[9].strip("-")
    col16= coTrait_coVar[l[4]]
    l[15]= "has_phenotype_variable("+col16+")|"+l[15].strip()+"|evaluation_location(morocco)\t\n"
    OUTWRITE.write('\t'.join(l))
    #print l

    #print('\t'.join(l))


OUTWRITE.close()




