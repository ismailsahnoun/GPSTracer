import pandas as pd
import datetime
from datetime import date
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

#Format TimeDelta
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)
#Importation du Fichier de données
Url_Trajets='trajets.xlsx'
TRAJETS=pd.read_excel(Url_Trajets)
TRAJETS['Arrivee']=pd.to_timedelta(TRAJETS.Arrivee)
TRAJETS['Depart']=pd.to_timedelta(TRAJETS.Depart)

#Extraction du DataFrame de la période
TRAJETS['Date']=pd.to_datetime(TRAJETS.Date)
app = dash.Dash(__name__)

app.layout=html.Div([
    html.Div([
        html.Div([
            html.Img()
        ],
            className="one-third column",
        ),
        html.Div([
            html.Div([
                html.H2("GPS Tracer",style={"margin-bottom":"0px",'color':'white'}),
            ])
            
        ],className="one-third column",id='title1'),
    ],id="header",className="row flex-display",style={"margin-bottom":"10px"}),
    html.Div([
        html.Div([
            html.P('Sélectionner une période     :',className='fix_label',style={'color':'white',"margin-bottom":"10px"}),
            html.Td([ dcc.DatePickerRange(
                                id='my-date-picker-range',
                                min_date_allowed=date(1995, 8, 5),
                                max_date_allowed=date(2100, 9, 19),
                                initial_visible_month=date(2021, 8, 1),
            )],style={'fontSize':14}),
            html.P('Sélectionner un Chauffeur :',className='fix_label',style={'color':'white',"margin-bottom":"10px","margin-top":"10px"}),
            dcc.Dropdown(id='select_chauffeur',
                        multi=False,
                        clearable=True,
                        placeholder='Sélectionner un Chauffeur',
                        options=[{'label': i, 'value': i}
                             for i in (TRAJETS['Chauffeur'].unique())],className='dcc_compon'),
            html.P('Sélectionner un véhicule :',className='fix_label',style={'color':'white',"margin-bottom":"10px"}),
            dcc.Dropdown(   id='select_vehicule',
                    multi=False,
                    clearable=True,
                    placeholder='Sélectionner un Véhicule',
                    options=[{'label': j, 'value': j}
                             for j in (TRAJETS['Immatriculation'].unique())],className='dcc_compon'),
        ],className="create_container four columns", id="cross-filter-options"),
        html.Div([
            html.P("TOP 5 Chauffeurs ",className='fix_label',style={'color':'white','text-align':'center','fontSize':18}),
            dcc.Graph(id='pie_chart', config={'displayModeBar':'hover'}),
        ],className="create_container five columns"),
        html.Div([
            html.P("TOP 5 Vehicules ",className='fix_label',style={'color':'white','text-align':'center','fontSize':18}),
            dcc.Graph(id='pie_chart2', config={'displayModeBar':'hover'}),
        ],className="create_container five columns"),
        
    ],className="row flex-display"),

    html.Div([
        html.Div([
            html.P("Chauffeur",style={'textAlign':'center','color':'white','fontSize':16,'margin-top':'8px'}),
            html.P("Véhicule",style={'textAlign':'center','color':'white','fontSize':16,'margin-top':'8px'}),
        ],className="card_container two columns",style={'margin-top':'100px','background-color':'#192444'},
        ),
        html.Div([
            html.H6(children="Nombre des tournées",style={'textAlign':'center','color':'white','fontSize':18}),
            html.P(style={'textAlign':'center','color':'orange','fontSize':20},id="tourneech"),
            html.P(style={'textAlign':'center','color':'orange','fontSize':20},id="tourneev"),
        ],className="card_container three columns",
        ),
        html.Div([
            html.H6(children='Nombre des prestations',style={'textAlign':'center','color':'white','fontSize':18}),
            html.P(style={'textAlign':'center','color':'#dd1e35','fontSize':20},id="prestationsCH"),
            html.P(style={'textAlign':'center','color':'#dd1e35','fontSize':20},id="prestationsV"),
        ],className="card_container three columns",),
        html.Div([
            html.H6(children='Nombre des voitures',style={'textAlign':'center','color':'white','fontSize':18}),
            html.P(style={'textAlign':'center','color':'#00CC00','fontSize':20,'margin-top':'30px'},id="voitures"),
        ],className="card_container three columns",),
        html.Div([
            html.H6(children='Durée moyenne',style={'textAlign':'center','color':'white','fontSize':18}),
            html.P(style={'textAlign':'center','color':'#e55467','fontSize':20,'margin-top':'38px'},id="dureeMCH"),
            html.P(style={'textAlign':'center','color':'#e55467','fontSize':20,'margin-top':'8px'},id="dureeMV"),
        ],className="card_container three columns",),
        html.Div([
            html.H6(children='Durée totale',style={'textAlign':'center','color':'white','fontSize':18}),
            html.P(style={'textAlign':'center','color':'#e55445','fontSize':20,'margin-top':'38px'},id="dureeTCH"),
            html.P(style={'textAlign':'center','color':'#e55445','fontSize':20,'margin-top':'8px'},id="dureeTV"),
        ],className="card_container three columns",)
    ],className="row flex-display"),       

],id="mainContainer",style={"display":"flex","flex-direction":"column"})

