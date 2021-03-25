import numpy as np
import pandas as pd
import streamlit as st
import altair as alt


df=pd.read_excel('Base_sondage_maraichage.xlsx',
                 index_col="Identifiant",na_values=['NA'])
df = df.fillna({"Mode_irrigation": "Pluvial"})

cleanup_nums = {

"Mode_Production":     {"Principale": 1, "En succession": 2, 
                                        "En association": 3, "Sous étage": 4},
    
"Mode_irrigation": {"Localisée": 1, "Gravitaire": 2, "Aspersion": 3,
                                    "Pivot": 4,
                                  "Gravitaire,Localisée": 5, "Localisée,Pivot": 6, "Pluvial":7},
    
"Culture": {"Courgette": 1, "Pomme de terre": 2, "Tomate": 3,
                                    "Coriandre et persil": 4,
                                  "Haricot vert": 5, "Concombre": 6,
           "Menthe": 7, "Fève vert": 8, "Aubergine": 9,
                                    "Carotte": 10,
                                  "Chou fleur": 11, "Oignon":12, "Choux vert":13, "Celeri": 14,
            "Laitue": 15, "Tomate kiwat": 16, "Fraise": 17,
                                    "Piment fort": 18,
                                  "Artichaut": 19, "Absinthe": 20,
            "Haricot Helda": 21, "Topinambour": 22, "Myrtille": 23,
                                    "Endive": 24,
                                  "Navet": 25, "Pastèque":26, "Poivron": 27},
    
"Irrigation":     {"Non": 0, "Oui": 1},    
    
"Serre":     {"Non": 1, "Petit tunel": 2, 
                                        "Grand tunel": 3, "Canarienne": 4,
             "Multi-chapelle": 5},
        
}

df_cleaned= df.replace(cleanup_nums)

st.title('Etude Maraîchère')


st.write("""
Dans le cadre de mon stage au sein du Ministère de l'Agriculture, de la Pêche Maritime, du Développement Rural et des Eaux 
et Forêts - **Direction de la stratégie et des statistiques**, j’ai eu l’occasion de travailler sur une base de données 
réelle sous la direction du Chef de Services, des Enquêtes et Recensements **Mr MESTARI Soufiane**
""")

st.dataframe(df)




def SAU(i):
    grouped_df_by_culture = df[df.Culture.str.contains(i)]
    Somme = np.sum(grouped_df_by_culture.Superficie_Champ)
    return Somme

def SAU_V():
    V=[]
    for i in df.Culture.value_counts().index:
        V.append(SAU(i))
    return V

SAU_par_Culture = pd.DataFrame({"Culture":df.Culture.value_counts().index,"SAU":SAU_V(),
                                "% SAU": np.round((SAU_V()/np.sum(SAU_V()))*100,2) })

SAU_par_Culture['% SAU'] = SAU_par_Culture['% SAU'].astype(str) + '%'


st.header('Population')


select_box_1 = st.selectbox('', ["Mode Production","Mode irrigation","Culture","Irrigation","Serre",
                                       "Superficie Champ","SAU par culture"])



if select_box_1 == "Culture":
    chart = alt.Chart(df).mark_bar().encode(
    alt.X("count()", bin=False),
    y='Culture',color='Culture').properties(width=700, height=500)
    st.altair_chart(chart)
    
elif select_box_1 == "Mode Production":
    chart = alt.Chart(df).mark_bar().encode(
    alt.X("count()", bin=False),
    y='Mode_Production',color='Mode_Production').properties(width=700, height=200)
    st.altair_chart(chart)

elif select_box_1 == "Mode irrigation":
    chart = alt.Chart(df).mark_bar().encode(
    alt.X("count()", bin=False),
    y='Mode_irrigation',color='Mode_irrigation').properties(width=700, height=250)
    st.altair_chart(chart)

elif select_box_1 == "Irrigation":
    chart = alt.Chart(df).mark_bar().encode(
    alt.X("count()", bin=False),
    y='Irrigation',color='Irrigation').properties(width=700, height=150)
    st.altair_chart(chart)

