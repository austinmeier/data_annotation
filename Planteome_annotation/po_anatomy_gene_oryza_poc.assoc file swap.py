assoc= open("/Users/meiera/Desktop/po_anatomy_gene_oryza_poc.assoc")
OUTFILE= open("/Users/meiera/Desktop/fixed_po_anatomy_gene_oryza_poc.assoc", "w")

count=0

assoc.seek(00)

OUTFILE.write("!gaf-version: 2.0\n")

for line in assoc:
    if not line.startswith("!"):
        l= line.split("\t")
        col16= l[15].split("|")
        if 'isolated_from_germplasm(Nipponbare)' in col16:
            count = count+1
            l[7]='isolated_from_germplasm(Nipponbare)'
            col16.remove('isolated_from_germplasm(Nipponbare)')
            l[15]= '|'.join(col16)
        OUTFILE.write ('\t'.join(l))

print count

