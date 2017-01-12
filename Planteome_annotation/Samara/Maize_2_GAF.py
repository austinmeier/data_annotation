

#imports

import time
import csv
import requests
import json
import logging

#config
logger = logging.getLogger(__name__)
logging_format = "[%(levelname)s] %(name)s %(asctime)s %(message)s"
logging.basicConfig(format=logging_format, level=logging.DEBUG) #filename=errors,


# scrape_file = '/Users/meiera/Documents/Jaiswal/Planteome/GRIN_global/all_maize_GRIN_lines_Samara.tsv'  # maize
scrape_file = '/Users/meiera/Documents/Jaiswal/Planteome/GRIN_global/wheat_GRIN_samara_minusBarley.tsv'  # wheat
# OUTFILE = '/Users/meiera/Documents/Jaiswal/Planteome/GRIN_global/gaf/maize_gaf.assoc.1'  # maize
OUTFILE = '/Users/meiera/Documents/Jaiswal/Planteome/GRIN_global/gaf/wheat_gaf.assoc'  # wheat

# The mapfile is downloaded from MAL's google doc- Maize mappings.  The mapping is dated so new versions can be identified easily.
mapfile = '/Users/meiera/Documents/Jaiswal/Planteome/GRIN_global/maps/maize_map_10-12-16.tsv'

ERRORFILE = '/Users/meiera/Documents/Jaiswal/Planteome/GRIN_global/scraped_lines_not_included.txt'

logger.info('Raw scraped data: {}\nDestination of new GAF: {}\n'.format(scrape_file,OUTFILE))

# Taxon mapping was done by hand using the below grin taxon identifiers
maizetaxons =  {103579:'NCBITaxon:4576',
                   103580:'NCBITaxon:15945',
                   103582:'NCBITaxon:4579',
                   311986:'NCBITaxon:4575',  #this one I just binned into zea
                   311987:'NCBITaxon:381124',
                   400366:'NCBITaxon:76912',
                   410702:'NCBITaxon:112001',
                   417868:'NCBITaxon:1293079',
                   42209:'NCBITaxon:4580',
                   }
#
wheattaxons = {
    40544: 'NCBITaxon:4565',
    406896: 'NCBITaxon:4567',
    406901: 'NCBITaxon:4565',
    406902: 'NCBITaxon:4565',
    406903: 'NCBITaxon:4565',
    406904: 'NCBITaxon:4565',
}




# GRINTaxon:103579 Zea diploperennis H. H. Iltis et al.
# GRINTaxon:103580 Zea luxurians (Durieu & Asch.) R. M. Bird
# GRINTaxon:103582 Zea mays L. subsp. mexicana (Schrad.) H. H. Iltis
# GRINTaxon:311986 Zea hybr.
# GRINTaxon:311987 Zea mays L. subsp. mays
# GRINTaxon:400366 Zea mays L. subsp. parviglumis H. H. Iltis & Doebley
# GRINTaxon:410702 Zea mays L. subsp. huehuetenangensis (H. H. Iltis & Doebley) Doebley
# GRINTaxon:417868 Zea nicaraguensis H. H. Iltis & B. F. Benz
# GRINTaxon:42207 Zea mays L.
# GRINTaxon:42209 Zea perennis (Hitchc.) Reeves & Mangelsd.

# the result of the reference mapping using crossref.org  Manually edited the ones that are incorrect to use just 'GRIN' like those without a reference.

# check that the returned DOIs return the correct papers by adding them to the following URL:
# http://dx.doi.org/DOI:


