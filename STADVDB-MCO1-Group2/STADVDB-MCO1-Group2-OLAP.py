import mysql.connector
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import time

# Predefined temporary tables
TEMP_TABLES = [
    """
    CREATE TEMPORARY TABLE temp_genre_location_boxoffice AS (
        SELECT
            fm.Genre,
            dt.Location,
            SUM(fs.BoxOffice) AS TotalBoxOffice
        FROM
            factshowing fs
        JOIN
            factmovie fm ON fs.MovieID = fm.MovieID
        JOIN
            dimtheater dt ON fs.TheaterID = dt.TheaterID
        GROUP BY
            fm.Genre, dt.Location
    );
    """,
    """
    CREATE INDEX idx_genre_location ON temp_genre_location_boxoffice(Genre, Location);
    """,
    """
    CREATE TEMPORARY TABLE temp_location_theater_genre_title AS (
        SELECT
            dt.Location,
            dt.TheaterName,
            fm.Genre,
            fm.Title,
            SUM(fs.BoxOffice) AS TotalBoxOffice
        FROM
            factshowing fs
        JOIN
            factmovie fm ON fs.MovieID = fm.MovieID
        JOIN
            dimtheater dt ON fs.TheaterID = dt.TheaterID
        GROUP BY
            dt.Location, dt.TheaterName, fm.Genre, fm.Title
    );
    """,
    """
    CREATE INDEX idx_loc_thet_genre ON temp_location_theater_genre_title(Genre, Location, TheaterName, Title);
    """,
    """
    CREATE TEMPORARY TABLE temp_r_rated_title_boxoffice AS (
        SELECT
            fm.Title,
            fm.MovieRating,
            SUM(fs.BoxOffice) AS TotalBoxOffice
        FROM
            factshowing fs
        JOIN
            factmovie fm ON fs.MovieID = fm.MovieID
        WHERE
            fm.MovieRating = 'R'
        GROUP BY
            fm.Title, fm.MovieRating
    );
    """,
    """
    CREATE INDEX idx_Rrated_title ON temp_r_rated_title_boxoffice(MovieRating, Title);
    """,
    """
    CREATE TEMPORARY TABLE temp_r_rated_ny_boxoffice AS (
        SELECT
            fm.Title,
            fm.MovieRating,
            dt.Location,
            SUM(fs.BoxOffice) AS TotalBoxOffice
        FROM
            factshowing fs
        JOIN
            factmovie fm ON fs.MovieID = fm.MovieID
        JOIN
            dimtheater dt ON fs.TheaterID = dt.TheaterID
        WHERE
            fm.MovieRating = 'R'
            AND dt.Location = 'New York'
        GROUP BY
            fm.Title, fm.MovieRating, dt.Location
    );
    """,
    """
    CREATE INDEX idx_r_rated_ny ON temp_r_rated_ny_boxoffice(MovieRating, Title, Location);
    """,
    """
    CREATE TEMPORARY TABLE temp_titles_cities_boxoffice AS (
        SELECT
            fm.Title,
            SUM(CASE WHEN dt.Location = 'Chicago' THEN fs.BoxOffice ELSE 0 END) AS Chicago,
            SUM(CASE WHEN dt.Location = 'Dallas' THEN fs.BoxOffice ELSE 0 END) AS Dallas,
            SUM(CASE WHEN dt.Location = 'Houston' THEN fs.BoxOffice ELSE 0 END) AS Houston,
            SUM(CASE WHEN dt.Location = 'Los Angeles' THEN fs.BoxOffice ELSE 0 END) AS LosAngeles,
            SUM(CASE WHEN dt.Location = 'Miami' THEN fs.BoxOffice ELSE 0 END) AS Miami,
            SUM(CASE WHEN dt.Location = 'New York' THEN fs.BoxOffice ELSE 0 END) AS NewYork,
            SUM(CASE WHEN dt.Location = 'Orlando' THEN fs.BoxOffice ELSE 0 END) AS Orlando,
            SUM(CASE WHEN dt.Location = 'Philadelphia' THEN fs.BoxOffice ELSE 0 END) AS Philadelphia,
            SUM(CASE WHEN dt.Location = 'San Diego' THEN fs.BoxOffice ELSE 0 END) AS SanDiego,
            SUM(CASE WHEN dt.Location = 'San Francisco' THEN fs.BoxOffice ELSE 0 END) AS SanFrancisco
        FROM
            factshowing fs
        JOIN
            dimtheater dt ON fs.TheaterID = dt.TheaterID
        JOIN
            factmovie fm ON fs.MovieID = fm.MovieID
        GROUP BY
            fm.Title
    );
    """,
    """
    CREATE INDEX idx_titles_cities_boxoffice ON temp_titles_cities_boxoffice(Title);
    """,
    """
    CREATE TEMPORARY TABLE temp_salary_agent_gender AS (
        SELECT
            dage.AgentName,
            dact.Gender,
            SUM(fmc.Salary) AS TotalSalary
        FROM
            factmoviecast fmc
        JOIN
            dimactor dact ON fmc.ActorID = dact.ActorID
        JOIN
            dimagent dage ON dact.AgentID = dage.AgentID
        GROUP BY
            dage.AgentName, dact.Gender
    );
    """,
    """
    CREATE INDEX idx_salary_agent_gender ON temp_salary_agent_gender(AgentName, Gender);
    """,
    """
    CREATE TEMPORARY TABLE temp_salary_gender_nationality_agent AS (
        SELECT
            dact.Gender,
            dact.Nationality,
            dage.AgentName,
            SUM(fmc.Salary) AS TotalSalary
        FROM
            factmoviecast fmc
        JOIN
            dimactor dact ON fmc.ActorID = dact.ActorID
        JOIN
            dimagent dage ON dact.AgentID = dage.AgentID
        GROUP BY
            dact.Gender, dact.Nationality, dage.AgentName
    );
    """,
    """
    CREATE INDEX idx_salary_gender_nationality_agent ON temp_salary_gender_nationality_agent(Gender, Nationality, AgentName);
    """,
    """
    CREATE TEMPORARY TABLE temp_salary_american_actors AS (
        SELECT
            dact.ActorName,
            dact.Nationality,
            SUM(fmc.Salary) AS TotalSalary
        FROM
            factmoviecast fmc
        JOIN
            dimactor dact ON fmc.ActorID = dact.ActorID
        WHERE
            dact.Nationality = 'American'
        GROUP BY
            dact.ActorName, dact.Nationality
    );
    """,
    """
    CREATE INDEX idx_salary_american_actors ON temp_salary_american_actors(ActorName);
    """,
    """
    CREATE TEMPORARY TABLE temp_salary_american_actors_agent AS (
        SELECT
            dact.ActorName,
            dact.Nationality,
            dage.AgentName,
            SUM(fmc.Salary) AS TotalSalary
        FROM
            factmoviecast fmc
        JOIN
            dimactor dact ON fmc.ActorID = dact.ActorID
        JOIN
            dimagent dage ON dact.AgentID = dage.AgentID
        WHERE
            dact.Nationality = 'American'
            AND dage.AgentName = 'Creative Artists'
        GROUP BY
            dact.ActorName, dact.Nationality, dage.AgentName
    );
    """,
    """
    CREATE INDEX idx_salary_american_actors_agent ON temp_salary_american_actors_agent(ActorName, AgentName);
    """,
    """
    CREATE TEMPORARY TABLE temp_salary_specific_actors AS (
        SELECT
            fm.Title,
            SUM(CASE WHEN fmc.ActorID = 'A0001' THEN fmc.Salary ELSE 0 END) AS AngelinaJolie,
            SUM(CASE WHEN fmc.ActorID = 'A0002' THEN fmc.Salary ELSE 0 END) AS BradPitt,
            SUM(CASE WHEN fmc.ActorID = 'A0003' THEN fmc.Salary ELSE 0 END) AS JohnnyDepp,
            SUM(CASE WHEN fmc.ActorID = 'A0004' THEN fmc.Salary ELSE 0 END) AS WillSmith,
            SUM(CASE WHEN fmc.ActorID = 'A0005' THEN fmc.Salary ELSE 0 END) AS TomCruise,
            SUM(CASE WHEN fmc.ActorID = 'A0006' THEN fmc.Salary ELSE 0 END) AS JuliaRoberts,
            SUM(CASE WHEN fmc.ActorID = 'A0007' THEN fmc.Salary ELSE 0 END) AS ChristianBale,
            SUM(CASE WHEN fmc.ActorID = 'A0008' THEN fmc.Salary ELSE 0 END) AS LeonardoDiCaprio,
            SUM(CASE WHEN fmc.ActorID = 'A0009' THEN fmc.Salary ELSE 0 END) AS CateBlanchett,
            SUM(CASE WHEN fmc.ActorID = 'A0010' THEN fmc.Salary ELSE 0 END) AS RussellCrowe,
            SUM(CASE WHEN fmc.ActorID = 'A0011' THEN fmc.Salary ELSE 0 END) AS KeiraKnightly,
            SUM(CASE WHEN fmc.ActorID = 'A0012' THEN fmc.Salary ELSE 0 END) AS MarionCotillard,
            SUM(CASE WHEN fmc.ActorID = 'A0013' THEN fmc.Salary ELSE 0 END) AS MerylStreep,
            SUM(CASE WHEN fmc.ActorID = 'A0014' THEN fmc.Salary ELSE 0 END) AS PierceBrosnan
        FROM
            factmoviecast fmc
        JOIN
            dimactor dact ON fmc.ActorID = dact.ActorID
        JOIN
            factmovie fm ON fmc.MovieID = fm.MovieID
        GROUP BY
            fm.Title
    );
    """,
    """
    CREATE INDEX idx_salary_specific_actors ON temp_salary_specific_actors(Title);
    """,
    """
    CREATE TEMPORARY TABLE temp_rating_movie_title AS (
        SELECT
            fm.Title,
            ROUND(AVG(fmr.ReviewRating), 1) AS OverallRating
        FROM
            factmoviereview fmr
        JOIN
            factmovie fm ON fmr.MovieID = fm.MovieID
        GROUP BY
            fm.Title
    );
    """,
    """
    CREATE INDEX idx_rating_movie_title ON temp_rating_movie_title(Title);
    """,
    """
    CREATE TEMPORARY TABLE temp_rating_reviewer_class_movie_rating_genre AS (
        SELECT
            dr.ReviewerClass,
            fm.MovieRating,
            fm.Genre,
            ROUND(AVG(fmr.ReviewRating), 1) AS OverallRating
        FROM
            factmoviereview fmr
        JOIN
            factmovie fm ON fmr.MovieID = fm.MovieID
        JOIN
            dimreviewer dr ON fmr.ReviewerID = dr.ReviewerID
        GROUP BY
            dr.ReviewerClass, fm.MovieRating, fm.Genre
    );
    """,
    """
    CREATE INDEX idx_rating_reviewer_class_movie_rating_genre ON temp_rating_reviewer_class_movie_rating_genre(ReviewerClass, MovieRating, Genre);
    """,
    """
    CREATE TEMPORARY TABLE temp_rating_r_rated_title AS (
        SELECT
            fm.Title,
            fm.MovieRating,
            ROUND(AVG(fmr.ReviewRating), 1) AS OverallRating
        FROM
            factmoviereview fmr
        JOIN
            factmovie fm ON fmr.MovieID = fm.MovieID
        WHERE
            fm.MovieRating = 'R'
        GROUP BY
            fm.Title, fm.MovieRating
    );
    """,
    """
    CREATE INDEX idx_rating_r_rated_title ON temp_rating_r_rated_title(Title, MovieRating);
    """,
    """
    CREATE TEMPORARY TABLE temp_rating_r_thriller_title AS (
        SELECT
            fm.Title,
            fm.MovieRating,
            fm.Genre,
            ROUND(AVG(fmr.ReviewRating), 1) AS OverallRating
        FROM
            factmoviereview fmr
        JOIN
            factmovie fm ON fmr.MovieID = fm.MovieID
        WHERE
            fm.MovieRating = 'R'
            AND fm.Genre = 'Thriller'
        GROUP BY
            fm.Title, fm.MovieRating, fm.Genre
    );
    """,
    """
    CREATE INDEX idx_rating_r_thriller_title ON temp_rating_r_thriller_title(Title, MovieRating, Genre);
    """,
    """
    CREATE TEMPORARY TABLE temp_rating_reviewer_movie_title AS (
        SELECT
            fm.Title,
            SUM(CASE WHEN fmr.ReviewerID = 'R-001' THEN fmr.ReviewRating ELSE 0 END) AS RogerEbert,
            SUM(CASE WHEN fmr.ReviewerID = 'R-002' THEN fmr.ReviewRating ELSE 0 END) AS KennethTuran,
            SUM(CASE WHEN fmr.ReviewerID = 'R-003' THEN fmr.ReviewRating ELSE 0 END) AS DavidAnsen,
            SUM(CASE WHEN fmr.ReviewerID = 'R-004' THEN fmr.ReviewRating ELSE 0 END) AS PeterTravers,
            SUM(CASE WHEN fmr.ReviewerID = 'R-005' THEN fmr.ReviewRating ELSE 0 END) AS AnthonyScott
        FROM
            factmoviereview fmr
        JOIN
            dimreviewer dr ON fmr.ReviewerID = dr.ReviewerID
        JOIN
            factmovie fm ON fmr.MovieID = fm.MovieID
        GROUP BY
            fm.Title
    );
    """,
    """
    CREATE INDEX idx_rating_reviewer_movie_title ON temp_rating_reviewer_movie_title(Title);
    """
]

