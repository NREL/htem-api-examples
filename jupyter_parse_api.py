# Written by Marcus Schwarting in collaboration with the National Renewable
# Energy Laboratories. For further information please see the website 
# [insert website name here] as well as the recent publication on this work,
# [insert reference to upcoming paper here]. The goal of this project is to
# further the objectives laid out in the strategic objectives for the
# Materials Genome Initiative.
# 
# For further information on this code project, please email:
# Marcus Schwarting ==> marcus.schwarting@nrel.gov

import urllib, json
import pandas as pd

poss_out_types = {'xrd_all':{'positions':['xrd_angle','xrd_intensity','xrd_background']},\
                  'xrd_peak_count':{'positions':['peak_count']},\
                  'elements_req':{'samples':['elements']},\
                  'thickness':{'positions':['thickness']},\
                  'composition':{'positions':['xrf_compounds','xrf_concentration']},\
                  '4pp_all':{'positions':['fpm_voltage_volts','fpm_current_amps','fpm_sheet_resistance',\
                                          'fpm_standard_deviation','fpm_resistivity','fpm_conductivity']},\
                  '4pp_cond':{'positions':['fpm_conductivity']},\
                  '4pp_sheet_res':{'positions':['fpm_sheet_resistance']},\
                  '4pp_VC':{'positions':['fpm_voltage_volts','fpm_current_amps']},\
                  'oo_all':{'positions':['oo_all','opt_direct_bandgap','opt_indirect_bandgap','opt_average_vis_trans']},\
                  'oo_uvit':{'positions':['oo_uvit']},\
                  'oo_uvir':{'positions':['oo_uvir']},\
                  'oo_nirr':{'positions':['oo_nirr']},\
                  'oo_nirt':{'positions':['oo_nirt']},\
                  'bg_all':{'positions':['opt_direct_bandgap','opt_indirect_bandgap']},\
                  'bg_direct':{'positions':['opt_direct_bandgap']},\
                  'bg_indirect':{'positions':['opt_indirect_bandgap']},\
                  'prep_temp':{'samples':['deposition_initial_temp_c']},\
                  'prep_pressure':{'samples':['deposition_growth_pressure_mtorr']},\
                  'pdac_eval':{'samples':['pdac','num']},\
                  'positions_list':{'samples':['position_ids']},\
                  'positions_locations':{'positions':['position']}
                  }

