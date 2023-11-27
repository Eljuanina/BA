# this skript tags the bullinger data with the sentence approach

import openai
import time

# please replace with the actual api key
openai.api_key = "API-KEY"


# remove punctuation from file
def remove_punct(file):
    cleaned = []
    puncts = ",;.:-_!?'\"{([])}"
    with open(file) as file:
        content = file.readlines()
        # print(content)
        splitted = [el.split("|") for el in content]
        # print(splitted)
        cleaned_toks = []
        cleaned_sent = []
        for element in splitted:
            sentence = ""
            # for char in sentence
            for char in element[0]:
                if char not in puncts:
                    sentence += char
            if sentence == "":
                continue
            else:
                tokens = ""

                # to make sure that after every word is a whitespace and that it does not concatinate words later
                element[1] = element[1].replace(","," ")
                for el in element[1]:
                    # print(el)
                    if el not in puncts:
                        tokens += el
                    # print(tokens)
                    if el == " ":
                        tokens += " "
    
                tokens = tokens.split()
                # print(tokens)
                cleaned_toks.append(tokens)
                cleaned_sent.append(sentence)


    for i,e in enumerate(cleaned_sent):
        # change format
        row = e +" | "+"["
        for el in cleaned_toks[i]:
            row += el
            row += ","
        # remove last comma
        row = row[:-1]
        row += "]"
        cleaned.append(row)

    return cleaned

cleaned_list = remove_punct("../samples/total_tokenized.txt")


def perform_api_request_with_retry(sentence, tokens, model, max_retries=8):
    retry = 0
    while retry < max_retries:
        try:
            completion = openai.ChatCompletion.create(
                model = model,
                messages=[
                    {"role":"system","content": "You are a Latin linguist and part-of-speech tagging expert. You are using UPOS (universal part of speech tags). UPOS tags are ADJ,ADP,ADV,AUX,CCONJ,DET,INTJ,NOUN,NUM,PART,PRON,PROPN,PUNCT,SCONJ,SYM,VERB and X. X stands for 'other'."},
                    {"role":"user",
                    "content":f"Return the UPOS tag for the tokens of the sentence: {sentence} The sentence should be tokenized like that: {tokens}. Return the tags in the format TOKEN \t Tag. Every Token-Tag pair should be on a new line in the output file, so add a newline character after the tags. Only output the token and the tag (no explanations, no translations, no additional text)."}
                    ]
                )
            print(completion)
            return completion.choices[0].message.content
        except Exception as e:
            # print(f"Error: {e}")
            retry += 1
            # Implement exponential backoff with a sleep duration that increases with each retry
            sleep_duration = 2 ** retry
            # print(f"Retry {retry}, sleeping for {sleep_duration} seconds...")
            time.sleep(sleep_duration)
    return None  # If all retries fail


# Open your output file

# change the files to open to tag different files (I used the files for all the fine tuned models)
with open("gpt50-sent.txt", "w") as out:
    for row in cleaned_list:
        if row == "" or row == "\n" or row == " ":
            continue
        else:
            sentence, tokens = row.split("|")   
            result = perform_api_request_with_retry(sentence, tokens, model="ft:gpt-3.5-turbo-0613:cl-uzh:train-50:8GW6NJ4E") # for the name i added the model name, here 'train-50'
            if result:
                out.write(result)
                out.write("\n")






