print("🔥 DASHBOARD FILE LOADED 🔥")

# ---------------- IMPORTS ----------------
import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from sqlalchemy import create_engine, text

# ---------------- DATABASE ----------------
DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/health_fitness_db"
engine = create_engine(DATABASE_URL)

# ---------------- HELPERS ----------------
def kpi_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="text-muted"),
            html.H3(value)
        ]),
        color=color,
        inverse=True
    )

# ---------------- APP INIT ----------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# ---------------- LAYOUT ----------------
app.layout = dbc.Container(fluid=True, children=[

    html.H1("💪 Health & Fitness Dashboard", className="text-center my-4"),

    dbc.Row(
        dbc.Col(
            dbc.Input(
                id="user-input",
                placeholder="Enter user name",
                value="Sam",
                debounce=True
            ),
            width=4
        ),
        justify="center"
    ),

    html.Hr(),

    # KPIs
    dbc.Row([
        dbc.Col(id="kpi-calories", md=3),
        dbc.Col(id="kpi-sleep", md=3),
        dbc.Col(id="kpi-workouts", md=3),
        dbc.Col(id="kpi-mood", md=3),
    ], className="mb-4"),

    # TABS
    dbc.Tabs([
        dbc.Tab(label="🔥 Calories", tab_id="calories"),
        dbc.Tab(label="😴 Sleep", tab_id="sleep"),
        dbc.Tab(label="🏋️ Workouts", tab_id="workouts"),
        dbc.Tab(label="😊 Moods", tab_id="moods"),
    ], id="tabs", active_tab="calories"),

    html.Div(id="tab-content", className="p-4"),

    # ADD DATA
    dbc.Row([

        dbc.Col(dbc.Card([
            html.H4("➕ Add Workout"),
            dbc.Input(id="workout-type", placeholder="Workout (e.g. Lunges)"),
            dbc.Input(id="workout-duration", type="number", placeholder="Duration (min)"),
            dbc.Button("Add Workout", id="add-workout-btn", color="info", className="mt-2"),
            html.Div(id="add-workout-msg", className="mt-2")
        ], body=True), md=6),

        dbc.Col(dbc.Card([
            html.H4("➕ Add Mood"),
            dcc.Dropdown(
                id="mood-value",
                options=[{"label": m, "value": m} for m in
                         ["Happy", "Energetic", "Stressed", "Sad", "Tired"]],
                placeholder="Select mood"
            ),
            dbc.Button("Add Mood", id="add-mood-btn", color="warning", className="mt-2"),
            html.Div(id="add-mood-msg", className="mt-2")
        ], body=True), md=6)

    ], className="mt-4"),

    dcc.Interval(id="refresh", interval=5000)

])

# ---------------- TAB CONTENT ----------------
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab(tab):
    return {
        "calories": dcc.Graph(id="calorie-graph"),
        "sleep": dcc.Graph(id="sleep-graph"),
        "workouts": dcc.Graph(id="workout-graph"),
        "moods": dcc.Graph(id="mood-graph"),
    }[tab]

# ---------------- KPI UPDATE ----------------
@app.callback(
    Output("kpi-calories", "children"),
    Output("kpi-sleep", "children"),
    Output("kpi-workouts", "children"),
    Output("kpi-mood", "children"),
    Input("user-input", "value"),
    Input("refresh", "n_intervals")
)
def update_kpis(name, _):

    calories = pd.read_sql("""
        SELECT COALESCE(SUM(calories),0)
        FROM calories c JOIN users u ON c.user_id=u.user_id
        WHERE u.name ILIKE %s
    """, engine, params=(name,)).iloc[0][0]

    sleep = pd.read_sql("""
        SELECT COALESCE(AVG(sleep_hours),0)
        FROM sleep s JOIN users u ON s.user_id=u.user_id
        WHERE u.name ILIKE %s
    """, engine, params=(name,)).iloc[0][0]

    workouts = pd.read_sql("""
        SELECT COUNT(*)
        FROM workouts w JOIN users u ON w.user_id=u.user_id
        WHERE u.name ILIKE %s
    """, engine, params=(name,)).iloc[0][0]

    mood_df = pd.read_sql("""
        SELECT mood FROM mood m
        JOIN users u ON m.user_id=u.user_id
        WHERE u.name ILIKE %s
        ORDER BY date DESC LIMIT 1
    """, engine, params=(name,))

    mood_value = mood_df.iloc[0][0] if not mood_df.empty else "N/A"

    return (
        kpi_card("Calories", int(calories), "danger"),
        kpi_card("Avg Sleep (hrs)", round(sleep, 1), "info"),
        kpi_card("Workouts", workouts, "primary"),
        kpi_card("Current Mood", mood_value, "warning")
    )

