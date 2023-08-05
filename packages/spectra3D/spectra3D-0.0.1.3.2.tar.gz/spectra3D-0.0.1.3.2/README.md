# **SPECTRA 3D**
# Python Package

Python tool for using spectroscopy data along side 3D by reading and writing the special ply format.

![GIF of labelled 3D point cloud showing spectrum data](https://raw.githubusercontent.com/i3drobotics/Spectra3D/master/pySpectra3D/Spectra3D/pySpectra3D_example.gif)

## **Run**
This tool can be used to add spectral data to 3D data and write it to ply format. This brings several sources of data into one collated file that is much easier to deal with.

It is adviced to look at and run the example code [Samples](https://github.com/i3drobotics/Spectra3D/tree/master/pySpectra3D/SampleScripts) to understand the data format expected. This script demonstrates using spectra 3D with auto generated data or loading data from csv and ply files.

### **3D data**
3D data contains x,y,z co-ordinates generated from stereo cameras / lidar / photogrammetry. This script expects this data in the form of a ply file. This can include vertex color data which will be preserved. 

Example usage:
```python
res, data_3D = sp3D.read_ply(ply_3D_filename)
```
```
INPUTs
    filename (string): location of ply file
OUTPUTs
    res (bool): succeeded or failed to load ply data
    data_3D (PlyElement): 3D data read from file [TODO: Change this to standard numpy 3D data]
```

WARNING: module 'plyfile' used in this script only supports ply properties in the format:
```code
property {type} {name}
```
This appears to be the de facto standard however is not explicitly defined in the standard so be careful.

### **Spectral data**
The spectral data this module was created for is from Raman Spectroscopy. This data has two outputs; wavenumber and intensity. Also included is a machine learning result that tries to identify the substance described by the spectrum. The machine learning result is a sorted list of 5 possible substances with similarity rating for each (%). pySpectra3D expects this data as a 3 csv files (comma seperated). Firstly there should be csv file for each spectrum which contains 4 columns. 
```
| Wavenumber | Intensity | Label Index | Similarity |
|------------|-----------|-------------|------------|
| 1234.56    | 1234.56   | 2           | 0.999      |
| 1234.56    | 1234.56   | 5           | 0.123      |
| . . .      | . . .     | . . .       | . . .      |
```
There is an option when loading the csv data as to if includes headers in the first row ('isFirstRowHeader'). Set this to **true** if the csv contains headers. 

Secondly there should be a csv that contains a list of substance labels. The order of these should match the index used in 'label index' in the first csv. This index **MUST** be consistant across all spectrum files.
```
| Label              |
|--------------------|
| Aluminium_Sulphate |
| Potassium_Sulphate |
| . . .              |
```
Thirdly there should be a csv file contains the xyz co-ordinate of where the spectrum was recorded and the filename of that spectrum csv. The co-ordinate should be in the same co-ordinate system so that it is placed in the scene in the correct position (World zero should be the same in both).
```
| X     | Y     | Z     | Filename             |
|-------|-------|-------|----------------------|
| 1     | 2     | 3     | sample_spectrum1.csv |
| 4     | 5     | 6     | sample_spectrum2.csv |
| . . . | . . . | . . . | . . .                |
```

Example data is included in this repository to clarify this format. Check the [Samples](https://github.com/i3drobotics/Spectra3D/tree/master/pySpectra3D/SampleScripts) for an example of usage. 

## **Generating sample data**
Package contains functions for generating test data to try out the class. 
### **Generate 3D**
Function name: **'generate_3D'**

Generate random 3D data within chosen bounds. 

### **Generate labels**
Function name: **'generate_labels'**

Generate random strings as substance labels.

### **Generate spectrum**
Function name: **'generate_spectra'**

Generate random spectral data and labels within chosen bounds (this data is not representitive of a normal spectrum as it is random data). Label indices are chosen at random from chosen label list length.

## **PLY HEADER**
A custom ply header is used to store the extra spectroscopy data. This includes text labels that identify the material that was scanned and x y z positioning of where the data was captured from. The spectroscopy data includes wavenumber and intensity.
It is advised to keep the comments in the header of all ply files of this type to avoid confusion by explaining the data format. 
```
ply
format ascii 1.0
comment -------------------------------------------------------
comment This data format is a varient of the ply format for use
comment combining 3D and spectrometer data.
comment -------------------------------------------------------
comment Developed by i3D Robotics and is-instruments (C)2020
comment -------------------------------------------------------
comment Care has been taken to make sure the 3D data is still viewable
comment in standard ply readers however using custom properties and elements
comment may cause issues so it is advised to use i3DR's ply tools.
comment See [INSERT GITHUB LINK] for tools to read and write this data format
comment -------------------------------------------------------
comment Define in vertex element 3D point cloud data.
comment Also included is label_index, a scalar that can be used
comment to identify different types of points.
comment A label_index of 0 will refer to an un-lablled point.
comment Label_index can be used as a Scalar field to quickly see
comment the labelled groups in a point cloud.
element vertex 8
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
comment -------------------------------------------------------
comment Define in spectrum the spectrometer data.
element spectrum 1
property float x
property float y
property float z
property list uchar int label_indices
property list uchar float similarity
property list int float wavenumber
property list int float intensity
comment -------------------------------------------------------
comment Define in label the labels used in this dataset.
comment Text is in ascii integer.
element label 5
property list uchar int label_text
comment -------------------------------------------------------
end_header
```
