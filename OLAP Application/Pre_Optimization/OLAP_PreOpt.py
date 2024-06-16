import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import time

# Function to fetch data from the database based on the query
def fetch_data(query):
    config = {
        'user': 'root',
        'password': 'password',
        'host': 'localhost',
        'database': 'movieolap',
    }

    try:
        # Establish the connection
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Measure start time
        start_time = time.time()

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Measure end time
        end_time = time.time()

        # Calculate the total runtime
        runtime = end_time - start_time

        # Get column names
        column_names = [i[0] for i in cursor.description]

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=column_names)

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return df, runtime
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None, None

# Function to autofit the column widths
def autofit_columns(tree, data_frame):
    for col in data_frame.columns:
        max_len = max(data_frame[col].astype(str).map(len).max(), len(col)) + 2
        tree.column(col, width=max_len * 7)  # Adjusting the multiplier as needed

# Function to populate the Treeview with data
def populate_treeview(tree, data_frame, runtime):
    # Clear any existing data in the tree
    tree.delete(*tree.get_children())

    if data_frame is not None:
        tree["columns"] = list(data_frame.columns)
        tree["show"] = "headings"

        for column in tree["columns"]:
            tree.heading(column, text=column)

        autofit_columns(tree, data_frame)

        for row in data_frame.itertuples(index=False):
            tree.insert("", tk.END, values=row)

    # Display runtime
    runtime_label.config(text=f"Query executed in {runtime:.6f} seconds")

# Individual functions to execute each query
def query1_1():
    query = """
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
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query1_2():
    query = """
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
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query1_3():
    query = """
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
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query1_4():
    query = """
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
    AND
        dt.Location = 'New York'
    GROUP BY
        fm.Title, fm.MovieRating, dt.Location
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query1_5():
    query = """
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
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query2_1():
    query = """
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
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query2_2():
    query = """
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
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query2_3():
    query = """
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
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query2_4():
    query = """
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
    AND
        dage.AgentName = 'Creative Artists'
    GROUP BY
        dact.ActorName, dact.Nationality, dage.AgentName
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query2_5():
    query = """
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
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query3_1():
    query = """
    SELECT
        fm.Title,
        ROUND(AVG(fmr.ReviewRating), 1) AS OverallRating
    FROM
        factmoviereview fmr
    JOIN
        factmovie fm ON fmr.MovieID = fm.MovieID
    GROUP BY
        fm.Title
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query3_2():
    query = """
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
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query3_3():
    query = """
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
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query3_4():
    query = """
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
    AND
        fm.Genre = 'Thriller'
    GROUP BY
        fm.Title, fm.MovieRating, fm.Genre
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

def query3_5():
    query = """
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
    """
    df, runtime = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df, runtime)

# Main function to create the GUI
def main():
    root = tk.Tk()
    root.title("Movie OLAP Query Interface")

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)

    frame1 = ttk.Frame(notebook, width=800, height=400)
    frame2 = ttk.Frame(notebook, width=800, height=400)
    frame3 = ttk.Frame(notebook, width=800, height=400)

    frame1.pack(fill="both", expand=True)
    frame2.pack(fill="both", expand=True)
    frame3.pack(fill="both", expand=True)

    notebook.add(frame1, text="Movie Box Office Analysis")
    notebook.add(frame2, text="Actor Salary Analysis")
    notebook.add(frame3, text="Movie Rating Analysis")

    global tree
    tree_frame = ttk.Frame(root)
    tree_frame.pack(pady=10, fill="both", expand=True)

    # Creating a Treeview widget
    tree = ttk.Treeview(tree_frame)
    tree.pack(side="left", fill="both", expand=True)

    # Adding scrollbars
    tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree_scroll_y.pack(side="right", fill="y")

    tree.configure(yscrollcommand=tree_scroll_y.set)

    # Label to display runtime
    global runtime_label
    runtime_label = ttk.Label(root, text="")
    runtime_label.pack()

    # Creating labels and buttons for Frame 1 (Movie Box Office Analysis)
    queries1 = [
        ("Box Office by Genre and Location", query1_1),
        ("Box Office by Location, Theater, Genre, and Title", query1_2),
        ("Box Office for R-rated Movies by Title", query1_3),
        ("Box Office for R-rated Movies in New York", query1_4),
        ("Box Office for Titles in Various Cities", query1_5),
    ]

    for idx, (label_text, command) in enumerate(queries1):
        label = ttk.Label(frame1, text=label_text)
        label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

        button = ttk.Button(frame1, text="Run Query", command=command)
        button.grid(row=idx, column=1, padx=10, pady=5)

    # Creating labels and buttons for Frame 2 (Actor Salary Analysis)
    queries2 = [
        ("Total Salary by Agent and Gender", query2_1),
        ("Total Salary by Gender, Nationality, and Agent", query2_2),
        ("Total Salary for American Actors by Name", query2_3),
        ("Total Salary for American Actors by Agent", query2_4),
        ("Salary for Specific Actors by Movie Title", query2_5),
    ]

    for idx, (label_text, command) in enumerate(queries2):
        label = ttk.Label(frame2, text=label_text)
        label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

        button = ttk.Button(frame2, text="Run Query", command=command)
        button.grid(row=idx, column=1, padx=10, pady=5)

    # Creating labels and buttons for Frame 3 (Movie Rating Analysis)
    queries3 = [
        ("Overall Rating by Movie Title", query3_1),
        ("Rating by Reviewer Class, Movie Rating, and Genre", query3_2),
        ("Rating for R-rated Movies by Title", query3_3),
        ("Rating for R-rated Thriller Movies by Title", query3_4),
        ("Rating by Reviewer and Movie Title", query3_5),
    ]

    for idx, (label_text, command) in enumerate(queries3):
        label = ttk.Label(frame3, text=label_text)
        label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

        button = ttk.Button(frame3, text="Run Query", command=command)
        button.grid(row=idx, column=1, padx=10, pady=5)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    main()

