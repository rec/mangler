#!/usr/bin/perl --

require parse_args;
require html_head;
require do_split;

%env = parse_args( "every=3&use0=1&text=i+am+a+ghost");

$text = $env{"text"};

html_head("Reversed text.");
print "<body>\n";

print join( ' ', reverse split(/\s/, $text ));

print "\n</body></html>";