elif select_box_1 == "Serre":
    chart = alt.Chart(df).mark_bar().encode(
    alt.X("count()", bin=False),
    y='Serre',color='Serre').properties(width=700, height=200)
    st.altair_chart(chart)

elif select_box_1 == "Superficie Champ":
    chart = alt.Chart(df).transform_density(
    'Superficie_Champ',
    as_=['Superficie_Champ', 'density'],).mark_area().encode(
    x="Superficie_Champ:Q",
    y='density:Q',).properties(width=650, height=300)
    st.altair_chart(chart)

elif select_box_1 == "SAU par culture":
    chart = alt.Chart(SAU_par_Culture).mark_bar().encode(
    alt.X("SAU", bin=False),
    y='Culture',color='Culture')

    text = chart.mark_text(
    align='left',
    baseline='middle',
    dx=3 ).encode(
    text="% SAU")
    st.altair_chart((chart + text).properties(width=700, height=500))


st.header('Echantillonnage et Inférence')


select_box_2 = st.selectbox('', ["Echantillonnage aléatoire simple","Echantillonnage systématique",
                                       "Echantillonnage double","Echantillonnage à probabilités inégales",
                                       "Echantillonnage stratifié"])

select_box_3 = st.selectbox('', ["Mode irrigation","Mode Production","Culture","Irrigation",
                                 "Serre", "Superficie Champ", "SAU par culture"]) 




##################### Echantillonnage aléatoire simple ##################################

# import random
# seq=list(range(1,606,1))
# V1=sorted(random.sample(seq, 200))
# print("Random sample, n = 200:", V1)


V1 = [5, 6, 9, 10, 11, 12, 15, 16, 19, 20, 21, 23, 24, 27, 38, 40, 42, 46, 53, 56, 58, 59, 63, 64, 71, 72, 
      73, 81, 85, 89, 90, 92, 94, 95, 96, 98, 101, 102, 106, 110, 111, 112, 113, 115, 128, 129, 130, 131,
      132, 133, 142, 145, 148, 149, 151, 155, 161, 165, 166, 167, 168, 170, 172, 173, 175, 179, 182, 184, 185, 
      186, 192, 194, 195, 196, 199, 200, 201, 207, 208, 209, 211, 212, 215, 219, 220, 228, 230, 232, 233, 236, 
      243, 254, 256, 259, 261, 270, 275, 277, 279, 280, 281, 283, 285, 291, 293, 306, 307, 311, 318, 319, 321, 
      327, 332, 333, 336, 337, 340, 346, 347, 359, 362, 371, 377, 378, 383, 384, 386, 387, 388, 390, 392, 396, 
      398, 399, 400, 404, 405, 407, 408, 416, 417, 420, 423, 432, 434, 437, 439, 440, 442, 443, 450, 453, 458, 
      464, 465, 468, 472, 477, 478, 479, 484, 487, 488, 493, 494, 497, 502, 506, 507, 511, 517, 529, 530, 536, 
      540, 542, 544, 546, 547, 548, 549, 554, 555, 561, 564, 569, 571, 573, 574, 577, 578, 581, 583, 586, 593,
      599, 600, 601, 603, 605]

df_EAS=df.iloc[V1]


def SAU_EAS(i):
    grouped_df_by_culture = df_EAS[df_EAS.Culture.str.contains(i)]
    Somme = np.sum(grouped_df_by_culture.Superficie_Champ)
    return Somme

def SAU_V_EAS():
    V=[]
    for i in df_EAS.Culture.value_counts().index:
        V.append(SAU_EAS(i))
    return V

SAU_par_Culture_EAS = pd.DataFrame({"Culture":df_EAS.Culture.value_counts().index,"SAU":SAU_V_EAS(),
                                "% SAU": np.round((SAU_V_EAS()/np.sum(SAU_V_EAS()))*100,2) })