def htem_data_collect(param_list,out_types):
    '''
    This function is the main function used to collect and utilize data from 
    the HTEM database (https://api.hpc.nrel.gov/xrd/api/). The variables that
    are utilized by this function are as follows:
        
        param_list: This is the list of parameters for which we would like to
        acquire data for. This list can take one of four forms:
            PDAC list: When a new sample is made, its initial name is not the
            four-digit code that the API generates. The naming convention for
            a new sample references the PDAC machine that made the sample, 
            then the five-digit number of the sample (ascending by the order
            the sample was made). There are five deposition chambers for 
            which data is readily available. The final form will be fed in as
            a list of strings that could look like this: [PDAC_COM1_00844, 
            PDAC_COM3_00132, PDAC_COM4_00588, PDAC_COM5_00021].
            Elements list: Suppose one wants to do a more general search of a
            particular material available in our database. This search tool is
            available in our database as well. One can enter a list of 
            elements in list format like so: ['Zn', 'Ni', 'O']. The elements
            need not be entered in alphabetical order. Also, this provides
            a list of samples that have ALL of the following elements present,
            not ANY of the following elements present. For example, if one 
            were to search for ['Zn','O'], then the resulting search would 
            query ZnO, SnZnO, ZnNiCoO, etc. Searching by element can be quite
            a bit more time-intensive and provide a very large quantity of 
            data from the database. One should use this setting with care.
            Sample list: When a sample is submitted to the API, it is given
            a unique 4-digit identifier we call the 'sample id'. One can 
            submit a list of samples like so: [7229,7230,7231].
            Position list: Within a single sample, there are 44 individually
            identified positions. When a gradient (compositional, temperature,
            or other) is applied across the sample, the 44 unique positions 
            allows for one to see trends across the substrate. While normally
            an entire sample would be selected for analysis, the option to 
            search based on a specific position number is also available.
        Note that a list must be provided that has a continuity throughout of
        one of the four available types. One may not mix the available types.
        One should also be wary of queries that are expected to yield a large
        quantity of output as this may take quite a long time to load.
        
        out_types: There are many different fields available to search 
        through in this large database. In order to more efficiently process
        a user's queries, a user is expected to specify which variables they 
        would like to see returned to them. To have the function return each
        of these fields, a list of requested fields must be supplied. The 
        list of available options is quite extensive, but is enumerated here:
            'xrd_all': Includes X-Ray Diffraction spectra in three parts,
            specifically the XRD wavelength, XRD intensity, and XRD
            background. Note that we commonly subtract the background from the
            intensity before doing any post-processing analysis. This field 
            is specific to the positions.
            'xrd_peak_count': A built-in algorithm does a rudimentary analysis
            of the peaks located within X-Ray Diffraction spectra. This field
            should be taken with a grain of salt since a generalized peak 
            fitting algorithm that accurately locates peaks in both amorphous
            and crystalline materials is not an easy task. See Jupyter
            Notebooks for more examples of this. This field is specific to 
            the positions.
            'elements_req': This returns all of the elements contained in a
            sample. The field is specific to the X-Ray Fluorescence data,
            however in the absence of this the researcher's recordings at the
            time of deposition are set. This is specific to the sample level.
            'thickness': Another data field gathered from the X-Ray 
            Fluorescence is the thickness of the sample at a given position.
            This field is specific to the positions.
            '4pp_all': In this case, the '4pp' stands for 4-Point Probe, which 
            is used to take measures on conductivity, sheet resistance, etc.
            The 'all' in the command means to take all metrics gathered from
            the 4-Point analysis. This field is specific to the positions.
            '4pp_cond': Returns the conductivity. This field is specifc to 
            the positions.
            '4pp_sheet res': Returns the sheet resistance. This field is 
            specific to the positions.
            '4pp_VC': In order to measure the conductivity and sheet 
            resistance, a linear relationship between the voltage and the 
            current must be established. This voltage/current pair is what
            is returned. This field is specific to the positions.
            'oo_all': Returns all data taken from Ocean Optics measurements,
            including UVIR, UVIT, NIRR, NIRT (described below), and the 
            tabulated direct and indirect band gaps (calculated using MARS).
            'oo_uvit': Returns just the UVIT (Ultraviolet Intensity of 
            Transmittance), a measurement of the Ocean Optics equipment.
            'oo_uvir': Returns just the UVIR (Ultraviolet Intensity of 
            Reflectance), a measurement of the Ocean Optics Equipment.
            'oo_nirt': Returns just the NIRT (Near-Infrared Transmittance),
            a measurement of the Ocean Optics Equipment.
            'oo_nirr': Returns just the NIRR (Near-Infrared Reflectance),
            a measurement of hte Ocean Optics Equipment.
            'bg_all': Returns the direct and indirect band gaps from the 
            materials; these are identified using a MARS technique described
            in Schwarting et. al., paper to appear.
            'bg_direct': Returns just the direct band gap (MARS Method)
            'bg_indirect': Returns just the indirect band gap (MARS Method)
            'prep_temp': Returns the temperature at which the sample was
            prepared in the combinatorial deposition chamber.
            'prep_pressure': Returns the pressure at which the sample was 
            prepared in the combinatorial deposition chamber.
            'pdac_eval': A simple argument fed to the system that returns the 
            PDAC number (denoting the combinatorial chamber that made the 
            sample) and the sample number.
            'positions_list': Returns a list of all positions available for
            a sample.
    
    The output format of this code takes the following form:
        A pandas-formatted DataFrame that includes all of the data types 
        that were selected at the input.
    '''
    for i in out_types:
        if i not in poss_out_types.keys():
            raise ValueError('Error: Invalid Parameter '+str(i))
    sample_level = []
    position_level = []
    for item in out_types:
        if 'samples' in poss_out_types[item].keys():
            for s in poss_out_types[item]['samples']:
                sample_level.append(s)
        if 'positions' in poss_out_types[item].keys():
            for p in poss_out_types[item]['positions']:
                position_level.append(p)
    sample_level = list(set(sample_level))
    position_level = list(set(position_level))
    if len(param_list) == 0:
        raise ValueError('Error: No Parameters Provided!')
    if type(param_list[0]) == str:
        if 'PDAC' in param_list[0]:
            return pdac_handle(param_list,sample_level,position_level)
        else:
            return elements_handle(param_list,sample_level,position_level)
    elif type(param_list[0]) == int:
        if len(str(param_list[0])) <= 5:
            return samples_handle(param_list,sample_level,position_level)
        else:
            return positions_handle(param_list,sample_level,position_level)

