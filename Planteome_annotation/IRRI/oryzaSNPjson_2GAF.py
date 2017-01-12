import time
import urllib2
import json
import re

outdir = "/Users/meiera/Documents/SVN/associations/to-associations/test_IRRI_TO/"

traitdict ={}   #this is what we will use
with open("/Users/meiera/Documents/git/data_annotation/Planteome_annotation/IRRI/OryzaSNPtraitmap.csv") as infile:
    for line in infile:
        line1 = line.split(',')
        traitdict[line1[0]] =  {'TOid':line1[1].strip(),'traitname':line1[2].strip(),'evidencecode':'IDA'}


sampletraitdict ={  ### this is what the actual trait dictionary looks like
    # 43718:{'TOid':'TO:0000269','traitname':'100-grain weight (gm) - cultivated','evidencecode':'IDA'},
    # 43693:{'TOid':'TO:0000140','traitname':'Apiculus color at post-harvest','evidencecode':'IDA'},
    # 43694:{'TOid':'TO:0000140','traitname':'Apiculus color at reproductive','evidencecode':'IDA'},
    # 43695:{'TOid':'TO:0000294','traitname':'Auricle color at vegetative','evidencecode':'IDA'},
    # 43696:{'TOid':'TO:0000141','traitname':'Awn color','evidencecode':'IDA'},
    43766:{'TOid':'TO:0000141','traitname':'Awn color (Late observation)','evidencecode':'IDA'}

}

#########################################################################
#                           MAIN
#########################################################################



def main(traitdict):
    for x in traitdict:
        trait = traitdict[x] #returns a dictionary
        outname = re.sub('[^a-zA-Z0-9 \n\.]', '', trait['traitname'])
        outfile = "%s%s_OryzaSNP.assoc"%(outdir,outname.replace(" ","_"))
        with open(outfile, "w") as assocfile:
            assocfile.write("!gaf-version: 2.0\n")
            trait_json= mk_json(x)
            print trait_json
            for object in trait_json:
                gafline(object,trait,assocfile)


#########################################################################
#                       web calls
#########################################################################

def mk_json(traitnumber): #traitnumber is the ID that Oryzasnp uses, eg: 43696
    phenotypeID= str(traitnumber)
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
             and col9() and col12() and col13(phenotype_object) and col14() and col15 and col16(phenotype_object,testtrait):

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
            col16(phenotype_object,testtrait)+"\t"+
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
        return str(phenotype_object['irisId']).replace(" ","_")
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
    return testtrait['TOid']

#required
def col6():
    #return IRIC  (no pmid)
    return "IRIC"

#required
def col7(testtrait):
    #return the evidence code
    return testtrait['evidencecode']

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
    return "Planteome:Austin_Meier"

#not required for GAF, but required for germplasm
def col16(phenotype_object,phenotypename):
    """displays the phenotype score along with the trait name as recorded.  No spaces allowed."""
    if 'value' in phenotype_object:
        #return the value
        phenotype_value = str(phenotype_object['value']).replace(" ", "_")
        return "has_phenotype_score(" + phenotypename['traitname'].replace(" ", "_") + "=" + phenotype_value +")"
        #return phenotypename['traitname']+ str(phenotype_object['value'])
    else:
        print('record for\n', phenotype_object,"\nwill not be included.  It is missing a value")
        return False

    #return the variable (if it exists)
    #return the method, if it exists
    #return the evaluation location (evaluation_location(x))







#########################################################################
#                    run actual code here
#########################################################################
if __name__ == "__main__":
    main(traitdict)
