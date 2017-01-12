
# GRINTaxon:40544	    Triticum aestivum L. subsp. aestivum
# GRINTaxon:406896    Triticum turgidum L. subsp. durum (Desf.) Husn.
# GRINTaxon:406901	Triticum aestivum L. subsp. compactum (Host) Mackey
# GRINTaxon:406902	Triticum aestivum L. subsp. macha (Dekapr. & Menabde) Mackey
# GRINTaxon:406903	Triticum aestivum L. subsp. spelta (L.) Thell.
# GRINTaxon:406904	Triticum aestivum L. subsp. sphaerococcum (Percival) Mackey
#
#
#
wheattaxons = {
    40544: 'NCBITaxon:4565',
    406896: 'NCBITaxon:4567',
    406901: 'NCBITaxon:4565',
    406902: 'NCBITaxon:4565',
    406903: 'NCBITaxon:4565',
    406904: 'NCBITaxon:4565',
}

wheatmapfile = '/Users/meiera/Downloads/GRINDesc_mappings_wheat.tsv'
wheattraitmap = {}

with open(wheatmapfile, 'r') as infile:
    for row in infile:
        rowlist = row.split("\t")
        if rowlist[3]:
            wheattraitmap[rowlist[0]] = rowlist[3]


print wheattraitmap