def pdac_handle(pdac_list,sample_level,position_level):
    '''
    This function is responsible for handling any queries that are made in the
    form of a PDAC and experimental sample number specification.
    Inputs:
        pdac_list: A list of strings of the form 'PDAC_COMX_12345'
        sample_level: A list of variables to be found at the sample level
        position_level: A list of variables to be found at the position level
    Returns:
        A pandas dataframe which includes all of the information queried.
    '''
    sample_level = sample_level + ['pdac','num']
    samples_forward = []
    for i in pdac_list:
        # We first split up the string into the machine and sample numbers.
        com_num = str(int(i.replace('PDAC_COM','').split('_')[0]))
        samp_num = i.replace('PDAC_COM','').split('_')[1]
        # Pings the website available at this address for PDAC lookups.
        url = 'https://api.hpc.nrel.gov/xrd/api/samples?num='+samp_num+'&pdac='+com_num
        response = urllib.urlopen(url)
        data = json.loads(response.read())[0]
        samples_forward.append(int(data['id']))
    # Once the PDAC identifiers are changed to sample ids, they are forwarded
    # on to the samples_handle function for further processing.
    return pd.DataFrame(samples_handle(samples_forward,sample_level,position_level))

def elements_handle(elt_list,sample_level,position_level):
    '''
    This function is responsible for handling any queries that are made in the
    form of a list of elements required for the sample, ex. ['Zn', 'Co', 'O'].
    Inputs:
        pdac_list: A list of elements in the form ['X', 'Y', 'Z']
        sample_level: A list of variables to be found at the sample level
        position_level: A list of variables to be found at the position level
    Returns:
        A pandas dataframe which includes all of the information queried.
    '''
    sample_level.append('elements')
    elt_list = sorted(elt_list)
    elt_str = ''
    for elt in elt_list[:-1]:
        elt_str = elt_str+str(elt) + ','
    elt_str = elt_str + elt_list[-1]
    url = 'https://api.hpc.nrel.gov/xrd/api/samples?element='+elt_str+'&which=all'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    elements_forward = []
    for sample in data:
        elements_forward.append(sample[u'id'])
    # Once a list of elements are changed to sample ids, they are forwarded on
    # to the samples_handle for further processing.
    return pd.DataFrame(samples_handle(elements_forward,sample_level,position_level))

def samples_handle(samples_list,sample_level,position_level):
    '''
    This function is responsible for handling any queries that are made in the
    form of a list of samples (4-digit ids).
    Inputs:
        samples_list: A list of samples in the form [1111,1112,1113,etc.]
        sample_level: A list of variables to be found at the sample level
        position_level: A list of variables to be found at the position level
    Returns:
        A pandas dataframe which includes all of the information queried.
    '''
    if len(position_level) != 0:
        positions_forward = []
        for sample in samples_list:
            url = 'https://api.hpc.nrel.gov/xrd/api/samples/'+str(sample)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            for k in data['position_ids']:
                try:
                    positions_forward.append(int(k))
                except TypeError:
                    pass
        sample_level.append('id')
        return positions_handle(positions_forward,sample_level,position_level)
    else:
        sample_format_return = {}
        for sample in samples_list:
            url = 'https://api.hpc.nrel.gov/xrd/api/samples/'+str(sample)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            individual_dict = {}
            for item in sample_level:
                try:
                    individual_dict.update({item:data[item]})
                except KeyError: #That is, if data is unavailable for for a sample, pad with None
                    individual_dict.update({item:None})
            sample_format_return.update({sample:individual_dict})
        return pd.DataFrame(sample_format_return)

