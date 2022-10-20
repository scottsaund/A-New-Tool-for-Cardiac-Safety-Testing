# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:26:37 2022

@author: sandr
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

#wd = os.chdir('/Users/sandr/Dropbox/DISSERTATION/MYOKIT OUTPUT/%_BLOCK_FIGS')

def per_block(i,base,negative,x):
    return((i/base)-negative) *x


drug_name = ["Astemizole","Nifedipine","Ibutilide","Piperacillin","Dofetilide","Disopyramide","Mibefradil","Verapamil","Cisapride"]
ord_90 =np.array([[0.27163323, 0.28539987, 0.31772858, 0.40795432, 0.57446342],[0.27163323, 0.25149501, 0.21729733, 0.19779526, 0.18989657],[0.27163323, 0.6907817 , 1, 0.83073003, 0.8588833],[0.27163323, 0.27557298, 0.34806866, 0.50477395, 0.58961515],[0.27163323, 0.27498236, 0.29545408, 0.40686111, 0.69396748],[0.27163323, 0.27741639, 0.29991062, 0.38089941, 0.5562974 ],[0.27163323, 0.27064296, 0.27098046, 0.26485236, 0.28814028],[0.27163323, 0.2883635 , 0.3539407 , 0.49872347, 0.59632317],[0.27163323, 0.28384397, 0.33489654, 0.49678516, 0.50829297]])
ord_30 =np.array([[0.16956446, 0.17498706, 0.19367066, 0.22728254, 0.26682146],[0.16956446, 0.15132766, 0.11626826, 0.08315366, 0.07052769],[0.16956446, 0.2723829 , 0.28646691, 0.07750203, 0.07671139],[0.16956446, 0.15941909, 0.17166422, 0.19668607, 0.19357324],[0.16956446, 0.17191768, 0.18088099, 0.23025401, 0.27158295],[0.16956446, 0.17327888, 0.18387805, 0.22018402, 0.26297701],[0.16956446, 0.16998504, 0.16828963, 0.15954043, 0.14425456],[0.16956446, 0.17140879, 0.18957533, 0.21832495, 0.22380403],[0.16956446, 0.17526191, 0.19998682, 0.2536845 , 0.18889299]])
paci_90 =np.array([[0.435457339,0.457035981,0.50722613,0.64209474,0.890497102],[0.435457339,0.331256048,0.220719443,0.160115913,0.146116825],[0.435457339,0.284657491,0.604528529,1,1],[0.435457339,0.328245764,0.249444664,0.19684951,0.18415127],[0.435457339,0.439579765,0.471888308,0.639543246,1],[0.435457339,0.4457625,0.480786463,0.601233584,0.840269952],[0.435457339,0.435542245,0.427829134,0.360365428,0.231100031],[0.435457339,0.386448263,0.346748654,0.254557628,0.201205084],[0.435457339,0.454118802,0.530204229,0.761147238,0.389780796]])
paci_30 =np.array([[0.221566959,0.236639735,0.270462255,0.366486834,0.471698079],[0.221566959,0.14111078,0.066240407,0.043473622,0.037192029],[0.221566959,0.153017323,0.267804563,0.705918704,0.683116757],[0.221566959,0.132030615,0.06659752,0.046643891,0.042836445],[0.221566959,0.225012756,0.237412796,0.361646921,0.53348834],[0.221566959,0.228048837,0.251901769,0.336919591,0.550919604],[0.221566959,0.221231027,0.211156482,0.15899124,0.063263059],[0.221566959,0.173483562,0.118112516,0.063312488,0.047829629],[0.221566959,0.228689687,0.290547819,0.474507045,0.183205749]])

data = []
# Slice out index 0 from each array (remove baseline)
ord_90=ord_90[:,1:]
ord_30=ord_30[:,1:]
paci_90=paci_90[:,1:]
paci_30=paci_30[:,1:]


for i in range(len(drug_name)):
    label = drug_name[i]
    o9 = per_block(ord_90, 0.271, 1, 100)
    o3 = per_block(ord_30, 0.169, 1, 100)
    p9 = per_block(paci_90, 0.435, 1, 100)
    p3 = per_block(paci_30, 0.222, 1, 100)
    
    for j in range(len())
    o910 = o9[2]
    
    print(o910)
    
    result=[label,o9[i],o3[i],p9[i],p3[i]]
    data.append(result)
    #pd.DataFrame(data).to_csv("%Block.csv")
        

    plt.figure(figsize=(7,6))
    plt.title(label)
    plt.plot(o9[i],
         marker="^",
         color="purple",
         label="ord-2011")
    plt.plot(p9[i],
         marker="s",
         color = "orange",
         label="paci-2013")
    plt.semilogx()
    plt.ylabel("$\Delta$""APD90")
    plt.xlabel("Conc(M)")
    plt.legend()
    plt.show()
    plt.savefig("deltaAPD90_"+ label+'.png',dpi=300,bbow_inches="tight")
    plt.close()


    plt.figure(figsize=(7,6))
    plt.title(label)
    plt.plot(o3[i],
             marker="^",
             color="purple",
             label="ord-2011")
    plt.plot(p3[i],
             marker="s",
             color = "orange",
             label="paci-2013")
    plt.semilogx()
    plt.ylabel("$\Delta$""APD30")
    plt.xlabel("Conc(M)")
    plt.legend()
    plt.show()
    plt.savefig("deltaAPD30_"+ label+'.png',dpi=300,bbow_inches="tight")
    plt.close()
    
    #herg and cav inhib gradient
    plt.figure(figsize=(7,6))   
    plt.title(drug_name[i])
    plt.plot(o9[i],p9[i],label='APD90',marker="^",color="black")
    plt.plot(o3[i],p3[i],label='APD30',marker="s",color="red")
    
    plt.xlabel("ord-2011")
    plt.ylabel("paci-2013")
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.savefig("%_inhib_gradient_"+ label+'.png',dpi=300,bbow_inches="tight")
    plt.close()
  
