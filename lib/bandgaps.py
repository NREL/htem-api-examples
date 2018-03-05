import numpy as np
from pyearth import Earth,export
import matplotlib.pyplot as plt
import re
import scipy.signal


def linregress(x,y):
    '''
    This function computes a basic linear regression when given x and y data.
    It returns the slope, intercept, R-squared value, and x_intercept.
    For further information on an alternative, see sklearn.linear_model.LinearRegression.
    '''
    if len(x) != len(y):
        print("Error: Lists must be the same size!")
        return
    x_squared=[]
    x_times_y=[]
    for i in range(0,len(x)):
        x_squared.append(float(x[i])**2)
        x_times_y.append(float(x[i])*float(y[i]))
    intercept=(sum(y)*sum(x_squared)-sum(x)*sum(x_times_y))/(len(x)*sum(x_squared)-sum(x)**2)
    slope=(len(x)*sum(x_times_y)-sum(x)*sum(y))/(len(x)*sum(x_squared)-sum(x)**2)
    y_mean=sum(y)/len(y)
    y_res = []
    y_tot = []
    for i in range(0,len(y)):
        modeled_pt = slope*x[i]+intercept
        y_res.append((modeled_pt-y_mean)**2)
        y_tot.append((y[i]-y_mean)**2)
    R_squared = sum(y_res)/sum(y_tot)
    x_intercept = -intercept/slope
    return slope, intercept, R_squared, x_intercept



def santosh_newhouse_gregoire_method(energy,absorption_coefficient,bg_type ='direct',show_graph=True):
    return 'This method has not yet been given permission to be used.'




