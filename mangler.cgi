#!/usr/bin/perl --

use FindBin 1.51 qw( $RealBin );
use lib $RealBin;

require parse_args;

use CGI::Carp qw(fatalsToBrowser);

%env = parse_args( "cmd=weave&text=you+should+never+see+this+in+a+browser+really+honest+and+for+true&every=3&use0=1&filter=0&noHTML=1");

$default = "";
$isLine = $env{"splitBy"} eq "line";
$isWord = $env{"splitBy"} eq "word";
$isChar = $env{"splitBy"} eq "char";
$split  = $isLine ? "\n" : ($isChar ? "\^*" : " ");
$text   = $env{"text"};
$cmd    = $env{"cmd"} || "none";
@parts  = split( /$split/, $text );

$defaultFilter = 50;
$defaultText = "Have fun with this toy.  Just play with it.\nSet all the values, just click around.\nPlay with the filter, for some commands.\nMangle text joyously, play with it.\n\n\nThe back and forward on your browser\ncan be used to undo and redo.\nIt's up to you.";

#for (@parts) {
#    s/^\s*//g;
#    s/\s*$//g;
#}

# we create all these global variables!
#

$last   = @parts-1;
$join   = $isChar ? "" : $split;
# $join = $isLine ? "/\n" : " ";
$name   = "poetry mangler";
$submit = "mangler.cgi";
$title  = $cmd eq "none" ? "$name" : "$name: $cmd $target";
$seed   = $env{"seed"};
srand $seed if defined $seed;
$filter = $env{"filter"};
$filter = $defaultFilter unless defined $filter;

$wordSelected = $isWord ? "selected" : "";
$lineSelected = $isLine ? "selected" : "";
$charSelected = $isChar ? "selected" : "";


if (defined $text) {

    # all this work has led up to this one line... here:
    $result = join( $join, &$cmd( ) );  # $cmd can modify any variable it likes.

} else {

    # no text at all, don't bother to mangle, use default.
    $result = $defaultText;

}


# we applied the mangler, and now we report it!


$noHTML = $env{"noHTML"};

if ($noHTML) {
    print "$result\n";
    exit 0;
}
print <<EOF;
Content-type: text/html

<html>
  <head><title>$title</title></head>
  <body>
    <form name="theForm" method="POST" action="$submit">
     How should I mangle? <select name="cmd">
	<option value="none">none</option>
	<option value="random">random</option>
	<option value="reverse">reverse</option>
	<option value="sort">sort</option>
	<option value="weave">weave</option>
	<option value="interleave" selected>interleave</option>
	<option value="every">every</option>
	<option value="filter">filter</option>
	<option value="stutter">stutter</option>
	<option value="stagger">stagger</option>
      </select>
      Mangle by
      <select name="splitBy">
	<option value="word" $wordSelected>word</option>
	<option value="line" $lineSelected>line</option>
	<option value="char" $charSelected>char</option>
      </select>

    <br>
    Your text here.<br>
    <textarea rows="20" name="text" cols="132">$result</textarea> <br>

    <input color="red" type="submit" name="Mangle!" value="Mangle!">
<!--
    <input color="red" type="reset" name="Clear!" value="Clear!">
-->
    <br>
    Every (for "every" command only):
      <select name="every">
	<option>1</option>
	<option>2</option>
	<option selected>3</option>
	<option>4</option>
	<option>5</option>
	<option>6</option>
	<option>7</option>
	<option>8</option>
	<option>9</option>
	<option>10</option>
	<option>11</option>
	<option>12</option>
	<option>13</option>
	<option>14</option>
	<option>15</option>
	<option>16</option>
	<option>17</option>
	<option>18</option>
	<option>19</option>
	<option>20</option>
      </select>
    <br>

    On each (for "every" command only):
    <input type="checkbox" name="use0" CHECKED value="1">1
    <input type="checkbox" name="use1" value="1">2
    <input type="checkbox" name="use2" value="1">3
    <input type="checkbox" name="use3" value="1">4
    <input type="checkbox" name="use4" value="1">5
    <input type="checkbox" name="use5" value="1">6
    <input type="checkbox" name="use6" value="1">7
    <input type="checkbox" name="use7" value="1">8
    <input type="checkbox" name="use8" value="1">9
    <input type="checkbox" name="use9" value="1">10<br>
    -------------------------------- <input type="checkbox" name="use10" value="1">11
    <input type="checkbox" name="use11" value="1">12
    <input type="checkbox" name="use12" value="1">13
    <input type="checkbox" name="use13" value="1">14
    <input type="checkbox" name="use14" value="1">15
    <input type="checkbox" name="use15" value="1">16
    <input type="checkbox" name="use16" value="1">17
    <input type="checkbox" name="use17" value="1">18
    <input type="checkbox" name="use18" value="1">19
    <input type="checkbox" name="use19" value="1">20
    <br><p>
    Filter: <input type="text" name="filter" value="$filter"> (0-100%, for filter, stutter, stagger only)<br>
    Seed: <input type="text" name="seed" value="$seed"> (A random seed for random, filter, stutter, stagger only.)<br>
    Re-entering the same seed gets the same random numbers each time.
<p><p>Use the back and forward buttons in the browser!<br>Cut and paste!<br>Play with the filter and the manglers!
  </form>
</body></html>
EOF



sub none    { return @parts; }

sub reverse { return reverse @parts; }

sub sort { return sort @parts; }

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

sub weave {
    local @ret;

    for (0..$last) {
	local $rem = $_ % 2;
	local $div = ($_-$rem)/2;
	local $loc = ($rem == 0) ? $div : $div + int( $last/2 );
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
	$loc = $_ + int ($last-$loc) * rand;
	if ($_ != $loc) {
	    ($ret[$_], $ret[$loc]) = ($ret[$loc], $ret[$_]);
	}
    }
    return @ret;
}

sub frand() { return $filter/100 > rand; }


sub filter {
    @ret = ();
    for (@parts) {
	 push @ret, $_ if frand();
    }
    return @ret;
}

sub stutter {
    @ret = ();
    for (@parts) {
	for ($i=0; $i==0 || ($i<5 && frand()); $i++) {
	    push @ret, $_;
	}
    }
    return @ret;
}

sub stagger {
    # $title = "STAGGER!!";
    @ret = ();
    for ($i=0, $steps=0; $i<=$last && $steps <= $last*20; $steps++) {
	push @ret, $parts[$i];
	if ($i==0) { $i=1; }
	else       { $i += (((50 + $filter/2) >= rand()*100) ? 1 : -1);  }
    }
    return @ret;
}
