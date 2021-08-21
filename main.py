from enum import unique
from logging import PlaceHolder
import pandas as pd
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

#Importation du Fichier de données
Url_Trajets='trajets.xlsx'
TRAJETS=pd.read_excel(Url_Trajets)

#Extraction du DataFrame de la période
TRAJETS['Date']=pd.to_datetime(TRAJETS.Date)
D_Periode=pd.to_datetime('2021-8-1')
F_Periode=pd.to_datetime('2021-9-1')
periode = (TRAJETS['Date'] >= D_Periode) & (TRAJETS['Date'] <= F_Periode)
TRAJETS_P=TRAJETS.loc[periode]

TRAJETS_P['Arrivee']=pd.to_timedelta(TRAJETS_P.Arrivee)
TRAJETS_P['Depart']=pd.to_timedelta(TRAJETS_P.Depart)

#Exctraction du DataFrame du Chauffeur à partir de celui de la période
Nom_Chauffeur="Nadir Barache"
Test_Chauffeur=(TRAJETS_P['Chauffeur']==Nom_Chauffeur)
Trajets_C=TRAJETS_P.loc[Test_Chauffeur]

#Exctraction du DataFrame du Véhicule à partir de celui de la période
Nom_Vehicule="FT-430-JJ"
Test_Vehicule=(TRAJETS_P['Immatriculation']==Nom_Vehicule)
Trajets_V=TRAJETS_P.loc[Test_Vehicule]

#Requêtes des KPI du Chauffeur

# NB de Tournées du Chauffeur
NB_TourneeCH=Trajets_C.Tournee.nunique()

# Durée totale des Prestations du Chauffeur
Trajets_C['DIFF']=Trajets_C['Arrivee']-Trajets_C['Depart']
DUREE_TOTALECH=Trajets_C.DIFF.sum()

# NB de Vehicules
NB_Vehicule=Trajets_C.Immatriculation.nunique()

# Durée Moyenne des Prestations du Chauffeur
DUREE_MOYCH=Trajets_C.DIFF.mean()

# NB de Prestations du Chauffeur
NB_PrestationCH=len(Trajets_C)

# TOP 5 Chauffeurs 
TOP_C=TRAJETS_P.groupby('Chauffeur').size().sort_values(ascending=False).reset_index(name='Nombre Prestations')

#Requêtes des KPI du Véhicule

# NB de Tournées du Véhicule
NB_TourneeV=Trajets_V.Tournee.nunique()

# Durée totale des Prestations du Véhicule
Trajets_V['DIFF']=Trajets_V['Arrivee']-Trajets_V['Depart']
DUREE_TOTALEV=Trajets_V.DIFF.sum()

# Durée Moyenne des Prestations du Véhicule
DUREE_MOYV=Trajets_V.DIFF.mean()

# NB de Prestations du Véhicule
NB_PrestationV=len(Trajets_V)

# TOP 5 Véhicules 
TOP_V=TRAJETS_P.groupby('Immatriculation').size().sort_values(ascending=False).reset_index(name='Nombre Prestations')


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)


app.layout = html.Div(children=[
    html.Div(children=
        html.P('Sélectionner un Chauffeur :', className='fix_label', style={'color': 'white'})
    ),

    dcc.Dropdown(   id='Select_Chauffeur',
                    multi=False,
                    clearable=True,
                    placeholder='Select Countries',
                    options=[{'label': i, 'value': i}
                             for i in (TRAJETS_P['Chauffeur'].unique())],className='dcc_compon'
                )
])  
if __name__=="__main__":
    app.run_server(debug=True)
    