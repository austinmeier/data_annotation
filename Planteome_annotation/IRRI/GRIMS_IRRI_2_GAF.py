#1. Pull down all traits with data in the database

#2. Create list of lists of [irriID, irritrait, TO:ID, CO:ID, CO:variable,evidence_code]

#3. Iterate over the "trait dictionary", and for every trait, create a line.


#########################################################################
#                       imports
#########################################################################
import time
import csv



#########################################################################
#                       test stuffs
#########################################################################
#starts with the column number that these scores will be found- in this case column 7 (or index[6]) is awncolor
testtrait = [6,"Awn color","awco_rev", "TO:0000141", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"]

testtraitlist =[[6,"Awn color","awco_rev", "TO:0000141", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"],
                [43715,"flag leaf angle","fla_repro", "TO:0000124", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"]]


#########################################################################
#                           import data
#########################################################################

#rawdata="/Users/meiera/Documents/Jaiswal/Planteome/IRRI/irri_data_text/combined_requete.tsv"
rawdata="/Users/meiera/Documents/Jaiswal/Planteome/IRRI/irri_data_text/test_requete.tsv"
rawcsv = open(rawdata,'rb')







#########################################################################
#                           MAIN
#########################################################################



def main(testtraitlist):
    outfile = "/Users/meiera/Documents/git/data_annotation/Planteome_annotation/IRRI/GRIMS_awncolor.assoc"
    OUTWRITE = open(outfile, "w")
    OUTWRITE.write("!gaf-version: 2.0\n")
    for testtrait in testtraitlist:
        for line in GRIMS:
            accession = line.split("\t")
            gafline(accession,traitinfo,OUTWRITE)
    OUTWRITE.close()



#########################################################################
#                        one run, one GAF line
#########################################################################
"""
accession is equal to one row in the GRIMS dataframe
traitinfo is the list that includes the name of the trait, its CO#, TO#, column in GRIMS dataframe where the scores can be found, and evidence code
outfile is where to write the GAF line
"""

def gafline(accession,traitinfo, outfile):

    #check to make sure each column call function returns a value, if any return False, it will not write a GAF line
    if  col2(accession) and col3(accession)  and col5(traitinfo) and col6() and col7(traitinfo) \
             and col9() and col12() and col13(accession) and col14() and col15 and col16(accession,traitinfo[2]):


        outfile.write(
        #print(
            col1()+"\t"+
            col2(accession)+"\t"+
            col3(accession)+"\t"+
            col4()+"\t"+
            col5(traitinfo)+"\t"+
            col6()+"\t"+
            col7(traitinfo)+"\t"+
            col8(accession)+"\t"+
            col9()+"\t"+
            col10(accession)+"\t"+
            col11(accession)+"\t"+
            col12()+"\t"+
            col13(accession)+"\t"+
            col14()+"\t"+
            col15()+"\t"+
            col16(accession,traitinfo[2])+"\t"+
            "\n")

    else: print("sump'n aint right with this trait")


# required
def col1():
    return "GRIMS"

#required
def col2(accession):
    #check if the dictionary from json contains an irisId
    if accession[0]!="":
    #return the IRIS_ID
        return str(accession[0])
    else:
        print('record for\n', accession,"\nwill not be included.  It is missing an accession number")
        return False

#required
def col3(accession):
    #check if name field is populated
    if accession[186] !="":
        #return the germplasm name (unless here is a germplasm symbol)
        return accession[186]
    else:
        print('record for\n', accession,"\nwill not be included.  It is missing a name")
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
def col8(accession):
    #check if the dictionary from json contains a country
    if 'country' in accession:
        #return the relationship "from_country" and the country of origin
        country_origin = accession['country']
        column8 = "from_country(%s)"%(country_origin)
        return column8.replace(" ","_")
    else:
        return ""



#required
def col9():
    #return aspect
    return "T"

#not required
def col10(accession):
    #check if the dictionary from json contains a name
    if 'name' in accession:
        #return the germplasm name (unless here is a germplasm symbol)
        Name= str(accession['name']).split('::')
        return Name[0]
    else:
        #this name is not required, so it won't return anything.  However, in this case, if there isn't a name,
        #it will error out on col3(), so it doesn't really matter
        return ""


#not required
def col11(accession):
    #check if the dictionary from json contains a iricStockPhenotypeId
    if 'name' in accession:
        Name= str(accession['name']).split('::')
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
def col13(accession):
    #return taxonID
    #might need translation for subpopulation.
    #if accession['subpopulation']== "indx":
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
def col16(accession,phenotypename):
    if 'value' in accession:
        #return the value
        phenotype_value = str(accession['value'])
        return "has_phenotype_score(" + phenotypename + "=" + phenotype_value +")"
        return phenotypename+ str(accession['value'])
    else:
        print('record for\n', accession,"\nwill not be included.  It is missing a value")
        return False

    #return the variable (if it exists)
    #return the method, if it exists
    #return the evaluation location (evaluation_location(x))







#########################################################################
#                    run actual code here
#########################################################################
with rawcsv as infile:
    GRIMS= csv.reader(infile, delimiter='\t', quotechar='"')

    for accession in GRIMS:

        print col3(accession)