crossref_org_results = {
    ". . C7. unspecified Skdlsj.": "GRIN",
    ". . PVP 7900036. Off. J. Pl. Var. Protect. Off.": "GRIN",
    "Anderson, E., and W. L. Brown. 1951. The Standard Exotics.. Maize Gen Coop Newsl 25: 17-18.": "GRIN",
    "Anonymous. 1961. Minutes of the North Central Corn Breeding Research Committee, Chicago, IL, March 1-2, 1961.. unspecified .": "GRIN",
    "Anonymous. 1987. Seedsmans Handbook 14th Edition, Mike Brayton Seeds, Inc.. unspecified .": "GRIN",
    "Anonymous. 1989. Seedsmans Handbook 16th Edition, Mike Brayton Seeds, Inc.. unspecified .": "GRIN",
    "Bryan, A.A., and R.W. Jugenheimer. 1937. Hybrid corn in Iowa. Iowa Agric.. unspecified Iowa Agric. Exp. Stn. Bull. 366..|Bryan, A.A., and R.W. Jugenheimer. 1937. Hybrid corn in Iowa.. (unspecified) Iowa Agric. Exp. Stn. Bull. 366.": "GRIN",
    "Bryan, A.A., and R.W. Jugenheimer. 1937. Hybrid corn in Iowa.. (unspecified) Iowa Agric. Exp. Stn. Bull. 366.": "GRIN",
    "Buendgen, M.R., Hable, B.J.. 1996. Inbred corn line ZS1679. US Patent Number 5,589,606. U.S. Patent 5,589,606": "10.1002/bbb.115",
    "C.A. Abel, R.L. Wilson, J.C. Robbins. 1995. Peruvian Maize Resistance to O. nubilalis. unspecified 88:1045-1046.": "10.1093/jee/88.4.1044",
    "C.A. Abel, R.L. Wilson, J.C. Robbins. 1995. Peruvian Maize Resistance to O. nubilalis. unspecified 88:1045-1048.": "10.1093/jee/88.4.1044",
    "Carlone Jr, M.R.. 1997. Inbred corn line ZS1022. US Patent Number 5,602,314. U.S. Patent 5,602,314": "GRIN",
    "Colorado State University, Department of Agronomy. 1961. The Colorado Corn Collection. unspecified Maize Genetics Cooperation News Letter.|Dr. David W. Crumpacker. 1961. Colorado's Open-Pollinated Corn Varieties. unspecified Colorado Farm and Home Research.": "GRIN",
    "David V. Uhr and Major M. Goodman. 1995. Temperate Maize Inbreds Derived from Tropical Germplasm: I. Testcross Yield Trials. Crop Sci. (Madison) 35:779-784": "10.2135/cropsci1995.0011183x003500030024x",
    "Eagles, H. A. and Brooking, I. R.. 1981. Populations of maize with more rapid and reliable seedling emergence than cornbelt dents at low temperatures. Euphytica 30(3):755-763.": "10.1007/bf00038805",
    "Edward S. Buckler, et al.. 2009. The Genetic Architecture of Maize Flowering Time. Science 325:714-718.|Michael D. McMullen, et al.. 2009. Genetic Properties of the Maize Nested Association Mapping Population. Science 325:737-740.|Sherry A. Flint-Garcia, Anne-Celine Thuillet, Jianming Yu, Gael Pressoir, Susan M. Romero, Sharon E. Mitchell, John Doebley, Stephen Kresovich, Major M. Goodman, Edward S. Buckler. 2005. Maize association population: a high-resolution platform for quantitative trait locus dissection. Plant J 44 (6), 1054-1064.": "10.1111/j.1365-313x.2005.02591.x",
    "Edward S. Buckler, et al.. 2009. The Genetic Architecture of Maize Flowering Time. Science 325:714-718.|Michael D. McMullen, et al.. 2009. Genetic Properties of the Maize Nested Association Mapping Population. Science 325:737-740.|Sherry A. Flint-Garcia, Anne-Celine Thuillet, Jianming Yu, Gael Pressoir, Susan M. Romero, Sharon E. Mitchell, John Doebley, Stephen Kresovich, Major M. Goodman, Edward S. Buckler. 2005. Maize association population: a high-resolution platform for quantitative trait locus dissection. Plant J 44 (6), 1054-1064.|R.A. Moreau, V. Singh, and K.B. Hicks. 2001. Comparison of Oil and Phytosterol Levels in Germplasm Accessions of Corn, Teosinte, and Job's Tears. J Agric Food Chem 49:3793-3795.": "10.1111/j.1365-313x.2005.02591.x",
    "Fleming, A.A.. 1983. Family grows same corn for 200 years.. unspecified Crops and Soils, January 1983:5-6.": "10.1016/0378-4290(83)90019-9",
    "Fleming, A.A.. 1983. Family grows some corn for 200 years.. unspecified Crops and Soils, January 1983:5-6.": "10.1007/978-1-349-05106-9_2",
    "Hardacre, A. K. and Eagles, H. A.. 1980. Comparisons Among Populations of Maize for Growth at 13C. Crop Sci 20(6):780-784.": "10.2135/cropsci1980.0011183x002000060025x",
    "Henderson, C.B.. 1976. Maize Research and Breeders Manual No. 8, Illinois Foundation Seeds, Inc.. unspecified .": "10.2172/876683",
    "Henderson, C.B.. 1976. Maize Research and Breeders Manual No. 8, Illinois Foundation Seeds, Inc.. unspecified .|Rossman, C.E.. 1964. Released inbred lines of corn. (unspecified) Michigan Agric. Exp. Stn. Quarterly Bull.": "10.1111/j.2041-5370.1994.tb01908.x",
    "L. Zhou, J. Zhang, J. Yan, and R. Song. 2011. Two transposable element insertions are causative mutations for the major domestication gene teosinte branced 1 in modern maize. Cell Res 21(8):1267-1270. doi:10.1038/cr.2011.104|R.A. Moreau, V. Singh, and K.B. Hicks. 2001. Comparison of Oil and Phytosterol Levels in Germplasm Accessions of Corn, Teosinte, and Job's Tears. J Agric Food Chem 49:3793-3795.": "10.1038/cr.2011.104",
    "Lerette, R.J.. 1997. Inbred corn line ZSO541. US Patent Number 5,625,131. U.S. Patent 5,625,131": "10.1016/s0172-2190(97)90099-5",
    "Martin-Ortigosa, S., Valenstein, J. S., Lin, V. S. Y., Trewyn, B. G. and Wang, K.. 2012. Gold Functionalized Mesoporous Silica Nanoparticle Mediated Protein and DNA Codelivery to Plant Cells Via the Biolistic Method. Advanced Funct Mater .": "10.1002/adfm.201290102",
    "Messmer, M.J., Stelpflug, R.G.. 1997. Inbred corn line ZS1202. US Patent Number 5,602,315. U.S. Patent 5,602,315": "10.1126/science.315.5812.602",
    "N.W. Widstrom and M.E. Snook. 2001. EPM6 and SIM6 MAIZE. Crop Sci 41(6):2009-2010.": "10.2135/cropsci2001.2009",
    "Pablo Garcia-Palacios, Ruben Milla, Manuel Delgado-Baquerizo, Nieve Martin-Robles, Monica Alvaro-Sanchez, and Diana H. Wall. 2013. Side-Effects of Plant Domestication: Ecosystem Impacts of Changes in Litter Quality. New Phytol 198: 504-513.": "10.1111/nph.12127",
    "R. Bernardo, J. Romero-Severson, J. Ziegle, J. Hauser, L. Joe, G. Hookstra, and R.W. Doerge. 2000. Parental contribution and coefficient of coancestry among maize inbreds: pedigree, RFLP, and SSR data. Theor Appl Genet 100:552-556.": "10.1007/s001220050072",
    "R.A. Moreau, V. Singh, and K.B. Hicks. 2001. Comparison of Oil and Phytosterol Levels in Germplasm Accessions of Corn, Teosinte, and Job's Tears. J Agric Food Chem 49:3793-3795.": "10.1021/jf010280h",
    "R.A. Moreau, V. Singh, and K.B. Hicks. 2001. Comparison of Oil and Phytosterol Levels in Germplasm Accessions of Corn, Teosinte, and Job's Tears. J Agric Food Chem 49:3793-3795.|C.A. Abel, R.L. Wilson, J.C. Robbins. 1995. Peruvian Maize Resistance to O. nubilalis. unspecified 88:1045-1048.": "10.1021/jf010280h",
    "R.A. Moreau, V. Singh, and K.B. Hicks. 2001. Comparison of Oil and Phytosterol Levels in Germplasm Accessions of Corn, Teosinte, and Job's Tears. J Agric Food Chem 49:3793-3795.|Marshall D. Sundberg; Christopher LaFargue; Alan R. Orr. 1995. Inflorescence Development in the \"Standard Exotic\" Maize, Argentine Popcorn (Poaceae). Amer J Bot Vol. 82, No. 1. (Jan., 1995), pp. 64-74..|Anderson, E., and W. L. Brown. 1951. The Standard Exotics.. Maize Gen Coop Newsl 25: 17-18.": "10.2307/2445788",
    "R.A. Moreau, V. Singh, and K.B. Hicks. 2001. Comparison of Oil and Phytosterol Levels in Germplasm Accessions of Corn, Teosinte, and Job's Tears. J Agric Food Chem 49:3793-3795.|Sanchez G., J.J., M.M. Goodman, and C.W. Stuber. 2000. Isozymatic and morphological diversity in the races of maize of Mexico.. Econ Bot Econ. Bot. 54:43-59..": "10.1007/bf02866599",
    "Rhodes C.A., Carey E. E., Dickinson D.B.. 1982. Illinois sweet corn inbreds with the su se genotype.. (HortScience) 17:411-412": "10.1104/pp.63.3.416",
    "Rossman, E.C.. 1964. Released Inbred Lines of Corn, Michigan Agricultural Experiment Station Quarterly Bulletin.. unspecified 46(4):499-501.": "10.4148/2378-5977.1077",
    "Rossman, E.C.. 1964. Released Inbred Lines of Corn, Michigan Agricultural Experiment Station Quarterly Bulletin.. unspecified 46(4):499-501.|Rossman, C.E.. 1964. Released inbred lines of corn. (unspecified) Michigan Agric. Exp. Stn. Quarterly Bull.": "10.2135/cropsci1964.0011183x000400050039x",
    "Rossman, E.C.. 1964. Released Inbred Lines of Corn, Michigan Agricultural Experiment Station Quarterly Bulletin.. unspecified 46(4):499-501.|Rossman, E.C.. 1954. Released inbred lines of corn. (unspecified) Michigan Agric. Exp. Stn. Quarterly Bull.": "10.2134/agronj1954.00021962004600050015x",
    "Rossman, E.C.. 1964. Released Inbred Lines of Corn, Michigan Agricultural Experiment Station Quarterly Bulletin.. unspecified 46(4):499-501.|Rossman, E.C.. 1958. Released inbred lines of corn. unspecified Michigan Agric. Exp. Stn. Quarterly Bull..|Rossman, C.E.. 1964. Released inbred lines of corn. (unspecified) Michigan Agric. Exp. Stn. Quarterly Bull.": "10.1021/jf60169a007",
    "Rossman, E.C.. 1964. Released Inbred Lines of Corn, Michigan Agricultural Experiment Station Quarterly Bulletin.. unspecified 46(4):499-501.|Rossman, E.C.. 1964. Released inbred lines of corn. (unspecified) Michigan Agric. Exp. Stn. Quarterly Bull.": "10.2135/cropsci1964.0011183x000400050039x",
    "Sanchez G., J.J., M.M. Goodman, and C.W. Stuber. 2000. Isozymatic and morphological diversity in the races of maize of Mexico.. Econ Bot Econ. Bot. 54:43-59..": "10.1007/bf02866599",
    "Sanchez Gonzalez, J., T.A. Kato Yamakake, M. Aguilar Sanmiguel, J.M. Hernandez Casillas, A. Lopez Rodriguez, and J.A. Ruiz Corral. 1998. Distribucion y Caracterization del Teocintle. unspecified INIFAP, Mexico.": "10.2135/cropsci2010.09.0538",
    "Sherry A. Flint-Garcia, Anne-Celine Thuillet, Jianming Yu, Gael Pressoir, Susan M. Romero, Sharon E. Mitchell, John Doebley, Stephen Kresovich, Major M. Goodman, Edward S. Buckler. 2005. Maize association population: a high-resolution platform for quantitative trait locus dissection. Plant J 44 (6), 1054-1064.": "10.1111/j.1365-313x.2005.02591.x",
    "Sherry A. Flint-Garcia, Anne-Celine Thuillet, Jianming Yu, Gael Pressoir, Susan M. Romero, Sharon E. Mitchell, John Doebley, Stephen Kresovich, Major M. Goodman, Edward S. Buckler. 2005. Maize association population: a high-resolution platform for quantitative trait locus dissection. Plant J 44 (6), 1054-1064.|. 1950. Eleventh Annual Corn Improvement Conference of the North Central Region.": "10.1111/j.1365-313x.2005.02591.x",
    "Sherry A. Flint-Garcia, Anne-Celine Thuillet, Jianming Yu, Gael Pressoir, Susan M. Romero, Sharon E. Mitchell, John Doebley, Stephen Kresovich, Major M. Goodman, Edward S. Buckler. 2005. Maize association population: a high-resolution platform for quantitative trait locus dissection. Plant J 44 (6), 1054-1064.|Anonymous.. 1987. Seedsmans handbook 14th edition.. unspecified .": "10.1111/j.1365-313x.2005.02591.x",
    "Sherry A. Flint-Garcia, Anne-Celine Thuillet, Jianming Yu, Gael Pressoir, Susan M. Romero, Sharon E. Mitchell, John Doebley, Stephen Kresovich, Major M. Goodman, Edward S. Buckler. 2005. Maize association population: a high-resolution platform for quantitative trait locus dissection. Plant J 44 (6), 1054-1064.|C.A. Abel, R.L. Wilson, J.C. Robbins. 1995. Peruvian Maize Resistance to O. nubilalis. unspecified 88:1045-1048.": "10.1111/j.1365-313x.2005.02591.x",
    "Sherry A. Flint-Garcia, Anne-Celine Thuillet, Jianming Yu, Gael Pressoir, Susan M. Romero, Sharon E. Mitchell, John Doebley, Stephen Kresovich, Major M. Goodman, Edward S. Buckler. 2005. Maize association population: a high-resolution platform for quantitative trait locus dissection. Plant J 44 (6), 1054-1064.|Henderson, C.B.. 1976. Maize Research and Breeders Manual No. 8, Illinois Foundation Seeds, Inc.. unspecified .": "10.1111/j.1365-313x.2005.02591.x",
    "Sherry A. Flint-Garcia, Anne-Celine Thuillet, Jianming Yu, Gael Pressoir, Susan M. Romero, Sharon E. Mitchell, John Doebley, Stephen Kresovich, Major M. Goodman, Edward S. Buckler. 2005. Maize association population: a high-resolution platform for quantitative trait locus dissection. Plant J 44 (6), 1054-1064.|R.A. Moreau, V. Singh, and K.B. Hicks. 2001. Comparison of Oil and Phytosterol Levels in Germplasm Accessions of Corn, Teosinte, and Job's Tears. J Agric Food Chem 49:3793-3795.": "10.1111/j.1365-313x.2005.02591.x",
    "Sherry A. Flint-Garcia, Anne-Celine Thuillet, Jianming Yu, Gael Pressoir, Susan M. Romero, Sharon E. Mitchell, John Doebley, Stephen Kresovich, Major M. Goodman, Edward S. Buckler. 2005. Maize association population: a high-resolution platform for quantitative trait locus dissection. Plant J 44 (6), 1054-1064.|Rossman, E.C.. 1964. Released Inbred Lines of Corn, Michigan Agricultural Experiment Station Quarterly Bulletin.. unspecified 46(4):499-501.": "10.1111/j.1365-313x.2005.02591.x",
    "Sherry A. Flint-Garcia, Anne-Celine Thuillet, Jianming Yu, Gael Pressoir, Susan M. Romero, Sharon E. Mitchell, John Doebley, Stephen Kresovich, Major M. Goodman, Edward S. Buckler. 2005. Maize association population: a high-resolution platform for quantitative trait locus dissection. Plant J 44 (6), 1054-1064.|Wicks, Z.W. III, M.L. Carson, and D.L. Robbins. 1986. Registration of SD40 Parental Line of Maize. Crop Sci. (Madison) Crop Sci. 26(6):1267": "10.1111/j.1365-313x.2005.02591.x",
    "Stelpflug R.G., Messmer M.J.. 1997. Inbred corn line ZS1783. US Patent Number 5,602,316. U.S. Patent 5,602,316": "GRIN",
    "Stelpflug, R.G., Messmer, M.J.. 1996. Inbred corn line ZS1284. US Patent Number 5,569,820. U.S. Patent 5,569,820": "GRIN",
    "Troyer, A.F.. 1986. Inbred corn line. US Patent Number 4,594,810. U.S. Patent 4,594,810": "GRIN",
    "W. Paul Williams, Frank M. Davis. 2000. Two Maize Germplasm Lines. Crop Sci 40(2):584.": "10.2135/cropsci2000.0015rgp",
    "Wicks, Z.W. III, M.L. Carson, and D.L. Robbins. 1986. Registration of SD41 Parental Line of Maize. Crop Sci. (Madison) Crop Sci. 26(6):1267-1268": "10.2135/cropsci1986.0011183x002600060062x",
    "William F. Tracy, Sherry R. Whitt and Edward S. Buckler. 2006. Recurrent Mutation and Genome Evolution: Example of Sugary1 and the Origin of Sweet Maize. Crop Sci 46:49-54.": "10.2135/cropsci2006-03-0149tpg",
    "William F. Tracy, Sherry R. Whitt and Edward S. Buckler. 2006. Recurrent Mutation and Genome Evolution: Example of Sugary1 and the Origin of Sweet Maize. Crop Sci 46:49-54.|R.A. Moreau, V. Singh, and K.B. Hicks. 2001. Comparison of Oil and Phytosterol Levels in Germplasm Accessions of Corn, Teosinte, and Job's Tears. J Agric Food Chem 49:3793-3795.": "10.2135/cropsci2006-03-0149tpg",
    "Y. Wu, M. Campbell, Y. Yen, Z. Wicks, and A.M.H. Ibrahim. 2009. Genetic analysis of high amylose content in maize (Zea mays L.) using a triploid endosperm model. Euphytica 166:155-164.": "10.1007/s10681-008-9798-y"
}



