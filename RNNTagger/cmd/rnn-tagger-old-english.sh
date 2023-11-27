#!/bin/sh

# Set these paths appropriately

BIN=./bin
SCRIPTS=./scripts
LIB=./lib
PyRNN=./PyRNN
PyNMT=./PyNMT
TMP=/tmp/rnn-tagger$$
LANGUAGE=old-english

TOKENIZER="perl ${SCRIPTS}/tokenize.pl"
ABBR_LIST=${LIB}/Tokenizer/${LANGUAGE}-abbreviations
TAGGER="python3 $PyRNN/rnn-annotate.py"
RNNPAR=${LIB}/PyRNN/${LANGUAGE}

$TOKENIZER -a $ABBR_LIST $1 > $TMP.tok

$TAGGER $RNNPAR $TMP.tok

rm $TMP.tok