def positions_handle(positions_list,sample_level,position_level):
    '''
    This function is responsible for handling any queries that are made in the
    form of a list of positions. These could be all in the same sample or available
    from different samples. This is the most specific lookup within the database.
    Inputs:
        positions_list: A list of positions in the form [111111,111112,111113,etc.]
        sample_level: A list of variables to be found at the sample level
        position_level: A list of variables to be found at the position level
    Returns:
        A pandas dataframe which includes all of the information queried.

    '''
    if len(position_level) != 0:
        position_format_return = {}
        for position in positions_list:
            url = 'https://api.hpc.nrel.gov/xrd/api/positions/'+str(position)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            individual_dict = {}
            for item in position_level:
                try:
                    if 'oo_' not in item:
                        individual_dict.update({item:data[item]})
                    else: #Optical data needs to be handled separately due to the nesting in the API.
                        if item == 'oo_all':
                            individual_dict.update({'uvit_wavelength':data['oo']['uvit']['wavelength']})
                            individual_dict.update({'uvit_response':data['oo']['uvit']['response']})
                            individual_dict.update({'uvir_wavelength':data['oo']['uvir']['wavelength']})
                            individual_dict.update({'uvir_response':data['oo']['uvir']['response']})
                            individual_dict.update({'nirt_wavelength':data['oo']['nirt']['wavelength']})
                            individual_dict.update({'nirt_response':data['oo']['nirt']['response']})
                            individual_dict.update({'nirr_wavelength':data['oo']['nirr']['wavelength']})
                            individual_dict.update({'nirr_response':data['oo']['nirr']['response']})
                        elif item == 'oo_uvit': #UV Spectrum, Transmittance
                            individual_dict.update({'uvit_wavelength':data['oo']['uvit']['wavelength']})
                            individual_dict.update({'uvit_response':data['oo']['uvit']['response']})
                        elif item == 'oo_uvir': #UV Spectrum, Reflectance
                            individual_dict.update({'uvir_wavelength':data['oo']['uvir']['wavelength']})
                            individual_dict.update({'uvir_response':data['oo']['uvir']['response']})
                        elif item == 'oo_nirt': #NIR Spectrum, Transmittance
                            individual_dict.update({'nirt_wavelength':data['oo']['nirt']['wavelength']})
                            individual_dict.update({'nirt_response':data['oo']['nirt']['response']})
                        elif item == 'oo_nirr': #NIR Spectrum, Reflectance
                            individual_dict.update({'nirr_wavelength':data['oo']['nirr']['wavelength']})
                            individual_dict.update({'nirr_response':data['oo']['nirr']['response']})
                except KeyError: #That is, if data is unavailable for a position, pad with 'None'
                    individual_dict.update({item:None})
            sample_id = str(data['sample_id'])
            url = 'https://api.hpc.nrel.gov/xrd/api/samples/'+str(sample_id)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            for item in sample_level:
                try:
                    individual_dict.update({item:data[item]})
                except KeyError: #That is, if the data is unavailable for a position, pad with 'None'
                    individual_dict.update({item:None})
            position_format_return.update({position:individual_dict})
        return pd.DataFrame(position_format_return)
    else:
        samples_list = []
        for position in positions_list:
            url = 'https://api.hpc.nrel.gov/xrd/api/positions/'+str(position)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            samples_list.append(data['sample_id'])
        samples_list = set(samples_list)
        sample_level.append('position_ids')
        return samples_handle(samples_list,sample_level,position_level)

