import plotly.plotly as py
import pandas as pd
import plotly.graph_objs as go
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output
from sklearn import preprocessing
le = preprocessing.LabelEncoder()

external_stylesheets = ['https://codepen.io/larkie11/pen/NJmbLx.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#MAIN DATA SET
adf = pd.read_csv('athlete_events.csv')

#NAN SETS ARE NOT FILTERED OUT AS WE WANT ALL PARTICIPANTS EVEN IF THEY HAVE CERTAIN NAN COLUMNS
#WILL BE CHECKED IN THEIR OWN FIGURES/PLOTS/STATS

#DATASET FOR MEDALISTS
df = adf.copy()
df = df.dropna(subset=['Medal'])
df= df.drop_duplicates(subset=['ID'])
malemedalists = df.loc[df['Sex']=='M']
femalemedalists = df.loc[df['Sex']=='F']

#FOR DROP DOWN IN STATS AREA, Getting all unique sports and medals into its own nparray
available_indicators = df['Sport'].unique()
available_indicators.sort()
available_indicators = np.append('All sports',available_indicators)
available_indicators2 = df['Medal'].unique()
available_indicators2 = np.append('All',available_indicators2)
available_indicators2 = np.append('None',available_indicators2)

count = df.copy()
#FOR WORLD MAP = ONLY NEED COUNT OF MEDALS #group by noc and medal
count = count.groupby(['NOC','Medal'],as_index=False).size().reset_index(name='count')
count['total']=""
#total count of all medals for each NOC
count['total']=count.groupby('NOC')['count'].transform(sum)
#Get only bronze for all NOC
bronze = count.loc[count['Medal']=='Bronze']
#Get only silver for all NOC
silver = count.loc[count['Medal']=='Silver']
#Get only gold for all NOC
gold = count.loc[count['Medal']=='Gold']

#no duplicated participants that take part in multiple events over seasons/years (regardless of medal or not)
dropduplicates = adf.drop_duplicates(subset=['ID'])
#for converting of categorical to numerical values to do correlation
heatmapd = dropduplicates.copy()

#PARTICIPANTS OVER THE YEARS BY GENDER
genders = dropduplicates.groupby(['Sex','Year'],as_index=False).size().reset_index(name='count')
#add count of females and males and their total each year
genders['total']=genders.groupby('Year')['count'].transform(sum)
genders['fmcount']=genders.groupby('Sex')['count'].transform(sum)
#SEPERATE DATASET TO FEMALES AND MALES
females = genders.loc[genders['Sex']=='F']
males = genders.loc[genders['Sex']=='M']

#3d cluster plot but very laggy since a lot of data points
scatter = dict(
    mode = "markers",
    name = "y",
    type = "scatter3d",    
    x = dropduplicates['Games'], y = dropduplicates['City'], z = dropduplicates['Sport'],
    marker = dict( size=2, color="rgb(23, 190, 207)" )
)
clusters = dict(
    alphahull = 7,
    name = "y",
    opacity = 0.1,
    type = "mesh3d",    
    x = dropduplicates['Games'], y = dropduplicates['City'], z = dropduplicates['Sport']
)
klayout = dict(
		width=1400, height=700,
        margin=dict( l=150, r=150, b=50, t=50, pad=4, autoexpand=True ),
    title = '3d point clustering of the sports competition held during each event',
    scene = dict(
        xaxis = dict( title = 'Games' ,zeroline=False ),
        yaxis = dict( title = 'City' ,zeroline=False ),
        zaxis = dict( title = 'Sport' ,zeroline=False ),
    )
)
kfig = dict( data=[scatter, clusters], layout=klayout )

#TOTAl MEDALS MAP
data = [go.Choropleth(
    locations = count['NOC'],
    z = count['total'],
    text = "Total Medals",
    colorscale = [
        [0, "rgb(5, 10, 172)"],
        [0.35, "rgb(40, 60, 190)"],
        [0.5, "rgb(70, 100, 245)"],
        [0.6, "rgb(90, 120, 245)"],
        [0.7, "rgb(106, 137, 247)"],
        [1, "rgb(220, 220, 220)"]
    ],
    autocolorscale = False,
    reversescale = True,
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(180,180,180)',
            width = 0.5
        )),
    colorbar = go.choropleth.ColorBar(
        tickprefix = '',
        title = 'Count of medals'),
)]
layout = go.Layout(
autosize=False,
        width=1400, height=600,
        margin=dict( l=150, r=150, b=0, t=50, pad=1, autoexpand=True ),
    title = go.layout.Title(
        text = 'Total medals won by countries'
    ),
    geo = go.layout.Geo(
        showframe = False,
        showcoastlines = False,
        projection = go.layout.geo.Projection(
            type = 'natural earth'
        )
    ),
    annotations = [go.layout.Annotation(
        x = 0.55,
        y = 0.1,
        xref = 'paper',
        yref = 'paper',
        text = '',
        showarrow = False
    )]
)
fig = go.Figure(data = data, layout = layout)

