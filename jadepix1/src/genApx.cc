#include <Math/DisplacementVector2D.h>
#include <Math/Vector2D.h>
#include <Math/Vector3D.h>
#include <TFile.h>
#include <TTree.h>

#include <memory>

// FIXME: these includes should be absolute and provided with installation?

#include "/opt/allpix/v1.1.0/src/objects/MCParticle.hpp"
#include "/opt/allpix/v1.1.0/src/objects/PixelCharge.hpp"
#include "/opt/allpix/v1.1.0/src/objects/PixelHit.hpp"
#include "/opt/allpix/v1.1.0/src/objects/PropagatedCharge.hpp" 

/**
 * Construct a ROOT TTree from the data objects that can be used for comparison
 */
std::shared_ptr<TTree> constructComparisonTree(TFile* file, std::string dut) {
    // Read pixel hit output
    TTree* pixel_hit_tree = static_cast<TTree*>(file->Get("PixelHit"));
    if(!pixel_hit_tree) {
        std::cout << "Could not read tree PixelHit, cannot continue." << std::endl;
        return std::make_shared<TTree>();
    }

    TBranch* pixel_hit_branch = pixel_hit_tree->FindBranch(dut.c_str());
    if(!pixel_hit_branch) {
        std::cout << "Could not find the DUT branch on tree PixelHit, cannot continue." << std::endl;
        return std::make_shared<TTree>();
    }

    std::vector<allpix::PixelHit*> input_hits;
    pixel_hit_branch->SetObject(&input_hits);

    // Read deposited and propagated charges for history
    TTree* deposited_charge_tree = static_cast<TTree*>(file->Get("DepositedCharge"));
    if(!deposited_charge_tree) {
        std::cout << "Could not read tree DepositedCharge" << std::endl;
    }
    TTree* propagated_charge_tree = static_cast<TTree*>(file->Get("PropagatedCharge"));
    if(!propagated_charge_tree) {
        std::cout << "Could not read tree PropagatedCharge" << std::endl;
    }

    // Read pixel charge output
    TTree* pixel_charge_tree = static_cast<TTree*>(file->Get("PixelCharge"));
    if(!pixel_charge_tree) {
        std::cout << "Could not read tree PixelCharge" << std::endl;
    }

    TBranch* pixel_charge_branch = pixel_charge_tree->FindBranch(dut.c_str());
    std::vector<allpix::PixelCharge*> input_charges;
    pixel_charge_branch->SetObject(&input_charges);

    // Read MC truth
    TTree* mc_particle_tree = static_cast<TTree*>(file->Get("MCParticle"));
    if(!mc_particle_tree) {
        std::cout << "Could not read tree MCParticle" << std::endl;
    }
    TBranch* mc_particle_branch = mc_particle_tree->FindBranch(dut.c_str());
    if(!mc_particle_branch) {
        std::cout << "Could not find the DUT branch on tree MCParticle" << std::endl;
    }

    std::vector<allpix::MCParticle*> input_particles;
    mc_particle_branch->SetObject(&input_particles);

    // Initialize output tree and branches
    auto output_tree = std::make_shared<TTree>("clusters", ("Cluster information for " + dut).c_str());
    int event_num;
    // Event number
    output_tree->Branch("eventNr", &event_num);
    // Cluster size
    int output_cluster, output_cluster_x, output_cluster_y;
    double aspect_ratio;
    output_tree->Branch("size", &output_cluster);
    output_tree->Branch("sizeX", &output_cluster_x);
    output_tree->Branch("sizeY", &output_cluster_y);
    output_tree->Branch("aspectRatio", &aspect_ratio);
    // Charge info
    int output_total_charge;
    std::vector<int> output_charge;
    output_tree->Branch("totalCharge", &output_total_charge);
    output_tree->Branch("charge", &output_charge);
    // Signal info
    int output_total_signal;
    std::vector<int> output_signal;
    std::vector<int> output_seed_signal;
    std::vector<int> output_clus_signal;
    output_tree->Branch("totalSignal", &output_total_signal);
    output_tree->Branch("signal", &output_signal);
    output_tree->Branch("seed_signal", &output_seed_signal);
    output_tree->Branch("cluster_signal", &output_clus_signal);
    // Single pixel row / col
    std::vector<int> output_rows;
    std::vector<int> output_cols;
    output_tree->Branch("row", &output_rows);
    output_tree->Branch("col", &output_cols);
    // Real track information
    int output_track_count;
    double output_track_x, output_track_y;
    output_tree->Branch("trackCount", &output_track_count); // FIXME: problems arise if not one
    output_tree->Branch("trackLocalX", &output_track_x);
    output_tree->Branch("trackLocalY", &output_track_y);
    // Calculated track information and residuals
    double output_x, output_y, output_res_x, output_res_y;
    output_tree->Branch("localX", &output_x);
    output_tree->Branch("localY", &output_y);
    output_tree->Branch("resX", &output_res_x);
    output_tree->Branch("resY", &output_res_y);

    // Convert tree for every event
    for(int i = 0; i < pixel_hit_tree->GetEntries(); ++i) {
        pixel_hit_tree->GetEntry(i);
        if(pixel_charge_tree)
            pixel_charge_tree->GetEntry(i);
        if(mc_particle_tree)
            mc_particle_tree->GetEntry(i);
        if(deposited_charge_tree)
            deposited_charge_tree->GetEntry(i);
        if(propagated_charge_tree)
            propagated_charge_tree->GetEntry(i);

        // Set event number
        event_num = i + 1;

        // Set cluster sizes
        output_cluster = input_hits.size();
        std::set<int> unique_x;
        std::set<int> unique_y;
        for(auto& hit : input_hits) {
            unique_x.insert(hit->getPixel().getIndex().x());
            unique_y.insert(hit->getPixel().getIndex().y());
        }
        output_cluster_x = unique_x.size();
        output_cluster_y = unique_y.size();
        aspect_ratio = static_cast<double>(output_cluster_y) / output_cluster_x;

        // Set charge information
        output_charge.clear();
        output_total_charge = 0;
        for(auto& pixel_charge : input_charges) {
            output_charge.push_back(pixel_charge->getCharge());
            output_total_charge += pixel_charge->getCharge();
        }

        // Set signal information
        output_signal.clear();
        output_total_signal = 0;
        for(auto& hit : input_hits) {
            output_signal.push_back(hit->getSignal());
            output_total_signal += hit->getSignal();
        }

        // Set pixel position information
        output_rows.clear();
        output_cols.clear();
        for(auto& hit : input_hits) {
            // FIXME defined order
            output_rows.push_back(hit->getPixel().getIndex().y());
            output_cols.push_back(hit->getPixel().getIndex().x());
        }

	//temp
	const int NCOLS = 48;
	const int NROWS = 16;
	int PIX_SEED_THR = 500; // ADC
	int PIX_CLU_THR = 500; // ADC

	int pix_map_sig[NCOLS][NROWS]={0};

	for(auto& hit : input_hits) {
	   auto _row = hit->getPixel().getIndex().y();
	   auto _col = hit->getPixel().getIndex().x();
	   pix_map_sig[_col][_row] += hit->getSignal();
	}

	int tmp_seed_signal=0;
	int x_seed = 0;
	int y_seed = 0;
	int tmp_clu_sig =0;
	const size_t clustersize = static_cast<size_t>(std::round(3/2));

	for(int i=0; i<NCOLS; i++)
		for(int j=0; j<NCOLS; j++) {
			if(tmp_seed_signal < pix_map_sig[i][j]){
			       	tmp_seed_signal = pix_map_sig[i][j];
				x_seed = i;
				y_seed = j;
			}
		}

        if(tmp_seed_signal > PIX_SEED_THR)
		output_seed_signal.push_back(tmp_seed_signal);

	for(int i= x_seed - clustersize; i< x_seed + clustersize; i++)
		for(int j= y_seed - clustersize; j< y_seed + clustersize; j++)
		{
			if( (i>0) && (i<NCOLS) && (j>0) && (j<NROWS)){
			if(pix_map_sig[i][j] > PIX_CLU_THR)
				tmp_clu_sig += pix_map_sig[i][j];
			}

		}

	output_clus_signal.push_back(tmp_clu_sig);

        // Get information about the actual track
        output_track_count = 1 + input_particles.size();
        output_track_x = 0;
        output_track_y = 0;

        // FIXME: guess the truth position from the average of start and end points
        for(auto& particle : input_particles) {
            output_track_x += (particle->getLocalStartPoint().x() + particle->getLocalEndPoint().x()) / 2.0;
            output_track_y += (particle->getLocalStartPoint().y() + particle->getLocalEndPoint().y()) / 2.0;
        }
        if(!input_particles.empty()) {
            output_track_x /= input_particles.size();
            output_track_y /= input_particles.size();
        }

        // Calculate local x using a simple center of gravity fit
        // FIXME no corrections are applied
        ROOT::Math::XYZVector totalPixel;
        double totalSignal = 0;
        for(auto& hit : input_hits) {
            totalPixel += static_cast<ROOT::Math::XYZVector>(hit->getPixel().getLocalCenter()) * hit->getSignal();
            totalSignal += hit->getSignal();
        }
        totalPixel /= totalSignal;
        output_x = totalPixel.x();
        output_y = totalPixel.y();
        output_res_x = output_track_x - output_x;
        output_res_y = output_track_y - output_y;

        output_tree->Fill();
    }

    return output_tree;
}


void print_usage(){
  printf("NAME\n\tgenApx - Gen Allpix root files\n");
  printf("\nSYNOPSIS\n\tgenApx input output\n "); 

}

int main(int argc, char** argv) {
  if (argc < 2) {
    print_usage() ;  
    return -1; 
  }


TString inputFile = std::string(argv[1]);
TString outputFile = std::string(argv[2]);


printf("Input: %s\n", inputFile.Data()); 


auto fin = new TFile(inputFile);

auto fout = new TFile(outputFile, "RECREATE");

auto tree = constructComparisonTree(fin, "mydetector");
tree->Write();
fout->Close(); 

printf("File saved as: %s\n", outputFile.Data());

}

