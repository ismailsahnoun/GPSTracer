import pandas as pd
import datetime
from datetime import date
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

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
    ],id="header",className="row flex-display",style={"margin-bottom":"25px"}),

    html.Div([
        html.Div([
            html.H6(children="Nombre des tournées",style={'textAlign':'center','color':'white'}),
            html.P(style={'textAlign':'center','color':'orange','fontSize':28},id="tournee"),
        ],className="card_container three columns",
        ),
        html.Div([
            html.H6(children='Nombre des prestations',style={'textAlign':'center','color':'white'}),
            html.P("data mte3i",style={'textAlign':'center','color':'#dd1e35','fontSize':28},id="prestations"),
        ],className="card_container three columns",),
        html.Div([
            html.H6(children='Durée totale',style={'textAlign':'center','color':'white'}),
            html.P(style={'textAlign':'center','color':'green','fontSize':28},id="dureeT"),
        ],className="card_container three columns",),
        html.Div([
            html.H6(children='Durée moyenne',style={'textAlign':'center','color':'white'}),
            html.P(style={'textAlign':'center','color':'#e55467','fontSize':28},id="dureeM"),
        ],className="card_container three columns",)
    ],className="row flex-display"),

    html.Div([
        html.Div([
            html.P('Sélectionner une période     :',className='fix_label',style={'color':'white'}),
            html.Td([ dcc.DatePickerRange(
                                id='my-date-picker-range',
                                min_date_allowed=date(1995, 8, 5),
                                max_date_allowed=date(2100, 9, 19),
                                initial_visible_month=date(2021, 8, 1),
                                start_date=date(2021, 8, 23),
                                end_date=date(2021, 8, 23)
            )],style={'fontSize':14}),
            html.P('Sélectionner un Chauffeur :',className='fix_label',style={'color':'white'}),
            dcc.Dropdown(id='select_chauffeur',
                        multi=False,
                        clearable=True,
                        placeholder='Sélectionner un Chauffeur',
                        options=[{'label': i, 'value': i}
                             for i in (TRAJETS['Chauffeur'].unique())],className='dcc_compon'),
            html.P("Nombre de Voitures utilisées ",className='fix_label',style={'color':'orange','text-align':'center','fontSize':18}),
            html.P(className='fix_label',style={'color':'orange','text-align':'center','fontSize':18},id="nbv"),
            html.P('Sélectionner un véhicule :',className='fix_label',style={'color':'white'}),
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

],id="mainContainer",style={"display":"flex","flex-direction":"column"})

@app.callback(
    Output('tournee', 'children'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('select_chauffeur','value'),])
def update_NBTOURNEE(start_date, end_date,input_chauffeur):
    periode = (TRAJETS['Date'] >=start_date) & (TRAJETS['Date'] <= end_date)
    TRAJETS_P=TRAJETS.loc[periode]
    Test_Chauffeur=(TRAJETS_P['Chauffeur']==input_chauffeur)
    Trajets_C=TRAJETS_P.loc[Test_Chauffeur]
    NB_TourneeCH=Trajets_C.Tournee.nunique()
    return NB_TourneeCH

@app.callback(
    Output('prestations','children'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('select_chauffeur','value'),])
def update_NBPRESTATION(start_date,end_date,input_chauffeur):
    periode = (TRAJETS['Date'] >=start_date) & (TRAJETS['Date'] <= end_date)
    TRAJETS_P=TRAJETS.loc[periode]
    Test_Chauffeur=(TRAJETS_P['Chauffeur']==input_chauffeur)
    Trajets_C=TRAJETS_P.loc[Test_Chauffeur]
    NB_PrestationCH=len(Trajets_C)
    return NB_PrestationCH

@app.callback(
    Output('dureeT','children'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('select_chauffeur','value'),])
def update_NBPRESTATION(start_date,end_date,input_chauffeur):
    periode = (TRAJETS['Date'] >=start_date) & (TRAJETS['Date'] <= end_date)
    TRAJETS_P=TRAJETS.loc[periode]
    Test_Chauffeur=(TRAJETS_P['Chauffeur']==input_chauffeur)
    Trajets_C=TRAJETS_P.loc[Test_Chauffeur]
    Trajets_C['DIFF']=Trajets_C['Arrivee']-Trajets_C['Depart']
    DUREE_TOTALECH=str(Trajets_C.DIFF.sum())
    return DUREE_TOTALECH
@app.callback(
    Output('dureeM','children'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('select_chauffeur','value'),])
def update_NBPRESTATION(start_date,end_date,input_chauffeur):
    periode = (TRAJETS['Date'] >=start_date) & (TRAJETS['Date'] <= end_date)
    TRAJETS_P=TRAJETS.loc[periode]
    Test_Chauffeur=(TRAJETS_P['Chauffeur']==input_chauffeur)
    Trajets_C=TRAJETS_P.loc[Test_Chauffeur]
    Trajets_C['DIFF']=Trajets_C['Arrivee']-Trajets_C['Depart']
    DUREE_MOYCH=str (Trajets_C.DIFF.mean())
    return DUREE_MOYCH
@app.callback(
    Output('nbv', 'children'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('select_chauffeur','value'),])
def update_NBTOURNEE(start_date, end_date,input_chauffeur):
    periode = (TRAJETS['Date'] >=start_date) & (TRAJETS['Date'] <= end_date)
    TRAJETS_P=TRAJETS.loc[periode]
    Test_Chauffeur=(TRAJETS_P['Chauffeur']==input_chauffeur)
    Trajets_C=TRAJETS_P.loc[Test_Chauffeur]
    NB_Vehicule=Trajets_C.Immatriculation.nunique()
    return NB_Vehicule

@app.callback(
    Output('pie_chart','figure'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),])
def update_TOPCHGRAPH(start_date,end_date):
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