#Bronze Map
data1 = [go.Choropleth(
    locations = bronze['NOC'],
    z = bronze['count'],
    text = "Bronze Medals",
    colorscale = [
        [0, "rgb(102, 0, 102)"],
        [0.35, "rgb(204, 0, 204)"],
        [0.5, "rgb(153, 51, 255)"],
        [0.6, "rgb(178, 102, 255)"],
        [0.7, "rgb(204, 153, 255)"],
        [1, "rgb(236, 216, 239)"]
    ],
    autocolorscale = False,
    reversescale = True,
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(180,180,180)',
            width = 0.5
        )),
    colorbar = go.choropleth.ColorBar(
        tickprefix = '',
        title = 'Count of bronze medals'),
)]
layout1 = go.Layout(
autosize=False,
        width=1400, height=500,
        margin=dict( l=150, r=150, b=0, t=50, pad=4, autoexpand=True ),
    title = go.layout.Title(
        text = 'Bronze medals won by countries'
    ),
    geo = go.layout.Geo(
        showframe = False,
        showcoastlines = False,
        projection = go.layout.geo.Projection(
            type = 'equirectangular'
        )
    ),
    annotations = [go.layout.Annotation(
        x = 0.55,
        y = 0.1,
        xref = 'paper',
        yref = 'paper',
        text = '',
        showarrow = False
    )]
)
fig1 = go.Figure(data = data1, layout = layout1)

#Silver Map
data2 = [go.Choropleth(
    locations = silver['NOC'],
    z = silver['count'],
    text = "Silver Medals",
    colorscale = [
        [0, "rgb(51, 0, 25)"],
        [0.35, "rgb(153, 0, 76)"],
        [0.5, "rgb(255, 0, 157)"],
        [0.6, "rgb(255, 102, 178)"],
        [0.7, "rgb(255, 204, 229)"],
        [1, "rgb(255, 236, 246)"]
    ],
    autocolorscale = False,
    reversescale = True,
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(180,180,180)',
            width = 0.5
        )),
    colorbar = go.choropleth.ColorBar(
        tickprefix = '',
        title = 'Count of silver medals'),
)]
layout2 = go.Layout(
autosize=False,
        width=1400, height=500,
        margin=dict( l=150, r=150, b=0, t=50, pad=4, autoexpand=True ),
    title = go.layout.Title(
        text = 'Silver medals won by countries'
    ),
    geo = go.layout.Geo(
        showframe = False,
        showcoastlines = False,
        projection = go.layout.geo.Projection(
            type = 'equirectangular'
        )
    ),
    annotations = [go.layout.Annotation(
        x = 0.55,
        y = 0.1,
        xref = 'paper',
        yref = 'paper',
        text = '',
        showarrow = False
    )]
)
fig2 = go.Figure(data = data2, layout = layout2)