# Define a function to fetch data based on a query
def fetch_data(query):
    # Database connection details
    db_config = {
        'user': 'root',
        'password': 'password',
        'host': 'localhost',
        'database': 'movieoptv3'
    }
    
   
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Create temporary tables
    for table in TEMP_TABLES:
        cursor.execute(table)
        
    start_time = time.time()
    df = pd.read_sql(query, conn)
    conn.close()
    end_time = time.time()
    execution_time = end_time - start_time
    return df, execution_time

# Individual functions to execute each query
def query1_1():
    query = """
    SELECT
        Genre,
        Location,
        TotalBoxOffice
    FROM
        temp_genre_location_boxoffice;
    """
    return query

def query1_2():
    query = """
    SELECT
        Location,
        TheaterName,
        Genre,
        Title,
        TotalBoxOffice
    FROM
        temp_location_theater_genre_title;
    """
    return query

def query1_3():
    query = """
    SELECT
        Title,
        MovieRating,
        TotalBoxOffice
    FROM
        temp_r_rated_title_boxoffice;
    """
    return query

def query1_4():
    query = """
    SELECT
        Title,
        MovieRating,
        Location,
        TotalBoxOffice
    FROM
        temp_r_rated_ny_boxoffice;
    """
    return query

def query1_5():
    query = """
    SELECT
        Title,
        Chicago,
        Dallas,
        Houston,
        LosAngeles,
        Miami,
        NewYork,
        Orlando,
        Philadelphia,
        SanDiego,
        SanFrancisco
    FROM
        temp_titles_cities_boxoffice;
    """
    return query

