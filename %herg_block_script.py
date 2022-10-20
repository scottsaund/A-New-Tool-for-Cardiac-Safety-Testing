# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 22:18:17 2022

@author: sandr
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 15:32:18 2022

@author: sandr
"""
import matplotlib.pyplot as plt
import myokit
import numpy as np
import os
import pandas as pd
import seaborn as sns


#m = get_model()

cwd = os.chdir('/Users/sandr/Dropbox/DISSERTATION/MYOKIT OUTPUT/ord-2011_NEWFIG/APD_DATA')


# PACING PROTOCOL

bcl = 1000
p = myokit.pacing.blocktrain(bcl, 0.5)

m.set_value("cell.mode", 1)

def doseresponse(x,MinY,MaxY,ic50s,hills):
    #function to calculate Y values of dose-response
    #Y values are % max response
    return MinY+(MaxY-MinY)/(1+(ic50s/x)**hills)

free_cmax_list = np.array([0.742,0.002,0.0003,0.009,0.035,0.98,0.012,0.008,0.0004,0.088,19.54,0.071,1378,0.003,0.0005,5.171,0.14])*1e-6 
hERG_hills =np.array([0.91,1.20,0.78,1.15,0.88,0.98,1.38,0.8,1.44,0.89,1,0.97,1,1.04,1.16,1,1.53])
hERG_ic50s = np.array([14.4,0.03,0.004,0.05,0.16,0.5,1.7,44,6.1,0.25,2054,2.3,3405.1,0.02,0.04,1433.9,0.018])*1e-6
cav_ic50s = np.array([1036.7,26.7,1.1,0.93,1,3.5,0.51,0.012,11.4,0.2,54.2,3.6,1226,11.8,0.24,299,62.5])*1e-6
cav_hills = [1,1,1.66,1.8,1.28,1.35,1.44,1.02,1.38,0.80,0.89,1,1,1,1.49,1.38,1.16]
drug_labels = ['Disopyramide','Dofetilde','Astemizole','Terfenadine','Bepridil','Thioridazine','Mibefradil','Nifedipine','Loratadine','Verapamil','Lamivudine','Clozapine','Piperacillin','Cisapride','Pimozide','Pentobarbital','Ibutilide']

cmax_multiple = [0.1,1,10,30]
data_list=[]
hergI=[]
cavI=[]
percentage_block=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

for ii in range(len(drug_labels)):
    drug_name=drug_labels[ii]
    free_cmax=free_cmax_list[ii]
    herg_ic50=hERG_ic50s[ii]
    cav_ic50=cav_ic50s[ii]
    herg_hill=hERG_hills[ii]
    cav_hill=cav_hills[ii]
    cmax_list=np.logspace(-1,2,6)*free_cmax
    herg_list=[doseresponse(i,0,1,herg_ic50,herg_hill) for i in cmax_list]      # herg_list = doseresponse func based on herg data for each array in cmax_list
    cav_list=[doseresponse(i,0,1,cav_ic50,cav_hill)for i in cmax_list]      # "cav data
    
    #PLOT DOSE RESPONSE AND SAVE TO DIRECTORY
    x=np.logspace(-7,-3,50)
    
    
    plt.figure(figsize=(7,6))
    plt.title(drug_name)
    for q in range(len(drug_name)):
        response_curve=doseresponse(x,0,1,herg_ic50,herg_hill)
        herg_inhib=[1-doseresponse(np.array(cmax_multiple),0,1,herg_ic50,herg_hill)for i in drug_name]
        cav_inhib=[1-doseresponse(np.array(cmax_multiple),0,1,cav_ic50,cav_hill)for i in drug_name]
        hergI.append(herg_inhib)
        cavI.append(cav_inhib)
        plt.plot(cmax_list[ii],herg_list[ii],label=drug_name)
        

    
        # OPEN EMPTY FIGURE BEFORE THE SIMULATION
        
        rocket_colors = sns.color_palette("rocket",3)
        plt.figure(figsize=(7,6))
        plt.title(drug_name)
        plt.xlabel('Time(ms)',fontsize=14)
        plt.ylabel('Membrane_Voltage(mV)',fontsize=14)
        plt.xlim=(1000)
        
        #   SIMULATION
             
        for i in range(len(herg_list)):
           
            s = myokit.Simulation(m, p)
            s.set_constant('ikr.Dens', 1-herg_list[i])
            s.set_constant('ical.Dens', 1-cav_list[i])
            s.set_constant('ina.Dens', 1.0)
            
            #PRE-PACE 1000 BEATS
            s.pre(bcl*100)
            #SHOW NEXT 1000ms
            d = s.run(1000)
    
            
            maxV=np.max(np.array(d['membrane.V']))  #maxV = max value of array generated from membrane.V simulation
            minV=np.min(np.array(d['membrane.V']))  #"minV
            APA=maxV-minV
            vAPD90=APA*0.1+minV
            vAPD30=APA*0.7+minV
            
            # find apd90 and 30
            for it in range(len(d['membrane.V'])):
            	if d['membrane.V'][it]>vAPD90:
            		APD90=d['engine.time'][it]    
            	if d['membrane.V'][it]>vAPD30:
            		APD30= d['engine.time'][it]
            run_result=[drug_name, cmax_list[i],APD30,APD90]
            
    
            
            
            print(run_result)
            
            # PACK DATA INTO CSV FILES
            data_list.append(run_result)              
            #np.savetxt('/Users/sandr/Dropbox/DISSERTATION/MYOKIT OUTPUT/ord-2011_NEWFIG/ord_'+drug_name+str(cmax_multiple[i])+'.csv', np.array([d['engine.time'],d['membrane.V']]))
            pd.DataFrame(data_list).to_csv("ord_2011_NEWFIG_cmax_APD30_APD90.csv")
            
            
            # Display the result
            plt.grid(True)
            plt.plot(d['engine.time'], d['membrane.V'], label= str(cmax_multiple[i])+" x cmax", color=rocket_colors[i%3])
            plt.minorticks_on()
            plt.tick_params(direction="in",which='minor',right=True,top=True)
            plt.tick_params(direction="in",which='major',right=True,top=True)
            plt.tick_params(labelsize=14)
            
        plt.legend()
        plt.show()
        plt.savefig("paci_"+ drug_name+'.png',dpi=300,bbow_inches="tight")
        
        plt.close()