#Gold map
data3 = [go.Choropleth(
    locations = gold['NOC'],
    z = gold['count'],
    text = "Gold Medals",
    colorscale = [
        [0, "rgb(255, 130,4)"],
        [0.35, "rgb(185, 101, 5)"],
        [0.5, "rgb(243, 144, 31)"],
        [0.6, "rgb(252, 194, 129)"],
        [0.7, "rgb(246, 210, 92)"],
        [1, "rgb(250, 247, 235)"]
    ],
    autocolorscale = False,
    reversescale = True,
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(180,180,180)',
            width = 0.5
        )),
    colorbar = go.choropleth.ColorBar(
        tickprefix = '',
        title = 'Count of gold medals'),
)]
layout3 = go.Layout(
	autosize=False,
        width=1400, height=500,
        margin=dict( l=150, r=150, b=0, t=50, pad=4, autoexpand=True ),
    title = go.layout.Title(
        text = 'Gold medals won by countries'
    ),
    geo = go.layout.Geo(
        showframe = False,
        showcoastlines = False,
        projection = go.layout.geo.Projection(
            type = 'equirectangular'
        )
    ),
    annotations = [go.layout.Annotation(
        x = 0.55,
        y = 0.1,
        xref = 'paper',
        yref = 'paper',
        text = '',
        showarrow = False
    )]
)
fig3 = go.Figure(data = data3, layout = layout3)

#Map each non-numerical value to a numerical value for correlation
for x in heatmapd.columns:
    if heatmapd[x].dtypes=='object':
       heatmapd[x]=le.fit_transform(heatmapd[x].astype(str))
corr = heatmapd.corr()
heatmapsu = go.Heatmap(
                       x=corr.columns,
                       y=corr.columns,
					   z=corr.values,
					   colorscale = 'Viridis')  
heatmapdata=[heatmapsu]
heatmaplayout = go.Layout(autosize=True,
                       width=900, 
                       height=700,
					   margin=dict( l=170, r=170, b=50, t=50, pad=4, autoexpand=True ),
						
                       title='Feature Correlation Map')
heatmapfig = go.Figure(data=heatmapdata,layout=heatmaplayout)

#BAR CHART FEMALES VS MALES OVER THE YEARS
femalestrace = go.Scatter(
    x=females['Year'],
    y=females['count'],
	    mode = 'lines',
    name='Females',
)
malestrace = go.Scatter(
    x=males['Year'],
    y=males['count'],
	    mode = 'lines',
    name='Males'
)
genderdata = [femalestrace,malestrace]
genderslayout= go.Layout(
    xaxis=dict(tickangle=-45),
    barmode='group',
	title='Count of F/M participants over the years'
)
gendersfig = go.Figure(data=genderdata,layout=genderslayout)

#BOX PLOTS
tracemheight = go.Box(
    x = malemedalists['Height'],
    name = "Height",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(7,40,89)'),
    line = dict(
        color = 'rgb(7,40,89)'),
)
tracemweight = go.Box(
    x = malemedalists['Weight'],
    name = "Weight",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(8,81,156)',
        ),
    line = dict(
        color = 'rgb(8,81,156)')
)
tracemage = go.Box(
    x=malemedalists['Age'],
    name = "Age",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(107,174,214)'),
    line = dict(
        color = 'rgb(107,174,214)')
)
malelayoutbox = go.Layout(
    title = "Box Plot Male Medalists Outliers"
)
maledatabox = [tracemage,tracemweight,tracemheight]
malebox = go.Figure(data=maledatabox, layout=malelayoutbox)
tracefheight = go.Box(
    x = femalemedalists['Height'],
    name = "Height",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(153,0,0)'),
    line = dict(
        color = 'rgb(153,0,0)'),
)
tracefweight = go.Box(
    x = femalemedalists['Weight'],
    name = "Weight",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(255,0,255)',
        ),
    line = dict(
        color = 'rgb(255,0,255)')
)
tracefage = go.Box(
    x=femalemedalists['Age'],
    name = "Age",
    boxpoints = 'outliers',
    marker = dict(
        color = 'rgb(102,0,51)'),
    line = dict(
        color = 'rgb(102,0,51)')
)
femaledatabox = [tracefage,tracefweight,tracefheight]

