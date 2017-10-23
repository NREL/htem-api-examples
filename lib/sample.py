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
    
    def __init__(self,ID,which):
        self.ID = ID
        self.which = which
        
    def properties(self):
        url = 'https://api.hpc.nrel.gov/xrd/api/positions/'+str(self.ID)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        df = pd.DataFrame()
        ### POPULATE PANDAS df USING DATA FROM THE URL ABOVE!!!    
        return df
    
    def spectra(self):
        url = 'https://api.hpc.nrel.gov/xrd/api/positions/'+str(self.ID)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        df = pd.DataFrame()
        if self.which == 'xrd':
            df['xrd_angle'] = data['xrd_angle']
            df['xrd_background'] = data['xrd_background']
            df['xrd_intensity'] = data['xrd_intensity']
        elif self.which == 'optical':
            try:
                df['uvit_wave'] = data['oo']['uvit']['wavelength']
                df['uvit_response'] = data['oo']['uvit']['response']
            except KeyError: #No uvit available
                pass
            try:
                df['uvir_wave'] = data['oo']['uvir']['wavelength']
                df['uvir_response'] = data['oo']['uvir']['response']
            except KeyError: #No uvir available
                pass
            try:
                df['nirt_wave'] = data['oo']['nirt']['wavelength']
                df['nirt_response'] = data['oo']['nirt']['response']
            except KeyError: #No nirt available
                pass
            try:
                df['nirr_wave'] = data['oo']['nirr']['wavelength']
                df['nirr_response'] = data['oo']['nirr']['response']
            except KeyError: #No nirr available
                pass

        return df


test = Sample(367780, 'optical')
df = test.spectra()
print(df)