# ---------------- GRAPHS ----------------
@app.callback(Output("calorie-graph", "figure"), Input("user-input", "value"))
def calorie_graph(name):
    df = pd.read_sql("""
        SELECT date, SUM(calories) calories
        FROM calories c JOIN users u ON c.user_id=u.user_id
        WHERE u.name ILIKE %s GROUP BY date ORDER BY date
    """, engine, params=(name,))
    return px.bar(df, x="date", y="calories", template="plotly_dark")

@app.callback(Output("sleep-graph", "figure"), Input("user-input", "value"))
def sleep_graph(name):
    df = pd.read_sql("""
        SELECT date, sleep_hours
        FROM sleep s JOIN users u ON s.user_id=u.user_id
        WHERE u.name ILIKE %s ORDER BY date
    """, engine, params=(name,))
    return px.line(df, x="date", y="sleep_hours", markers=True, template="plotly_dark")

@app.callback(Output("workout-graph", "figure"), Input("user-input", "value"))
def workout_graph(name):
    df = pd.read_sql("""
        SELECT date, workout_type, calories_burned
        FROM workouts w JOIN users u ON w.user_id=u.user_id
        WHERE u.name ILIKE %s ORDER BY date
    """, engine, params=(name,))
    return px.bar(df, x="date", y="calories_burned",
                  color="workout_type",
                  template="plotly_dark",
                  title="Workout Calories Burned")

@app.callback(Output("mood-graph", "figure"), Input("user-input", "value"))
def mood_graph(name):
    df = pd.read_sql("""
        SELECT mood, COUNT(*) count
        FROM mood m JOIN users u ON m.user_id=u.user_id
        WHERE u.name ILIKE %s GROUP BY mood
    """, engine, params=(name,))
    return px.pie(df, names="mood", values="count", title="Mood Distribution")

# ---------------- ADD WORKOUT ----------------
@app.callback(
    Output("add-workout-msg", "children"),
    Input("add-workout-btn", "n_clicks"),
    State("user-input", "value"),
    State("workout-type", "value"),
    State("workout-duration", "value"),
    prevent_initial_call=True
)
def add_workout(_, name, wtype, duration):

    if not name or not wtype or not duration:
        return "Please fill all fields"

    with engine.begin() as conn:
        # ensure user exists
        conn.execute(text("""
            INSERT INTO users (name)
            SELECT :n
            WHERE NOT EXISTS (
                SELECT 1 FROM users WHERE name ILIKE :n
            )
        """), {"n": name})

        # insert workout
        conn.execute(text("""
            INSERT INTO workouts (user_id, workout_type, duration, calories_burned, date)
            SELECT user_id, :w, :d,
                   CASE LOWER(:w)
                     WHEN 'lunges' THEN 230
                     WHEN 'jumping jacks' THEN 200
                     WHEN 'squats' THEN 250
                     ELSE 150
                   END,
                   CURRENT_DATE
            FROM users WHERE name ILIKE :n
        """), {"w": wtype, "d": duration, "n": name})

    return "✅ Workout added!"


# ---------------- ADD MOOD ----------------
@app.callback(
    Output("add-mood-msg", "children"),
    Input("add-mood-btn", "n_clicks"),
    State("user-input", "value"),
    State("mood-value", "value"),
    prevent_initial_call=True
)
def add_mood(_, name, mood):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO mood (user_id, mood, date)
            SELECT user_id, :m, CURRENT_DATE FROM users WHERE name ILIKE :n
        """), {"m": mood, "n": name})
    return "😊 Mood logged!"

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)
