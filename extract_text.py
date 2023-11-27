# this script is used to extract the latin sentences from the bullinger corpus
# extract texts from editions/hbbw/ and non_edited/transcribed


import os
import glob
from lxml import etree

def extract_text_within_tags(element, target_lang):
    """
    Extract text from an element, including text within the specified language tag.
    """
    # empty list to store the extracted text parts
    text_parts = []
    # iterate over itertext() of the element which includes the text content of the element and all its descendants
    for text in element.itertext():
        # check if the text content of the current element is non-empty after stripping whitespace characters 
        # and if the current element's language tag is in the target_lang list (in our case only "la")
        if text.strip() and element.get("lang") in target_lang:
            # append stripped text
            text_parts.append(text.strip())
    # join the collected texts parts back into a string
    return " ".join(text_parts)

def extract_and_write_sentences(input_files, output_file):
    """This function extracts the sentences from the input files and writes them into an xml output file.
        Input: 
            - list of file paths
        Output:
            - output file path
    """

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # initialize a new xml root element for the output XML
    new_root = etree.Element("sentences")

    # iterate over each input file in the input_files list
    for input_file in input_files:
        # Parse the XML file for every file and get the root element
        tree = etree.parse(input_file)
        root = tree.getroot()

        # find all <s> elements with language attribute "la"
        sentences = root.findall(".//letter/div/p/s[@lang='la']")

        # extract author's name and the year from the document if they are available
        sender_name_elem = root.find(".//sender/person/name")
        sender_name = sender_name_elem.text.strip() if sender_name_elem is not None else "Unknown Author"

        year_elem = root.find(".//date/min/year")
        year = year_elem.text.strip() if year_elem is not None else "Unknown Year"

        # loop over the sentences and extract their text content and attributes
        # start is set equal to 1 to start the enumeration at 1
        # this because we use this for the naming of the sentences later (count letter) and for this naming convention
        # it is more suitable to start at 1
        for idx, sentence in enumerate(sentences, start = 1):
            if sentence.text is not None:
                # extract the text within <s> tags, excluding other language tags (e.g., <fl> or <de>)
                sentence_text = extract_text_within_tags(sentence, target_lang=["la"])
            else:
                continue

            # create a new element for the sentence and set its text and attributes
            new_sentence = etree.Element("sentence")
            new_sentence.text = sentence_text
            new_sentence.set("file_sent", f"{input_file[:-4]}_sent{idx}")
            new_sentence.set("author", sender_name)
            new_sentence.set("year", year)

            # Append the new sentence element to the new root
            new_root.append(new_sentence)

    # Create a new XML tree with the new root element
    new_tree = etree.ElementTree(new_root)

    # Write the new XML to the output file
    with open(output_file, "wb") as f:
        new_tree.write(f, pretty_print=True, encoding="utf-8", xml_declaration=True)

# names of the folder structure in the "bullinger_texte/data/editions/hbbw/" directory
folder_names = ["01", "01A1", "01A2", "O2", "O3", "04", "05", "06", "07", "08", "09", "10", "10A", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "20A"]
# empty list to store all the input file paths
input_files = []

for edition in folder_names:
    # construct the path to the folder containing the XML files for the current edition
    path = os.path.join("bullinger_texte/data/editions/hbbw/", edition)
    # use glob.glob() to find all files with the extension .xml within the current path
    # and append the list of file paths to input_files
    input_files += glob.glob(os.path.join(path, "*.xml"))


# create separate output files for sentences from "editions/hbbw" and "non_edited/transcribed" paths
# extract sentences from the loop above (over "editions/hbbw" path) and write to the output file
extract_and_write_sentences(input_files, "full_text_xml/all_latin_editions.xml")

path_transcribed = "bullinger_texte/data/non_edited/transcribed"
transcribed_files = glob.glob(os.path.join(path_transcribed, "*.xml"))

# Extract sentences from the second loop (over "transcribed" path) and write to the output file
extract_and_write_sentences(transcribed_files, "full_text_xml/all_latin_transcribed.xml")