SAU_par_Culture_EAS['% SAU'] = SAU_par_Culture_EAS['% SAU'].astype(str) + '%'

if select_box_2 == "Echantillonnage aléatoire simple":
    
    if select_box_3 == "Culture":
        chart = alt.Chart(df_EAS).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Culture',color='Culture').properties(width=700, height=500)
        st.altair_chart(chart)
    
    elif select_box_3 == "Mode Production":
        chart = alt.Chart(df_EAS).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Mode_Production',color='Mode_Production').properties(width=700, height=200)
        st.altair_chart(chart)

    elif select_box_3 == "Mode irrigation":
        chart = alt.Chart(df_EAS).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Mode_irrigation',color='Mode_irrigation').properties(width=700, height=250)
        st.altair_chart(chart)
    
    elif select_box_3 == "Irrigation":
        chart = alt.Chart(df_EAS).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Irrigation',color='Irrigation').properties(width=700, height=150)
        st.altair_chart(chart)
    
    elif select_box_3 == "Serre":
        chart = alt.Chart(df_EAS).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Serre',color='Serre').properties(width=700, height=200)
        st.altair_chart(chart)
    
    elif select_box_3 == "Superficie Champ":
        chart = alt.Chart(df_EAS).transform_density(
        'Superficie_Champ',
        as_=['Superficie_Champ', 'density'],).mark_area().encode(
        x="Superficie_Champ:Q",
        y='density:Q',).properties(width=650, height=300)
        st.altair_chart(chart)
    
    elif select_box_3 == "SAU par culture":
        chart = alt.Chart(SAU_par_Culture_EAS).mark_bar().encode(
        alt.X("SAU", bin=False),
        y='Culture',color='Culture')
    
        text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3 ).encode(
        text="% SAU")
        st.altair_chart((chart + text).properties(width=700, height=500))
        
        
        
##################### Echantillonnage systématique ##################################

def systematic_sampling(df, step):
    
    indexes = np.arange(0,len(df),step=step)
    systematic_sample = df.iloc[indexes]
    return systematic_sample
    
df_ES=systematic_sampling(df, 3)
df_ES=df_ES.iloc[1:]
df_ES=df_ES.iloc[:200]


def SAU_ES(i):
    grouped_df_by_culture = df_ES[df_ES.Culture.str.contains(i)]
    Somme = np.sum(grouped_df_by_culture.Superficie_Champ)
    return Somme

def SAU_V_ES():
    V=[]
    for i in df_ES.Culture.value_counts().index:
        V.append(SAU_ES(i))
    return V

SAU_par_Culture_ES = pd.DataFrame({"Culture":df_ES.Culture.value_counts().index,"SAU":SAU_V_ES(),
                                "% SAU": np.round((SAU_V_ES()/np.sum(SAU_V_ES()))*100,2) })

SAU_par_Culture_ES['% SAU'] = SAU_par_Culture_ES['% SAU'].astype(str) + '%'

if select_box_2 == "Echantillonnage systématique":
    
    if select_box_3 == "Culture":
        chart = alt.Chart(df_ES).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Culture',color='Culture').properties(width=700, height=500)
        st.altair_chart(chart)
    
    elif select_box_3 == "Mode Production":
        chart = alt.Chart(df_ES).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Mode_Production',color='Mode_Production').properties(width=700, height=200)
        st.altair_chart(chart)

    elif select_box_3 == "Mode irrigation":
        chart = alt.Chart(df_ES).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Mode_irrigation',color='Mode_irrigation').properties(width=700, height=250)
        st.altair_chart(chart)
    
    elif select_box_3 == "Irrigation":
        chart = alt.Chart(df_ES).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Irrigation',color='Irrigation').properties(width=700, height=150)
        st.altair_chart(chart)
    
    elif select_box_3 == "Serre":
        chart = alt.Chart(df_ES).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Serre',color='Serre').properties(width=700, height=200)
        st.altair_chart(chart)
    
    elif select_box_3 == "Superficie Champ":
        chart = alt.Chart(df_ES).transform_density(
        'Superficie_Champ',
        as_=['Superficie_Champ', 'density'],).mark_area().encode(
        x="Superficie_Champ:Q",
        y='density:Q',).properties(width=650, height=300)
        st.altair_chart(chart)
    
    elif select_box_3 == "SAU par culture":
        chart = alt.Chart(SAU_par_Culture_ES).mark_bar().encode(
        alt.X("SAU", bin=False),
        y='Culture',color='Culture')
    
        text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3 ).encode(
        text="% SAU")
        st.altair_chart((chart + text).properties(width=700, height=500))



