//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
// $Id$
// 
/// \file JadePixEventActionMessenger.hh
/// \brief Definition of the JadePixEventActionMessenger class

#ifndef JadePixEventAction_h
#define JadePixEventAction_h 1

#include "JadePixEventAction.hh"
#include "JadePixEventActionMessenger.hh"
#include "JadePixSD.hh"
#include "JadePixHit.hh"
#include "JadePixAnalysis.hh"
#include "JadePixDigi.hh"
#include "JadePixDigitizer.hh"
#include "JadePixWriter.hh"

#include "G4RunManager.hh"
#include "G4Event.hh"
#include "G4SDManager.hh"
#include "G4HCofThisEvent.hh"
#include "G4UnitsTable.hh"
#include "G4UserEventAction.hh"
#include "G4DigiManager.hh"
#include "G4ios.hh"

#include "Randomize.hh"
#include <iomanip>

class JadePixEventAction: public G4UserEventAction
{
    public:
        JadePixEventAction();
        ~JadePixEventAction();
        void PrintEventStatistics(G4double hitEdep, G4double truthEdep) const;
        JadePixHitsCollection *GetHitsCollection(const G4String& hcName, const G4Event* event) const;
        void BeginOfEventAction(const G4Event* event);
        void EndOfEventAction(const G4Event* event);
        void SetPrintModulo(G4int printModulo) {fPrintModulo = printModulo;};

    private:
        JadePixEventActionMessenger *fMessenger;

        G4DigiManager* fDM;
        
        G4int fPrintModulo;
       
};

#endif
