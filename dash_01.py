import plotly.express as px
from dash import Dash, dcc, html

# Charger les données et les regrouper par année.
gapminder = px.data.gapminder()
years = gapminder["year"].unique()

data = {
    year: gapminder.query("year == @year")
    for year in years
}

# Choisir l'année affichée.
year = 2002

# Créer l'application.
app = Dash(__name__)

# Construire le graphique.
fig = px.scatter(
    data[year],
    x="gdpPercap",
    y="lifeExp",
    color="continent",
    size="pop",
    hover_name="country",
)

# Organiser les éléments de la page.
app.layout = html.Div(
    children=[
        html.H1(
            children=f"Espérance de vie et PIB par habitant ({year})",
            style={"textAlign": "center", "color": "#167D9A"},
        ),
        dcc.Graph(
            id="graph1",
            figure=fig,
        ),
        html.Div(
            children=(
                f"Ce graphique présente les données de {year}. "
                "Chaque bulle représente un pays. "
                "Sa couleur indique son continent et sa taille "
                "représente sa population. "
                "Survolez les bulles pour afficher les détails."
            ),
        ),
    ]
)

# Démarrer le serveur lorsque ce fichier est exécuté.
if __name__ == "__main__":
    app.run(debug=True)