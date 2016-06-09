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
#testtrait = [6,"Awn color","awco_rev", "TO:0000141", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"]

testtraitlist =[[10,"Apiculus color","AUCO_REV_VEG", "TO:0000141", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"]]


#########################################################################
#                           import data
#########################################################################

rawdata="/Users/meiera/Documents/Jaiswal/Planteome/IRRI/irri_data_text/combined_requete.tsv"
#rawdata="/Users/meiera/Documents/Jaiswal/Planteome/IRRI/irri_data_text/test_requete.tsv"
rawcsv = open(rawdata,'rb')

errors="/Users/meiera/Documents/Jaiswal/Planteome/IRRI/irri_data_text/errorfile.txt"
#outfile = "/Users/meiera/Documents/git/data_annotation/Planteome_annotation/IRRI/GRIMS_awncolor.assoc"
outfile = "/Users/meiera/Documents/SVN/associations/to-associations/test_IRRI_TO/GRIMS_awncolor2.assoc"




#########################################################################
#                           MAIN
#########################################################################



def main(testtraitlist,rawcsv):
    global OUTWRITE
    global ERRORFILE
    global excluded_list
    OUTWRITE = open(outfile, "w")
    OUTWRITE.write("!gaf-version: 2.0\n")
    ERRORFILE = open(errors,"w")
    ERRORFILE.write("these are your errors:")
    excluded_list=[]
    with rawcsv as infile:
        GRIMS = csv.reader(infile, delimiter='\t', quotechar='"')
        for trait in testtraitlist:
            for accession in GRIMS:
                gafline(accession,trait,OUTWRITE)
    print str(len(excluded_list))+" accessions were not included.  See errorfile.txt for details."
    OUTWRITE.close()
    ERRORFILE .close()



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
             and col9() and col12() and col13(accession) and col14() and col15 and col16(accession,traitinfo):


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
            col16(accession,traitinfo)+"\t"+
            "\n")

    else: excluded_list.append(accession[0])


# required
def col1():
    return "GRIMS"

#required
def col2(accession):
    #check if the dictionary from json contains an irisId
    if accession[0] != "":
    #return the IRIS_ID
        return str(accession[0])
    else:
        ERRORFILE.write("Accession:" + str(accession[0]) + "- will not be included.  It is missing an accession number")
        return False

#required
def col3(accession):
    #check if name field is populated
    if accession[187] != "":
        #return the germplasm name (unless here is a germplasm symbol)
        return accession[187]
    else:
        ERRORFILE.write("Accession:" + str(accession[0]) + "-will not be included.  It is missing a name")
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
    return "GRIMS"

#required
def col7(testtrait):
    #return the evidence code
    return testtrait[6]

#not required
def col8(accession):
    #check if the sheet contains a country in column 154 "ORI_COUNTRY" or "LOCATION_M"

    if accession[154] !="":
        #return the germplasm name (unless here is a germplasm symbol)
        country_origin= accession[154]
        column8= "from_country(%s)"%(country_origin)
        return column8.replace(" ","_")
    else:
        ERRORFILE.write('Accession:' + str(accession[0]) + " is missing a country of origin")
        return ""

#required
def col9():
    #return aspect
    return "T"

#not required
def col10(accession):
    #187 has just the name, 188 has the name;some other codes; separated with semicolons; eg: "RADIN EBOS 64; ; FAO GS 1180; ;"

       #check if name field is populated
    if accession[187] !="":
        #return the germplasm name (unless here is a germplasm symbol)
        return accession[187]
    else:
        errorfile.write('Accession:' + str(accession[0]) + " - will not be included.  It is missing a name")
        return ""


#not required
def col11(accession):
    #throw some SYNONYMS in there
    full_ccno_name=accession[188].split(";")
    if len(full_ccno_name) >1:
        return full_ccno_name[2]
    else:
        return ""


#required
def col12():
    #return object type
    return "germplasm"

#required
def col13(accession):
    taxon=accession[96]
    if taxon=="Indica": return "NCBITaxon:39946"
    elif taxon =="Japonica": return "NCBITaxon:39947"
    elif taxon =="Javanica": return "NCBITaxon:4530"
    elif taxon =="Intermediate(hybrid)": return "NCBITaxon:1080340"
    else: return "NCBITaxon:4530"
    #return "NCBITaxon:4530"   #this is the generic oryza stativa NCBITaxon

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
def col16(accession,testtrait):
    #print testtrait[0]
    if accession[testtrait[0]] !="":
        return "has_phenotype_score(%s)"%(accession[testtrait[0]])
    else:
        ERRORFILE.write("Accession:%s has no score for %s"%(accession[0],testtrait[1]))
        return False






#########################################################################
#                    run actual code here
#########################################################################

main(testtraitlist,rawcsv)
    #for accession in GRIMS:
     #   print col16(accession,testtrait)


