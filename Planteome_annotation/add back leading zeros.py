infile= open("/Users/meiera/Documents/SVN/associations/to-associations/TO_IMP_gene_O.sativa.assoc")
outfile= open("/Users/meiera/Desktop/TO_IMP_gene_O.sativa2.assoc","w")

for line in infile:
    line_list= line.split("\t")
    line_list[1]="GR:"+line_list[1].zfill(7)
    outfile.write( "\t".join(line_list))

outfile.close()