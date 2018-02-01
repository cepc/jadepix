#include "JadePixCluster.h"

JadePixCluster::~JadePixCluster(void)
{
}


void JadePixCluster::Reconstruct(){
  JadePixGeo* _JadePixGeo = JadePixGeo::GetGeo();
  int nofCol = _JadePixGeo->Layer(0).ColNo();
  int nofRow = _JadePixGeo->Layer(0).RowNo();
  double pixPitchX = _JadePixGeo->Layer(0).PitchX() *um;
  double pixPitchY = _JadePixGeo->Layer(0).PitchY() *um;
  double _tmpX=0;
  double _tmpY=0;
  vector<JadePixDigi*>::iterator m_itDigi;
  m_edep=0;
  for(m_itDigi=m_digiVec.begin();m_itDigi<m_digiVec.end();m_itDigi++){
    m_edep += (*m_itDigi)->GetADC();
    _tmpX += ((1.*(*m_itDigi)->GetColId()+0.5)*pixPitchX)*(*m_itDigi)->GetADC();
    _tmpY += ((1.*(*m_itDigi)->GetRowId()+0.5)*pixPitchY)*(*m_itDigi)->GetADC();
  }

  _tmpX /= m_edep;
  _tmpX += (-nofCol*pixPitchX/2);
  _tmpY /= m_edep;
  _tmpY += (-nofRow*pixPitchY/2);

  m_pos.set(_tmpX,_tmpY,0);
  m_time = (m_digiVec[0])->GetTDC();
  m_trackId = (m_digiVec[0])->GetTrackId();
  m_chipId = (m_digiVec[0])->GetGlobalChipId();
}