##################### Echantillonnage double ##################################

######### EAS


# seq=list(range(1,606,1))
# C=sorted(random.sample(seq, 100))
# print("Random sample, n = 100:", C)


C = [7, 11, 14, 16, 22, 28, 44, 45, 46, 56, 73, 74, 77, 90, 91, 101, 104, 113, 117, 122, 124, 138, 142, 143, 
     144, 148, 155, 159, 161, 168, 174, 190, 192, 203, 207, 208, 214, 215, 216, 219, 221, 239, 245, 264, 269, 
     273, 274, 278, 280, 281, 283, 290, 295, 300, 302, 303, 312, 313, 314, 321, 322, 324, 332, 343, 348, 356, 
     357, 358, 362, 384, 389, 399, 400, 411, 412, 413, 420, 434, 443, 460, 463, 467, 471, 483, 493, 498, 519, 
     526, 531, 532, 534, 547, 556, 565, 583, 590, 593, 597, 600, 601]

df_ED_EAS=df.iloc[C]

######### ES

def systematic_sampling(df, step):
    
    indexes = np.arange(0,len(df),step=step)
    systematic_sample = df.iloc[indexes]
    return systematic_sample
    
df_ED_ES=systematic_sampling(df, 6)
df_ED_ES=df_ED_ES.iloc[1:]


######### ED
df_ED = pd.concat([df_ED_EAS, df_ED_ES])



def SAU_ED(i):
    grouped_df_by_culture = df_ED[df_ED.Culture.str.contains(i)]
    Somme = np.sum(grouped_df_by_culture.Superficie_Champ)
    return Somme

def SAU_V_ED():
    V=[]
    for i in df_ED.Culture.value_counts().index:
        V.append(SAU_ED(i))
    return V

SAU_par_Culture_ED = pd.DataFrame({"Culture":df_ED.Culture.value_counts().index,"SAU":SAU_V_ED(),
                                "% SAU": np.round((SAU_V_ED()/np.sum(SAU_V_ED()))*100,2) })

SAU_par_Culture_ED['% SAU'] = SAU_par_Culture_ED['% SAU'].astype(str) + '%'

if select_box_2 == "Echantillonnage double":
    
    if select_box_3 == "Culture":
        chart = alt.Chart(df_ED).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Culture',color='Culture').properties(width=700, height=500)
        st.altair_chart(chart)
    
    elif select_box_3 == "Mode Production":
        chart = alt.Chart(df_ED).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Mode_Production',color='Mode_Production').properties(width=700, height=200)
        st.altair_chart(chart)

    elif select_box_3 == "Mode irrigation":
        chart = alt.Chart(df_ED).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Mode_irrigation',color='Mode_irrigation').properties(width=700, height=250)
        st.altair_chart(chart)
    
    elif select_box_3 == "Irrigation":
        chart = alt.Chart(df_ED).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Irrigation',color='Irrigation').properties(width=700, height=150)
        st.altair_chart(chart)
    
    elif select_box_3 == "Serre":
        chart = alt.Chart(df_ED).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Serre',color='Serre').properties(width=700, height=200)
        st.altair_chart(chart)
    
    elif select_box_3 == "Superficie Champ":
        chart = alt.Chart(df_ED).transform_density(
        'Superficie_Champ',
        as_=['Superficie_Champ', 'density'],).mark_area().encode(
        x="Superficie_Champ:Q",
        y='density:Q',).properties(width=650, height=300)
        st.altair_chart(chart)
    
    elif select_box_3 == "SAU par culture":
        chart = alt.Chart(SAU_par_Culture_ED).mark_bar().encode(
        alt.X("SAU", bin=False),
        y='Culture',color='Culture')
    
        text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3 ).encode(
        text="% SAU")
        st.altair_chart((chart + text).properties(width=700, height=500))
        
        
        
        
        
