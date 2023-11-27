# is used this file to transform the xml content of the editions and transcriptions into txt format
from lxml import etree


def xml2txt(infile,outfile):
    tree = etree.parse(infile)
    # use xpath to extract all the sentences from the sampled file
    sentences = tree.xpath(".//sentence/text()")
    with open(outfile,"w") as out:
        for i,sent in enumerate(sentences):
            # print(sent)

            # if last sentence then do not add newline
            if i != len(sentences)-1:
                out.write(sent+"\n")
            else:
                out.write(sent)



xml2txt("samples_editions.xml","editions.txt")

xml2txt("samples_transcriptions.xml","transcriptions.txt")