@app.callback(
    Output('tourneech', 'children'),
    Output('prestationsCH','children'),
    Output('dureeTCH','children'),
    Output('dureeMCH','children'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('select_chauffeur','value'),])
def update_Chauffeur(start_date, end_date,input_chauffeur):
    if (start_date==None) & (end_date==None):
        return '','','',''
    elif (input_chauffeur==None):
        return '','','',''
    else:
        periode = (TRAJETS['Date'] >=start_date) & (TRAJETS['Date'] <= end_date)
        TRAJETS_P=TRAJETS.loc[periode]
        Test_Chauffeur=(TRAJETS_P['Chauffeur']==input_chauffeur)
        Trajets_C=TRAJETS_P.loc[Test_Chauffeur]
        NB_TourneeCH=Trajets_C.Tournee.nunique()
        NB_PrestationCH=len(Trajets_C)
        Trajets_C['DIFF']=Trajets_C['Arrivee']-Trajets_C['Depart']
        DUREE_TOTALECH=strfdelta(Trajets_C.DIFF.sum(), "{days}j {hours}:{minutes}:{seconds}s")
        DUREE_MOYCH=strfdelta(Trajets_C.DIFF.mean(), "{days}j {hours}:{minutes}:{seconds}s")
        return NB_TourneeCH,NB_PrestationCH,DUREE_TOTALECH,DUREE_MOYCH
@app.callback(
    Output('tourneev', 'children'),
    Output('prestationsV','children'),
    Output('dureeTV','children'),
    Output('dureeMV','children'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('select_vehicule','value'),])
def update_Vehicule(start_date, end_date,input_vehicule):
    if (start_date==None) & (end_date==None):
        return '','','',''
    elif (input_vehicule==None):
        return '','','',''
    else:
        periode = (TRAJETS['Date'] >=start_date) & (TRAJETS['Date'] <= end_date)
        TRAJETS_P=TRAJETS.loc[periode]
        Test_Vehicule=(TRAJETS_P['Immatriculation']==input_vehicule)
        Trajets_V=TRAJETS_P.loc[Test_Vehicule]
        NB_TourneeV=Trajets_V.Tournee.nunique()
        NB_PrestationV=len(Trajets_V)
        Trajets_V['DIFF']=Trajets_V['Arrivee']-Trajets_V['Depart']
        DUREE_TOTALEV=strfdelta(Trajets_V.DIFF.sum(), "{days}j {hours}:{minutes}:{seconds}s")
        DUREE_MOYV=strfdelta(Trajets_V.DIFF.mean(), "{days}j {hours}:{minutes}:{seconds}s")
        return NB_TourneeV,NB_PrestationV,DUREE_TOTALEV,DUREE_MOYV
@app.callback(
    Output('voitures', 'children'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),])
def update_NBV(start_date, end_date):
    if (start_date==None) & (end_date==None):
        return ''
    else:
        periode = (TRAJETS['Date'] >=start_date) & (TRAJETS['Date'] <= end_date)
        TRAJETS_P=TRAJETS.loc[periode]
        NB_Vehicule=TRAJETS_P.Immatriculation.nunique()
        return NB_Vehicule
@app.callback(
    Output('pie_chart','figure'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),])
def update_TOPCHGRAPH(start_date,end_date):
    if (start_date==None) & (end_date==None):
        return {}
    else:
        periode = (TRAJETS['Date'] >=start_date) & (TRAJETS['Date'] <= end_date)
        TRAJETS_P=TRAJETS.loc[periode]
        TOP_C=TRAJETS_P.groupby('Chauffeur').size().sort_values(ascending=False).reset_index(name='Nombre_Prestations')
        piechart=px.pie(
            data_frame=TOP_C,
            values=TOP_C.Nombre_Prestations,
            names=TOP_C.Chauffeur,
            hole=.5,
            color_discrete_sequence=px.colors.sequential.Turbo,
        )
        return (piechart)
@app.callback(
    Output('pie_chart2','figure'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),])
def update_TOPVGRAPH(start_date,end_date):
    if (start_date==None) & (end_date==None):
        return {}
    else:
        periode = (TRAJETS['Date'] >=start_date) & (TRAJETS['Date'] <= end_date)
        TRAJETS_P=TRAJETS.loc[periode]
        TOP_V=TRAJETS_P.groupby('Immatriculation').size().sort_values(ascending=False).reset_index(name='Nombre_Prestations')
        piechart2=px.pie(
            data_frame=TOP_V,
            values=TOP_V.Nombre_Prestations,
            names=TOP_V.Immatriculation,
            hole=.5,
            color_discrete_sequence=px.colors.sequential.Inferno
        )
        return (piechart2)

if __name__=="__main__":
    app.run_server(debug=True)