############################## Echantillonnage à probabilités inégales ##################################
       
df2=df
total = df2['Superficie_Champ'].sum()
sample_size = 200 #number of samples to be selected
interval_width = int(total/sample_size)
df2['Cumul_Superficie_Champ'] = df2['Superficie_Champ'].cumsum()
num = interval_width #can be a random number also as in the example
sampled_series = np.arange(num, total, interval_width)
cum_array = np.asarray(df2['Cumul_Superficie_Champ'])
selected_samples = np.zeros(sample_size, dtype='int32')
idx = np.searchsorted(cum_array,sampled_series) #the heart of code
result = cum_array[idx-1] 
df_PPS = df2[df2['Cumul_Superficie_Champ'].isin(result)]




def SAU_PPS(i):
    grouped_df_by_culture = df_PPS[df_PPS.Culture.str.contains(i)]
    Somme = np.sum(grouped_df_by_culture.Superficie_Champ)
    return Somme

def SAU_V_PPS():
    V=[]
    for i in df_PPS.Culture.value_counts().index:
        V.append(SAU_PPS(i))
    return V

SAU_par_Culture_PPS = pd.DataFrame({"Culture":df_PPS.Culture.value_counts().index,"SAU":SAU_V_PPS(),
                                "% SAU": np.round((SAU_V_PPS()/np.sum(SAU_V_PPS()))*100,2) })

SAU_par_Culture_PPS['% SAU'] = SAU_par_Culture_PPS['% SAU'].astype(str) + '%'

if select_box_2 == "Echantillonnage à probabilités inégales":
    
    if select_box_3 == "Culture":
        chart = alt.Chart(df_PPS).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Culture',color='Culture').properties(width=700, height=500)
        st.altair_chart(chart)
    
    elif select_box_3 == "Mode Production":
        chart = alt.Chart(df_PPS).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Mode_Production',color='Mode_Production').properties(width=700, height=200)
        st.altair_chart(chart)

    elif select_box_3 == "Mode irrigation":
        chart = alt.Chart(df_PPS).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Mode_irrigation',color='Mode_irrigation').properties(width=700, height=250)
        st.altair_chart(chart)
    
    elif select_box_3 == "Irrigation":
        chart = alt.Chart(df_PPS).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Irrigation',color='Irrigation').properties(width=700, height=150)
        st.altair_chart(chart)
    
    elif select_box_3 == "Serre":
        chart = alt.Chart(df_PPS).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Serre',color='Serre').properties(width=700, height=200)
        st.altair_chart(chart)
    
    elif select_box_3 == "Superficie Champ":
        chart = alt.Chart(df_PPS).transform_density(
        'Superficie_Champ',
        as_=['Superficie_Champ', 'density'],).mark_area().encode(
        x="Superficie_Champ:Q",
        y='density:Q',).properties(width=650, height=300)
        st.altair_chart(chart)
    
    elif select_box_3 == "SAU par culture":
        chart = alt.Chart(SAU_par_Culture_PPS).mark_bar().encode(
        alt.X("SAU", bin=False),
        y='Culture',color='Culture')
    
        text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3 ).encode(
        text="% SAU")
        st.altair_chart((chart + text).properties(width=700, height=500))
        



############################## Echantillonnage stratifié ##################################

median = np.median(df.Superficie_Champ)

df_ESR1=df.loc[df['Superficie_Champ'] < median]
df_ESR2=df.loc[df['Superficie_Champ'] >= median]

n=200

