# this script performs stratified sampling and samples in total 100 sentences from different authors 
# and years from the non_edited/transcribed directory

import random
import os
from lxml import etree

# set random seed
random.seed(22)

def read_sentences_from_file(file_path):
    """This function takes the path to an xml file as input, parses it and extracts all <sentence> elements from the xml. 
        It returns a list of these sentences."""

    # Parse the XML file and extract sentences
    tree = etree.parse(file_path)
    # get the root
    root = tree.getroot()
    # find all <sentence> elements
    sentences = root.findall("sentence")
    # return the list of sentences
    return sentences

def stratified_sampling(sentences, num_samples_per_author):
    """This function performs stratified sampling.
        Input: 
            - list of sentences
            - number of samples per author
    """

    # group sentences by author
    author_groups = {}
    # iterate over the sentences and extracts the author attribute and 
    # creates a key using the author's name to group the sentences
    for sentence in sentences:
        author = sentence.get("author")
        if author not in author_groups:
            author_groups[author] = []
        author_groups[author].append(sentence)

    # sample sentences from each author to ensure representation from all authors
    sampled_sentences = []
    for group_sentences in author_groups.values():
        num_samples_available = len(group_sentences)
        if num_samples_available < num_samples_per_author:
            # if there are fewer sentences available than required, take all available sentences
            sampled_sentences.extend(group_sentences)
        else:
            # if there are enough sentences, sample randomly
            sampled_sentences.extend(random.sample(group_sentences, k=num_samples_per_author))

    return sampled_sentences

# read sentences from the "all_latin_transcribed.xml" file
output_file_path = "full_text_xml/all_latin_transcribed.xml"
sentences = read_sentences_from_file(output_file_path)

# perform stratified sampling to randomly select 5 sentences from each author
sampled_sentences = stratified_sampling(sentences, num_samples_per_author=5)

# shuffle the sampled sentences to ensure randomization
random.shuffle(sampled_sentences)

# take the first 100 sentences to ensure we have exactly 100 sampled sentences
sampled_sentences = sampled_sentences[:100]

# create a new root element for the output XML
new_root = etree.Element("sampled_sentences")

# append the sampled sentences to the new root
for idx, sentence in enumerate(sampled_sentences, start=1):
    new_sentence = etree.Element("sentence", attrib=sentence.attrib)
    new_sentence.text = sentence.text
    new_sentence.set("sampled_sent", str(idx))
    new_root.append(new_sentence)

# create a new XML tree with the new root element
new_tree = etree.ElementTree(new_root)

# write the new XML to the output file "samples_transcriptions.xml"
output_file_path = "samples/samples_transcriptions.xml"
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
with open(output_file_path, "wb") as f:
    new_tree.write(f, pretty_print=True, encoding="utf-8", xml_declaration=True)
