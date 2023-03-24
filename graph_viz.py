import pandas as pd 
df=pd.read_csv('transfer_window.csv', sep=';')

#https://towardsdatascience.com/visualizing-networks-in-python-d70f4cbeb259

import networkx as nx

G=nx.from_pandas_edgelist(df, source='club_from', target='club_to', edge_attr='fee')
nx.draw(G, with_labels=True)

from pyvis.network import Network

net=Network(notebook=True, filter_menu=True)

net.from_nx(G)
net.show_buttons()
net.show('example.html')

#graph statistics
#https://programminghistorian.org/en/lessons/exploring-and-analyzing-network-data-with-python

nx.degree_centrality(G)
print(nx.info(G))
density = nx.density(G)

#principal component and diameter

# If your Graph has more than one component, this will return False:
print(nx.is_connected(G))

# Next, use nx.connected_components to get the list of components,
# then use the max() command to find the largest one:
components = nx.connected_components(G)
largest_component = max(components, key=len)

# Create a "subgraph" of just the largest component
# Then calculate the diameter of the subgraph, just like you did with density.
subgraph = G.subgraph(largest_component)
diameter = nx.diameter(subgraph)
print("Network diameter of largest component:", diameter)

#centrality
degree_dict = dict(G.degree(G.nodes()))
nx.set_node_attributes(G, degree_dict, 'degree')

from operator import itemgetter

sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)

#create dash variables

#whole dataset

G=nx.from_pandas_edgelist(df, source='club_from', target='club_to', edge_attr='fee')

node=nx.to_dict_of_dicts(G)
edge=nx.to_edgelist(G)

edges=[]
for index,row in df.iterrows() :
    d={}
    d['id']=row['name']
    d['from']=row['club_from']
    d['to']=row['club_to']
    edges.append(d)
    

a=list(pd.unique(df['club_from']))
b=list(pd.unique(df['club_to']))
c=a+b
nodes_list=set(c)

nodes=[]
for node in nodes_list:
    d={}
    d['id']=node
    d['label']=node
    nodes.append(d)
    
    
#serie A

df_serieA=df[df['league_to'] =='Serie A']
G_serieA=nx.from_pandas_edgelist(df_serieA, source='club_from', target='club_to', edge_attr='fee')

node=nx.to_dict_of_dicts(G)
edge=nx.to_edgelist(G)

edges_serieA=[]
for index,row in df_serieA.iterrows() :
    d={}
    d['id']=row['name']
    d['from']=row['club_from']
    d['to']=row['club_to']
    edges_serieA.append(d)
    

a_serieA=list(pd.unique(df_serieA['club_from']))
b_serieA=list(pd.unique(df_serieA['club_to']))
c_serieA=a_serieA+b_serieA
nodes_list_serieA=set(c_serieA)

nodes_serieA=[]
for node in nodes_list_serieA:
    d={}
    d['id']=node
    d['label']=node
    nodes_serieA.append(d)
    
    
    

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import visdcc

app = Dash(__name__)

app.layout = html.Div([
      visdcc.Network(id = 'net', 
                     options = dict(height= '600px', width= '100%')),
      html.Br(),html.Br(),
      dcc.RadioItems(id = 'color',
                     options=[{'label': 'Red'  , 'value': '#ff0000'},
                              {'label': 'Green', 'value': '#00ff00'},
                              {'label': 'Blue' , 'value': '#0000ff'} ],
                     value='Red'  )             
      ,
      html.Br(),html.Br(),
      dcc.RadioItems(id = 'dataset',
               options=[#{'label': 'Premier League'  , 'value': 'Premier League'},
                        {'label': 'Serie A', 'value': 'Serie A'},
                        #{'label': 'Bundesliga' , 'value': 'Bundesliga'},
                        {'label': 'All' , 'value': 'All'}],
               value='All')
      ])

# if __name__ == '__main__':
#     app.run_server(debug=True, use_reloader=False)

@app.callback(
    Output('net', 'data'),
    [Input('dataset', 'value')])
def myfun(value):
    if value=='All':
        data ={'nodes':nodes,
               'edges':edges}
        
    if value=='Serie A':
        data ={'nodes':nodes_serieA,
               'edges':edges_serieA}
            
    return data

@app.callback(
    Output('net', 'options'),
    [Input('color', 'value')])
def myfun(x):
    return {'nodes':{'color': x}}  

    


if __name__ == '__main__':
    app.run_server(debug=False)