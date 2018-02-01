#pragma once

#ifndef JadePixCluster_H
#define JadePixCluster_H

#include <vector>

#include <iostream>
#include "CLHEP/Vector/ThreeVector.h"

#include "CLHEP/Units/PhysicalConstants.h"
#include "CLHEP/Units/SystemOfUnits.h"

#include "JadePixDigi.h"
#include "JadePixGeo.h"
typedef CLHEP::Hep3Vector Hep3Vector;

using namespace std;
using namespace CLHEP;

class JadePixCluster;
class JadePixDigi;

class JadePixCluster{
    public:
        JadePixCluster(int trackId,int chipId, double edep, double time, double posX, double posY, double posZ, double angle):m_trackId(trackId),m_chipId(chipId),m_edep(edep),m_time(time),m_pos(Hep3Vector(posX,posY,posZ)),m_enterAngle(angle){};
        JadePixCluster(){};
        ~JadePixCluster(void);

        void AddDigi(JadePixDigi *digi){m_digiVec.push_back(digi);};
        int GetNofDigi() const {return m_digiVec.size();};
        void Reconstruct();
        Hep3Vector GetPos() const {return m_pos;};
        int GetId() const {return m_id;};
        void SetId(int id) {m_id=id;};
        void Print();

        double GetADC() const {return m_edep;};
        double GetTDC() const {return m_time;};


        void AddTruth(JadePixCluster* tr) {m_trHitVec.push_back(tr);};
        int NofTrHit() const {return m_trHitVec.size();};
        JadePixCluster* GetTruth(int i) const {return m_trHitVec[i];};


        void SetChipId(int chip){m_chipId=chip;};
        int GetChipId() const {return m_chipId;};

        void SetTrackId(int track){m_trackId=track;};
        int GetTrackId() const {return m_trackId;};

        double GetEnterAngle() const{return m_enterAngle;};
    private:
        int m_trackId;
        int m_chipId;
        double m_edep;
        double m_time;
        Hep3Vector m_pos;
        int m_id;
        vector<JadePixDigi*> m_digiVec;
        vector<JadePixCluster*> m_trHitVec;
        double m_enterAngle;
};

#endif
