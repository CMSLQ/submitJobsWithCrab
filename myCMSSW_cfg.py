
import FWCore.ParameterSet.Config as cms

process = cms.Process("treeCreator")

process.load("FWCore.MessageService.MessageLogger_cfi")

############## IMPORTANT ########################################
# if you run over many samples ans you save the log remember to reduce
# the size of the output by prescaling the report of the event number
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.default.limit = 100
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
#################################################################

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
       #'file:/home/lockner/Data/Summer08_Bkgnd/QCD_AOD.root'     # AOD (QCD)
       #'file:/home/santanas/Data/C81A2D83-ED9A-DD11-98F1-0015C5E59E7F.root'  #FULLSIM RECO (QCD)
       #'file:/home/lockner/Data/Summer08_Bkgnd/new_TTbar_madgraph.root'  #FULLSIM RECO (TTbar)
       'file:/home/lockner/Data/Summer08_Bkgnd/Zjet_Madgraph_RECO.root'  #FULLSIM RECO (Z+jets)
    )
)

process.treeCreator = cms.EDAnalyzer('RootTupleMaker'
)

#process.treeCreator.rootfile        = cms.untracked.string("TTree_ZJet_3_jetThr10.root")
process.treeCreator.rootfile        = cms.untracked.string("THISROOTFILE")
process.treeCreator.maxgenparticles = cms.untracked.int32(35)
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

process.treeCreator.useSkim1st2ndGenLQ = cms.untracked.bool(True)
process.treeCreator.skim1st2ndGenLQpTEle  =  cms.untracked.double(20)
process.treeCreator.skim1st2ndGenLQpTMu  =  cms.untracked.double(20)
process.treeCreator.skim1st2ndGenLQpTJet  =  cms.untracked.double(10)
process.treeCreator.skim1st2ndGenLQDeltaRJetEle  =  cms.untracked.double(0.1)

######## electron isolation  ########
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")
process.load("EgammaAnalysis.EgammaIsolationProducers.egammaElectronTkIsolation_cfi")
process.load("EgammaAnalysis.EgammaIsolationProducers.egammaElectronTkNumIsolation_cfi")
process.load("EgammaAnalysis.EgammaIsolationProducers.egammaEcalRecHitIsolation_cfi") #only in RECO
process.load("EgammaAnalysis.EgammaIsolationProducers.egammaHcalIsolation_cfi") #only in RECO
process.load("EgammaAnalysis.EgammaIsolationProducers.egammaTowerIsolation_cfi") #for AOD


#process.egammaElectronTkIsolation.trackProducer = cms.InputTag("gsWithMaterialTracks")
process.egammaElectronTkIsolation.ptMin = cms.double(1.5)
process.egammaElectronTkIsolation.intRadius = cms.double(0.02)
process.egammaElectronTkIsolation.extRadius = cms.double(0.2)
process.egammaElectronTkIsolation.maxVtxDist = cms.double(0.1)

process.egammaElectronTkNumIsolation.ptMin = cms.double(1.5)
process.egammaElectronTkNumIsolation.intRadius = cms.double(0.02)
process.egammaElectronTkNumIsolation.extRadius = cms.double(0.2)
process.egammaElectronTkNumIsolation.maxVtxDist = cms.double(0.1)

process.egammaEcalRecHitIsolation.extRadius = cms.double(0.3)
process.egammaEcalRecHitIsolation.useIsolEt = cms.bool(True)
process.egammaHcalIsolation.useIsolEt = cms.bool(True)
process.egammaTowerIsolation.useIsolEt = cms.bool(True)

process.reducedEcalRecHitIsolation = cms.EDProducer("EgammaEcalRecHitIsolationProducer",
    absolut = cms.bool(True),
    ecalBarrelRecHitProducer = cms.InputTag("reducedEcalRecHitsEB"),
    ecalEndcapRecHitCollection = cms.InputTag(""),
    intRadius = cms.double(0.0),
    ecalEndcapRecHitProducer = cms.InputTag("reducedEcalRecHitsEE"),
    extRadius = cms.double(0.3),
    useIsolEt = cms.bool(True),
    ecalBarrelRecHitCollection = cms.InputTag(""),
    etMin = cms.double(0.0),
    emObjectProducer = cms.InputTag("pixelMatchGsfElectrons")
)

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
                     * process.egammaElectronTkIsolation * process.egammaElectronTkNumIsolation
                     * process.egammaEcalRecHitIsolation
                     * process.reducedEcalRecHitIsolation
                     * process.egammaHcalIsolation #for RECO
                     * process.egammaTowerIsolation #for AOD
                     * process.treeCreator)