femalelayoutbox = go.Layout(
    title = "Box Plot Female Medalists Outliers"
)
femalebox = go.Figure(data=femaledatabox, layout=femalelayoutbox)

#MAIN LAYOUT
app.layout = html.Div([
	html.H3("Choose the category to show"),
    dcc.Dropdown(
        id="my-input",
        options = [
            {'label':'Map: Medals won by countries', 'value':'1'},
            {'label':'Plots', 'value':'2'},
			{'label':'Figures', 'value':'3'},
			{'label':'Graphs', 'value':'5'},
			{'label':'Statistics of participants in Olympics', 'value':'6'},
			{'label':'Prediction', 'value':'4'},
        ],
		#default value
        value = '1'
    ),
	#value 1
	 html.Div(
        id="map_total", 
        children = [
        dcc.Graph(id = 'plot_id', figure = fig) ,
		dcc.Graph(id = 'bronze_map', figure = fig1), 
		dcc.Graph(id = 'silver_map', figure = fig2), 
		dcc.Graph(id = 'gold_map', figure = fig3),

	]),
	#value2
	 html.Div(
        id="dd_plots", 
        children = [
		dcc.Graph(id = 'malebox_plot', figure = malebox), # dropdown
		dcc.Graph(id = 'femalebox_plot', figure = femalebox), # dropdown
	]),
	#value 3
	html.Div(
        id="dd_figures", 
        children = [
		dcc.Graph(id = 'heat_map', figure = heatmapfig), # dropdown
	]),
	#value 4
	html.Div(
        id="dd_prediction", 
        children = [
		html.H2('Prediction in the Jupyter Notebook!'),
	]),
	#value 6
	html.Div(
        id="statistic_sports", 

		style={'textAlign':'center'},
        children = [
		html.H4("Statistics of unique participants in Olympics"),
		html.H5('All sports, unique participants from {} to {}'.format(genders.Year.min(),genders.Year.max())),
        html.P('Height Median: {0:.2f}'.format(dropduplicates['Height'].median())),
        html.P('Height Mean: {0:.2f}'.format(dropduplicates['Height'].mean())),
		html.P('Age Median: {0:.2f}'.format(dropduplicates['Age'].median())),
        html.P('Age Mean: {0:.2f}'.format(dropduplicates['Age'].mean())),
		html.P('Weight Median: {0:.2f}'.format(dropduplicates['Weight'].median())),
        html.P('Weight Mean: {0:.2f}'.format(dropduplicates['Weight'].mean())),
		html.P('Total Participants: {0:.0f}'.format(genders['count'].sum())),

		html.H5('Filter statistics'),
        dcc.Dropdown(
                id='dd_sports',
                options=[{'label': i, 'value': i} for i in available_indicators],
				value='1',
                placeholder="Select a sport"
         ),
		 dcc.Dropdown(
                id='dd_medal',
				options = [
            {'label':'No medals', 'value':'non-medalist'},
            {'label':'All participants', 'value':'participants'},
			{'label':'Gold', 'value':'Gold medalist'},
			{'label':'Silver', 'value':'Silver medalist'},
			{'label':'Bronze', 'value':'Bronze medalist'},],
				value='participant(s)',
                placeholder="Select the medal",
         ),
		 dcc.Dropdown(
                id='dd_attributes',
                options = [
            {'label':'Age', 'value':'Age'},
            {'label':'Height/cm', 'value':'Height'},
			{'label':'Weight/KG', 'value':'Weight'},
        ],
		value='1',
        placeholder="Select an attribute",
		),
		dcc.Dropdown(
                id='dd_genders',
                options = [
            {'label':'All genders', 'value':''},
            {'label':'Female/F', 'value':'F'},
			{'label':'Male/M', 'value':'M'},
        ],
		value='',
        placeholder="Select a gender",
         ),
	]),
	html.Div(id='my-div'),

	#value 5
	 html.Div(
        id="year_graph", 
        children = [
		dcc.Graph(id = 'genders_bar', figure = gendersfig), # dropdown
		#dcc.Graph(id = '3dcluster', figure = kfig), # dropdown

		  dcc.Graph(id='graph-with-slider'),
				dcc.Slider(
				id='year-slider',
				min=df['Year'].min(),
				max=df['Year'].max(),
				value=df['Year'].min(),
				marks={str(Year): str(Year) for Year in df['Year'].unique()}
			)
    ]),
])

