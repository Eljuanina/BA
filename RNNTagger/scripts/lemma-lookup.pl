#!/usr/bin/env perl

use warnings;
use strict;
#use utf8::all;
use utf8;
use open ':utf8';       # all open() use UTF-8
use open ':std';        # standard filehandles too

my $lemma_file = shift or die;
open(FILE, $lemma_file) or die "Error: unable to open \"$lemma_file\"";

my %lemma;
while (<FILE>) {
    die unless /^(.*?) ## (.*)$/;
    my $word = $1;
    my $tag = $2;
    
    $word =~ s/ //g;
    $word =~ s/<>/ /g;
    $tag =~ s/ //g;

    my $lemma = <FILE>;
    chomp($lemma);
    $lemma =~ s/ //g;
    $lemma =~ s/<>/ /g;

    if ($lemma =~ /<(unk|ood)>/) {
	if (length($word) == 1) {
	    $lemma = $word;
	}
	else {
	    $lemma = '<unknown>';
	}
    }
    
    $lemma{"$word\t$tag"} = $lemma;

    die unless <FILE> eq "\n"; # empty line must follow
}

while (<>) {
    chomp;
    if ($_ eq "") {
	print("\n");
    }
    else {
	chomp;
	print("$_\t$lemma{$_}\n");
    }
    
}
