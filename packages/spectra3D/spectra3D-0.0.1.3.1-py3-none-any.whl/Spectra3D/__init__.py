__author__ = "Ben Knight @ Industrial 3D Robotics"
__maintainer__ = "Ben Knight"
__email__ = "bknight@i3drobotics.com"
__copyright__ = "Copyright 2020, Industrial 3D Robotics"
__license__ = "MIT"
__docformat__ = 'reStructuredText'

from plyfile import PlyData, PlyElement, PlyProperty, PlyListProperty
import numpy as np
from numpy.polynomial import Polynomial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import random
import string
import os

class Spectra3D():
    """
    Python tool for using spectroscopy data along side 3D by reading and writing the special ply format.
    See README for details on usages: https://github.com/i3drobotics/Spectra3D/blob/master/pySpectra3D/Spectra3D/README.md
    """
    def __init__(self):
        """
        Initalisation function for Spectra3D class. Defines comments that get added to ply output for elements and valid characters from csv strings.
        Usage sp3D = self.Spectra3D()
        """
        self.printable = set(string.printable)
        self.ply_comments = [  
            'This data format is a varient of the ply format for use',
            'combining 3D and spectrometer data.',
            '-------------------------------------------------------',
            'Developed by i3D Robotics and is-instruments (C)2020',
            '-------------------------------------------------------',
            'Care has been taken to make sure the 3D data is still viewable',
            'in standard ply readers however using custom properties and elements',
            "may cause issues so it is advised to use i3DR's ply tools.",
            'See [INSERT GITHUB LINK] for tools to read and write this data format'
        ]
        self.spectrum_comments = [
            'Define in spectrum the spectrometer data.'
        ]
        self.vertex_comments = [
            'Define in vertex element 3D point cloud data.',
            'Also included is label_index, a scalar that can be used',
            'to identify different types of points.',
            'A label_index of 0 will refer to an un-lablled point.',
            'Label_index can be used as a Scalar field to quickly see',
            'the labelled groups in a point cloud.'
        ]
        self.label_comments = [
            'Define in label the labels used in this dataset.',
            'Text is in ascii integer.'
        ]

    def write_csv(self,filename,data_list):
        """
        Write array to comma seperated csv file.
        :param filename: path to csv file
        :param data_list: list to write to csv file
        :type filename: string
        :type data_list: list
        """
        with open(filename, mode='w',newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',',quotechar = "'")
            for d in data_list:
                csv_writer.writerow(d)

    def read_csv(self,filename,isFirstRowHeader=False):
        """
        Read array from comma seperated csv file.
        :param filename: path to csv file
        :param isFirstRowHeader: if the first row in the csv file are headers so that they are ignored
        :type filename: string
        :type isFirstRowHeader: bool
        :returns: rows from file
        :rtype: list
        """
        rows = []
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if (isFirstRowHeader):
                    pass
                else:
                    rows.append(row)
                line_count += 1
        return rows

    def read_spectra_list(self,filename,isFirstRowHeader=False):
        """
        Read spectrum list from comma seperated csv file.
        :param filename: path to spectra csv file
        :param isFirstRowHeader: if the first row in the csv file are headers so that they are ignored
        :type filename: string
        :type isFirstRowHeader: bool
        :returns: (success of reading, xyzs data from file, spectra filenames from file)
        :rtype: (bool, list, list)
        """
        xyzs = []
        spectra_files = []
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if (isFirstRowHeader):
                    pass
                else:
                    if (len(row) != 4):
                        return False, None, None
                    x = float(''.join(filter(lambda x: x in self.printable, row[0])))
                    y = float(''.join(filter(lambda x: x in self.printable, row[1])))
                    z = float(''.join(filter(lambda x: x in self.printable, row[2])))
                    xyzs.append([x,y,z])
                    spectra_filename = ''.join(filter(lambda x: x in self.printable, row[3]))
                    spectra_files.append(spectra_filename)
                line_count += 1
        return True, xyzs, spectra_files

    def generate_labels(self,num_of_labels=10,string_length_range=(5,10)):
        """
        Generate list of random character labels for testing. 
        :param num_of_labels: number of labels to generate
        :param string_length_range: range of string length to generate string randomly between (min,max)
        :type num_of_labels: int
        :type string_length_range: list of ints
        :returns: generated labels
        :rtype: list
        """
        labels = []
        chars = string.ascii_uppercase + string.digits
        for i in range(0,num_of_labels):
            size = random.randint(string_length_range[0],string_length_range[1])
            text = ''.join(random.choice(chars) for _ in range(size))
            labels.append(text)
        return labels

    def generate_3D(self,x_range=[0,100],y_range=[0,100],z_range=[0,100],num_of_points=1000):
        """
        Generate random 3D data for testing.
        :param x_range: range of random ints to generate x values (min,max)
        :param y_range: range of random ints to generate y values (min,max)
        :param z_range: range of random ints to generate z values (min,max)
        :param num_of_points: number of 3D points to generate
        :type x_range: list of ints
        :type y_range: list of ints
        :type z_range: list of ints
        :type num_of_points: int
        :returns: generated 3D data
        :rtype: PlyData
        """
        data = []
        for i in range(0,num_of_points):
            x = random.uniform(x_range[0], x_range[1])
            y = random.uniform(y_range[0], y_range[1])
            z = random.uniform(z_range[0], z_range[1])
            r = 175
            g = 175
            b = 175
            data.append((x,y,z,r,g,b))
        vertex = np.array(data,
            dtype=[('x', 'f4'), ('y', 'f4'),('z', 'f4'),
                    ('red', 'u1'), ('green', 'u1'),('blue', 'u1')])
        el = PlyElement.describe(vertex, 'vertex')
        return PlyData([el])

    def generate_spectra(self,wavenumber_range=[0,1000],intensity_range=[0,1000],x_range=[0,100],y_range=[0,100],z_range=[0,100],num_of_points=1000,label_list_length=10):
        """
        Generate random spectra for testing.
        :param wavenumber_range: range of random ints to generate wavenumber (min,max)
        :param intensity_range: range of random ints to generate intensity (min,max)
        :param x_range: range of random ints to generate x values (min,max)
        :param y_range: range of random ints to generate y values (min,max)
        :param z_range: range of random ints to generate z values (min,max)
        :param num_of_points: number of spectrum points to generate
        :param label_list_length: random label indicies are generated between 0 and this value
        :type wavenumber_range: list of ints
        :type intensity_range: list of ints
        :type x_range: list of ints
        :type y_range: list of ints
        :type z_range: list of ints
        :type num_of_points: int
        :type label_list_length: int
        :returns: (generated spectrum data, generated xyz capture positions of data)
        :rtype: (list, list)
        """
        data = []
        spectra_data = []
        for n in range(0,num_of_points):
            w = random.uniform(wavenumber_range[0],wavenumber_range[1])
            i = random.uniform(intensity_range[0],intensity_range[1])
            spectra_data.append((w,i))
        spectra_data = sorted(spectra_data,key=lambda l:l[0], reverse=True)
        label_data = []
        for i in range(0,5):
            l = random.randint(0,label_list_length-1)
            s = random.uniform(0.5,1.0)
            label_data.append((l,s))
        label_data = sorted(label_data,key=lambda l:l[1], reverse=True)

        index = 0
        for d in range(0,len(spectra_data)):
            w = spectra_data[index][0]
            i = spectra_data[index][1]
            l,s = "",""
            if index < len(label_data):
                l = label_data[index][0]
                s = label_data[index][1]
            row = [w,i,l,s]
            data.append(row)
            index += 1

        xyz_data = [random.uniform(x_range[0], x_range[1]),random.uniform(y_range[0], y_range[1]),random.uniform(z_range[0], z_range[1])]
        return data, xyz_data
        
    def check_element_properties(self,plydata_element_properties,required_properties):
        """
        Check ply elements properties contains the required properties defined in 'required_properties'
        :param plydata_element_properties: List of PlyProperty's to check
        :param required_properties: List of PlyProperty's required to find in 'plydata_element_properties'
        :type plydata_element_properties: List
        :type required_properties: List
        :returns: valid
        :rtype: bool
        """
        # initialise found array
        properties_found = []
        for p in required_properties:
            properties_found.append(False)
        # search for required properties in ply element properties
        for p in plydata_element_properties:
            i = 0
            for c_p in required_properties:
                # look for property name in required
                if (p.name == c_p.name):
                    # look for property type in required
                    if (p.val_dtype == c_p.val_dtype):
                        # check if property is a list
                        if hasattr(p, 'len_dtype'):
                            # check if required propety is a list
                            if (hasattr(c_p, 'len_dtype')):
                                # look for property list type in required
                                if (p.len_dtype == c_p.len_dtype):
                                    properties_found[i] = True
                                    break
                        else:
                            properties_found[i] = True
                            break
                i+=1
        i = 0
        # check all required properties were found
        for p_f in properties_found:
            if not p_f:
                print("Failed to find required property: {}".format(required_properties[i]))
                return False
            i+=1
        return True

    def check_valid_plydata(self,plydata):
        """
        Check ply data is valid as expected by the defined ply format
        :param plydata: ply data to check
        :type plydata: PlyData
        :returns: valid
        :rtype: bool
        """
        # check data is of correct format
        # check data contains correct number of elements
        correct_num_of_elements = 3
        if len(plydata.elements) != correct_num_of_elements:
            print("Invalid number of elements. MUST be {}".format(correct_num_of_elements))
            return False
        # check data elements are of the correct name
        correct_elements = ["vertex","spectrum","label"]
        for c_e, e in zip(correct_elements, plydata.elements):
            if (e.name != c_e):
                print("Invalid element name. MUST be {}".format(c_e))
                return False
        # check vertex element contains at least the properties 'x','y','z' (can contain other properties if need be)
        required_props = [PlyProperty("x","float"),PlyProperty("y","float"),PlyProperty("z","float")]
        found_element_props = self.check_element_properties(plydata.elements[0].properties,required_props)
        if (not found_element_props):
            return False
        # check spectrum element contains the correct properties
        required_props = [PlyProperty("x","float"),PlyProperty("y","float"),PlyProperty("z","float"),
                            PlyListProperty("label_indices","uchar","int"),
                            PlyListProperty("similarity","uchar","float"),
                            PlyListProperty("wavenumber","int","float"),
                            PlyListProperty("intensity","int","float")]
        found_element_props = self.check_element_properties(plydata.elements[1].properties,required_props)
        if (not found_element_props):
            return False
        # check label element contains the correct properties
        required_props = [PlyListProperty("label_text","uchar","int")]
        found_element_props = self.check_element_properties(plydata.elements[2].properties,required_props)
        if (not found_element_props):
            return False
        return True

    def read_spectra(self,spectra_csv,xyz,isFirstRowHeader=False):
        """
        Read spectra from csv file into desired format
        :param spectra_csv: filename of comma seperated csv spectra data. Col1: Wavenumber, Col2: Intensity, Col3: Label_index, Col4: Similarity.
        :param xyz: x,y,z co-ordinate of where the measurement was taken.
        :param isFirstRowHeader: defines if first row of the csv file contains the header names. If so the first row is skipped when loading the data.
        :type spectra_csv: string
        :type xyz: list
        :type isFirstRowHeader: bool
        :returns: (read_success, spectral data (xyz,wavenumber,intensity,label_index,similarity) )
        :rtype: (bool,list)
        """
        data_spectra = []
        # check xyz is the correct size
        if (len(xyz) != 3):
            return False,None
        data_spectra.append(xyz)
        wavenumber = []
        intensity = []
        label = []
        similarity = []
        # read csv file
        with open(spectra_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if (len(row) != 4):
                    print("Invalid number of rows in csv. Expected 2: (Wavenumber, Intensity, Labels, Similarity).")
                    return False,None
                save_this_row = True
                if line_count == 0 and isFirstRowHeader:
                    save_this_row = False
                line_count += 1
                if (save_this_row):
                    w = ''.join(filter(lambda x: x in self.printable, row[0]))
                    i = ''.join(filter(lambda x: x in self.printable, row[1]))
                    wavenumber.append(float(w))
                    intensity.append(float(i))
                    if (row[2] != ""):
                        l = ''.join(filter(lambda x: x in self.printable, row[2]))
                        label.append(int(l))
                    if (row[3] != ""):
                        s = ''.join(filter(lambda x: x in self.printable, row[3]))
                        similarity.append(float(s))
        if (len(wavenumber) != len(intensity)):
            print("Failed to create spectra3D: Wavenumber and intensity data are diffent lengths")
            return False,None
        if (len(label) != len(similarity)):
            print("Failed to create spectra3D: Labels and similarity data are diffent lengths")
            return False,None
        data_spectra.append(wavenumber)
        data_spectra.append(intensity)
        data_spectra.append(label)
        data_spectra.append(similarity)
        return True,data_spectra

    def read_spectra_labels(self,label_csv,isFirstRowHeader=False):
        """
        Read spectrum labels from csv to desired format
        :param label_csv: filename of comma seperated csv label data.
        :param isFirstRowHeader: defines if first row of the csv file contains the header names. If so the first row is skipped when loading the data.
        :type label_csv: string
        :type isFirstRowHeader: bool
        :returns: (read_success, substance labels)
        :rtype: (bool,list)
        """
        label = []
        # read csv file
        with open(label_csv) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if (len(row) != 1):
                    print("Invalid number of rows in csv. Expected 1: (Label text).")
                    return False,None
                save_this_row = True
                if line_count == 0 and isFirstRowHeader:
                    save_this_row = False
                line_count += 1
                if (save_this_row):
                    text = ''.join(filter(lambda x: x in self.printable, row[0]))
                    label.append(text)
        return True,label

    def createSpectra3D(self,data_spectra,data_labels,data_3D):
        """
        Read spectrum labels from csv to desired format
        :param data_spectra: Spectum data. Col1: Wavenumber, Col2: Intensity, Col3: Label_index, Col4: Similarity.
        :param data_labels: Label of substances. MUST be in the same order as indices used in data_spectra's label_index
        :param data_3D: 3D data points
        :type data_spectra: list
        :type data_labels: list
        :type data_3D: PlyElement
        :returns: (success, Spectra3D ply data)
        :rtype: (bool,PlyData)
        :todo: fix numpy creation issue in 'label_data' when all strings are the same size

        """
        plydata_3D = data_3D

        # convert spectra data in correct format for plydata
        spectrum_dt = np.dtype({'names': ['x','y','z','label_indices','similarity','wavenumber','intensity'], 
                                'formats':['f4','f4','f4',np.object,np.object,np.object,np.object]})
        spectrum_list = []
        for sp in data_spectra:
            # check data_spectra is correct length
            if (len(sp) != 5):
                print("Failed to create spectra3D: Data_spectra is incorrect length")
                return False,None
            # check xyz in spectra data is correct length
            if (len(sp[0]) != 3):
                print("Failed to create spectra3D: XYZ data is incorrect length")
                return False,None
            x,y,z = sp[0]

            wavenumber = sp[1]
            intensity = sp[2]
            label_indices = sp[3]
            similarity = sp[4]
            # check spectra data is correct length
            if (len(wavenumber) != len(intensity)):
                print("Failed to create spectra3D: Wavenumber and intensity data are diffent lengths")
                return False,None
            if (len(label_indices) != len(similarity)):
                print("Failed to create spectra3D: Labels and similarity data are diffent lengths")
                return False,None

            spectrum_list.append((x,y,z, label_indices, similarity, wavenumber, intensity))

        spectrum_data = np.array(spectrum_list,dtype=spectrum_dt)

        plydata_spectrum = PlyElement.describe(spectrum_data, 'spectrum',comments=self.spectrum_comments,
                                    val_types={'label_indices': 'i4','similarity': 'f4',
                                                'wavenumber': 'f4','intensity': 'f4'},
                                    len_types={'label_indices': 'u1','similarity': 'u1',
                                                'wavenumber': 'i4','intensity': 'i4'})

        # convert label data in correct format for plydata
        labels = []
        for d in data_labels:
            text = []
            for c in d:
                text.append(ord(c))
            labels.append(text)
        label_dt = np.dtype({'names': ['label_text'], 'formats':[np.object]})
        #TODO fix numpy creation issue when all strings are the same size
        label_data = np.array(labels,dtype=label_dt)

        plydata_label = PlyElement.describe(label_data, 'label', comments=self.label_comments,
                                    val_types={'label_text': 'i4'},
                                    len_types={'label_text': 'u1'})

        # add default comments to plydata for vectex element
        plydata_3D.comments = self.vertex_comments

        plydata = PlyData([plydata_3D, plydata_spectrum,plydata_label],
                      text=False, comments=self.ply_comments)

        return True, plydata
        
    def read_ply(self,filename):
        """
        Read data from ply file
        :param filename: Path of ply file to load from.
        :type filename: string
        :returns: (ply data includes expected data format, ply data)
        :rtype: (bool,PlyData)
        """
        # read data from file
        plydata = PlyData.read(filename)
        isDataValid = self.check_valid_plydata(plydata)
        self.plydata = plydata
        return isDataValid, plydata

    def write_ply(self,plydata,filename,isBinary=False):
        """
        Write PlyData to ply file
        :param plydata: ply data to write to file
        :param filename: Path of ply file to write to.
        :type plydata: PlyData
        :type filename: string
        """
        with open(filename, mode='wb') as f:
            PlyData(plydata, text=True, comments=plydata.comments).write(f)

    def plt_matplotlib(self,plydata):
        """
        Plot ply data on 3D graph. If spectrum data is included then also plots this data and enables interface for clicking these points to view the data in more detail.
        :param plydata: ply data to write to file
        :type plydata: PlyData
        """
        vertex = plydata['vertex']
        fig3D = plt.figure()
        ax3D = fig3D.add_subplot(111, projection='3d')

        (x, y, z) = (vertex[t] for t in ('x', 'y', 'z'))

        required_props = [PlyProperty("red","uchar"),PlyProperty("green","uchar"),PlyProperty("blue","uchar")]
        found_element_props = self.check_element_properties(plydata.elements[0].properties,required_props)
        rgbs = 'red'
        if (found_element_props):
            rgbs = []
            for t in vertex:
                rgbs.append((t['red']/255,t['green']/255,t['blue']/255,0.5))

        ax3D.scatter(x, y, z, zdir='z', c= rgbs, s=1)

        if 'spectrum' in plydata:
            print("Spectrum included")
            (xs, ys, zs, i_s) = (plydata['spectrum'][t] for t in ('x', 'y', 'z',"label_indices"))
            colors = []
            for i in i_s:
                colors.append(i[0])
            ax3D.scatter(xs, ys, zs, zdir='z', c= colors, s=30, picker=1, depthshade=False)
            self.figSpec = None
            
            def onpick(event):
                if (event.mouseevent.button == 1):
                    index = event.ind[0]
                    l = plydata['spectrum']["label_indices"][index]
                    l_is = []
                    for i in l:
                        l_i = plydata["label"]["label_text"][i]
                        l_s = "".join(str(chr(l)) for l in l_i)
                        l_is.append(l_s)

                    s = plydata['spectrum']["similarity"][index]
                    x = float('%.3g' % plydata['spectrum']["x"][index])
                    y = float('%.3g' % plydata['spectrum']["y"][index])
                    z = float('%.3g' % plydata['spectrum']["z"][index])
                    w = plydata['spectrum']["wavenumber"][index]
                    i = plydata['spectrum']["intensity"][index]

                    if (self.figSpec):
                        plt.close(fig=self.figSpec)

                    self.figSpec = plt.figure(figsize=(8, 6))
                    axSpec = self.figSpec.add_subplot(111)

                    columns = ('Substance','Similarity (%)')
                    data = []
                    for li, si in zip(l_is,s):
                        si_rounded = round(si * 100,2)
                        data.append([str(li),str(si_rounded)])
                    
                    # Add a table at the bottom of the axes
                    plt.table(cellText=data,
                        colLabels=columns,cellLoc='center',colWidths=[0.4 for c in columns],
                        loc='upper right')
                    plt.plot(w,i,'-', c='black')
                    axSpec.set_title("Spectrum @ ({},{},{})".format(x,y,z))
                    axSpec.set_ylim([0,200])
                    #axSpec.set_xlim([0,2500])

                    plt.show()
                
            fig3D.canvas.mpl_connect("pick_event", onpick)

        plt.show()

if __name__ == "__main__":
    file_3D_in = "Data/wood_room_scan_20000.ply"
    file_spectral_list_in = "Data/spectrum_list.csv"
    file_labels_in = "Data/spectrum_labels.csv"
    file_out = "Data/sample_data_out.ply"

    sp3D = Spectra3D()

    # generate example data for testing
    gen3D = False
    genSpec = True

    if (gen3D):
        # generate 3D data
        x_range = (0,10)
        y_range = (0,10)
        z_range = (0,10)
        num_of_points = 1000
        file_3D = "Data/gen_3D_data.ply"
        print("Generating 3D test data...")
        ply3D = sp3D.generate_3D(x_range,y_range,z_range,num_of_points)
        # save 3D data to PLY
        sp3D.write_ply(ply3D,file_3D)
        file_3D_in = file_3D

    # read point cloud data from PLY file
    print("Reading 3D data...")
    res, data_3D = sp3D.read_ply(file_3D_in)
    data_3D = data_3D["vertex"]

    # generate spectra
    if (genSpec):
        if (not gen3D):
            x_range = (min(data_3D["x"]),max(data_3D["x"]))
            y_range = (min(data_3D["y"]),max(data_3D["y"]))
            z_range = (min(data_3D["z"]),max(data_3D["z"]))
        num_of_spectra = 20
        wavenumber_range = (0,2500)
        intensity_range = (0,100)
        num_of_points = 1000
        num_of_labels = 5
        file_labels = "Data/gen_labels.csv"
        file_spectra_list = "Data/gen_spectrum_list.csv"

        # generate label data
        data_labels = sp3D.generate_labels(num_of_labels)
        data_labels_formatted = []
        for d in data_labels:
            d_formatted = [d]
            data_labels_formatted.append(d_formatted)
        # save list of labels to csv
        sp3D.write_csv(file_labels,data_labels_formatted)
        file_labels_in = file_labels
        
        # generate spectrum data (xyz position and spectrum data)
        print("Generating spectral test data...")
        xyz_spectra = []
        for i in range(0,num_of_spectra):
            file_spectra = 'Data/gen_spectrum_data_{}.csv'.format(i)
            spectra_data, xyz_data = sp3D.generate_spectra(wavenumber_range,intensity_range,x_range,y_range,z_range,num_of_points,len(data_labels))
            # write spectral data to csv
            sp3D.write_csv(file_spectra,spectra_data)
            file_spectra_formatted = '\"{}\"'.format(file_spectra)
            xyz_spectra.append([xyz_data[0],xyz_data[1],xyz_data[2],file_spectra_formatted])
        # write xyz data with file name location of spectra to csv
        sp3D.write_csv(file_spectra_list,xyz_spectra)
        file_spectral_list_in = file_spectra_list

    # read list of substance labels from csv
    res, data_labels = sp3D.read_spectra_labels(file_labels_in)

    # read list of spectra from csv
    res, xyzs, spectra_file_list = sp3D.read_spectra_list(file_spectral_list_in)

    print("Reading Spectrometer data...")
    data_spectra = []
    for spectra_file, xyz in zip(spectra_file_list,xyzs):
        # Read spectra data from csv and convert it to format expected by 'createSpectra3D'
        res, data_spectra_n = sp3D.read_spectra(spectra_file,xyz,True)
        data_spectra.append(data_spectra_n)
    
    if (res):
        print("Creating spectra3D data...")
        res, plydata = sp3D.createSpectra3D(data_spectra,data_labels,data_3D)
        if (res):
            print("Saving data...")
            sp3D.write_ply(plydata,file_out)
            print("Data saved sucessfully.")

            res,plydata = sp3D.read_ply(file_out)
            print("Plotting data...")
            sp3D.plt_matplotlib(plydata)
            print("Data plot ready.")

    # clean up generated files
    if (gen3D):
        os.remove(file_3D_in)
    if (genSpec):
        os.remove(file_labels_in)
        os.remove(file_spectral_list_in)
        for i in range(0,num_of_spectra):
            file_spectra = 'Data/gen_spectrum_data_{}.csv'.format(i)
            os.remove(file_spectra)