#MAIN UPDATE CALLBACKS
#Statistic page
@app.callback(Output(component_id='my-div', component_property='children'), [Input('my-input', 'value'),Input('dd_sports', 'value'),Input('dd_medal','value'),Input('dd_attributes','value'),Input('dd_genders','value')])
def update_plot(my_input,sports_input,medal_input,attributes_input,genders_input):
	text = ''
	filtered_df=dropduplicates.copy()
	filtered_df['Medal'] = filtered_df['Medal'].fillna('None')	
	filtered_df['Height'] = filtered_df['Height'].fillna('None')	
	filtered_df['Weight'] = filtered_df['Weight'].fillna('None')	

	if my_input=='6':
		median = mean = -1
		print(sports_input)
		if (sports_input != 'All sports') and (sports_input != '1') :
			filtered_df = filtered_df[filtered_df.Sport == sports_input]
		if (medal_input!='participant(s)') and (medal_input!='non-medalist') and (medal_input!='all participants'):
			if (medal_input == 'Gold medalist'):
				filtered_df = filtered_df[filtered_df.Medal == 'Gold']
			if (medal_input == 'Silver medalist'):
				filtered_df = filtered_df[filtered_df.Medal == 'Silver']
			if (medal_input == 'Bronze medalist'):
				filtered_df = filtered_df[filtered_df.Medal == 'Bronze']
		if (medal_input=='non-medalist')and (medal_input!='all participants'):
			filtered_df = filtered_df[filtered_df.Medal == 'None']

		if (genders_input == 'F') or (genders_input =='M') :
			filtered_df = filtered_df[filtered_df.Sex == genders_input]

		#ATTRIBUTES ARE NEEDED FOR SHOWING STATS
		#NULL VALUES NOT DROPPED AS WE WANT THE NUMBER OF ALL PARTICIPANTS TO STAY CONSISTENT IN EACH ATTRIBUTE
		#EG. SOME PARTICIPANTS MAY HAVE ONLY AGE AND NOT THE REST AND THEY WILL BE DROPPED IN THE OTHER ATTRIBUTES
		if attributes_input =='Age':
			#filtered_df = filtered_df.dropna(subset=['Age'])
			filtered_df['Age'].replace('None', np.nan, inplace=True)			
			median = filtered_df['Age'].median()
			mean = filtered_df['Age'].mean()
		if attributes_input =='Height':
			filtered_df['Height'].replace('None', np.nan, inplace=True)	
			median = filtered_df['Height'].median()
			mean = filtered_df['Height'].mean()
		if attributes_input =='Weight':
			filtered_df['Weight'].replace('None', np.nan, inplace=True)	
			median = filtered_df['Weight'].median()
			mean = filtered_df['Weight'].mean()
		
		if (sports_input == 'All sports') or (sports_input == '1'):
			if (median >= 0) and (mean >= 0):
					return [
						html.P('{} statistics for all sports, {} {} {}'.format(attributes_input,filtered_df['ID'].count(),medal_input,genders_input)),
						html.P('Median: {0:.2f}'.format(median)),
						html.P('Mean: {0:.2f}'.format(mean)),
						dash_table.DataTable(
								id='table',
								columns=[{"id": i, "name": i} for i in filtered_df.columns],
								data=filtered_df.to_dict("rows"),
								 style_table={
									'height': '700px',
									'overflowY': 'scroll',
									'border': 'thin lightgrey solid'
									},),
						]
		elif (sports_input != 'All sports') and (sports_input != '1'):
			if (median >= 0) and (mean >= 0):
				
				return [
							html.P('{} statistics for {}, {} {} {}'.format(attributes_input,sports_input, filtered_df['ID'].count(),medal_input, genders_input )),
							html.P('Median: {0:.2f}'.format(median)),
							html.P('Mean: {0:.2f}'.format(mean)),
							dash_table.DataTable(
								id='table',
								columns=[{"id": i, "name": i} for i in filtered_df.columns],
								data=filtered_df.to_dict("rows"),
								 style_table={
									'height': '700px',
									'overflowY': 'scroll',
									'border': 'thin lightgrey solid'
									},),
							]
			else:
				if (attributes_input!='1'):
					if (filtered_df['ID'].count() >= 1):
						return [
			html.P('{} statistics for {}, {} {} {}'.format(attributes_input,sports_input, filtered_df['ID'].count(),medal_input, genders_input )),
			html.P('Not enough data to calculate median and mean'),
			dash_table.DataTable(
								id='table',
								columns=[{"id": i, "name": i} for i in filtered_df.columns],
								data=filtered_df.to_dict("rows"),
								 style_table={
									'height': '700px',
									'overflowY': 'scroll',
									'border': 'thin lightgrey solid'
									},),
			]
		#SHOWS TABLE EVERYTIME DROP DOWN CHANGES
		if (filtered_df['ID'].count() >= 1):
			return [
					dash_table.DataTable(
								id='table',
								columns=[{"id": i, "name": i} for i in filtered_df.columns],
								data=filtered_df.to_dict("rows"),
								 style_table={
									'height': '700px',
									'overflowY': 'scroll',
									'border': 'thin lightgrey solid'
									},),
			]
		else:
			return [
			html.P('No results found'),
			html.P('Not enough data to calculate median and mean')]

