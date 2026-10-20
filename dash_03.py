import plotly.express as px
from dash import Dash, Input, Output, dcc, html

# Charger les données.
gapminder = px.data.gapminder()

# Récupérer automatiquement les années disponibles.
years = sorted(int(year) for year in gapminder["year"].unique())

# Ranger les données dans un dictionnaire, par année.
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
        dcc.Graph(id="graph1"),
        html.Div(id="description"),
    ]
)


@app.callback(
    Output("graph1", "figure"),
    Output("title", "children"),
    Output("description", "children"),
    Input("year-slider", "value"),
)
def update_dashboard(selected_year):
    """Actualiser le graphique et les textes selon l'année choisie."""
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


if __name__ == "__main__":
    app.run(debug=True)