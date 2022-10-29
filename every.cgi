#!/usr/bin/perl --

#

require parse_args;
require html_head;
require do_split;

# %env = parse_args();
%env = parse_args( "every=3&use0=1&text=i+am+a+ghost");

$every = $env{"every"};
$text = $env{"text"};
@words = split(/\s/, $text );
$len = @words-1;

html_head("Every $every words (out of $len)...");
print "<body>\n";

for $word (0..$len) {
     # local ($word) = ($_);
     local ($rem) = ($word % $every);
     local ($name) = ("use$rem");
     # print "$word $rem $name $words[$word]\n"; 
     print "$words[$word] " if ($env{$name});
}

print "<p>\n</body></html>";


