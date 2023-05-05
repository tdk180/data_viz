import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from dash import Dash, dcc, html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import networkx as nx

# Load extra layouts
cyto.load_extra_layouts()

df=pd.read_csv('transfer_window.csv', sep=',')
df=df.rename(columns={"club_from": "from", "club_to": "to"})
df=df[df['league_to']=="Premier League"]
df=df[df['country_to']=="England"]
df=df.sort_values(by=['market_value'], ascending=False)
df=df.head(100)

league_from={}
for index,row in df.iterrows():
    if row['from'] not in league_from.keys():
        league_from[row['from']]=row['league_from']

for index,row in df.iterrows():
    if row['to'] not in league_from.keys():
        league_from[row['to']]=row['league_to']
        
G=nx.from_pandas_edgelist(df, source='from', target='to')

from community import community_louvain
part=community_louvain.best_partition(G)

nx.set_node_attributes(G, league_from, "league_from")
nx.set_node_attributes(G, part, "community")
data=nx.cytoscape_data(G)

for el in data['elements']['nodes']:
    el['classes']=el['data']['league_from'].replace(' ','')
    
for el in data['elements']['nodes']:
    el['classes']=el['classes']+" "+str(el['data']['community'])
    
cyto_id = 'cytoscape' # just the name of the plot
style = {'width': '100%', 'height': '400px'} # the size of the plot
layout = {'name': 'circle'} # breadthfirst cose-bilkent

stylesheet=[
            # Group selectors
            {
                'selector': 'node',
                'style': {
                    'content': 'data(id)'
                }
            },

            # Class selectors
            {
                'selector': '.LaLiga',
                'style': {
                    'background-color': '#E16B19',
                    'line-color': '#219ebc',
                    'shape': 'triangle'
                }
            },
            {
                'selector': '.Others',
                'style': {
                    'background-color': 'lightgrey',
                    'line-color': '#219ebc',
                    'shape': 'triangle'
                }
            },
    {
                'selector': '.PremierLeague',
                'style': {
                    'background-color': '#031b5e',
                    'line-color': '#219ebc',
                    'shape': 'triangle'
                }
            },{
                'selector': '.Bundesliga',
                'style': {
                    'background-color': '#ca0302',
                    'line-color': '#219ebc',
                    'shape': 'triangle'
                }
            },
    {
                'selector': '.SerieA',
                'style': {
                    'background-color': '#25AA0A',
                    'line-color': '#219ebc',
                    'shape': 'triangle'
                }
            },
    {
                'selector': '.Ligue1',
                'style': {
                    'background-color': '#7e33c5',
                    'line-color': '#219ebc',
                    'shape': 'triangle'
                }
            }
            
            
        ]

import seaborn as sns
import matplotlib

cyto_id = 'cytoscape' # just the name of the plot
style = {'width': '100%', 'height': '800px'} # the size of the plot
layout = {'name': 'circle'} # breadthfirst cose-bilkent
#generate partition of max(part.values())+1 colors
palette = sns.color_palette("Spectral", 11)

stylesheet=[
            # Group selectors
            {
                'selector': 'node',
                'style': {
                    'content': 'data(id)'
                }
            }
            ]

for x in range(0,11):
    y=str(x)
    color=matplotlib.colors.rgb2hex(palette[x])
    selector={
                'selector': f'.{y}',
                'style': {
                    'background-color':f'{color}',
                    'line-color': '#219ebc',
                    'shape': 'dot'
                }
            }
    stylesheet.append(selector)

cyto_id = 'cytoscape' # just the name of the plot
style = {'width': '100%', 'height': '800px'} # the size of the plot

app = Dash(__name__)
server= app.server

app.layout = html.Div([dcc.Dropdown(
        id='dropdown-update-layout',
        value='circle',
        clearable=False,
        options=[
            {'label': name.capitalize(), 'value': name}
            for name in ['circle', 'concentric', 'cose-bilkent']
        ]
    ),

    dcc.Dropdown(
        id='dropdown-update-color',
        value='league',
        clearable=False,
        options=[
            {'label': name.capitalize(), 'value': name}
            for name in ['league', 'community']
        ]
    ),
    cyto.Cytoscape(id = cyto_id,
                   style = style,
                   layout = {'name': 'concentric'},
                   stylesheet=[
            # Group selectors
            {
                'selector': 'node',
                'style': {
                    'content': 'data(id)'
                }
            }
            ]
,
                   elements = data['elements'])]
    )



@app.callback(Output('cytoscape', 'stylesheet'),
              Input('dropdown-update-color', 'value'))
def update_layout(stylesheet):
    if stylesheet=='league':
        stylesheet=[
            # Group selectors
            {
                'selector': 'node',
                'style': {
                    'content': 'data(id)'
                }
            
            },
            
             {
                'selector': 'edge',
                'style': {
                    'line-color': 'black',
                     'opacity': '0.2'
                }
             },


            # Class selectors
            {
                'selector': '.LaLiga',
                'style': {
                    'background-color': '#E16B19',
                    'line-color': '#219ebc',
                    'shape': 'dot'
                }
            },
            {
                'selector': '.Others',
                'style': {
                    'background-color': 'lightgrey',
                    'line-color': '#219ebc',
                    'shape': 'dot'
                }
            },
    {
                'selector': '.PremierLeague',
                'style': {
                    'background-color': '#031b5e',
                    'line-color': '#219ebc',
                    'shape': 'dot'
                }
            },{
                'selector': '.Bundesliga',
                'style': {
                    'background-color': '#ca0302',
                    'line-color': '#219ebc',
                    'shape': 'dot'
                }
            },
    {
                'selector': '.SerieA',
                'style': {
                    'background-color': '#25AA0A',
                    'line-color': '#219ebc',
                    'shape': 'dot'
                }
            },
    {
                'selector': '.Ligue1',
                'style': {
                    'background-color': '#7e33c5',
                    'line-color': '#219ebc',
                    'shape': 'dot'
                }
            }
            
            
        ]


        return stylesheet
    if stylesheet=='community':
        stylesheet=[
                    # Group selectors
                    {
                        'selector': 'node',
                        'style': {
                            'content': 'data(id)'
                        }
                    },
             {
                'selector': 'edge',
                'style': {
                    'line-color': 'black',
                    'opacity': '0.2'
                }
             }
                    ]
        palette = sns.color_palette("viridis", max(part.values())+1)

        for x in range(0,max(part.values())+1):
            y=str(x)
            color=matplotlib.colors.rgb2hex(palette[x])
            selector={
                        'selector': f'.{y}',
                        'style': {
                            'background-color':f'{color}',
                            'shape': 'dot'
                        }
                    }
            stylesheet.append(selector)
            
        return stylesheet

@app.callback(Output('cytoscape', 'layout'),
              Input('dropdown-update-layout', 'value'))
def update_layout(layout):
    if layout=='circle':
        return {
            'name': layout,
            'animate': True,
            
        }
    if layout=='cose-bilkent':
        return {
            'name': layout,
            'animate': True,
            'idealEdgeLength': 200
        }
    if layout=='concentric':
        return {
            'name': layout,
            'animate': True,
            'minNodeSpacing': 70
        }

    
if __name__ == '__main__':
    app.run_server( debug=False)


