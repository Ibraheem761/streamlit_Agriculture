import numpy as np
import pandas as pd
import streamlit as st
import altair as alt


df=pd.read_excel('Base_sondage_maraichage.xlsx', index_col="Identifiant", na_values=['NA'])

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


