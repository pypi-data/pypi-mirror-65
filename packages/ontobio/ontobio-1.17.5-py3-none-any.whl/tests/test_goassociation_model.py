from ontobio.model import association
from ontobio.io import gafparser
from ontobio.io import gpadparser

def test_negated_qualifers():

    gaf = ["PomBase", "SPBC11B10.09", "cdc2", "NOT", "GO:0007275", "PMID:21873635", "IBA", "PANTHER:PTN000623979|TAIR:locus:2099478", "P", "Cyclin-dependent kinase 1", "UniProtKB:P04551|PTN000624043", "protein", "taxon:284812", "20170228", "GO_Central", "", ""]
    association = gafparser.to_association(gaf).associations[0]
    to_gaf = association.to_gaf_tsv()
    assert to_gaf[3] == "NOT"

    to_gpad = association.to_gpad_tsv()
    assert to_gpad[2] == "NOT"