# the database- needs a dbxref if links are to work correctly
DATABASE_1 = 'GRIN'

# evidence code.  Self explainatory
EVIDENCE_CODE_7 = 'EXP'

# aspect is 'T' for trait.
ASPECT_9 = 'T'

# everything is germplasm
OBJECT_TYPE_12 = 'germplasm'

# Date will be generated at the time of running this script
DATE_14 = str(time.strftime('%m%d%Y'))

# Default to me, the script's author
ASSIGNED_BY_15 = 'Planteome:Austin_Meier'

wheatmapfile = '/Users/meiera/Downloads/GRINDesc_mappings_wheat.tsv'
wheattraitmap = {}

with open(wheatmapfile, 'r') as infile:
    for row in infile:
        rowlist = row.split("\t")
        if rowlist[3]:
            wheattraitmap[rowlist[0]] = rowlist[3]



def mapmaker(mapfile):
    """pass in a tsv, returns a dictionary with keys"""
    grin_decoder = {}
    with open(mapfile,'r') as i:
        map = csv.reader(i, delimiter='\t', quotechar='"')
        for row in map:
            # if
            if len(row[6]) >= 1:
                grin_key = row[6].split('|')
                for gk in grin_key:
                    grin_decoder[gk] = row[2]

    # print len(grin_decoder)
    return grin_decoder


