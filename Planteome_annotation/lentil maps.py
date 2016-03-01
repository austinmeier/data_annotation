"""
lentil_maps= open("/Users/meiera/Documents/Jaiswal/TO/test_folder/lentil_GRIN_germplasm_annotation/lentil_trait_maps.csv")

lentil_traits={}

for line in lentil_maps:
    line1=line.strip('\n')
    line2=line1.split(",")
    lentil_traits[line2[0]] = line2[2]

print lentil_traits

"""
lentil_PI_translate= open("/Users/meiera/Documents/Jaiswal/TO/test_folder/lentil_GRIN_germplasm_annotation/PI_translate_GRIN.csv")

lentil_PI={}

for line in lentil_PI_translate:
    line1=line.strip('\n')
    line2=line1.split(",")
    lentil_PI[line2[1]] = line2[0]

print lentil_PI