def segmentation_method(energy,absorption_coefficient,bg_type ='direct',show_graph=True):
    direct_abs_corrected = absorption_coefficient
    t = []
    for k in direct_abs_corrected:
        t.append(k/(max(direct_abs_corrected)))

    direct_abs_corrected=t
    if show_graph == True:
        plt.figure()
        plt.scatter(energy,direct_abs_corrected)
    first_deriv = []
    energy_deriv = []
    for k in range(0,len(energy)-1):

        first_deriv.append((direct_abs_corrected[k+1]-direct_abs_corrected[k])/(energy[k+1]-energy[k]))
        energy_deriv.append(energy[k])
    first_deriv.append(first_deriv[-1])
    energy_deriv.append(energy[-1])
    first_deriv_savgol_filt = np.ndarray.tolist(scipy.signal.savgol_filter(first_deriv,25,4))

    energy_negats_elim = []
    first_deriv_negats_elim = []

    for k in range(0,len(first_deriv_savgol_filt)):
        if first_deriv_savgol_filt[k] > float(np.average(first_deriv_savgol_filt)):
            energy_negats_elim.append(energy[k])
            first_deriv_negats_elim.append(direct_abs_corrected[k])
    EA = []
    E = []
    for k in range(0,len(energy_negats_elim)):
        if energy_negats_elim[k] < np.average(energy_negats_elim)+2*np.std(energy_negats_elim):
            E.append(energy_negats_elim[k])
            EA.append(first_deriv_negats_elim[k])
    
    new_energy = E
    new_absorption_direct = EA
    spring_quotient = 1.0 #USE THIS TO ALTER THE NUMBER OF LINES SELECTED!
    try:
        position_linregress_vals_10_role = []
        s = range(0,len(new_energy),len(new_energy)/10)
        for k in range(0,len(s)-1):
            slope, intercept, R_squared, x_intercept=linregress(new_energy[s[k]:s[k+1]],new_absorption_direct[s[k]:s[k+1]])
            if slope < 0 or x_intercept < 0 or x_intercept > 10 or R_squared<.75:
                pass
            else:
                position_linregress_vals_10_role.append(tuple([s[k],s[k+1],slope,intercept,R_squared,x_intercept]))
        position_linregress_vals_10_role = sorted(position_linregress_vals_10_role,key=lambda item:item[2])
        for h in position_linregress_vals_10_role:
            if h[2]<float(position_linregress_vals_10_role[-1][2]/spring_quotient):
                position_linregress_vals_10_role.remove(h)
    except ValueError:
        position_linregress_vals_10_role = None


    try:
        position_linregress_vals_9_role = []
        r = range(0,len(new_energy),len(new_energy)/9)
        for k in range(0,len(r)-1):
            slope, intercept, R_squared, x_intercept=linregress(new_energy[r[k]:r[k+1]],new_absorption_direct[r[k]:r[k+1]])
            if slope < 0 or x_intercept < 0 or x_intercept > 10 or R_squared<.75:
                pass
            else:
                position_linregress_vals_9_role.append(tuple([r[k],r[k+1],slope,intercept,R_squared,x_intercept]))
        position_linregress_vals_9_role = sorted(position_linregress_vals_9_role,key=lambda item:item[2])
        for h in position_linregress_vals_9_role:
            if h[2]<float(position_linregress_vals_9_role[-1][2]/spring_quotient):
                position_linregress_vals_9_role.remove(h)
    except ValueError:
        position_linregress_vals_9_role = None


    try:
        position_linregress_vals_8_role = []
        r = range(0,len(new_energy),len(new_energy)/8)
        for k in range(0,len(r)-1):
            slope, intercept, R_squared, x_intercept=linregress(new_energy[r[k]:r[k+1]],new_absorption_direct[r[k]:r[k+1]])
            if slope < 0 or x_intercept < 0 or x_intercept > 10 or R_squared<.75:
                pass
            else:
                position_linregress_vals_8_role.append(tuple([r[k],r[k+1],slope,intercept,R_squared,x_intercept]))
        position_linregress_vals_8_role = sorted(position_linregress_vals_8_role,key=lambda item:item[2])
        for h in position_linregress_vals_8_role:
            if h[2]<float(position_linregress_vals_8_role[-1][2]/spring_quotient):
                position_linregress_vals_8_role.remove(h)
    except ValueError:
        position_linregress_vals_8_role = None

    try:
        position_linregress_vals_7_role = []
        t = range(0,len(new_energy),len(new_energy)/7)
        for k in range(0,len(t)-1):
            slope, intercept, R_squared, x_intercept=linregress(new_energy[t[k]:t[k+1]],new_absorption_direct[t[k]:t[k+1]])
            if slope < 0 or x_intercept < 0 or x_intercept > 10 or R_squared<.75:
                pass
            else:
                position_linregress_vals_7_role.append(tuple([t[k],t[k+1],slope,intercept,R_squared,x_intercept]))
        position_linregress_vals_7_role = sorted(position_linregress_vals_7_role,key=lambda item:item[2])
        for h in position_linregress_vals_7_role:
            if h[2]<float(position_linregress_vals_7_role[-1][2]/spring_quotient):
                position_linregress_vals_7_role.remove(h)
    except ValueError:
        position_linregress_vals_7_role = None

    try:
        position_linregress_vals_6_role = []
        t = range(0,len(new_energy),len(new_energy)/6)
        for k in range(0,len(t)-1):
            slope, intercept, R_squared, x_intercept=linregress(new_energy[t[k]:t[k+1]],new_absorption_direct[t[k]:t[k+1]])
            if slope < 0 or x_intercept < 0 or x_intercept > 10 or R_squared<.75:
                pass
            else:
                position_linregress_vals_6_role.append(tuple([t[k],t[k+1],slope,intercept,R_squared,x_intercept]))
        position_linregress_vals_6_role = sorted(position_linregress_vals_6_role,key=lambda item:item[2])
        for h in position_linregress_vals_6_role:
            if h[2]<float(position_linregress_vals_6_role[-1][2]/spring_quotient):
                position_linregress_vals_6_role.remove(h)
    except ValueError:
        position_linregress_vals_6_role = None

    try:
        position_linregress_vals_5_role = []
        t = range(0,len(new_energy),len(new_energy)/5)
        for k in range(0,len(t)-1):
            slope, intercept, R_squared, x_intercept=linregress(new_energy[t[k]:t[k+1]],new_absorption_direct[t[k]:t[k+1]])
            if slope < 0 or x_intercept < 0 or x_intercept > 10 or R_squared<.75:
                pass
            else:
                position_linregress_vals_5_role.append(tuple([t[k],t[k+1],slope,intercept,R_squared,x_intercept]))
        position_linregress_vals_5_role = sorted(position_linregress_vals_5_role,key=lambda item:item[2])
        for h in position_linregress_vals_5_role:
            if h[2]<float(position_linregress_vals_5_role[-1][2]/spring_quotient):
                position_linregress_vals_5_role.remove(h)
    except ValueError:
        position_linregress_vals_5_role = None

    try:
        band_gaps_list = [position_linregress_vals_5_role[-1][5],
                          position_linregress_vals_6_role[-1][5],
                          position_linregress_vals_7_role[-1][5],
                          position_linregress_vals_8_role[-1][5],
                          position_linregress_vals_9_role[-1][5],
                          position_linregress_vals_10_role[-1][5]]
        mean_band_gaps = np.mean(band_gaps_list)
        std_band_gaps = np.std(band_gaps_list)
        for h in band_gaps_list:
            if h > mean_band_gaps+2*std_band_gaps or h<mean_band_gaps-2*std_band_gaps:
                band_gaps_list.remove(h)
        mean_band_gaps = np.mean(band_gaps_list)
        std_band_gaps = np.std(band_gaps_list)
        x=np.linspace(min(new_energy),max(new_energy),num=1000)
        if show_graph == True:
            for h in [position_linregress_vals_5_role[-1]]:
                plt.scatter(x,x*h[2]+h[3],color='g',s=2)
            for h in [position_linregress_vals_6_role[-1]]:
                plt.scatter(x,x*h[2]+h[3],color='c',s=2)
            for h in [position_linregress_vals_7_role[-1]]:
                plt.scatter(x,x*h[2]+h[3],color='m',s=2)
            for h in [position_linregress_vals_8_role[-1]]:
                plt.scatter(x,x*h[2]+h[3],color='yellow',s=2)
            for h in [position_linregress_vals_9_role[-1]]:
                plt.scatter(x,x*h[2]+h[3],color='orange',s=2)
            for h in [position_linregress_vals_10_role[-1]]:
                plt.scatter(x,x*h[2]+h[3],color='r',s=2)
            if bg_type == 'direct':
                plt.title('Tauc Plot for Direct Transitions',fontsize=20)
            elif bg_type == 'indirect':
                plt.title('Tauc Plot for Indirect Transitions',fontsize=20)
            elif bg_type == 'log10':
                plt.title('Tauc Plot for LOG10 Transitions',fontsize=20)
            else:
                plt.title('Tauc Plot for Raw Alpha Transitions',fontsize=20)
            plt.xlabel('Energy (eV)',fontsize=14)
            plt.ylabel('(E'+u"\u03B1"+')'+u"\u00B2",fontsize=14)
            plt.xticks(fontsize=14)
            plt.yticks(fontsize=14)
            plt.axis([min(energy),max(energy),0,1])
            plt.show()
        return mean_band_gaps
    except (ValueError, IndexError):
        print("Empty Sequence!")
        return