C1=np.std(df_ESR1["Superficie_Champ"])/np.mean(df_ESR1["Superficie_Champ"])
C2=np.std(df_ESR2["Superficie_Champ"])/np.mean(df_ESR2["Superficie_Champ"])
Xq1=(np.median(df_ESR1["Superficie_Champ"]))**0.5
Xq2=(np.median(df_ESR2["Superficie_Champ"]))**0.5

Nh1=n*((C1*Xq1)/(C1*Xq1+C2*Xq2))
Nh2=n*((C2*Xq2)/(C1*Xq1+C2*Xq2))

# import random
seq=list(range(1,606,1))

# V1=sorted(random.sample(seq, int(Nh1)))
V1= [16, 40, 44, 48, 50, 97, 136, 138, 151, 170, 211, 227, 300, 303, 307, 331, 368, 398, 399, 
     409, 416, 431, 458, 459,460, 468, 473, 486, 500, 504, 505, 525, 536, 539, 542, 578]

# V2=sorted(random.sample(seq, int(Nh2)))

V2= [6, 10, 18, 30, 33, 34, 46, 49, 51, 56, 59, 66, 72, 79, 89, 92, 93, 94, 98, 113, 117, 118, 121, 123, 128, 131, 133,
     135, 136, 138, 142, 143, 147, 148, 159, 160, 165, 166, 170, 173, 174, 175, 176, 179, 182, 183, 185, 189, 192, 197,
     205, 206, 212, 214, 215, 223, 224, 228, 232, 239, 243, 247, 248, 249, 251, 252, 258, 259, 271, 273, 276, 279, 280,
     288, 291, 295, 296, 297, 298, 299, 301, 305, 306, 310, 316, 317, 320, 321, 323, 325, 327, 333, 337, 340, 342, 347, 
     350, 354, 362, 364, 365, 376, 377, 385, 387, 389, 395, 396, 398, 403, 414, 421, 422, 423, 425, 426, 427, 432, 437,
     444, 449, 451, 452, 453, 458, 464, 467, 479, 480, 483, 484, 490, 512, 513, 517, 519, 525, 528, 534, 541, 542, 543, 
     549, 552, 553, 554, 555, 559, 560, 565, 566, 567, 570, 571, 573, 576, 578, 579, 584, 586, 588, 600, 602, 604]

# Dataframe de la premiere strata (18% de n)
df_ESR001=df.loc[df_cleaned['Superficie_Champ'] < median]
df_ESR001=df.iloc[V1]

# Dataframe de la deuxieme strata (82% de n)
df_ESR002=df.loc[df_cleaned['Superficie_Champ'] >= median]
df_ESR002=df.iloc[V2]

df_ESR=pd.concat([df_ESR001, df_ESR002])



def SAU_ESR(i):
    grouped_df_by_culture = df_ESR[df_ESR.Culture.str.contains(i)]
    Somme = np.sum(grouped_df_by_culture.Superficie_Champ)
    return Somme

def SAU_V_ESR():
    V=[]
    for i in df_ESR.Culture.value_counts().index:
        V.append(SAU_ESR(i))
    return V

SAU_par_Culture_ESR = pd.DataFrame({"Culture":df_ESR.Culture.value_counts().index,"SAU":SAU_V_ESR(),
                                "% SAU": np.round((SAU_V_ESR()/np.sum(SAU_V_ESR()))*100,2) })

SAU_par_Culture_ESR['% SAU'] = SAU_par_Culture_ESR['% SAU'].astype(str) + '%'

