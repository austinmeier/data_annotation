#1. Pull down all traits with data in the database

#2. Create list of lists of [irriID, irritrait, TO:ID, CO:ID, CO:variable,evidence_code]

#3. Iterate over the "trait dictionary", and for every trait, create a line.


#########################################################################
#                       imports
#########################################################################
import time
import csv
import logging
import os


#########################################################################
#                       test stuffs
#########################################################################
#starts with the column number that these scores will be found- in this case column 7 (or index[6]) is awncolor
#testtrait = [6,"Awn color","awco_rev", "TO:0000141", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"]

testtraitlist =[[10,"Apiculus color","AUCO_REV_VEG", "TO:0000141", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"]]

testtrait = {
    'colnum': 10,
    'name': 'Apiculus color',
    'GRIMS MORPHO1': 'AUCO_REV_VEG',
    'to_id': "TO:0000141",
    'co_id': 'CO:xxxxxxx',
    'pheno_relation': 'has_absolute_phenotype({})',
    'unit': None,
    'evidence': 'IDA'
}

testtraitlist = []


#########################################################################
#                           import data
#########################################################################

outdir = "/Users/meiera/Documents/SVN/associations/to-associations/test_IRRI_TO/"


rawdata="/Users/meiera/Documents/Jaiswal/Planteome/IRRI/irri_data_text/combined_requete.tsv"
#rawdata="/Users/meiera/Documents/Jaiswal/Planteome/IRRI/irri_data_text/test_requete.tsv"
rawcsv = open(rawdata,'rb')

errors="/Users/meiera/Documents/Jaiswal/Planteome/IRRI/irri_data_text/errorfile.txt"
#outfile = "/Users/meiera/Documents/git/data_annotation/Planteome_annotation/IRRI/GRIMS_awncolor.assoc"
outfile = "/Users/meiera/Documents/SVN/associations/to-associations/test_IRRI_TO/GRIMS_awncolor2.assoc"
mapfile = "/Users/meiera/Documents/Jaiswal/Planteome/IRRI/GBUSER_TK_MORPH1_2.tsv"

logger = logging.getLogger(__name__)
logging_format = "[%(levelname)s] %(name)s %(asctime)s %(message)s"
logging.basicConfig(format=logging_format, level=logging.CRITICAL) #filename=errors,

testtrait = {
    'colnum': 10,
    'name': 'Apiculus color',
    'GRIMS MORPHO1': 'AUCO_REV_VEG',
    'to_id': "TO:0000141",
    'co_id': 'CO:xxxxxxx',
    'pheno_relation': 'has_absolute_phenotype({})',
    'unit': None,
    'evidence': 'IDA'
}

def load_map(mapfile):
    headers = []
    with open(rawdata,'rb') as infile:
        reader = csv.reader(infile, delimiter='\t', quotechar='"')
        headers = next(reader)
        # headers = infile.readline().split('\t')
    print headers
    with open(mapfile,'rb') as infile:
        traitmap = csv.reader(infile, delimiter='\t', quotechar='"')
        for trait in traitmap:
            logger.debug('#############################################################\n                   {}                    \n#############################################################'.format(trait[0]))
            # check that there is only one TO mapping.
            to_mapping = filter(None, trait[7].split(","))  # trait[7].split(",")
            logger.debug('number of TO classes mapped to {}: {}'.format(trait[0],len(to_mapping)))
            if len(to_mapping) == 0:
                logger.warning('No TO class match found for {}'.format(trait[0]))
                continue
            elif len(to_mapping) > 1:
                logger.warning('multiple TO classes mapped to {}'.format(trait[0]))
                continue
            # find the column number that contains the scores of the trait
            if trait[0] in headers:
                colnum = headers.index(trait[0])
            else:
                logger.warning('{} not found in data headers'.format(trait[0]))
                continue
            # choose the correct phenotype relationship
            if trait[3] == 'absolute':
                phenorelation = 'has_absolute_phenotype({}{})'
            elif trait[3] == 'relative':
                phenorelation = 'has_relative_phenotype({}{})'
            else:
                logger.warning('no absolute/relative rating for mapped to: {} the relationship found is: "{}"'.format(trait[0],trait[3]))
                continue
            if trait[2] != '':
                unit = trait[2]
            else:
                unit = ''
            trait_dict = {
                'colnum': colnum,
                'name': trait[1],
                'GRIMS MORPHO1': trait[0],
                'to_id': trait[7],
                'co_id': trait[5],
                'pheno_relation': phenorelation,
                'unit': unit,
                'evidence': 'IDA'
            }
            # print trait_dict['unit']
            testtraitlist.append(trait_dict)
    return headers
#########################################################################
#                           MAIN
#########################################################################

def main(testtraitlist,rawdata):
    # global OUTWRITE
    global excluded_list
    excluded_list=[]

    for trait in testtraitlist:
        outfile = outdir + str(trait['GRIMS MORPHO1']) + '.assoc'
        # OUTWRITE = open(outfile, 'w')
        with open(rawdata, 'rb') as infile, open(outfile,'w') as OUTWRITE:
            OUTWRITE.write("!gaf-version: 2.0\n")
            GRIMS = csv.reader(infile, delimiter='\t', quotechar='"')
            for accession in GRIMS:
                gafline(accession,trait,OUTWRITE)
    print str(len(excluded_list))+" accessions were not included.  See errorfile.txt for details."
    logger.warning(str(len(excluded_list)) + " accessions were not included.  See errorfile.txt for details.")
    # OUTWRITE.close()


#########################################################################
#                        one run, one GAF line
#########################################################################


def gafline(accession,traitinfo, outfile):
    """
    check to make sure each column call function returns a value, if any return False, it will not write a GAF line
    :param accession: This is a row from the GRIMS file
    :param traitinfo: A single trait, list form -- [10,"Apiculus color","AUCO_REV_VEG", "TO:0000141", "CO:xxxxxxx", "CO:xxxxxxx", "IDA"]
    :param outfile: self explanitory
    :return: nothing.  Just writes lines to the outfile.
    """
    logger.critical('The accession:\n{}\nThe trait:\n{}'.format(accession,traitinfo))
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
    """DB"""
    return "GRIMS"


def col2(accession):
    """DB Object ID: required."""
    #check if the dictionary from json contains an irisId
    if accession[1] != "":
    #return the IRIS_ID
        return str(accession[0])
    else:
        #ERRORFILE.write("Accession:" + str(accession[0]) + "- will not be included.  It is missing an accession number")
        logger.warning("Accession:\t" + str(accession[0]) + "\t- will not be included.  It is missing an accession number")
        return False


def col3(accession):
    """DB Object Symbol: required"""
    #check if name field is populated
    if accession[187] != "":
        #return the germplasm name (unless here is a germplasm symbol)
        return accession[187]
    else:
        #ERRORFILE.write("Accession:" + str(accession[0]) + "-will not be included.  It is missing a name")
        logger.warning("Accession:\t" + str(accession[0]) + "\t-will not be included.  It is missing a name")
        return False


def col4():
    """Qualifier: not required"""
    return ""


def col5(testtrait):
    """Direct Annotation (TO:xxxxxxxx or CO:xxxxxxxx): required"""
    return testtrait['to_id']  #replace with 'co_id' to annotate to this

#required
def col6():
    """	DB:Reference (|DB:Reference)"""
    #return IRIC  (no pmid)
    return "GRIMS"

def col7(testtrait):
    """Evidence Code: required"""
    return testtrait['evidence']

def col8(accession):
    """With (or) From: not required"""
    #check if the sheet contains a country in column 154 "ORI_COUNTRY" or "LOCATION_M"
    if accession[154] !="":
        #return the germplasm name (unless here is a germplasm symbol)
        country_origin= accession[154]
        column8= "from_country(%s)"%(country_origin)
        return column8.replace(" ","_")
    else:
        logger.warning('Accession:\t' + str(accession[0]) + "\tis missing a country of origin")
        return ""

def col9():
    """Aspect: required"""
    return "T"

def col10(accession):
    """DB Object Name: not required"""
    #187 has just the name, 188 has the name;some other codes; separated with semicolons; eg: "RADIN EBOS 64; ; FAO GS 1180; ;"

       #check if name field is populated
    if accession[187] != "":
        #return the germplasm name (unless here is a germplasm symbol)
        return accession[187]
    else:
        logger.warning('Accession:\t' + str(accession[0]) + "\twill not be included.  It is missing a name")
        return ""

def col11(accession):
    """	DB Object Synonym (|Synonym): not required"""
    #throw some SYNONYMS in there
    full_ccno_name = accession[188].split(";")
    if len(full_ccno_name) >1:
        return full_ccno_name[1]
    else:
        return ""

def col12():
    """DB Object type: required"""
    return "germplasm"

#required
def col13(accession):
    """Taxon (|taxon): required"""
    taxon=accession[96]
    if taxon=="Indica": return "NCBITaxon:39946"
    elif taxon =="Japonica": return "NCBITaxon:39947"
    elif taxon =="Javanica": return "NCBITaxon:4530"
    elif taxon =="Intermediate(hybrid)": return "NCBITaxon:1080340"
    else: return "NCBITaxon:4530"  #this is the generic oryza stativa NCBITaxon

def col14():
    """Date: required"""
    date=str(time.strftime('%m%d%Y'))
    return date

#not required
def col15():
    """Assigned by: not required"""
    return "Planteome:Austin_Meier"

#not required for GAF, but required for germplasm
def col16(accession,testtrait):
    """Annotation extension: required (for germplasm)"""
    #
    if accession[testtrait['colnum']] !="":
        return testtrait['pheno_relation'].format(accession[testtrait['colnum']],testtrait['unit'])
    else:
        # ERRORFILE.write("Accession:%s has no score for %s"%(accession[0],testtrait[1]))
        logger.warning("Accession:{} has no score for {}".format(accession[0],testtrait['name']))
        return False






#########################################################################
#                    run actual code here
#########################################################################




if __name__ == "__main__":
    load_map(mapfile)
    # print rawdata
    # print len(testtraitlist)
    main(testtraitlist,rawdata)

#
# print len(testtraitlist)
# print testtraitlist