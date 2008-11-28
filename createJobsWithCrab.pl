#!/usr/local/bin/perl

#--------------------------------------------------------------
# Francesco Santanastasio  <francesco.santanastasio@cern.ch>
#--------------------------------------------------------------

print "Starting...\n";

use Time::Local;
use Getopt::Std;


## input info

my $storageDir;
my $tagname;
my $inputList;
my $templateCrab;
my $myCMSSWconfig;

getopts('h:d:v:i:t:c:');

if(!$opt_d) {help();}
if(!$opt_v) {help();}
if(!$opt_i) {help();}
if(!$opt_t) {help();}
if(!$opt_c) {help();}

if($opt_h) {help();}
if($opt_d) {$storageDir = $opt_d;}
if($opt_v) {$tagname = $opt_v;}
if($opt_i) {$inputList = $opt_i;}
if($opt_t) {$templateCrab = $opt_t;}
if($opt_c) {$myCMSSWconfig = $opt_c;}


#my $storageDir = "/home/santanas/Data/test/RootNtuples";
#my $tagname = "V00-00-05";

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime(time);
$year = $year + 1900;
$mon = $mon + 1;

my $date = "$year$mon$mday\_$hour$min$sec"; 
#my $date = "currentdate";

## create directories

my $productionDir = $storageDir."\/".$tagname."\_".$date;
my $cfgfilesDir = $productionDir."\/"."cfgfiles"; 
my $outputDir = $productionDir."\/"."output"; 
my $workDir = $productionDir."\/"."workdir"; 

print("mkdir -p $productionDir \n");
print("mkdir -p $cfgfilesDir \n");
print("mkdir -p $outputDir \n");
print("mkdir -p $workDir \n");

system("mkdir -p $productionDir");
system("mkdir -p $cfgfilesDir");
system("mkdir -p $outputDir");
system("mkdir -p $workDir");

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
    print "mkdir -p $thisWorkDir\n";
    system "mkdir -p $thisWorkDir";


    ## outputfile .root
    my $outputfile = $datasetName.""."\.root"; 
    #print "outputfilename : $outputfile ... \n";


    ## read template CMSSW config file
    open (TEMPLATECMSSW, "<$myCMSSWconfig") || die ("...error opening file $myCMSSWconfig $!");
    @templateCMSSWFile = <TEMPLATECMSSW>;
    #print @templateCMSSWFile;
    close(TEMPLATECMSSW);


    ## create new CMSSW config file
    my $newCMSSWconfig = $cfgfilesDir."/".$datasetName."\_"."cmssw"."\_cfg"."\.py";
    print "creating $newCMSSWconfig ... \n";

    open(NEWCMSSWCONFIG,">$newCMSSWconfig");
    
    foreach $templateCMSSWFileLine(@templateCMSSWFile)
    {

	chomp ($templateCMSSWFileLine);
	#print("$templateCMSSWFileLine\n");

        #%%%%%%%%%%%%% IMPORTANT %%%%%%%%%%%%% 

        ## THIS PART SHOULD CHANGE ACCORDINGLY WITH THE CMSSW CONFIG FILE ##
	
	if($templateCMSSWFileLine=~/THISROOTFILE/)
	{
	    $templateCMSSWFileLine = "process.treeCreator.rootfile = cms.untracked.string\(\"$outputfile\"\)";
	    #print("$templateCMSSWFileLine\n");
	}

        ####################################################################

	print NEWCMSSWCONFIG "$templateCMSSWFileLine\n";

    }

    close(NEWCMSSWCONFIG);


    ## read template crab config file
    open (TEMPLATECRAB, "<$templateCrab") || die ("...error opening file $templateCrab $!");
    @templateCrabFile = <TEMPLATECRAB>;
    #print @templateCrabFile;
    close(TEMPLATECRAB);


    ## create new crab config file
    my $newcrabconfig = $cfgfilesDir."/".$datasetName."\_"."crab"."\.cfg";
    print "creating $newcrabconfig ... \n";

    open(NEWCRABCONFIG,">$newcrabconfig");
    
    foreach $templateCrabFileLine(@templateCrabFile)
    {

	chomp ($templateCrabFileLine);
	#print("$templateCrabFileLine\n");
	
	if($templateCrabFileLine=~/THISDATASET/)
	{
	    $templateCrabFileLine = "datasetpath = $dataset";
	    #print("$templateCrabFileLine\n");
	}

	if($templateCrabFileLine=~/THISCMSSWCONFIGFILE/)
	{
	    $templateCrabFileLine = "pset = $newCMSSWconfig";
	    #print("$templateCrabFileLine\n");
	}

	if($templateCrabFileLine=~/THISNEVENTS/)
	{
	    $templateCrabFileLine = "total_number_of_events = $Nevents";
	    #print("$templateCrabFileLine\n");
	}

	if($templateCrabFileLine=~/THISNJOBS/)
	{
	    $templateCrabFileLine = "number_of_jobs = $Njobs";
	    #print("$templateCrabFileLine\n");
	}

	if($templateCrabFileLine=~/THISOUTPUTFILE/)
	{
	    $templateCrabFileLine = "output_file = $outputfile";
	    #print("$templateCrabFileLine\n");
	}

	if($templateCrabFileLine=~/THISUIWORKINGDIR/)
	{
	    $templateCrabFileLine = "ui_working_dir = $thisWorkDir";
	    #print("$templateCrabFileLine\n");
	}

	if($templateCrabFileLine=~/THISOUTPUTDIR/)
	{
	    $templateCrabFileLine = "outputdir = $outputDir";
	    #print("$templateCrabFileLine\n");
	}

	print NEWCRABCONFIG "$templateCrabFileLine\n";

    }


    close(NEWCRABCONFIG);


    ## create crab jobs for this dataset
    print "creating jobs for dataset $dataset ... \n"; 

    print "crab -create -cfg $newcrabconfig\n";
    system "crab -create -cfg $newcrabconfig";

    ## submit crab jobs for this dataset
    #print "submitting jobs for dataset $dataset ... \n"; 
    #print "crab -submit -c $thisWorkDir\n";
    #system "crab -submit -c $thisWorkDir";

}


#---------------------------------------------------------#

sub help(){
    print "Usage: ./createJobsWithCrab.pl -d <storageDir> -v <tagname> -i <inputList> -t <templateCrab> -c <myCMSSWconfig> [-h <help?>] \n";
    print "Example: ./createJobsWithCrab.pl -d /home/santanas/Data/test/RootNtuples -v V00-00-05 -i inputList.txt -t template_crab.cfg -c myCMSSW_cfg.py \n";
    print "Options:\n";
    print "-d <storageDir>:       choose the storage directory\n";
    print "-v <tagname>:          choose the tagname of RootNtupleMaker\n";
    print "-i <inputList>:        choose the input list with the datasets\n";
    print "-t <templateCrab>:     choose the crab template\n";
    print "-c <myCMSSWconfig>:    choose the CMSSW config file\n";
    print "-h <yes> :             to print the help \n";
    die "please, try again...\n";
}
