import operator
import xml.sax


class msgfContentHandler(xml.sax.ContentHandler):
    def __init__(self, score_config):
        self.sii = dict()
        self.in_sii = False
        self.current_sii = None
        self.peptides = dict()
        self.in_peptide = False
        self.current_peptide = None
        self.in_pep_seq = False
        self.comparison_operator = score_config["comparison"]
        self.score_threshold = score_config["score_threshold"]
        self.score_name = score_config["score_name"]
        self.score_function = operator.attrgetter(score_config["comparison"])

    def characters(self, chars):
        if self.in_pep_seq:
            self.peptides[self.current_peptide] = chars

    def startElement(self, name, attrs):
        if name == "Peptide":
            self.peptides[attrs["id"]] = None
            self.in_peptide = True
            self.current_peptide = attrs["id"]

        if name == "PeptideSequence" and self.in_peptide:
            self.in_pep_seq = True

        if name == "SpectrumIdentificationItem":
            if attrs["rank"] == "1":
                self.in_sii = True
                self.current_sii = {"peptide_ref": attrs["peptide_ref"]}

        if self.in_sii and name == "cvParam":
            if attrs["name"] == self.score_name:
                if self.score_function(operator)(
                    float(attrs["value"]), self.score_threshold
                ):
                    self.current_sii[self.score_name] = attrs["value"]

    def endElement(self, name):
        if name == "SpectrumIdentificationItem" and self.in_sii:
            self.in_sii = False
            self.sii[self.current_sii["peptide_ref"]] = self.current_sii
            self.current_sii = None
        if name == "PeptideSequence":
            self.in_pep_seq = False
        if name == "Peptide":
            self.in_peptide = False


def parse_mzid(mzid_file, score_config):
    verified_peptides = set()
    parser = xml.sax.make_parser()
    ch = msgfContentHandler(score_config)
    parser.setContentHandler(ch)
    parser.parse(mzid_file)
    for peptide_ref in ch.sii.keys():
        verified_peptides.add(ch.peptides[peptide_ref])
    return verified_peptides
