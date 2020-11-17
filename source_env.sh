software_dir=`cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd`

export PATH=${software_dir}/bin/FastQC:$PATH
export PATH=${software_dir}/bin/TrimGalore-0.6.6:$PATH
export PATH=${software_dir}/bin/LoRDEC-0.5.3-Linux/bin:$PATH
export PATH=${software_dir}/bin/DBG2OLC-master/compiled:$PATH
export PATH=${software_dir}/bin/DBG2OLC-master/utility:$PATH

export LD_LIBRARY_PATH=${software_dir}/bin/hdf5-1.8.21/lib:$LD_LIBRARY_PATH
export PATH=${software_dir}/bin/blasr-smrtanalysis-2.2/alignment/bin/:$PATH

export PYTHONPATH=$PYTHONPATH:${software_dir}/bin/PBSuite_15.8.24
export PATH=$PATH:${software_dir}/bin/PBSuite_15.8.24/bin

export PATH=${software_dir}/bin/minimap2-2.17_x64-linux:$PATH

export PATH=${software_dir}/bin/SSPACE-LongRead_v1-1:$PATH


export PATH=${software_dir}/bin/TGS-GapCloser-release_v1.0.1:${software_dir}/bin/TGS-GapCloser-release_v1.0.1/bin:$PATH

export PATH=${software_dir}/bin/LR_Gapcloser-master/src:$PATH

export PATH=${software_dir}:$PATH



