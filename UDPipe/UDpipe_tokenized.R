# Install and load udpipe package
if (!requireNamespace("udpipe", quietly = TRUE)) {
  install.packages("udpipe")
}
library(udpipe)

# Download and load the UDpipe model for Latin
dl <- udpipe_download_model(language = "latin-proiel")
udmodel_latin <- udpipe_load_model(file = "latin-proiel-ud-2.5-191206.udpipe")

# Read the input text files
file_path <- "~/Desktop/BA_code/samples/tokenized.txt"
txt <- readLines(file_path, warn = FALSE)
# print(typeof(txt))
# --> make this a list and then to use tokenozer-vertical again


# Annotate and convert the text to data frames
#x <- udpipe_annotate(udmodel_latin, x = txt,tokenizer = "vertical")
x <- udpipe_annotate(udmodel_latin, x = txt)
x <- as.data.frame(x)


# Define the output file paths and folder
output_folder <- "~/Desktop/BA_code/UDPipe"
output_file <- file.path(output_folder, "udpipe_tokenized.txt")

# Create output folder if it doesn't exist
if (!file.exists(output_folder)) {
  dir.create(output_folder)
}

# Write token and POS tag to the output file for editions
writeLines(paste(x$token, x$upos, sep = "\t"), output_file)
cat("Tagged data for editions has been written to the output file.\n")

