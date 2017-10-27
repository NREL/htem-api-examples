# Written by Marcus Schwarting in collaboration with the National Renewable
# Energy Laboratories. For further information please see the website 
# https://htem.nrel.gov/ as well as the recent publication on this work,
# [insert reference to upcoming paper here]. The goal of this project is to
# further the objectives laid out in the strategic objectives for the
# Materials Genome Initiative.
# 
# For further information on this code project, please email:
# Marcus Schwarting ==> marcus.schwarting@nrel.gov

#API SAMPLE(S) SPECIFIC!

import urllib, json
import pandas as pd

class Library:
    def __init__(self,identity):
        self.identity = identity

    def search_by_ids(self,ids_list):
        #I think it might be easier for one to just iterate over the positions in the sample.py,
        #was this function supposed to query over POSITIONS or SAMPLES? Come back later...
        t = []
        for i in ids_list:
            url = 'https://htem-api.nrel.gov/api/positions/'+str(i)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            df = pd.DataFrame()
            for i in data:
                df[i] = [data[i]]
            t.append(df)
        return t

    def search_by_composition(self,only=[],not_including=[],any_of=[]):
        url = 'https://htem-api.nrel.gov/api/samples/'+str(self.identity)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        positions = data['position_ids'] #Should the samples level also be queried for "elements"?
        df = pd.DataFrame()
        for k in positions:
            url = 'https://htem-api.nrel.gov/api/positions/'+str(k)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            leveled_position = data['position']
            positions_elements_list = list(data['xrf_elements'])
            if len(set(positions_elements_list).intersection(not_including)) != 0:
                df['elements_'+str(leveled_position)] = [False]
                continue
            if len(set(positions_elements_list).intersection(only)) == len(only):
                df['elements_'+str(leveled_position)] = [True]
                continue
            if len(set(positions_elements_list).intersection(only)) != 0:
                df['elements_'+str(leveled_position)] = [True]
                continue
            else:
                df['elements_'+str(leveled_position)] = [False]
        return df
            
    def properties(self):
        url = 'https://htem-api.nrel.gov/api/samples/'+str(self.identity)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        df = pd.DataFrame()
        for i in data:
            df[i] = [data[i]]
        return df

    def spectra(self,which):
        url = 'https://htem-api.nrel.gov/api/samples/'+str(self.identity)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        positions = data['position_ids']
        df = pd.DataFrame()
        for k in positions:
            url = 'https://htem-api.nrel.gov/api/positions/'+str(k)
            #There is the potential to replace this with mvl_optical or mvl_xrd, 
            #but these seem to be broken at the moment...
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            leveled_position = data['position']
            if which == 'xrd':
                df['xrd_angle_'+str(leveled_position)] = data['xrd_angle']
                df['xrd_background_'+str(leveled_position)] = data['xrd_background']
                df['xrd_intensity_'+str(leveled_position)] = data['xrd_intensity']
            elif which == 'optical':
                try:
                    df['uvit_wave_'+str(leveled_position)] = data['oo']['uvit']['wavelength']
                    df['uvit_response_'+str(leveled_position)] = data['oo']['uvit']['response']
                except KeyError: #No uvit available
                    pass
                try:
                    df['uvir_wave_'+str(leveled_position)] = data['oo']['uvir']['wavelength']
                    df['uvir_response_'+str(leveled_position)] = data['oo']['uvir']['response']
                except KeyError: #No uvir available
                    pass
                try:
                    df['nirt_wave_'+str(leveled_position)] = data['oo']['nirt']['wavelength']
                    df['nirt_response_'+str(leveled_position)] = data['oo']['nirt']['response']
                except KeyError: #No nirt available
                    pass
                try:
                    df['nirr_wave_'+str(leveled_position)] = data['oo']['nirr']['wavelength']
                    df['nirr_response_'+str(leveled_position)] = data['oo']['nirr']['response']
                except KeyError: #No nirr available
                    pass
            else:
                pass
        return df
