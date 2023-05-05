import pandas as pd 
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)
server= app.server

df=pd.read_csv('transfer_window.csv', sep=',')
league_year=df.groupby(['league_to', 'year'], as_index=False)['fee'].sum()
premier=league_year[league_year['league_to']=="Premier League"]
serieA=league_year[league_year['league_to']=="Serie A"]
bundesliga=league_year[league_year['league_to']=="Bundesliga"]
laliga=league_year[league_year['league_to']=="LaLiga"]
ligue1=league_year[league_year['league_to']=="Ligue 1"]
others=league_year[league_year['league_to']=="Others"]


app.layout = html.Div(className='row',style={'display': 'flex',  'fontSize': 14}, children=[
        html.Div([
        dcc.Graph(id = 'bar_plot')
        ],  style={'border': 'solid red', 'width':'100%'},
        className='two columns'),
        html.Div([
        dcc.Graph(id = 'pie_chart')],style={'border': 'solid red', 'width':'100%'},className='two columns')])
    
    
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
             Input(component_id='bar_plot', component_property='selectedData'))

def graph_update(selectedData):
    fig_stacked_bar = go.Figure(data= [go.Bar(name='Premier League',x=premier["year"], y=premier["fee"], marker_color='#031b5e'),
                      go.Bar(name='Serie A',x=serieA["year"], y=serieA["fee"], marker_color='#25AA0A'),
                      go.Bar(name='Bundesliga',x=bundesliga["year"], y=bundesliga["fee"], marker_color='#ca0302'),
                      go.Bar(name='LaLiga',x=laliga["year"], y=laliga["fee"], marker_color='#E16B19'),
                      go.Bar(name='Ligue 1',x=ligue1["year"], y=ligue1["fee"], marker_color='#7e33c5'),
                      go.Bar(name='Others',x=others["year"], y=others["fee"], marker_color='lightgrey')])

    fig_stacked_bar.update_layout(barmode='stack')
    

    return fig_stacked_bar


@app.callback(
    Output(component_id='pie_chart', component_property='figure'),
    Input(component_id='bar_plot', component_property='hoverData'),
    Input(component_id='bar_plot', component_property='clickData'),
    Input(component_id='bar_plot', component_property='selectedData'))

def update_side_graph(hov_data, clk_data, slct_data):
    
    if clk_data is None:
        fig_pie=px.pie(values=[760,2974], names=['zero', 'non-zero'], title='Percentage of zero transfers', 
                       color_discrete_map = 'viridis')

        fig_pie.update_traces(hoverinfo = 'label+percent', textfont_size = 20,
                  textinfo = 'label+percent', pull = [0.1, 0, 0.2, 0, 0, 0])

        return fig_pie
    
    else:
        #print(clk_data['points'][0]['x'])
        #print(clk_data)
        # print(f'click data: {clk_data}')
        # print(f'selected data: {slct_data}')
        year=clk_data['points'][0]['x']
        
        df2=df[df['year']==year]
        tot=len(df2)
        zero=len(df2[df2['fee']==0])
        
        fig_pie=px.pie(values=[zero,tot-zero], names=['zero', 'non-zero'], title=f'Percentage of zero transfers in {year}', 
                       color_discrete_map = 'viridis')

        fig_pie.update_traces(hoverinfo = 'label+percent', textfont_size = 20,
                  textinfo = 'label+percent', pull = [0.1, 0, 0.2, 0, 0, 0])


        return fig_pie


if __name__ == '__main__': 
    app.run_server(port=127)
