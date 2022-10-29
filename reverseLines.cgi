#!/usr/bin/perl --

#

require parse_args;
require html_head;
require do_split;

%env = parse_args( "every=3&use0=1&text=i+am+a+ghost");

$text = $env{"text"};

html_head("Reversed text (by lines).");
print "<body>\n";

print join( '<br>', reverse split(/\//, $text ));

print "\n</body></html>";


