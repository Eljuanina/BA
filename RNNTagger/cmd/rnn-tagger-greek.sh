#!/bin/sh

# Set these paths appropriately

BIN=./bin
SCRIPTS=./scripts
LIB=./lib
PyRNN=./PyRNN
PyNMT=./PyNMT
TMP=/tmp/rnn-tagger$$
LANGUAGE=greek

TOKENIZER="perl ${SCRIPTS}/tokenize.pl"
ABBR_LIST=${LIB}/Tokenizer/${LANGUAGE}-abbreviations
MWL="perl ${SCRIPTS}/greek-mwls.pl"
TAGGER="python3 $PyRNN/rnn-annotate.py"
RNNPAR=${LIB}/PyRNN/${LANGUAGE}
REFORMAT="perl ${SCRIPTS}/reformat.pl"
LEMMATIZER="python3 $PyNMT/nmt-translate.py"
NMTPAR=${LIB}/PyNMT/${LANGUAGE}

$TOKENIZER -a $ABBR_LIST $1 | $MWL > $TMP.tok

$TAGGER $RNNPAR $TMP.tok > $TMP.tagged

$REFORMAT $TMP.tagged > $TMP.reformatted

$LEMMATIZER --print_source $NMTPAR $TMP.reformatted > $TMP.lemmas

$SCRIPTS/lemma-lookup.pl $TMP.lemmas $TMP.tagged 

rm $TMP.tok  $TMP.tagged  $TMP.reformatted $TMP.lemmas
