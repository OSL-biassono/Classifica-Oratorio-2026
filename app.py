import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from io import BytesIO
st.logo("Loghi/Logo Oratorio S.Luigi - Scritte Nere.png")
col = "F"
title_text = "Classifica Generale"
options = ["Generale", "Prima Fascia", "Seconda Fascia", "Terza Fascia", "Quarta Fascia"]
url = "https://parrocchiabiassono-my.sharepoint.com/:x:/g/personal/coordinatori_parrocchiabiassono_it/IQAttF3fvJItQIQj3bVil1hdAbnmhbu8VLlNzdkkDOPFq3Q?e=282CWQ&download=1"
color_map = {
    "Gialli": "#FFD700",
    "Verdi":  "#2ecc71",
    "Rossi":  "#e74c3c",
    "Blu":    "#3498db"
}
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers, allow_redirects=True)

selection = st.segmented_control("Classifiche", options, selection_mode="single")
if selection == "Generale":
    col = "F"
    title_text = "Classifica Generale"
elif selection == "Prima Fascia":
    col = "B"
    title_text = "Classifica della Prima Fascia"
elif selection == "Seconda Fascia":
    col = "C"
    title_text = "Classifica della Seconda Fascia"
elif selection == "Terza Fascia":
    col = "D"
    title_text = "Classifica della Terza Fascia"
elif selection == "Quarta Fascia":
    col = "E"
    title_text = "Classifica della Quarta Fascia"

df = pd.read_excel(BytesIO(response.content), sheet_name="db", usecols="A," + col, index_col="Classifica")
colori = [color_map.get(squadra, "#ffffff") for squadra in df.index]

st.write("""
        # Classifica Oratorio Feriale 2026
        *""" + title_text + """*""")
fig = go.Figure(go.Bar(
    x=df.iloc[:, 0],
    y=df.index,
    orientation='h',
    marker=dict(color=colori),
    text=df.iloc[:, 0],
    textposition='inside',
    insidetextanchor="end",
    textfont=dict(size=16)
))
fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True)
st.plotly_chart(fig, use_container_width=True, config={
    "modeBarButtonsToRemove": [
        "zoom2d",
        "select2d",
        "lasso2d",
    ],
    "scrollZoom": False,  # disabilita zoom con scroll del mouse
    "doubleClick": False,
})
