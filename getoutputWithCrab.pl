#!/usr/local/bin/perl

#--------------------------------------------------------------
# Francesco Santanastasio  <francesco.santanastasio@cern.ch>
#--------------------------------------------------------------

print "Starting...\n";

use Time::Local;
use Getopt::Std;


## input info

my $prodDir;
my $inputList;

getopts('h:d:i:');

if(!$opt_d) {help();}
if(!$opt_i) {help();}

if($opt_h) {help();}
if($opt_d) {$prodDir = $opt_d;}
if($opt_i) {$inputList = $opt_i;}

## create directories

my $productionDir = $prodDir;
my $workDir = $productionDir."\/"."workdir"; 

#my $outputDir = $productionDir."\/"."output"; 


## read input list

open (INPUTLIST, "<$inputList") || die ("...error opening file $inputList $!");
@inputListFile = <INPUTLIST>;
#print @inputListFile;
close(INPUTLIST);


## loop over datasets in the list

foreach $inputListLine(@inputListFile)
{
    chomp($inputListLine); 
    #print $inputListLine;

    ## split each line
    my ($dataset, $Nevents, $Njobs) = split(/\s+/, $inputListLine);
    my @datasetParts = split(/\//, $dataset);
    shift @datasetParts; #remove the first element of the list which is an empty-space

    #print "$dataset\n";
    #print "@datasetParts\n";
    #print "$datasetParts[1]\n";
    #print "$Nevents\n";
    #print "$Njobs\n";
    #print "\n";

    print "\n";
    print "processing dataset : $dataset ... \n";


    ## create datasetname

    my $datasetName="";
    my $counter=0;
    foreach $name(@datasetParts)
    {
	$counter++;
	if( $counter < scalar(@datasetParts) ) {$datasetName=$datasetName.$name."__";}
	else {$datasetName=$datasetName.$name;}
	    
    }
    $counter=0;


    ## create workdir for this dataset
    my $thisWorkDir=$workDir."/".$datasetName;


    ## check status of crab jobs for this dataset
    print "checking status of crab jobs for dataset $dataset ... \n"; 

    print "crab -status -c $thisWorkDir\n";
    system "crab -status -c $thisWorkDir";


    ## get output of crab jobs for this dataset
    print "getting output of crab jobs for dataset $dataset ... \n"; 

    print "crab -getoutput -c $thisWorkDir\n";
    system "crab -getoutput -c $thisWorkDir";

}


#---------------------------------------------------------#

sub help(){
    print "Usage: ./getoutputWithCrab.pl -d <prodDir> -i <inputList> [-h <help>] \n";
    print "Example: ./getoutputWithCrab.pl -d /home/santanas/Data/test/RootNtuples/V00-00-05_xxx_xxx -i inputList.txt \n";
    print "Options:\n";
    print "-d <prodDir>:          choose the production directory\n";
    print "-i <inputList>:        choose the input list with the datasets\n";
    print "-h <help>:             this help print-out\n";
    die "please, try again...\n";
}
