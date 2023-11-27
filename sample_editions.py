# this script performs stratified sampling and samples in total 100 sentences from different editions, authors 
# and years from the editions/hbbw directory

import random
import os
from lxml import etree

# set random seed
random.seed(13)

def read_sentences_from_file(file_path):
    """This function takes the path to the xml file as input, parses it and extracts all the <sentence> elements. 
    It returns a list of these sentences."""

    # Parse the XML file and extract sentences
    tree = etree.parse(file_path)
    # get the root
    root = tree.getroot()
    # find all <sentence> elements
    sentences = root.findall("sentence")
    # return list
    return sentences

def stratified_sampling(sentences, num_samples_per_edition):
    """This function performs stratified sampling.
        Input: 
            - a list of sentences
            - number of samples per edition and author
            """
    # group sentences based on their edition and author
    edition_author_groups = {}
    # iterate over each sentnece and extract author and edition
    for sentence in sentences:
        edition = sentence.get("file_sent").split("hbbw/")[1].split("/")[0]
        author = sentence.get("author")
        # create this key to group the sentences
        key = f"{edition}-{author}"
        if key not in edition_author_groups:
            edition_author_groups[key] = []
        edition_author_groups[key].append(sentence)

    # sample sentences from each group to ensure representation from all editions and authors
    sampled_sentences = []
    for group_sentences in edition_author_groups.values():
        num_samples_available = len(group_sentences)
        if num_samples_available < num_samples_per_edition:
            # if there are fewer sentences available than required, take all available sentences
            sampled_sentences.extend(group_sentences)
        else:
            # if there are enough sentences, sample randomly
            sampled_sentences.extend(random.sample(group_sentences, k=num_samples_per_edition))

    return sampled_sentences

# read sentences from the "all_latin_editions.xml" file
output_file_path = "full_text_xml/all_latin_editions.xml"
sentences = read_sentences_from_file(output_file_path)

# perform stratified sampling to randomly select 5 sentences from each edition and author (we have 24 editions)
sampled_sentences = stratified_sampling(sentences, num_samples_per_edition=5)

# shuffle the sampled sentences to ensure randomization
random.shuffle(sampled_sentences)

# take the first 100 sentences to ensure we have exactly 100 sampled sentences
# so that we have in the end 50% sample sentences from the editions and 50% from the transcriptions
sampled_sentences = sampled_sentences[:100]

# sort the sampled sentences based on their edition
# to be able to write it ordered to the output file
sampled_sentences.sort(key=lambda s: s.get("file_sent").split("hbbw/")[1].split("/")[0])

# create a new root element for the output XML
new_root = etree.Element("sampled_sentences")

# append the sampled sentences to the new root
for idx, sentence in enumerate(sampled_sentences, start=1):
    new_sentence = etree.Element("sentence", attrib=sentence.attrib)
    new_sentence.text = sentence.text
    # add this as a counter of number of samples to each sample sentence
    new_sentence.set("sampled_sent", str(idx))
    new_root.append(new_sentence)

# create a new XML tree with the new root element
new_tree = etree.ElementTree(new_root)

# write the new XML to the output file "sampled_sentences.xml"
output_file_path = "samples/samples_editions.xml"
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
with open(output_file_path, "wb") as f:
    new_tree.write(f, pretty_print=True, encoding="utf-8", xml_declaration=True)
