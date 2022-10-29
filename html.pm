#!/usr/bin/perl --

sub html_head {
    local ($title) = @_;

    print "Content-type: text/html\n\n";
    print "<html>\n <head>\n";

    print "  <title>$title</title>\n";
    print " </head>\n";
}

sub start_body {
    print "<body>\n";
}

sub end_body_html {
    print "</body></html>\n";
}


return 1;