def GAF_convert(x, trait_translator, taxon_translator, ref_hash): # pass in the split list, the mapping to TO terms, and the reference hash table
    gafline=[col1(),
             col2(x),
             col3(x),
             col4(),
             col5(x,trait_translator),
             col6(x, ref_hash),
             col7(),
             col8(x),
             col9(),
             col10(x),
             col11(x),
             col12(),
             col13(x,taxon_translator),
             col14(),
             col15(),
             col16(x),
             ""
             ]
    logger.debug(gafline)
    return gafline



# required
def col1():
    """the database"""
    return DATABASE_1

#required
def col2(x):
    """Database object ID"""
    try:  # the ID is in the scrape as 'GRIN:xxxxxxx'
        obj_ID = x[8].split(':')[1]
        return obj_ID
    except:
        return False

#required
def col3(x):
    """Database object symbol"""
    #check if name field is populated
    if x[10] != "":
        #return the germplasm name
        return x[10].strip("'")
    elif x[9] != "":
        return x[9].strip("'")
    else:
        return False

#not required
def col4():
    """qualifier- never used"""
    return ""

#required
def col5(x,trait_translator):
    """Direct Annotation - TO:xxxxxxx"""
    if x[2] in trait_translator:
        return trait_translator[x[2]]
    else:
        return False

