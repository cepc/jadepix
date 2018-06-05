#!/usr/bin/env bash

# Main driver to submit 
# Author: 
#      Maoqiang Jing <jingmq@ihep.ac.cn> 
#      Tao Yang <yangtao@ihep.ac.cn> 
# Created [2018-02-02 Fri 19:24]


usage() {
    printf "NAME\n\tsubmit.sh - Main driver to submit\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%-5s\n" "./run.sh [OPTION]"
    printf "\nOPTIONS\n"
    printf "\n\t%-9s  %-40s"  "0.1"      "[Simulate jadepix1]" 
    printf "\n\t%-9s  %-40s"  "0.1.1"    "Run jadepix1 conf files"
    printf "\n\t%-9s  %-40s"  "0.1.2"    "Run genApx" 
    printf "\n\t%-9s  %-40s"  "0.1.3"    "Display electric field on zx plane"
    printf "\n\t%-9s  %-40s"  "0.1.4"    "Display electric field on yz plane"
    printf "\n\t%-9s  %-40s"  "0.1.5"    "Display electric field on xy plane"
    printf "\n"  
    printf "\n\t%-9s  %-40s"  "0.2"      "[Analyze jadepix sim data]"
    printf "\n\t%-9s  %-40s"  "0.2.1"    "Aanlyze charge collection efficiency"
    printf "\n\t%-9s  %-40s"  "0.2.2"    "plot adc histogram(sum and isolate)"
    printf "\n\t%-9s  %-40s"  "0.2.3"    "plot cce and entries proportion profile for cluster"
    printf "\n\t%-9s  %-40s"  "0.2.4"    "plot seed and cluster scatter"
    printf "\n"  
    printf "\n\t%-9s  %-40s"  "0.3"      "[Analyze Data]"
    printf "\n\t%-9s  %-40s"  "0.3.1"    "Analyze data"
    printf "\n"  
    printf "\n\t%-9s  %-40s"  "0.4"      "[Simulate jadepix using jadepix]"
    printf "\n\t%-9s  %-40s"  "0.4.1"    "Run jadepix"
    printf "\n"  
    printf "\n\t%-9s  %-40s"  "0.5"      "Run Electric field convert" 
    printf "\n\t%-9s  %-40s"  "0.5.1"    "Run convert electric field using AllPix Squared" 
    printf "\n\t%-9s  %-40s"  "0.5.2"    "Run convert electric field from TCAD" 
    printf "\n\t%-9s  %-40s"  "0.5.3"    "Run display electric field" 
    printf "\n\t%-9s  %-40s"  "0.5.4"    "Run display electric field using user tools[efield]" 
    printf "\n\t%-9s  %-40s"  "0.5.5"    "Run convert electric field from TCAD using user tools[efgen]" 
    printf "\n"  
    printf "\n\t%-9s  %-40s"  "0.6"      "[MoReWeb]"
    printf "\n"  
    printf "\n\t%-9s  %-40s"  "0.7"      "[Analyze JadePix1 for Iron55]"
    printf "\n\t%-9s  %-40s"  "0.7.1"    "Create python scripts for Iron55"
    printf "\n\t%-9s  %-40s"  "0.7.2"    "Create jobs for Iron55"
    printf "\n\t%-9s  %-40s"  "0.7.3"    "Run jobs for Iron55"
    printf "\n\t%-9s  %-40s"  "0.7.4"    "Combine root files for Iron55"
    printf "\n\t%-9s  %-40s"  "0.7.5"    "Create Cluster 2D results to root file"
    printf "\n\t%-9s  %-40s"  "0.7.6"    "Plot a1~a3 seed,cluster,size compare results"
    printf "\n\t%-9s  %-40s"  "0.7.7"    "Plot a4~a6 seed,cluster,size compare results"
    printf "\n\t%-9s  %-40s"  "0.7.8"    "Plot cluster and size 2D results"
    printf "\n\t%-9s  %-40s"  "0.7.9"    "Get iron55 peak information"
    printf "\n"  
    printf "\n\t%-9s  %-40s"  "0.8"      "[Analyze JadePix1 for Sr90]"
    printf "\n\t%-9s  %-40s"  "0.8.1"    "Create python scripts for Sr90"
    printf "\n\t%-9s  %-40s"  "0.8.2"    "Create jobs for Sr90"
    printf "\n\t%-9s  %-40s"  "0.8.3"    "Run jobs for Sr90"
    printf "\n\t%-9s  %-40s"  "0.8.4"    "Combine root files for Sr90"
    printf "\n\t%-9s  %-40s"  "0.8.5"    "Plot a1~a3 seed,cluster,size compare results"
    printf "\n\t%-9s  %-40s"  "0.8.6"    "Plot a4~a6 seed,cluster,size compare results"
    printf "\n\t%-9s  %-40s"  "0.8.7"    "Plot sr90 fit results"
    printf "\n"  
    printf "\n\t%-9s  %-40s"  "0.9"      "[Analyze JadePix1 for Pedestal]"
    printf "\n\t%-9s  %-40s"  "0.9.1"    "Create python scripts for Pedestal"
    printf "\n\t%-9s  %-40s"  "0.9.2"    "Create jobs for Pedestal"
    printf "\n\t%-9s  %-40s"  "0.9.3"    "Run jobs for Pedestal"
    printf "\n\t%-9s  %-40s"  "0.9.4"    "Combine root files for Pedestal"
    printf "\n\t%-9s  %-40s"  "0.9.5"    "Plot pedestal mean in 2D image"    
  }


