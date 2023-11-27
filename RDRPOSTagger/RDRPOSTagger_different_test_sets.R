# Install and load required packages
# install.packages("rJava")
library(rJava)
# install.packages("RDRPOSTagger", repos = "http://www.datatailor.be/rcube", type = "source")
library(RDRPOSTagger)

# Define a function to write tagged data to text file
write_tagged_text <- function(tagged_text, output_file) {
  writeLines(tagged_text, output_file)
}

# Function to tokenize and tag text
tag_and_write <- function(input_path, output_path, tagger) {
  # Read the input text file
  txt <- readLines(input_path, warn = FALSE)
  
  # Initialize an empty vector to store tagged words
  tagged_words <- character(0)
  
  # Loop through words in txt
  for (word in txt) {
    # Attempt to tokenize and tag the word
    tagged_text <- tryCatch({
      # Tokenize and tag the word
      tagged_word <- rdr_pos(tagger, x = word)
      # Combine 'token' and 'pos' into a single string with the desired format
      formatted_word <- paste(tagged_word$token, tagged_word$pos, sep = "\t")
      formatted_word
    }, error = function(e) {
      #cat("Error occurred while processing word:", word, "\n")
      #cat("Error message:", conditionMessage(e), "\n")
      # Print the token with "PUNCT" separated by a tab if this error occurs (means, it is punctuation)
      formatted_word <- paste(word, "PUNCT", sep = "\t")
      formatted_word
    })
    
    # Append the tagged word to the vector
    tagged_words <- c(tagged_words, tagged_text)
  }
  
  # Write tagged words to the output file
  write_tagged_text(tagged_words, output_path)
  
  cat("Tagged data has been written to the output file:", output_path, "\n")
}

# Create a tagger for UniversalPOS annotation
tagger <- rdr_model(language = "Latin-ITTB", annotation = "UniversalPOS")

# Define the paths
file_path <- "~/Desktop/ba_code/random-training-data-other-taggers/test_tok_ittb.txt"
output_file <- "~/Desktop/ba_code/random-training-data-other-taggers/test_sets/rdrpostagger_ittb.txt"

# Perform tagging and writing for tokenized file
tag_and_write(file_path, output_file, tagger)

# Define the paths
file_path <- "~/Desktop/ba_code/random-training-data-other-taggers/test_tok_llct.txt"
output_file <- "~/Desktop/ba_code/random-training-data-other-taggers/test_sets/rdrpostagger_llct.txt"

# Perform tagging and writing for tokenized file
tag_and_write(file_path, output_file, tagger)

# Define the paths
file_path <- "~/Desktop/ba_code/random-training-data-other-taggers/test_tok_udante.txt"
output_file <- "~/Desktop/ba_code/random-training-data-other-taggers/test_sets/rdrpostagger_udante.txt"

# Perform tagging and writing for tokenized file
tag_and_write(file_path, output_file, tagger)

# Define the paths
file_path <- "~/Desktop/ba_code/random-training-data-other-taggers/test_tok_proiel.txt"
output_file <- "~/Desktop/ba_code/random-training-data-other-taggers/test_sets/rdrpostagger_proiel.txt"

# Perform tagging and writing for tokenized file
tag_and_write(file_path, output_file, tagger)

# Define the paths
file_path <- "~/Desktop/ba_code/random-training-data-other-taggers/test_tok_perseus.txt"
output_file <- "~/Desktop/ba_code/random-training-data-other-taggers/test_sets/rdrpostagger_perseus.txt"

# Perform tagging and writing for tokenized file
tag_and_write(file_path, output_file, tagger)