#required
def col6(x, ref_hash):
    """Database reference - PMID"""
    # url = 'https://api.crossref.org/works'
    # if x[12].strip() != "":
    #     str_ref = x[12].strip()
    #
    #     if str_ref in ref_hash:
    #         return ref_hash[str_ref]
    #     else:
    #         data = {'query':str_ref}
    #         r = requests.get(url, params=data)
    #         api_doi = json.loads(r.text)
    #         try:
    #             ref_hash[str_ref] = api_doi['message']['items'][0]['DOI']
    #             return 'DOI:%s'%(ref_hash[str_ref])
    #         except KeyError:
    #             ref_hash[str_ref] = 'GRIN'  # put the GRIN default in the ref_hash to prevent extra API calls
    #             print "API call for {} did not return an items.  It returned:\n{}".format(str_ref, api_doi)
    #         except requests.exceptions.ConnectionError:
    #             ref_hash[str_ref] = 'GRIN'  # put the GRIN default in the ref_hash to prevent extra API calls
    #             print "Connection failed {}.".format(str_ref, )
    #
    # else:
    #     return "GRIN"
    # return 'GRIN'
    grindescript = x[2]
    return grindescript

#required
def col7():
    """Evidence code"""

    return EVIDENCE_CODE_7

#not required
def col8(x):
    """With or From"""
   #return the country that the germplasm was collected in.
    if x[11] != "":
        return "from_country(%s)"%(x[11].replace(" ","_"))  #spaces not allowed in this column
    else:
        return ""

