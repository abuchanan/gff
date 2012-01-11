def reader(path):
    """Read a GFF3 file, returning a Feature for every valid line."""

    with open(path) as fh:
        for line in fh:
            if line[:2] != '##':
                try:
                    yield Feature.from_string(line.strip())
                except InvalidGFFString:
                    pass


class InvalidGFFString(Exception): pass

class Feature(object):

    @classmethod
    def from_string(cls, raw):
        """Parse a GFF3 line."""

        cols = raw.split('\t')
        if len(cols) != 9:
            raise InvalidGFFString("invalid number of columns in raw GFF string")

        return cls(*cols)

    def __init__(self, seqid, source, feature_type, start, end, score, strand,
                 phase, raw_attributes):

        self.seqid = seqid
        self.source = source
        self.type = feature_type

        try:
            self.start = int(start)
            self.end = int(end)
        except ValueError:
            raise InvalidGFFString("couldn't parse start or end value")

        self.length = self.end - self.start + 1
        self.score = score
        self.strand = strand
        self.phase = phase
        self.raw_attributes = raw_attributes

        self.attributes = {}
        for token in raw_attributes.split(';'):
            if token != '':
                k, v = token.split("=")
                self.attributes[k] = v

    def __str__(self):
        return '\t'.join([self.seqid, self.source, self.type, str(self.start), 
                          str(self.end), self.score, self.strand, self.phase, 
                          self.raw_attributes])
