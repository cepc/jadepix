#include "JadeRecon.hh"
#include "JadePixSim.hh"
#include <string>
#include <iostream>

int main(int argc, char **argv){

    auto pSim = new JadePixSim(argc, argv);

    std::string recon_file = "JadePix.recdat";
    std::string raw_file;
    std::string::size_type pos;

    if(argc>=2){
        if(strcmp(argv[2],"-b")!=0){
            raw_file = argv[2];
        }else{
            raw_file = argv[3];
        }
    }else{
        raw_file = "JadePix.rawdat";
    }
    
    pos = raw_file.find('.');
    recon_file = raw_file.substr(0,pos) + ".recdat";

    delete pSim; 


    auto pRecon = new JadeRecon();
   
    pRecon->runRecon(raw_file,recon_file);

    delete pRecon;

    return 0;
}