#required
def col9():
    """Aspect"""
    return ASPECT_9

#not required
def col10(x):
    """DB Object name - name of the germplasm"""
    if x[10] != "":
        return x[10].strip("'")  # x[10] is the accession name
    else:
        return x[9].strip("'")  # if the name is absent, use the PI number


#not required
def col11(x):
    """synonyms"""
    synonyms = []
    for i in [x[9], x[10]]:
        if i != "":
            synonyms.append(i.strip("'"))
    if len(synonyms) > 0:
        return "|".join(synonyms)
    else:
        return ""


#required
def col12():
    """Object type"""
    return OBJECT_TYPE_12

#required
def col13(x,taxon_translator):
    """Taxon"""
    if x[0]:
        grintaxon = x[0].split(":")[1]
        ncbitaxon = taxon_translator.get(int(grintaxon),False)
        logger.debug('the scraped line GRINTaxon: {}'.format(grintaxon))
        logger.debug('the new NCBITaxon: {}'.format(ncbitaxon))

        return ncbitaxon
    else:
        logger.error('column1 was blank.  No GRINTaxon.')
        return False



#required
def col14():
    """Date"""
    return DATE_14

#not required
def col15():
    """Assigned by"""
    return ASSIGNED_BY_15

#not required for GAF, but required for germplasm
def col16(x):
    """Annotation Extension- phenotype score goes here"""
    phenotype_name = replace_illegal_chars(x[3])
    phenotype_score = replace_illegal_chars(x[7])
    return "has_phenotype_score({}={})".format(phenotype_name, phenotype_score)


