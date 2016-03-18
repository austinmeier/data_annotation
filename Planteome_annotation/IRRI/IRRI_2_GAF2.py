#1. Pull down all traits with data in the database

#2. Create list of lists of [irriID, irritrait, TO:ID, CO:ID, CO:variable,evidence_code]

#3. Iterate over the "trait dictionary", and for every trait, create a line.


#########################################################################
#                       imports
#########################################################################
import time
import urllib2
import json
"""

with open("/Users/meiera/Documents/git/data_annotation/Planteome_annotation/IRRI/test.json") as data_file:
    #unicode_json = json.load(data_file)
    trait_json=json.load(data_file)
"""



#########################################################################
#                       test stuffs
#########################################################################
testtrait = [43696,"Awn color","awco_rev", "TO:0000141", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"]

testtraitlist =[[43696,"Awn color","awco_rev", "TO:0000141", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"],
                [43715,"flag leaf angle","fla_repro", "TO:0000124", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"]]



#########################################################################
#                           MAIN
#########################################################################



def main(testtraitlist):
    outfile = "/Users/meiera/Documents/git/data_annotation/Planteome_annotation/IRRI/irri_test2.assoc"
    OUTWRITE = open(outfile, "w")
    OUTWRITE.write("!gaf-version: 2.0\n")
    for trait in testtraitlist:
        trait_json= mk_json(trait)

        for object in trait_json:
    #for object in webcalled1:
            gafline(object,trait,OUTWRITE)
    OUTWRITE.close()

#########################################################################
#                       web calls
#########################################################################

def mk_json(trait): #trait is a list that looks like this: [43696,"Awn color","awco_rev", "TO:0000141", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"]
    phenotypeID= str(trait[0])
    webcall = "http://oryzasnp.org/iric-portal/ws/variety/phenotypes/%s" %(phenotypeID)
    webcalled1=urllib2.urlopen(webcall).read()
    tempjson = "/Users/meiera/Documents/git/data_annotation/Planteome_annotation/IRRI/test1.json"
    TEMPJSON = open(tempjson, "w")
    TEMPJSON.write(webcalled1)
    TEMPJSON.close()
    with open("/Users/meiera/Documents/git/data_annotation/Planteome_annotation/IRRI/test1.json") as data_file:
        trait_json=json.load(data_file)
    return trait_json



#########################################################################
#                        one run, one GAF line
#########################################################################

def gafline(phenotype_object,testtrait, outfile):

    #check to make sure each column call function returns a value, if any return False, it will not write a GAF line
    if  col2(phenotype_object) and col3(phenotype_object)  and col5(testtrait) and col6() and col7(testtrait) \
             and col9() and col12() and col13(phenotype_object) and col14() and col15 and col16(phenotype_object,testtrait[2]):

        outfile.write(
        #print(
            col1()+"\t"+
            col2(phenotype_object)+"\t"+
            col3(phenotype_object)+"\t"+
            col4()+"\t"+
            col5(testtrait)+"\t"+
            col6()+"\t"+
            col7(testtrait)+"\t"+
            col8(phenotype_object)+"\t"+
            col9()+"\t"+
            col10(phenotype_object)+"\t"+
            col11(phenotype_object)+"\t"+
            col12()+"\t"+
            col13(phenotype_object)+"\t"+
            col14()+"\t"+
            col15()+"\t"+
            col16(phenotype_object,testtrait[2])+"\t"+
            "\n")

    else: print("sump'n aint right with this trait")


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
def col5(testtrait):
    #return the TO:xxxxxxxx or CO:xxxxxxxx
    #return "TO:0000141"   #this is the test one, "awn color"
    return testtrait[3]

#required
def col6():
    #return IRIC  (no pmid)
    return "IRIC"

#required
def col7(testtrait):
    #return the evidence code
    return testtrait[6]

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
        if len(Name)>1:
            return Name[1]
        else: return Name[0]
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







#########################################################################
#                    run actual code here
#########################################################################

main(testtraitlist)