def query2_1():
    query = """
    SELECT
        AgentName,
        Gender,
        TotalSalary
    FROM
        temp_salary_agent_gender;
    """
    return query

def query2_2():
    query = """
    SELECT
        Gender,
        Nationality,
        AgentName,
        TotalSalary
    FROM
        temp_salary_gender_nationality_agent;
    """
    return query

def query2_3():
    query = """
    SELECT
        ActorName,
        Nationality,
        TotalSalary
    FROM
        temp_salary_american_actors;
    """
    return query

def query2_4():
    query = """
    SELECT
        ActorName,
        Nationality,
        AgentName,
        TotalSalary
    FROM
        temp_salary_american_actors_agent;
    """
    return query

def query2_5():
    query = """
    SELECT
        Title,
        AngelinaJolie,
        BradPitt,
        JohnnyDepp,
        WillSmith,
        TomCruise,
        JuliaRoberts,
        ChristianBale,
        LeonardoDiCaprio,
        CateBlanchett,
        RussellCrowe,
        KeiraKnightly,
        MarionCotillard,
        MerylStreep,
        PierceBrosnan
    FROM
        temp_salary_specific_actors;
    """
    return query

def query3_1():
    query = """
    SELECT
        Title,
        OverallRating
    FROM
        temp_rating_movie_title;
    """
    return query