def mars_method(energy,absorption_coefficient,bg_type ='direct',show_graph=True):
    direct_abs_corrected = absorption_coefficient
    t = []
    for k in direct_abs_corrected:
        t.append(k/(max(direct_abs_corrected)))
    direct_abs_corrected=t
    
    model = Earth()
    try:
        model.fit(np.array(energy), np.array(direct_abs_corrected))
    except ValueError:
        return 'Problem in MARS fitting parameters!'
    
    energy_elbows = []
    energy_elbows.append(min(energy))
    energy_elbows.append(max(energy))
    for coeff in list(model.basis_)[1:]:
        try:
            if float(re.findall("\d+\.\d+", str(coeff))[0]) not in energy_elbows:
                energy_elbows.append(float(re.findall("\d+\.\d+", str(coeff))[0]))
        except IndexError:
            print(coeff)
            pass
    
    y_hat = model.predict(energy)
    if show_graph == True:
        plt.figure()
        plt.scatter(energy,direct_abs_corrected,color='k')
        plt.plot(energy,y_hat,'b.')
        plt.xlabel('Energy (eV)',fontsize=14)
        plt.ylabel('(E'+u"\u03B1"+')'+u"\u00B2",fontsize=14)
        if bg_type == 'direct':
            plt.title('Tauc Plot for Direct Transitions',fontsize=20)
        elif bg_type == 'indirect':
            plt.title('Tauc Plot for Indirect Transitions',fontsize=20)
        elif bg_type == 'log10':
            plt.title('Tauc Plot for LOG10 Transitions',fontsize=20)
        else:
            plt.title('Tauc Plot for Raw Alpha Transitions',fontsize=20)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
    function = export.export_sympy(model)

    direct_abs_elbows = []
    for coeff in energy_elbows:
        direct_abs_elbows.append(function.evalf(subs={'x0':coeff}))
    elbows_list = []
    for elbow_num in range(0,len(energy_elbows)):
        elbows_list.append(tuple([energy_elbows[elbow_num],direct_abs_elbows[elbow_num]]))
    elbows_list = sorted(elbows_list)
    
    line_segs = []
    for point in range(0,len(elbows_list)-1):
        que = []
        for w in energy:
            if w>elbows_list[point][0] and w<elbows_list[point+1][0]:
                que.append(w)
        num_pts = len(que)
        x_length = elbows_list[point+1][0]-elbows_list[point][0]
        length = ((elbows_list[point+1][0]-elbows_list[point][0])**2\
        +(elbows_list[point+1][1]-elbows_list[point][1])**2)**.5
        slope = (elbows_list[point+1][1]-elbows_list[point][1])/(elbows_list[point+1][0]-elbows_list[point][0])
        y_intercept = elbows_list[point+1][1]-slope*elbows_list[point+1][0]
        x_intercept = (-1*y_intercept) / slope
        weighting_factor = slope**2 * x_length*2 * abs(length)**.5 * num_pts
        try:
            if x_intercept > 0 and slope > 0 and num_pts>10:
                line_segs.append(tuple([x_length,length,slope,y_intercept,x_intercept,weighting_factor]))
        except TypeError:
            print('Weird complex zoo error..')
            pass

    line_segs = sorted(line_segs,key=lambda item:item[5])
#            print(line_segs)
    winner = max(line_segs,key=lambda item:item[5])
   
    adj_energy=np.linspace(min(energy),max(energy),num=1000)
    adj_winner = []
    for t in adj_energy:
        adj_winner.append(t*float(winner[2])+float(winner[3]))
    if show_graph == True:
        plt.scatter(adj_energy,adj_winner,color='r')
        plt.axis([min(energy),max(energy),0,1])
        plt.show()
    return winner[4]
