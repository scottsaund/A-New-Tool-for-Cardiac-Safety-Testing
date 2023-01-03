import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

path = os.chdir("/Users/Scott/Dropbox/DISSERTATION/DRUG_DOSE_RESP_DATA/smaller")

#PROVIDE INPUT DATA

x=np.logspace(-7,-3,6)
cmax_list = np.array([0.742,0.002,0.0003,0.009,0.035,0.98,0.012,0.008,0.0004,0.088,19.54,0.071,1378,0.003,0.0005,5.171,0.14])*1e-6 
hERG_hills =np.array([0.91,1.20,0.78,1.15,0.88,0.98,1.38,0.8,1.44,0.89,1,0.97,1,1.04,1.16,1,1.53])
hERG_ic50s = np.array([14.4,0.03,0.004,0.05,0.16,0.5,1.7,44,6.1,0.25,2054,2.3,3405.1,0.02,0.04,1433.9,0.018])*1e-6
cav_ic50s = np.array([1036.7,26.7,1.1,0.93,1,3.5,0.51,0.012,11.4,0.2,54.2,3.6,1226,11.8,0.24,299,62.5])*1e-6
cav_hills = [1,1,1.66,1.8,1.28,1.35,1.44,1.02,1.38,0.80,0.89,1,1,1,1.49,1.38,1.16]
drug_labels = ['Disopyramide','Dofetilde','Astemizole','Terfenadine','Bepridil','Thioridazine','Mibefradil','Nifedipine','Loratadine','Verapamil','Lamivudine','Clozapine','Piperacillin','Cisapride','Pimozide','Pentobarbital','Ibutilide']

hERGL= [] # array 
cavL= []  # "
CMAX_L = [0.1,0.3,1,3,10,30]


# hERG DOSE RESPONSE

def doseresponse(x,MinY,MaxY,hERG_ic50s,hERG_hills):
    #function to calculate Y values of dose-response
    #Y values are % max response
    return MinY+(MaxY-MinY)/(1+(hERG_ic50s/x)**hERG_hills)

# cav DOSE RESPONSE

def doseresponse(x,MinY,MaxY,cav_ic50s,cav_hills):
    #function to calculate Y values of dose-response
    #Y values are % max response
    return MinY+(MaxY-MinY)/(1+(cav_ic50s/x)**cav_hills)


for i in range(len(drug_labels)):
    response_curve = doseresponse(x,0,1,hERG_ic50s[i],hERG_hills[i])
    cmax=cmax_list[i]
    drug_conc=[0.1*cmax,0.3*cmax,cmax,3*cmax,10*cmax,30*cmax]
    hERG_inhibition=1-doseresponse(np.array(drug_conc),0,1,hERG_ic50s[i],hERG_hills[i])
    hERGL.append(hERG_inhibition)
    response_curve = doseresponse(x,0,1,cav_ic50s[i],cav_hills[i])
    cmax=cmax_list[i]
    drug_conc=[0.1*cmax,0.3*cmax,cmax,3*cmax,10*cmax,30*cmax]
    cav_inhibition=1-doseresponse(np.array(drug_conc),0,1,cav_ic50s[i],cav_hills[i])
    cavL.append(cav_inhibition)
    
    # SAVE DATA TO CSV
    
    #df=pd.DataFrame({"herg_inhib": hERGL, "cav_inhib": cavL})
    #df.to_csv("%_channel_block.csv", index=False)

    # PLOT
    
    plt.plot(CMAX_L,
             hERG_inhibition,
             marker="^",
             label = "hERG")
    plt.title(drug_labels[i],fontsize=20)
    
    plt.xlabel('log_Drug_Concentration(*cmax)',fontsize=18)
    plt.ylabel('Response(%_Max)',fontsize=18)
    plt.xscale('log')
    plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    plt.xticks(CMAX_L)
    
    plt.plot(CMAX_L,
             cav_inhibition,
             marker="o",
             label = "cav")
    plt.minorticks_on()
    plt.tick_params(direction="in",which="major",right=True,top=True)
    plt.tick_params(direction="in",which="minor",right=True,top=True)
    plt.tick_params(labelsize=14)
    plt.legend()
    plt.show() 
    
    plt.savefig(drug_labels[i]+'.png', dpi=300)
    print(hERGL)
