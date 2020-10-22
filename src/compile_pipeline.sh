mkdir ../bin
tar xavf TrimGalore-0.6.6.tar.gz
mv TrimGalore-0.6.6 ../bin

unzip fastqc_v0.11.9.zip
mv FastQC ../bin

tar xavf LoRDEC-0.5.3-Linux.tar.gz
mv LoRDEC-0.5.3-Linux ../bin

tar xavf DBG2OLC-revise.tar.gz
mv DBG2OLC-master ../bin/

tar xavf hdf5-1.8.21.tar.gz
cd hdf5-1.8.21
mkdir build && cd build
cmake -D CMAKE_INSTALL_PREFIX=../../../bin/hdf5-1.8.21 ..
make -j8 && make install
cd ../..

hdf_root=`cd "$( dirname "../bin/hdf5-1.8.21" )" && pwd`

export LIBRARY_PATH=${hdf_root}/hdf5-1.8.21/lib:$LIBRARY_PATH
export CPATH=${hdf_root}/hdf5-1.8.21/include:$CPATH

tar xavf blasr-smrtanalysis-2.2.tar.gz
cd blasr-smrtanalysis-2.2/
make -j8
cd ..
mv blasr-smrtanalysis-2.2 ../bin

tar xavf PBSuite_15.8.24-revise.tar.gz
mv PBSuite_15.8.24 ../bin

tar xavf minimap2-2.17_x64-linux.tar.bz2
mv minimap2-2.17_x64-linux ../bin

tar xavf SSPACE-LongRead_v1-1-revise.tar.gz
mv SSPACE-LongRead_v1-1 ../bin

tar xavf TGS-GapCloser-release_v1.0.1.tar.gz
cd TGS-GapCloser-release_v1.0.1
make
cd ..
mv TGS-GapCloser-release_v1.0.1 ../bin

unzip LR_Gapcloser-master.zip
chmod u+x LR_Gapcloser-master/src/*
mv LR_Gapcloser-master ../bin

