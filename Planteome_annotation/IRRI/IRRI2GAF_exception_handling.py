import time

#test dictionaries

null =None

dictionarylist=[

{"dictionaryName":"full",
    "iricStockPhenotypeId": 114565,
    "phenotypeId": 43696,
    "quanValue": 11,
    "qualValue": null,
    "varietyId": 2295,
    "irisId": "IRIS 313-11252",
    "subpopulation": "indx",
    "boxCode": null,
    "country": "India",
    "name": "ADR 52::IRGC 40638-2",
    "value": 11
  },

 {"dictionaryName":"noValue",
    "iricStockPhenotypeId": 114565,
    "phenotypeId": 43696,
    "quanValue": 11,
    "qualValue": null,
    "varietyId": 2295,
    "irisId": "IRIS 313-11252",
    "subpopulation": "indx",
    "boxCode": null,
    "country": "India",
    "name": "ADR 52::IRGC 40638-2"
  },

{"dictionaryName":"nocountry",
    "iricStockPhenotypeId": 114565,
    "phenotypeId": 43696,
    "quanValue": 11,
    "qualValue": null,
    "varietyId": 2295,
    "irisId": "IRIS 313-11252",
    "subpopulation": "indx",
    "boxCode": null,
    "name": "ADR 52::IRGC 40638-2",
    "value": 11
  },
{"dictionaryName":"noname",
    "iricStockPhenotypeId": 114565,
    "phenotypeId": 43696,
    "quanValue": 11,
    "qualValue": null,
    "varietyId": 2295,
    "irisId": "IRIS 313-11252",
    "subpopulation": "indx",
    "boxCode": null,
    "value": 11
  },

{"dictionaryName":"noirisId",
    "iricStockPhenotypeId": 114565,
    "phenotypeId": 43696,
    "quanValue": 11,
    "qualValue": null,
    "varietyId": 2295,
    "subpopulation": "indx",
    "boxCode": null,
    "name": "ADR 52::IRGC 40638-2",
    "value": 11
  },

{"dictionaryName":"noiricStockPhenotypeId",
    "phenotypeId": 43696,
    "quanValue": 11,
    "qualValue": null,
    "varietyId": 2295,
    "irisId": "IRIS 313-11252",
    "subpopulation": "indx",
    "boxCode": null,
    "name": "ADR 52::IRGC 40638-2",
    "value": 11
  },

{"dictionaryName":"nosubpopulation",
    "phenotypeId": 43696,
    "quanValue": 11,
    "qualValue": null,
    "varietyId": 2295,
    "irisId": "IRIS 313-11252",
    "boxCode": null,
    "name": "ADR 52::IRGC 40638-2",
    "value": 11
  },

]



#########################################################################
#                       test stuffs
#########################################################################
testtraitlist = [43696,"Awn color","awco_rev", "TO:0000141", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"]




#########################################################################
#                        one run, one GAF line
#########################################################################

def gafline(phenotype_object,irriTraitName, outfile):

    #check to make sure each column call function returns a value, if any return False, it will not write a GAF line
    if col1() and col2(phenotype_object) and col3(phenotype_object)  and col5() and col6() and col7() \
             and col9() and col12() and col13(phenotype_object) and col14() and col15 and col16(phenotype_object,irriTraitName):

        print phenotype_object['dictionaryName']
        #outfile.write(
        print(
            col1()+"\t"+
            col2(phenotype_object)+"\t"+
            col3(phenotype_object)+"\t"+
            col4()+"\t"+
            col5()+"\t"+
            col6()+"\t"+
            col7()+"\t"+
            col8(phenotype_object)+"\t"+
            col9()+"\t"+
            col10(phenotype_object)+"\t"+
            col11(phenotype_object)+"\t"+
            col12()+"\t"+
            col13(phenotype_object)+"\t"+
            col14()+"\t"+
            col15()+"\t"+
            col16(phenotype_object,irriTraitName)+"\t"+
            "\n")

#########################################################################
#                           MAIN
#########################################################################

def main():
    outfile = "/Users/austinmeier/Desktop/irri_test.assoc"
    OUTWRITE = open(outfile, "w")
    OUTWRITE.write("!gaf-version: 2.0\n")
    for object in trait_json:
        gafline(object ,OUTWRITE)
    OUTWRITE.close()




# required
def col1():
    return "IRIC"

#required
def col2(phenotype_object):
    #check if the dictionary from json contains an irisId
    if 'irisId' in phenotype_object:
    #return the IRIS_ID
        return str(phenotype_object['irisId'])
    else:
        print('record for\n', phenotype_object,"\nwill not be included.  It is missing an IRIS-ID")
        return False

#required
def col3(phenotype_object):
    #check if the dictionary from json contains a name
    if 'name' in phenotype_object:
        #return the germplasm name (unless here is a germplasm symbol)
        Name= str(phenotype_object['name']).split('::')
        return Name[0]
    else:
        print('record for\n', phenotype_object,"\nwill not be included.  It is missing a name")
        return False

#not required
def col4():
    return ""

#required
def col5():
    #return the TO:xxxxxxxx or CO:xxxxxxxx
    return "TO:0000141"   #this is the test one, "awn color"

#required
def col6():
    #return IRIC  (no pmid)
    return "IRIC"

#required
def col7():
    #return the evidence code
    return testtraitlist[6]

#not required
def col8(phenotype_object):
    #check if the dictionary from json contains a country
    if 'country' in phenotype_object:
        #return the relationship "from_country" and the country of origin
        country_origin = phenotype_object['country']
        column8 = "from_country(%s)"%(country_origin)
        return column8.replace(" ","_")
    else:
        return ""



#required
def col9():
    #return aspect
    return "T"

#not required
def col10(phenotype_object):
    #check if the dictionary from json contains a name
    if 'name' in phenotype_object:
        #return the germplasm name (unless here is a germplasm symbol)
        Name= str(phenotype_object['name']).split('::')
        return Name[0]
    else:
        #this name is not required, so it won't return anything.  However, in this case, if there isn't a name,
        #it will error out on col3(), so it doesn't really matter
        return ""


#not required
def col11(phenotype_object):
    #check if the dictionary from json contains a iricStockPhenotypeId
    if 'name' in phenotype_object:
        Name= str(phenotype_object['name']).split('::')
        return Name[1]
    else:
        return ""


#required
def col12():
    #return object type
    return "germplasm"

#required
def col13(phenotype_object):
    #return taxonID
    #might need translation for subpopulation.
    #if phenotype_object['subpopulation']== "indx":
    #   taxonID = "NCBITaxon:39946"
    #return taxonID
    return "NCBITaxon:4530"   #this is the generic oryza stativa NCBITaxon

#required
def col14():
    #return date
    date=str(time.strftime('%m%d%Y'))
    return date

#not required
def col15():
    #return assigned_by
    return "austin_meier"

#not required for GAF, but required for germplasm
def col16(phenotype_object,phenotypename):
    if 'value' in phenotype_object:
        #return the value
        phenotype_value = str(phenotype_object['value'])
        return "has_phenotype_score(" + phenotypename + "=" + phenotype_value +")"
        return phenotypename+ str(phenotype_object['value'])
    else:
        print('record for\n', phenotype_object,"\nwill not be included.  It is missing a value")
        return False

    #return the variable (if it exists)
    #return the method, if it exists
    #return the evaluation location (evaluation_location(x))






#for dict in dictionarylist:
#	try:



for dict in dictionarylist:
    print(dict['dictionaryName'])
    gafline(dict,testtraitlist[2],'xxx')


