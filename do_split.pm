#!/usr/bin/perl --

sub do_split {
    local ($text) = @_;
    $text =~ s/'/_/g;
    local (@words);
    local ($i);
    @words = split( /\W/, $text );
    local ($length) = (@words);
    for $i (0..$length-1) {
      $words[$i] =~ s/_/'/g;
    }
    return @words;
}

return 1;
