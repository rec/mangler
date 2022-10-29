#!/usr/bin/perl --

#

require parse_args;
require html_head;

%env = parse_args( "every=3&use0=1&text=i+am+a+ghost");

$text = $env{"text"};

html_head("Interleaved text.");
print "<body>\n";

@lines = split( /\//, $text);
$len = @lines-1;
for (0..$len) {
    local $rem = $_ % 2;
    local $div = ($_-$rem)/2;
    if ($rem == 0) {
	print $lines[ $div ];
    } else {
	print $lines[ $len-$div ];
    }
    print "<br>\n";
}

print "\n</body></html>";