#Graph with year
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = dropduplicates[dropduplicates.Year == selected_year]

    traces = []
    for i in filtered_df.Medal.unique():
        df_by_continent = filtered_df[filtered_df['Medal'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['Age'],
            y=df_by_continent['Weight'],
            text=df_by_continent['Team'].astype(str) + " " + df_by_continent['Sex'].astype(str) + df_by_continent['Sport'].astype(str),
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'Age'},
            yaxis={'title': 'Weight', 'range': [0, 200]},
			width=1400, height=600,
            margin={'l': 150, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
#show/hide on dropdown
@app.callback(Output('map_total', 'style'), [Input('my-input', 'value')])
def hide_graph(my_input):
    if my_input=='1':
        return {'display':'block'}
    return {'display':'none'}
	
@app.callback(Output('year_graph', 'style'), [Input('my-input', 'value')])
def hide_graph(my_input):
    if my_input=='5':
        return {'display':'block'}
    return {'display':'none'}
	
@app.callback(Output('dd_plots', 'style'), [Input('my-input', 'value')])
def hide_graph(my_input):
    if my_input=='2':
        return {'display':'block'}
    return {'display':'none'}
	
@app.callback(Output('dd_figures', 'style'), [Input('my-input', 'value')])
def hide_graph(my_input):
    if my_input=='3':
        return {'display':'block'}
    return {'display':'none'}
	
@app.callback(Output('dd_prediction', 'style'), [Input('my-input', 'value')])
def hide_graph(my_input):
    if my_input=='4':
        return {'display':'block'}
    return {'display':'none'}

@app.callback(Output('statistic_sports', 'style'), [Input('my-input', 'value'),Input('dd_sports', 'value'),Input('dd_medal','value'),Input('dd_attributes','value')])
def hide_graph(my_input,sports_input,medal_input,attributes_input):
    if my_input=='6':
        return {'display':'block'}
    return {'display':'none'}

if __name__ == '__main__':
	app.run_server()