if select_box_2 == "Echantillonnage stratifié":
    
    if select_box_3 == "Culture":
        chart = alt.Chart(df_ESR).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Culture',color='Culture').properties(width=700, height=500)
        st.altair_chart(chart)
    
    elif select_box_3 == "Mode Production":
        chart = alt.Chart(df_ESR).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Mode_Production',color='Mode_Production').properties(width=700, height=200)
        st.altair_chart(chart)

    elif select_box_3 == "Mode irrigation":
        chart = alt.Chart(df_ESR).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Mode_irrigation',color='Mode_irrigation').properties(width=700, height=250)
        st.altair_chart(chart)
    
    elif select_box_3 == "Irrigation":
        chart = alt.Chart(df_ESR).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Irrigation',color='Irrigation').properties(width=700, height=150)
        st.altair_chart(chart)
    
    elif select_box_3 == "Serre":
        chart = alt.Chart(df_ESR).mark_bar().encode(
        alt.X("count()", bin=False),
        y='Serre',color='Serre').properties(width=700, height=200)
        st.altair_chart(chart)
    
    elif select_box_3 == "Superficie Champ":
        chart = alt.Chart(df_ESR).transform_density(
        'Superficie_Champ',
        as_=['Superficie_Champ', 'density'],).mark_area().encode(
        x="Superficie_Champ:Q",
        y='density:Q',).properties(width=650, height=300)
        st.altair_chart(chart)
    
    elif select_box_3 == "SAU par culture":
        chart = alt.Chart(SAU_par_Culture_ESR).mark_bar().encode(
        alt.X("SAU", bin=False),
        y='Culture',color='Culture')
    
        text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3 ).encode(
        text="% SAU")
        st.altair_chart((chart + text).properties(width=700, height=500))




select_box_4 = st.selectbox('', ["Comparaison des moyennes","Comparaison des écarts-types"]) 


#### Comparaison des moyennes

l=np.array([np.mean(df['Superficie_Champ']),np.mean(df_EAS['Superficie_Champ']),np.mean(df_ES['Superficie_Champ']),
    np.mean(df_ED['Superficie_Champ']),np.mean(df_PPS['Superficie_Champ']),np.mean(df_ESR['Superficie_Champ'])])

l0=l/np.mean(df['Superficie_Champ'])
l1=l/np.mean(df_EAS['Superficie_Champ'])
l2=l/np.mean(df_ES['Superficie_Champ'])
l3=l/np.mean(df_ED['Superficie_Champ'])
l4=l/np.mean(df_PPS['Superficie_Champ'])
l5=l/np.mean(df_ESR['Superficie_Champ'])

index=['POP','EAS','ES','ED','PPS','ESR']

Compare_mean=pd.DataFrame({'POP':l0,'EAS':l1,'ES':l2,'ED':l3,'PPS':l4,'ESR':l5},index=index )



#### Comparaison des écarts-types

k=np.array([np.std(df['Superficie_Champ']),np.std(df_EAS['Superficie_Champ']),np.std(df_ES['Superficie_Champ']),
    np.std(df_ED['Superficie_Champ']),np.std(df_PPS['Superficie_Champ']),np.std(df_ESR['Superficie_Champ'])])

k0=k/np.std(df['Superficie_Champ'])
k1=k/np.std(df_EAS['Superficie_Champ'])
k2=k/np.std(df_ES['Superficie_Champ'])
k3=k/np.std(df_ED['Superficie_Champ'])
k4=k/np.std(df_PPS['Superficie_Champ'])
k5=l/np.std(df_ESR['Superficie_Champ'])

index=['POP','EAS','ES','ED','PPS','ESR']

Compare_sd=pd.DataFrame({'POP':k0,'EAS':k1,'ES':k2,'ED':k3,'PPS':k4,'ESR':l5},index=index )



if select_box_4 == "Comparaison des moyennes":
    st.dataframe(Compare_mean)

if select_box_4 == "Comparaison des écarts-types":
    st.dataframe(Compare_sd)



#####################################################################################################################

st.header('Conclusion')


st.write(r"""
**L'échantillonnage stratifié avec allocation proportionnelle** est le plan d’échantillonnage le plus approprié pour 
cette population:

""")

st.write(r""" 
$n_{h} = n \frac{C_{h} X_h^q}{\sum_{h}C_{h} X_h^q}$  avec $q=\frac{1}{2}$ et $C_{h}=\frac{S_{h}}{\bar{Y_{h}}}$

""")