def replace_illegal_chars(text):
    illegals = [' ', '(', ')', '|', ',']
    for ch in illegals:
        if ch in text:
            text = text.replace(ch, '_')
    return text


###############################

def main():
    # trait_translator = mapmaker(mapfile)  # for maize
    trait_translator = wheattraitmap  # for wheat
    taxon_translator = wheattaxons
    # send in empty dictionary the first time.  Then you can replace it once you manually verify the returned DOIs
    ref_hash = {}
    # ref_hash = crossref_org_results
    with open(scrape_file,'r') as scrape, open(ERRORFILE) as errors, open(OUTFILE, 'w') as outfile:
        outfile.write("!gaf-version: 2.0\n")
        next(scrape) #skips the header row
        for observation in scrape:
            linelist = observation.split('\t')
            gafline = GAF_convert(linelist,trait_translator,taxon_translator, ref_hash)
            if False in gafline:
                continue
            else:
                writable = '\t'.join(gafline)
                outfile.write(writable)
                outfile.write('\n')


    # uncomment this to see all the papers referenced and their DOI
    print json.dumps(ref_hash, sort_keys=True,indent=4, separators=(',', ': '))


if __name__ == "__main__":
    main()



#
# sy = ['a','b','c','d','e','f','g','h','h','h','h']
# u=col10(sy)
#
# print u