if [[ $# -eq 0 ]]; then
    usage
    printf "\nPlease enter your option: "
    read option
else
    option=$1
fi

case $option in

    # --------------------------------------------------------------------------
    #  0.1 allpix-squared ($ALLPIX version)
    # --------------------------------------------------------------------------

    0.1) echo "Simulating jadepix1..."
         ;;
    0.1.1) echo "Running jadepix1 conf files..."
           allpix -c conf/jadepix1_main.conf -o output_directory="../output/"
           ;;
    0.1.2) echo "Running genApx ..."
           ./bin/genApx output/data.root output/data_genapx.root
           ;;
    0.1.3) echo "Displaying electric field on zx plane..."
           mesh_plotter -p zx -f field/jadepix1_electric_field.init -c 15 
           ;;
    0.1.4) echo "Displaying electric field on yz plane..."
           mesh_plotter -p yz -f field/jadepix1_electric_field.init -c 12  
           ;;
    0.1.5) echo "Displaying electric field on xy plane..."
           mesh_plotter -p xy -f field/jadepix1_electric_field.init -c 92  
           ;;


    # --------------------------------------------------------------------------
    #  0.2 Analyze jadepix data 
    # --------------------------------------------------------------------------


    0.2) echo "Analyze jadepix sim data"
         ;;
    0.2.1) echo "Aanlyze charge collection efficiency"
	    ./python/cceanalysis.py
	    ;;
    0.2.2) echo "plot adc histogram(sum and isolate)"
        ./python/plot_adc_hit.py
        ;;
    0.2.3)echo "plot cce and entries proportion profile for cluster"
        ./python/plot_cce_profile.py
        ;;
    0.2.4)echo "plot seed and cluster scatter"
        ./python/plot_seed_and_cluster.py
        ;;

    # --------------------------------------------------------------------------
    #  0.3 Analyze real data 
    # --------------------------------------------------------------------------


    0.3) echo "Analyze Real Data..."
         ;;
    0.3.1) echo "Analyze one example data (10000 frames)"
	   cd  ./src/
           make
           ./pixelana /publicfs/atlas/atlasnew/higgs/tth/hbb/raw_pixel/20180208/File20180208-A1_001 ./test.root 10000
	   ;;

    # --------------------------------------------------------------------------
    #  0.4 JadePix simulate using jadepix
    # --------------------------------------------------------------------------

    0.4) echo "Run jadepix simulation..."
         ;;
    0.4.1) echo "Run one example data (10000 events)"
      source ../etc/cepcvtx_setup.sh
      ../bin/jadepix g4macros/Fe55.mac g4out/Jadepix_001.rawdat
	   ;;

    # --------------------------------------------------------------------------
    #  0.5  Electric field convert
    # --------------------------------------------------------------------------

    0.5) echo "Running electric field convert..."
         ;;

    0.5.1) echo "Run convert electric field using AllPix Squared" 
        cd field
        dfise_converter -f n2_dfise -R 'Epi' -r 5 -x 33 -y 15 -z 33
        cd ..
        ;;

    0.5.2) echo "Running convert electric field from TCAD..."
        ./bin/convert field/n2_dfise_ElectricField.init field/n2_dfise_ElectricField_rotation.init
        ;; 

    0.5.3) echo "Running display electric field..."
        cd field
        mesh_plotter -f n2_dfise_ElectricField_rotation.init -x 33 -y 33 -z 15
        cd ..
        ;; 

    0.5.4) echo "Running display electric field using user tools[efield]..."
        echo "Tips for displaying"
        echo "Using style [COLZ/ARR] for TH2D"
        echo "Using style [BOX2] for TH3D"
        ./bin/efield -f field/jadepix1_electric_field.init -NX 25 -NY 17 -NZ 92 -cutX 10 -cutY 15 -cutZ 91 -o field/jadepix1_EFDisplay.root 
        ;; 

    0.5.5) echo "Run convert electric field from TCAD using user tools[efgen]" 
        cd field
        ../bin/efgen -f n2_dfise -R "Epi+Footprint+nWell1+pWell1" -NX 33 -NY 33 -NZ 18 -r 5 -o field/n2_dfise_Epi_Well 
        cd ..
        ;; 

    # --------------------------------------------------------------------------
    #  0.6 MoReWeb
    # --------------------------------------------------------------------------


    0.6) echo "MoReWeb..."
        ;;


    # --------------------------------------------------------------------------
    #  0.7 Analyze JadePix1 source data for Iron55
    # --------------------------------------------------------------------------

    0.7) echo "Analyze JadePix1 for Iron55..."
        ;;

    0.7.1) echo "Create python scripts for Iron55"
        chmod u+x ./python/src/script_iron55_generator.py
        # ./*.py -ChipAddress
        # ./*.py -ChipAddressStart -ChipAddressEnd
        ./python/src/script_iron55_generator.py -a1 -a6
        ;;

    0.7.2) echo "Create jobs for Iron55"
        chmod u+x ./python/src/job_iron55_generator.py
        # ./*.py -ChipAddress
        # ./*.py -ChipAddressStart -ChipAddressEnd
        ./python/src/job_iron55_generator.py -a1 -a6
        ;;
    
    0.7.3) echo "Run A1 jobs for Iron55"
        chmod u+x ./python/run/jobs_a1_iron55/*
        for file in ./python/run/jobs_a1_iron55/*
        do
        if [ -f "$file" ]
        then
            echo "$file is submitted!"
            #hep_sub -g physics $file
        fi
        done        
        ;;

    0.7.4) echo "Combine root files for Iron55"
        # ./*.py -ChipAddress
        # ./*.py -ChipAddressStart -ChipAddressEnd
        ./python/src/combine_root_iron55.py -a1 -a6     
        ;;
    0.7.5) echo "Create Cluster 2D results to root file"
        ./python/src/cluster_2d_root.py
        ;;
    0.7.6) echo "Plot a1~a3 seed,cluster,size compare results"
        ./python/plot/plot_iron55_chip_a1_a2_a3.py
        ;;
    0.7.7) echo "Plot a4~a6 seed,cluster,size compare results"
        ./python/plot/plot_iron55_chip_a4_a5_a6.py
        ;;
    0.7.8) echo "Plot cluster and size 2D results"
        ./python/plot/plot_iron55_cluste_vs_size_a1_to_a6.py
        ;;
    0.7.9) echo "Get iron55 peak information"
        ./python/plot/plot_iron55_gauss_peak.py
        ;;


    # --------------------------------------------------------------------------
    #  0.8 Analyze JadePix1 for Sr90
    # --------------------------------------------------------------------------

    0.8) echo "Analyze JadePix1 for Sr90..."
        ;;

    0.8.1) echo "Create python scripts for Sr90"
        chmod u+x ./python/src/script_sr90_generator.py
        # ./*.py -ChipAddress
        # ./*.py -ChipAddressStart -ChipAddressEnd
        ./python/src/script_sr90_generator.py -a1 -a6
        ;;

    0.8.2) echo "Create jobs for Sr90"
        chmod u+x ./python/src/job_sr90_generator.py
        # ./*.py -ChipAddress
        # ./*.py -ChipAddressStart -ChipAddressEnd
        ./python/src/job_sr90_generator.py -a1 -a6
        ;;
    
    0.8.3) echo "Run A1 jobs for Sr90"
        chmod u+x ./python/run/jobs_a1_sr90/*
        for file in ./python/run/jobs_a1_sr90/*
        do
        if [ -f "$file" ]
        then
            echo "$file is submitted!"
            #hep_sub -g physics $file
        fi
        done        
        ;;

    0.8.4) echo "Combine root files for Sr90"
        chmod u+x ./python/src/combine_root_sr90.py
        # ./*.py -ChipAddress
        # ./*.py -ChipAddressStart -ChipAddressEnd
        ./python/src/combine_root_sr90.py -a1 -a6   
        ;;

    0.8.5) echo "Plot a1~a3 seed,cluster,size compare results"
        ./python/plot/plot_sr90_chip_a1_a2_a3.py
        ;;

    0.8.6) echo "Plot a4~a6 seed,cluster,size compare results"
        ./python/plot/plot_sr90_chip_a4_a5_a6.py
        ;;
    0.8.7) echo "Plot sr90 and fit results"
        ./python/plot/plot_sr90_landau_fit.py
        ;;


    # --------------------------------------------------------------------------
    #  0.9 Analyze JadePix1 for Pedestal 
    # --------------------------------------------------------------------------

    0.9) echo "Analyze JadePix1 for Pedestal..."
        ;;

    0.9.1) echo "Create python scripts for Pedestal"
        chmod u+x ./python/src/script_pedestal_generator.py
        # ./*.py -ChipAddress
        # ./*.py -ChipAddressStart -ChipAddressEnd
        ./python/src/script_pedestal_generator.py -a1 -a6
        ;;

    0.9.2) echo "Create jobs for Pedestal"
        chmod u+x ./python/src/job_pedestal_generator.py
        # ./*.py -ChipAddress
        # ./*.py -ChipAddressStart -ChipAddressEnd
        ./python/src/job_pedestal_generator.py -a1 -a6
        ;;
    
    0.9.3) echo "Run A1 jobs for Pedestal"
        chmod u+x ./python/run/jobs_a1_pedestal/*
        for file in ./python/run/jobs_a1_pedestal/*
        do
        if [ -f "$file" ]
        then
            echo "$file is submitted!"
            #hep_sub -g physics $file
        fi
        done
        ;;

    0.9.4) echo "Combine root files for Pedestal"
        chmod u+x ./python/src/combine_root_pedestal.py
        # ./*.py -ChipAddress
        # ./*.py -ChipAddressStart -ChipAddressEnd
        ./python/src/combine_root_pedestal.py -a1 -a6   
        ;;





    0.9.1) echo "Plot pedestal mean in 2D image"
        ./python/plot/plot_pedestal.py
        ;;  

esac
