
import FWCore.ParameterSet.Config as cms

process = cms.Process("treeCreator")

process.load("FWCore.MessageService.MessageLogger_cfi")

############## IMPORTANT ########################################
# if you run over many samples ans you save the log remember to reduce
# the size of the output by prescaling the report of the event number
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.default.limit = 1
#process.MessageLogger.cerr.FwkReport.reportEvery = 100
#################################################################

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
       #'file:/home/santanas/Data/Leptoquarks/LQ_300_HLT_080916_59_1.root'     #FASTSIM AOD (LQ)
       'file:/home/santanas/Data/C81A2D83-ED9A-DD11-98F1-0015C5E59E7F.root'  #FULLSIM RECO (QCD)
       #'file:/afs/cern.ch/user/l/lockner/scratch0/CMSSW_2_1_8/src/data/LQ300_HLT.root'

    )
)

process.treeCreator = cms.EDAnalyzer('RootTupleMaker'
)

################################################
process.treeCreator.rootfile        = cms.untracked.string("THISROOTFILE")
################################################

#process.treeCreator.rootfile        = cms.untracked.string("QCDDiJetPt120to170__Summer08_IDEAL_V9_v1__GEN-SIM-RECO.root")
process.treeCreator.maxgenparticles = cms.untracked.int32(50)
process.treeCreator.maxgenjets      = cms.untracked.int32(10)
process.treeCreator.maxelectrons    = cms.untracked.int32(10)
process.treeCreator.maxcalojets     = cms.untracked.int32(10)
process.treeCreator.maxmuons        = cms.untracked.int32(10)
process.treeCreator.aodsim          = cms.untracked.bool(True)
process.treeCreator.fastSim         = cms.untracked.bool(True)
process.treeCreator.PAT             = cms.untracked.bool(False)
process.treeCreator.debug           = cms.untracked.bool(False)
# overall luminosity normalization  (in pb-1) 	
process.treeCreator.luminosity      =  cms.untracked.double(100)
process.treeCreator.numEvents       = cms.untracked.int32(10)
process.treeCreator.saveTrigger     = cms.untracked.bool(True)

######## electron isolation  ########
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")
process.load("EgammaAnalysis.EgammaIsolationProducers.egammaElectronTkRelIsolation_cfi")
process.load("EgammaAnalysis.EgammaIsolationProducers.egammaElectronTkNumIsolation_cfi")
process.load("EgammaAnalysis.EgammaIsolationProducers.egammaEcalRecHitIsolation_cfi")
process.load("EgammaAnalysis.EgammaIsolationProducers.egammaHcalIsolation_cfi")

process.egammaEcalRecHitIsolation.extRadius = cms.double(0.3)
process.egammaEcalRecHitIsolation.etMin = cms.double(0.)

#process.egammaElectronTkRelIsolation.trackProducer = cms.InputTag("gsWithMaterialTracks")
process.egammaElectronTkRelIsolation.ptMin = cms.double(1.5)
process.egammaElectronTkRelIsolation.intRadius = cms.double(0.02)
process.egammaElectronTkRelIsolation.extRadius = cms.double(0.2)
process.egammaElectronTkRelIsolation.maxVtxDist = cms.double(0.1)


#############   Define the L2 correction service #####
process.L2RelativeJetCorrector = cms.ESSource("L2RelativeCorrectionService", 
    tagName = cms.string('Summer08_L2Relative_IC5Calo'),
    label = cms.string('L2RelativeJetCorrector')
)
#############   Define the L3 correction service #####
process.L3AbsoluteJetCorrector = cms.ESSource("L3AbsoluteCorrectionService", 
    tagName = cms.string('Summer08_L3Absolute_IC5Calo'),
    label = cms.string('L3AbsoluteJetCorrector')
)
#############   Define the L5 correction service #####
process.L5JetCorrector = cms.ESSource("L5FlavorCorrectionService",
    section = cms.string('b'), 
    tagName = cms.string('L5Flavor_fromTTbar_iterativeCone5'),
    label = cms.string('L5FlavorJetCorrector')
)
#############   Define the chain corrector service ###
process.L2L3JetCorrector = cms.ESSource("JetCorrectionServiceChain",  
    correctors = cms.vstring('L2RelativeJetCorrector','L3AbsoluteJetCorrector'),
    label = cms.string('L2L3JetCorrector')
)
#############   Define the chain corrector module ####
process.L2L3CorJet = cms.EDProducer("CaloJetCorrectionProducer",
    src = cms.InputTag("iterativeCone5CaloJets"),
    correctors = cms.vstring('L2L3JetCorrector')
)
## #############   Define the chain corrector service ###
process.L2L3L5JetCorrector = cms.ESSource("JetCorrectionServiceChain",  
    correctors = cms.vstring('L2RelativeJetCorrector','L3AbsoluteJetCorrector','L5FlavorJetCorrector'),
    label = cms.string('L2L3L5JetCorrector')
)
#############   Define the chain corrector module ####
process.L2L3L5CorJet = cms.EDProducer("CaloJetCorrectionProducer",
    src = cms.InputTag("iterativeCone5CaloJets"),
    correctors = cms.vstring('L2L3L5JetCorrector')
)
# set the record's IOV. Must be defined once. Choose ANY correction service. #
##process.prefer("L2L3JetCorrector") 
##process.prefer("L2L3L5JetCorrector") 

##process.p = cms.Path(process.L2L3CorJet * process.treeCreator)
#process.p = cms.Path(process.L2L3L5CorJet * process.L2L3CorJet * process.egammaIsolationSequence * process.treeCreator)
process.p = cms.Path(process.L2L3L5CorJet * process.L2L3CorJet
                     * process.egammaElectronTkRelIsolation * process.egammaElectronTkNumIsolation
                     * process.egammaEcalRecHitIsolation
                     * process.egammaHcalIsolation
                     * process.treeCreator)