def query3_2():
    query = """
    SELECT
        ReviewerClass,
        MovieRating,
        Genre,
        OverallRating
    FROM
        temp_rating_reviewer_class_movie_rating_genre;
    """
    return query

def query3_3():
    query = """
    SELECT
        Title,
        MovieRating,
        OverallRating
    FROM
        temp_rating_r_rated_title;
    """
    return query

def query3_4():
    query = """
    SELECT
        Title,
        MovieRating,
        Genre,
        OverallRating
    FROM
        temp_rating_r_thriller_title;
    """
    return query

def query3_5():
    query = """
    SELECT
        Title,
        RogerEbert,
        KennethTuran,
        DavidAnsen,
        PeterTravers,
        AnthonyScott
    FROM
        temp_rating_reviewer_movie_title;
    """
    return query

# Initialize the Dash app
app = dash.Dash(__name__)

# Update the layout of your app to include a div element for displaying the graph
app.layout = html.Div([
    dcc.Dropdown(
        id='query-dropdown',
        options=[
            {'label': 'Query 1_1: Total Box Office by Genre and Location', 'value': 'query1_1'},
            {'label': 'Query 1_2: Total Box Office by Theater, Genre, and Title', 'value': 'query1_2'},
            {'label': 'Query 1_3: Total Box Office for R-Rated Movies by Title', 'value': 'query1_3'},
            {'label': 'Query 1_4: Total Box Office for R-Rated Movies in New York by Title', 'value': 'query1_4'},
            {'label': 'Query 1_5: Total Box Office by Movie and Location', 'value': 'query1_5'},
            {'label': 'Query 2_1: Total Salary by Agent and Gender', 'value': 'query2_1'},
            {'label': 'Query 2_2: Total Salary by Nationality and Gender', 'value': 'query2_2'},
            {'label': 'Query 2_3: Total Salary for American Actors by Name', 'value': 'query2_3'},
            {'label': 'Query 2_4: Total Salary for American Actors Represented by Creative Artists', 'value': 'query2_4'},
            {'label': 'Query 2_5: Total Salary by Movie and Actor', 'value': 'query2_5'},
            {'label': 'Query 3_1: Overall Movie Ratings', 'value': 'query3_1'},
            {'label': 'Query 3_2: Overall Movie Ratings by Reviewer Class, Movie Rating, and Genre', 'value': 'query3_2'},
            {'label': 'Query 3_3: Overall Movie Ratings for R-Rated Movies by Title', 'value': 'query3_3'},
            {'label': 'Query 3_4: Overall Movie Ratings for R-Rated Thriller Movies by Title', 'value': 'query3_4'},
            {'label': 'Query 3_5: Overall Movie Ratings by Reviewer', 'value': 'query3_5'}
        ],
        value='query1_1',
        multi=False
    ),
    dcc.Graph(id='result-graph'),
    html.Div(id='query-result')
])

