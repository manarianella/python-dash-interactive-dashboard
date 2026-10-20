import plotly.express as px
from dash import Dash, Input, Output, State, ctx, dcc, html

# Charger les données et récupérer les années disponibles.
gapminder = px.data.gapminder()
years = sorted(int(year) for year in gapminder["year"].unique())

data = {
    year: gapminder.query("year == @year")
    for year in years
}

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            id="title",
            style={"textAlign": "center", "color": "#167D9A"},
        ),
        html.Label("Choisis une année :"),
        dcc.Slider(
            id="year-slider",
            min=min(years),
            max=max(years),
            marks={year: str(year) for year in years},
            step=None,
            value=2002,
        ),
        html.Div(
            children=[
                html.Button("Play", id="play-button", n_clicks=0),
                html.Button("Pause", id="pause-button", n_clicks=0),
            ],
            style={"textAlign": "center", "margin": "20px"},
        ),
        html.Label("Vitesse de défilement :"),
        dcc.Dropdown(
            id="speed-dropdown",
            options=[
                {"label": "Lente : une année toutes les 2 secondes", "value": 2000},
                {"label": "Normale : une année par seconde", "value": 1000},
                {"label": "Rapide : une année toutes les 0,5 seconde", "value": 500},
            ],
            value=1000,
            clearable=False,
        ),
        dcc.Graph(id="graph1"),
        html.Div(id="description"),
        dcc.Interval(
            id="interval",
            interval=1000,
            n_intervals=0,
            disabled=True,
        ),
    ]
)


@app.callback(
    Output("graph1", "figure"),
    Output("title", "children"),
    Output("description", "children"),
    Input("year-slider", "value"),
)
def update_dashboard(selected_year):
    """Actualiser le graphique et les textes."""
    figure = px.scatter(
        data[selected_year],
        x="gdpPercap",
        y="lifeExp",
        color="continent",
        size="pop",
        hover_name="country",
    )

    title = (
        f"Espérance de vie et PIB par habitant ({selected_year})"
    )

    description = (
        f"Ce graphique présente les données de {selected_year}. "
        "Chaque bulle représente un pays. "
        "L'axe horizontal indique le PIB par habitant et "
        "l'axe vertical indique l'espérance de vie. "
        "La couleur correspond au continent et "
        "la taille représente la population."
    )

    return figure, title, description


@app.callback(
    Output("interval", "disabled"),
    Input("play-button", "n_clicks"),
    Input("pause-button", "n_clicks"),
    prevent_initial_call=True,
)
def control_animation(play_clicks, pause_clicks):
    """Activer ou désactiver le minuteur selon le bouton cliqué."""
    return ctx.triggered_id == "pause-button"


@app.callback(
    Output("year-slider", "value"),
    Input("interval", "n_intervals"),
    State("year-slider", "value"),
    prevent_initial_call=True,
)
def next_year(n_intervals, current_year):
    """Passer à l'année suivante et revenir au début après 2007."""
    current_index = years.index(current_year)
    next_index = (current_index + 1) % len(years)

    return years[next_index]

@app.callback(
    Output("interval", "interval"),
    Input("speed-dropdown", "value"),
)
def update_speed(duration):
    """Modifier le délai entre deux changements d'année."""
    return duration

if __name__ == "__main__":
    app.run(debug=True)