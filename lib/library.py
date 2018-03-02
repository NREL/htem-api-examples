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

    @staticmethod
    def search_by_ids(ids_list):
        obj_list = []
        for i in ids_list:
            obj_list.append(Library(i))
        return obj_list

    @staticmethod
    def search_by_composition(only=[],not_including=[],any_of=[]):
        elt_url = 'https://htem-api.nrel.gov/api/sample_library?element='
        for i in only:
            elt_url = elt_url+str(i)+','
        response = urllib.urlopen(elt_url)
        data = json.loads(response.read())
        ids_list = []
        for i in data:
            elts = str(i['elements'])
            violated = False
            for k in not_including:
                if k in elts:
                    violated = True
            l = 0
            for k in only:
                if k in elts:
                    l = l+1
            if l == len(only) and violated == False:
                ids_list.append(i['id'])
            else:
                pass
        obj_list = []
        for i in ids_list:
            obj_list.append(Library(i))
        return obj_list

            
    def properties(self):
        url = 'https://htem-api.nrel.gov/api/sample_library/'+str(self.identity)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        df = pd.DataFrame()
        for i in data:
            df[i] = [data[i]]
        return df

    def spectra(self,which):
        url = 'https://htem-api.nrel.gov/api/sample_library/'+str(self.identity)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        positions = data['sample_ids']
        df = pd.DataFrame()
        for k in positions:
            url = 'https://htem-api.nrel.gov/api/sample/'+str(k)
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
                pos_df = pd.DataFrame()
                uvit_df = pd.DataFrame()
                try:
                    uvit_df['uvit_wave_'+str(leveled_position)] = data['oo']['uvit']['wavelength']
                    uvit_df['uvit_response_'+str(leveled_position)] = data['oo']['uvit']['response']
                except KeyError: #No uvit available
                    pass
                uvir_df = pd.DataFrame()
                try:
                    uvir_df['uvir_wave_'+str(leveled_position)] = data['oo']['uvir']['wavelength']
                    uvir_df['uvir_response_'+str(leveled_position)] = data['oo']['uvir']['response']
                except KeyError: #No uvir available
                    pass
                nirt_df = pd.DataFrame()
                try:
                    nirt_df['nirt_wave_'+str(leveled_position)] = data['oo']['nirt']['wavelength']
                    nirt_df['nirt_response_'+str(leveled_position)] = data['oo']['nirt']['response']
                except KeyError: #No nirt available
                    pass
                nirr_df = pd.DataFrame()
                try:
                    nirr_df['nirr_wave_'+str(leveled_position)] = data['oo']['nirr']['wavelength']
                    nirr_df['nirr_response_'+str(leveled_position)] = data['oo']['nirr']['response']
                except KeyError: #No nirr available
                    pass
                pos_df = pd.concat([uvit_df,uvir_df,nirt_df,nirr_df],axis=1)
                df = pd.concat([df,pos_df],axis=1)
            else:
                df = pd.DataFrame()
        return df