# Written by Marcus Schwarting in collaboration with the National Renewable
# Energy Laboratories. For further information please see the website 
# https://htem.nrel.gov/ as well as the recent publication on this work,
# [insert reference to upcoming paper here]. The goal of this project is to
# further the objectives laid out in the strategic objectives for the
# Materials Genome Initiative.
# 
# For further information on this code project, please email:
# Marcus Schwarting ==> marcus.schwarting@nrel.gov

#API POSITION(S) SPECIFIC!
import urllib, json
import pandas as pd

class Sample:
    
    def __init__(self,identity):
        self.identity = identity
        
    @staticmethod
    def search_by_ids(ids_list):
        obj_list = []
        for i in ids_list:
            obj_list.append(Sample(i))
        return obj_list

    def properties(self):
        url = 'https://htem-api.nrel.gov/api/sample/'+str(self.identity)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        df = pd.DataFrame()
        for i in data:
            df[i] = [data[i]]
        return df
            
    def spectra(self,which):
        url = 'https://htem-api.nrel.gov/api/sample/'+str(self.identity)
        #There is the potential to replace this with mvl_optical or mvl_xrd, 
        #but these seem to be broken at the moment...
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        df = pd.DataFrame()
        if which == 'xrd':
            df['xrd_angle'] = data['xrd_angle']
            df['xrd_background'] = data['xrd_background']
            df['xrd_intensity'] = data['xrd_intensity']
        elif which == 'optical':
            uvit_df = pd.DataFrame()
            try:
                uvit_df['uvit_wave'] = data['oo']['uvit']['wavelength']
                uvit_df['uvit_response'] = data['oo']['uvit']['response']
            except KeyError: #No uvit available
                pass
            uvir_df = pd.DataFrame()
            try:
                uvir_df['uvir_wave'] = data['oo']['uvir']['wavelength']
                uvir_df['uvir_response'] = data['oo']['uvir']['response']
            except KeyError: #No uvir available
                pass
            nirt_df = pd.DataFrame()
            try:
                nirt_df['nirt_wave'] = data['oo']['nirt']['wavelength']
                nirt_df['nirt_response'] = data['oo']['nirt']['response']
            except KeyError: #No nirt available
                pass
            nirr_df = pd.DataFrame()
            try:
                nirr_df['nirr_wave'] = data['oo']['nirr']['wavelength']
                nirr_df['nirr_response'] = data['oo']['nirr']['response']
            except KeyError: #No nirr available
                pass
            df = pd.concat([uvit_df,uvir_df,nirt_df,nirr_df],axis=1)
        else:
            df = pd.DataFrame()
        return df