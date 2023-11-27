# Install and load udpipe package
if (!requireNamespace("udpipe", quietly = TRUE)) {
  install.packages("udpipe")
}
library(udpipe)

# Download and load the UDpipe model for Latin
dl <- udpipe_download_model(language = "latin-proiel")
udmodel_latin <- udpipe_load_model(file = "latin-proiel-ud-2.5-191206.udpipe")

# Read the input text file
file_path_ittb <- "~/Desktop/ba_code/random-training-data-other-taggers/test_tok_ittb.txt"
txt_ittb <- readLines(file_path_ittb, warn = FALSE)

# Annotate and convert the text to data frames
x <- udpipe_annotate(udmodel_latin, x = txt_ittb)
x <- as.data.frame(x)

# Define the output file paths and folder
output_folder <- "~/Desktop/ba_code/random-training-data-other-taggers/test_sets/"
output_file <- file.path(output_folder, "udpipe_ittb.txt")

# Create output folder if it doesn't exist
if (!file.exists(output_folder)) {
  dir.create(output_folder)
}

# Write token and POS tag to the output file for editions
writeLines(paste(x$token, x$upos, sep = "\t"), output_file)
cat("Tagged data for editions has been written to the output file.\n")

######## now llct ##########
# Read the input text file
file_path_llct <- "~/Desktop/ba_code/random-training-data-other-taggers/test_tok_llct.txt"
txt_llct <- readLines(file_path_llct, warn = FALSE)

# Annotate and convert the text to data frames
#x <- udpipe_annotate(udmodel_latin, x = txt,tokenizer = "vertical")
x <- udpipe_annotate(udmodel_latin, x = txt_llct)
x <- as.data.frame(x)

# Define the output file paths
output_file <- file.path(output_folder, "udpipe_llct.txt")

# Create output folder if it doesn't exist
if (!file.exists(output_folder)) {
  dir.create(output_folder)
}

# Write token and POS tag to the output file for editions
writeLines(paste(x$token, x$upos, sep = "\t"), output_file)
cat("Tagged data for editions has been written to the output file.\n")

######## now udante ##########

# Read the input text file
file_path_udante <- "~/Desktop/ba_code/random-training-data-other-taggers/test_tok_udante.txt"
txt_udante <- readLines(file_path_udante, warn = FALSE)

# Annotate and convert the text to data frames
#x <- udpipe_annotate(udmodel_latin, x = txt,tokenizer = "vertical")
x <- udpipe_annotate(udmodel_latin, x = txt_udante)
x <- as.data.frame(x)

# Define the output file paths
output_file <- file.path(output_folder, "udpipe_udante.txt")

# Create output folder if it doesn't exist
if (!file.exists(output_folder)) {
  dir.create(output_folder)
}

# Write token and POS tag to the output file for editions
writeLines(paste(x$token, x$upos, sep = "\t"), output_file)
cat("Tagged data for editions has been written to the output file.\n")


######## now proiel ##########

# Read the input text file
file_path_proiel <- "~/Desktop/ba_code/random-training-data-other-taggers/test_tok_proiel.txt"
txt_proiel <- readLines(file_path_proiel, warn = FALSE)

# Annotate and convert the text to data frames
#x <- udpipe_annotate(udmodel_latin, x = txt,tokenizer = "vertical")
x <- udpipe_annotate(udmodel_latin, x = txt_proiel)
x <- as.data.frame(x)

# Define the output file paths
output_file <- file.path(output_folder, "udpipe_proiel.txt")

# Create output folder if it doesn't exist
if (!file.exists(output_folder)) {
  dir.create(output_folder)
}

# Write token and POS tag to the output file for editions
writeLines(paste(x$token, x$upos, sep = "\t"), output_file)
cat("Tagged data for editions has been written to the output file.\n")

######## now perseus ##########

# Read the input text file
file_path_perseus <- "~/Desktop/ba_code/random-training-data-other-taggers/test_tok_perseus.txt"
txt_perseus <- readLines(file_path_perseus, warn = FALSE)

x <- udpipe_annotate(udmodel_latin, x = txt_perseus)
x <- as.data.frame(x)

# Define the output file paths
output_file <- file.path(output_folder, "udpipe_perseus.txt")

# Create output folder if it doesn't exist
if (!file.exists(output_folder)) {
  dir.create(output_folder)
}

# Write token and POS tag to the output file for editions
writeLines(paste(x$token, x$upos, sep = "\t"), output_file)
cat("Tagged data for editions has been written to the output file.\n")


