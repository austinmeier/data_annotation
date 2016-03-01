import obo


obofile= "/Users/meiera/Documents/git/ibp-cassava-traits/cassava-trait-ontology.obo"

parser = obo.Parser(open(obofile))
CTO = {}
for stanza in parser:
    CTO[stanza.tags["id"][0]] = stanza.tags


print CTO['CO_334:0000000']