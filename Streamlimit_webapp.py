import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Police Department Incidents",
    page_icon="🚨",
    layout="wide"
)

df = pd.read_csv('PD_Incident_Reports.csv')
df['Hour'] = pd.to_datetime(df['Incident Time'],format="%H:%M").dt.hour
    

#Sidebar
st.sidebar.header('Selecciona un filtro:')
PoliceDistrict = st.sidebar.multiselect(
    "Choose The Police District",
    options=df['Police District'].unique(),
    default=df['Police District'].unique()
)

IncidentCategory = st.sidebar.multiselect(
    "Choose The Category of the Incident",
    options=df['Incident Category'].unique(),
    default=df['Incident Category'].unique()
)

Resolution = st.sidebar.multiselect(
    "Choose the status",
    options=df['Resolution'].unique(),
    default=df['Resolution'].unique()
)

IncidentYear = st.sidebar.multiselect(
    "Choose a Year",
    options=df['Incident Year'].unique(),
    default=df['Incident Year'].unique()
)


df_selection = df.query('`Police District` == @PoliceDistrict & `Incident Category` == @IncidentCategory & `Incident Year` == @IncidentYear & Resolution == @Resolution ' )






## Main page

st.title('🚨 Police Departments Incidents')
#st.markdown("##")

# Top kpis

Total_Crimes= int(df_selection["Incident Category"].count())
Most_incidents = ", ".join(df_selection["Incident Category"].mode().tolist())
Avg_Resolution = ", ".join(df_selection["Resolution"].mode().tolist())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Crimes:")
    st.subheader(f"{Total_Crimes:,}")
with middle_column:
    st.subheader("Most Incidents:")
    st.subheader(f"👮‍♂️ {Most_incidents}")
with right_column:
    st.subheader("Average Resolution:")
    st.subheader(f"📂 {Avg_Resolution}")

st.markdown('---')


#df = pd.read_csv('PD_Incident_Reports.csv')

# Calcular las frecuencias de los incidentes por año
df_freq = df_selection['Incident Year'].value_counts().reset_index()
df_freq.columns = ['Incident Year', 'Frequency']

# Crear el gráfico de barras
fig_total_crimes = px.bar(df_freq, x='Incident Year', y='Frequency',
                          title='<b>Incidents per Year</b>', template='plotly_white')

fig_total_crimes.update_xaxes(title='Year')
fig_total_crimes.update_yaxes(title='Frequency')


fig_total_crimes.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)',  # Color de las líneas de la cuadrícula en el eje x
        tickmode='linear',  # Establece el modo de las marcas del eje x en números enteros
        tick0=0,  # Establece el primer número de la marca del eje x
        dtick=1  # Establece la separación entre las marcas del eje x
    )
)



df_Hours = df_selection['Hour'].value_counts().reset_index()
df_Hours.columns = ['Hour', 'Frequency']
import plotly.graph_objects as go

fig_C_H = go.Figure()

fig_C_H.add_trace(go.Bar(x=df_Hours['Hour'], y=df_Hours['Frequency'], marker=dict(color='skyblue')))

fig_C_H.update_layout(
    title='<b>Incidents per Hour</b>',
    xaxis_title='Hour',
    yaxis_title='Frequency',
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)',
        tickmode='linear',
        tick0=0,
        dtick=1,
        range=[-0.5, 23.5]
    ),
    bargap=0.1
)

import pandas as pd
import plotly.express as px

# Calcula la frecuencia de incidencias por ubicación
df_frequency = df.groupby(['Latitude', 'Longitude']).size().reset_index(name='Frequency')

fig_map = px.scatter_mapbox(df_frequency,
                            lat='Latitude',
                            lon='Longitude',
                            color='Frequency',
                            color_continuous_scale='YlOrRd',
                            range_color=(0, df_frequency['Frequency'].max()),
                            mapbox_style='carto-positron',
                            zoom=10,
                            center={'lat': df_frequency['Latitude'].mean(), 'lon': df_frequency['Longitude'].mean()},
                            opacity=0.7,
                            labels={'Frequency': 'Frequency of Incidents'}
                            )

fig_map.update_layout(title='<b>Incident Frequency Map</b>',
                      plot_bgcolor="rgba(0,0,0,0)"
                      )





left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_total_crimes, use_container_width=True)
right_column.plotly_chart(fig_C_H, use_container_width=True)

# Mostrar el mapa abajo y centrado
st.plotly_chart(fig_map, use_container_width=True, height= 1200 )


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


