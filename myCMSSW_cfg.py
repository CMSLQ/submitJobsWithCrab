import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")

# initialize MessageLogger and output report
############## IMPORTANT ########################################
# if you run over many samples and you save the log, remember to reduce
# the size of the output by prescaling the report of the event number
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.cerr.default.limit = 100
#################################################################
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# source
process.source = cms.Source("PoolSource", 
     fileNames = cms.untracked.vstring('file:input_file.root')
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('THISROOTFILE')
)

# load the standard PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")

## Load additional RECO config
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'MC_31X_V3::All'
process.load("Configuration.StandardSequences.MagneticField_cff")

# add tcMET and pfMET
from PhysicsTools.PatAlgos.tools.metTools import *
addTcMET(process, 'TC')
addPfMET(process, 'PF')

# b-tag discriminators to be added to the PAT jets
process.allLayer1Jets.discriminatorSources = cms.VInputTag(
    cms.InputTag("jetBProbabilityBJetTags"),
    cms.InputTag("simpleSecondaryVertexBJetTags"),
    cms.InputTag("softMuonByPtBJetTags"),
    cms.InputTag("trackCountingHighEffBJetTags"),
)

# fix InputTags for ECAL IsoDeposits (to work with FastSim samples)
process.eleIsoDepositEcalFromHits.ExtractorPSet.barrelEcalHits = cms.InputTag("reducedEcalRecHitsEB")
process.eleIsoDepositEcalFromHits.ExtractorPSet.endcapEcalHits = cms.InputTag("reducedEcalRecHitsEE")
process.gamIsoDepositEcalFromHits.ExtractorPSet.barrelEcalHits = cms.InputTag("reducedEcalRecHitsEB")
process.gamIsoDepositEcalFromHits.ExtractorPSet.endcapEcalHits = cms.InputTag("reducedEcalRecHitsEE")

# load the coreTools of PAT
from PhysicsTools.PatAlgos.tools.coreTools import *
restrictInputToAOD(process, ['All'])

# Skim definition
process.load("Leptoquarks.LeptonJetFilter.leptonjetfilter_cfi")
process.LJFilterPAT = process.LJFilter.clone()
# Primary skim 
process.LJFilter.muLabel = 'muons'
process.LJFilter.elecLabel = 'gsfElectrons'
process.LJFilter.jetLabel = 'iterativeCone5CaloJets'
process.LJFilter.counteitherleptontype = False
process.LJFilter.muonsMin = -1
process.LJFilter.elecPT = 30.
# Secondary skim
process.LJFilterPAT.counteitherleptontype = False
process.LJFilterPAT.muonsMin = -1
process.LJFilterPAT.useElecID = True
process.LJFilterPAT.elecPT = 30.

# RootTupleMaker
process.treeCreator = cms.EDAnalyzer('RootTupleMakerPAT')
process.treeCreator.maxgenparticles = cms.untracked.int32(25)
process.treeCreator.maxgenjets      = cms.untracked.int32(10)
process.treeCreator.maxelectrons    = cms.untracked.int32(10)
process.treeCreator.maxcalojets     = cms.untracked.int32(10)
process.treeCreator.maxmuons        = cms.untracked.int32(10)
process.treeCreator.debug           = cms.untracked.bool(False)
# overall luminosity normalization  (in pb-1)   
process.treeCreator.luminosity      = cms.untracked.double(100)
process.treeCreator.numEvents       = cms.untracked.int32(10)
process.treeCreator.saveTrigger     = cms.untracked.bool(True)
process.treeCreator.usePDFweight    = cms.untracked.bool(False)
process.treeCreator.PDFSet          = cms.untracked.string("/cteq61.LHgrid")
process.treeCreator.doBeamSpotCorr  = cms.untracked.bool(False)
process.treeCreator.muonLabel       = cms.untracked.InputTag("cleanLayer1Muons");
process.treeCreator.electronLabel   = cms.untracked.InputTag("cleanLayer1Electrons");
process.treeCreator.caloJetLabel    = cms.untracked.InputTag("cleanLayer1Jets");
process.treeCreator.genJetLabel     = cms.untracked.InputTag("iterativeCone5GenJets");
process.treeCreator.electronPt      = cms.untracked.double(30.);
process.treeCreator.electronIso     = cms.untracked.double(0.1);
process.treeCreator.muonPt          = cms.untracked.double(20.);
process.treeCreator.muonIso         = cms.untracked.double(0.05);

# PAT sequence modification
process.patDefaultSequence.remove( process.countLayer1Objects )

# Path definition
process.p = cms.Path( process.LJFilter*process.patDefaultSequence*process.LJFilterPAT*process.treeCreator )
