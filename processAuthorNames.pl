#!/usr/local/bin/perl
 
$element = 1;
 
open(INFILE,"$ARGV[0]")||die("Usage: process_lastnames.pl FILENAME\n");
 
open(PREFIXES,"lastname_prefixes.txt")||die("Can't open lastnames_prefixes.txt file\n");
while(<PREFIXES>) {
    $prefix=$_;
    chop($prefix);
    push(@prefixes,$prefix);
}
 
while(<INFILE>) {
    $line=$_;
    chop($line);

    @lineparts=split(/\t/,$line);
    $numparts=@lineparts;
    $author=$lineparts[$element];
    $author=~s/ [eE]sq.? ?$//; # remove Esquire for authors
    $author=~s/ and ?$//; #remove "and" at the end (split off additional authors)
    $author=~s/ \w+ by ?$//; # remove "executrix by" and the like
    $author=~s/ [^aeiouy]+ ?$//; #remove trailing non-vowel words (fix for initials like "pv" that didn't g
    $author=~s/ \+/ /g;
    @parts=split(/\s+/,$author);
    $lastpart=@parts-1;
#    print "$author\n";
#    print "$lastpart\n";
    $lastname=$parts[$lastpart];
    if (($lastpart>=2)&&($parts[$lastpart-2] eq "van")&&($parts[$lastpart-1] eq "der")) {
        $lastpart-=2;
        $lastname="$parts[$lastpart-2] $parts[$lastpart-1] $lastname";
    }
    elsif (($lastpart>=1)&&(&member($parts[$lastpart-1],@prefixes))) {
        $lastname="$parts[$lastpart-1] $lastname";
        $lastpart--;
    }
#    print "$lastpart\n";
    $firstpartofname="";
    for($i=0;$i<$lastpart;$i++) {
        $firstpartofname.="$parts[$i] ";
    }
    $firstpartofname=~s/ $//;
    $fullname="$lastname" . ", " . "$firstpartofname";
     
    $skip="";
    if ((length($lastname)<=1)||($lastname=~/\?/)||!($lastname=~/[a-zA-Z]/)||($lastname eq "office")||($lastname=~/^librar/)||($lastname eq "home")||($lastname eq "etc")) { $skip="SKIP"; }
 
    if ($firstpartofname) {
#       printf("%-35s %-35s %4s\n",$author,$fullname,$skip);
        $lineparts[$element]=$fullname;
    }
    else {
#       printf("%-35s %-35s %4s\n",$author,$lastname,$skip);
        $lineparts[$element]=$lastname;
    }
 
    $newline=join("\t",@lineparts);
    # Make certain to restore tabs at the end of the line for blank fields.
    while($numparts<9) {
        $newline.="\t";
        $numparts++;
    }
 
    if (!$skip) {
        print "$newline\n";
    }
    else {
	    #print STDERR ">>>$lastname<<< from >>>$author<<<\n";
	 }
}
 
 
#Called by the form &member($item,@list) and returns "yes" if $item is a member
#of the list @list.
sub member {
    my($search,@inlist)=@_;
    $retval="";
    foreach $item (@inlist) {
        if ("$item" eq "$search") { $retval="yes"; }
    }
 
    $retval;
}