# Add a callback to update the graph when the dropdown value changes
@app.callback(
    [Output('result-graph', 'figure'),
     Output('query-result', 'children')],
    [Input('query-dropdown', 'value')]
)
def update_graph(selected_query):
    if selected_query is None:
        raise PreventUpdate  # If no value is selected, prevent updating the graph
    
    query_function = globals().get(selected_query)  # Get the function object from its name
    query = query_function()  # Call the function to get the query string
    
    df, execution_time = fetch_data(query)

    if selected_query == 'query1_1':
        fig = px.bar(df, x='Location', y='TotalBoxOffice', color='Genre', barmode='group',
                     title='Total Box Office by Location and Genre',
                     labels={'TotalBoxOffice': 'Total Box Office', 'Location': 'Theater Location'})
    elif selected_query == 'query1_2':
        fig = px.bar(df, x='TheaterName', y='TotalBoxOffice', color='Genre', barmode='group',
                    title='Total Box Office by Theater, Genre, and Title',
                    labels={'TotalBoxOffice': 'Total Box Office', 'TheaterName': 'Theater Name'})
    elif selected_query == 'query1_3':
        fig = px.pie(df, names='Title', values='TotalBoxOffice',
                    title='Total Box Office for R-Rated Movies by Title',
                    labels={'TotalBoxOffice': 'Total Box Office', 'Title': 'Movie Title'})
    elif selected_query == 'query1_4':
        fig = px.bar(df, x='Title', y='TotalBoxOffice', color='Location',
                    title='Total Box Office for R-Rated Movies in New York by Title',
                    labels={'TotalBoxOffice': 'Total Box Office', 'Title': 'Movie Title', 'Location': 'Location'})
    elif selected_query == 'query1_5':
        fig = px.bar(df, x='Title', y=['Chicago', 'Dallas', 'Houston', 'LosAngeles', 'Miami', 'NewYork', 'Orlando', 'Philadelphia', 'SanDiego', 'SanFrancisco'],
                    title='Total Box Office by Movie and Location',
                    labels={'value': 'Total Box Office', 'Title': 'Movie Title', 'variable': 'Location'})
    elif selected_query == 'query2_1':
        fig = px.bar(df, x='AgentName', y='TotalSalary', color='Gender', barmode='group',
                    title='Total Salary by Agent and Gender',
                    labels={'TotalSalary': 'Total Salary', 'AgentName': 'Agent Name'})
    elif selected_query == 'query2_2':
        fig = px.bar(df, x='Nationality', y='TotalSalary', color='Gender', barmode='group',
                    title='Total Salary by Nationality and Gender',
                    labels={'TotalSalary': 'Total Salary', 'Nationality': 'Nationality'})
    elif selected_query == 'query2_3':
        fig = px.pie(df, names='ActorName', values='TotalSalary',
                    title='Total Salary for American Actors by Name',
                    labels={'TotalSalary': 'Total Salary', 'ActorName': 'Actor Name'})
    elif selected_query == 'query2_4':
        fig = px.bar(df, x='ActorName', y='TotalSalary', color='AgentName',
                    title='Total Salary for American Actors Represented by Creative Artists',
                    labels={'TotalSalary': 'Total Salary', 'ActorName': 'Actor Name', 'AgentName': 'Agent Name'})
    elif selected_query == 'query2_5':
        fig = px.bar(df, x='Title', y=['AngelinaJolie', 'BradPitt', 'JohnnyDepp', 'WillSmith', 'TomCruise', 'JuliaRoberts', 'ChristianBale', 'LeonardoDiCaprio', 'CateBlanchett', 'RussellCrowe', 'KeiraKnightly', 'MarionCotillard', 'MerylStreep', 'PierceBrosnan'],
                    title='Total Salary by Movie and Actor',
                    labels={'value': 'Total Salary', 'Title': 'Movie Title', 'variable': 'Actor'})
    elif selected_query == 'query3_1':
        fig = px.bar(df, x='Title', y='OverallRating',
                    title='Overall Movie Ratings',
                    labels={'OverallRating': 'Overall Rating', 'Title': 'Movie Title'})
    elif selected_query == 'query3_2':
        fig = px.bar(df, x='MovieRating', y='OverallRating', color='Genre',
                    title='Overall Movie Ratings by Reviewer Class, Movie Rating, and Genre',
                    labels={'OverallRating': 'Overall Rating', 'MovieRating': 'Movie Rating', 'Genre': 'Genre'})
    elif selected_query == 'query3_3':
        fig = px.pie(df, names='Title', values='OverallRating',
                    title='Overall Movie Ratings for R-Rated Movies by Title',
                    labels={'OverallRating': 'Overall Rating', 'Title': 'Movie Title'})
    elif selected_query == 'query3_4':
        fig = px.bar(df, x='Title', y='OverallRating', color='Genre',
                    title='Overall Movie Ratings for R-Rated Thriller Movies by Title',
                    labels={'OverallRating': 'Overall Rating', 'Title': 'Movie Title', 'Genre': 'Genre'})
    elif selected_query == 'query3_5':
        fig = px.bar(df, x='Title', y=['RogerEbert', 'KennethTuran', 'DavidAnsen', 'PeterTravers', 'AnthonyScott'],
                    title='Overall Movie Ratings by Reviewer',
                    labels={'value': 'Overall Rating', 'Title': 'Movie Title', 'variable': 'Reviewer'})
    else:
        fig = {}  # Handle invalid query selection
    
    query_result = html.Div([
        html.H4(f'Query Result (Execution Time: {execution_time:.6f} seconds):'),
        html.Table([
            html.Thead(html.Tr([html.Th(col, style={'padding': '8px', 'background-color': '#f2f2f2', 'border': '1px solid #ddd'}) for col in df.columns])),
            html.Tbody([
                html.Tr([html.Td(df.iloc[i][col], style={'padding': '8px', 'border': '1px solid #ddd'}) for col in df.columns]) for i in range(len(df))
            ])
        ], className='table', style={'width': '100%', 'border-collapse': 'collapse'}),
    ], className='query-result', style={'width': '80%', 'font-family': 'Arial, sans-serif', 'text-align': 'left'})

    
    return fig, query_result


if __name__ == '__main__':
    app.run_server(debug=True)

