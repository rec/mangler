#!/usr/bin/perl --

require parse_args;

%env = parse_args( "cmd=filter&every=3&use0=1&seed=5&filter=0.4");

$default = "you+should+never+see+this+in+a+browser+really+honest+and+for+true";

$text   = $env{"text"} || $default;
$cmd    = $env{"cmd"}  || "none";
$split  = $env{"split"} || ' ';
@parts  = split( /$split/, $text );
$last   = @parts-1;
$isLine = $split eq '/';
# $join   = $isLine ? "/<br>/n" : " ";
$target = $isLine ? "lines"  : "words";
$name   = "poetry mangler";
$title  = $cmd eq "none" ? "$name" : "$name: $cmd $target";
$seed   = $env{"seed"};
srand $seed if defined $seed;

$result = join( $split, &$cmd( ) );  # $cmd can modify any variable it likes.

print "Content-type: text/html\n\n";
print "<html><head><title>$title</title></head>\n";
print "<body>\n";
print "$result\n</body></html>";

sub none    { return @parts; }

sub reverse { return reverse @parts; }

sub interleave {
    local @ret;
    
    for (0..$last) {
	local $rem = $_ % 2;
	local $div = ($_-$rem)/2;
	local $loc = ($rem == 0) ? $div : $last-$div;
	$ret[$_] = $parts[ $loc ];
    }
    return @ret;
}

sub every {
    $every = $env{"every"};
    $title = "$name: every $every $target";
    @ret = ();
    for (0..$last) {
	 $rem = $_ % $every;
	 push @ret, $parts[$_] if $env{"use$rem"};
    }
    return @ret;
}

sub random {
    @ret = @parts;
    for (0..$last-1) {
	$loc = $_ + int ($last-$loc+1) * rand;
	if ($_ != $loc) {
	    ($ret[$_], $ret[$loc]) = ($ret[$loc], $ret[$_]);
	}
    }
    return @ret;
}

sub filter {
    @ret = ();
    $filter = $env{"filter"};
    for (@parts) {
	 push @ret, $_ if ($filter > rand);
    }
    return @ret;
}
