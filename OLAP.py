import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

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

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Get column names
        column_names = [i[0] for i in cursor.description]

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=column_names)

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return df
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None

# Function to populate the Treeview with data
def populate_treeview(tree, data_frame):
    # Clear any existing data in the tree
    tree.delete(*tree.get_children())

    if data_frame is not None:
        tree["column"] = list(data_frame.columns)
        tree["show"] = "headings"

        for column in tree["columns"]:
            tree.heading(column, text=column)

        for row in data_frame.itertuples(index=False):
            tree.insert("", tk.END, values=row)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

def query2_5():
    query = """
    SELECT
        fm.Title,
        SUM(CASE WHEN
        fmc.ActorID = 'A0001' THEN fmc.Salary ELSE 0 END) AS AngelinaJolie,
        SUM(CASE WHEN fmc.ActorID = 'A0002' THEN fmc.Salary ELSE 0 END) AS BradPitt,
        SUM(CASE WHEN fmc.ActorID = 'A0003' THEN fmc.Salary ELSE 0 END) AS JohnnyDepp,
        SUM(CASE WHEN fmc.ActorID = 'A0004' THEN fmc.Salary ELSE 0 END) AS WillSmith,
        SUM(CASE WHEN fmc.ActorID = 'A0005' THEN fmc.Salary ELSE 0 END) AS TomCruise,
        SUM(CASE WHEN fmc.ActorID = 'A0006' THEN fmc.Salary ELSE 0 END) AS JuliaRoberts,
        SUM(CASE WHEN fmc.ActorID = 'A0007' THEN fmc.Salary ELSE 0 END) AS ChristianBale,
        SUM(CASE WHEN fmc.ActorID = 'A0008' THEN fmc.Salary ELSE 0 END) AS OrlandoBloom,
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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

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
    df = fetch_data(query)
    if df is not None:
        populate_treeview(tree, df)

# Main function to create the GUI
def main():
    global tree

    # Create the main window
    root = tk.Tk()
    root.title("MySQL Query Table Data")

    # Create buttons for each query
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Query 1.1", command=query1_1).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Query 1.2", command=query1_2).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Query 1.3", command=query1_3).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(button_frame, text="Query 1.4", command=query1_4).grid(row=0, column=3, padx=5, pady=5)
    tk.Button(button_frame, text="Query 1.5", command=query1_5).grid(row=0, column=4, padx=5, pady=5)
    tk.Button(button_frame, text="Query 2.1", command=query2_1).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Query 2.2", command=query2_2).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Query 2.3", command=query2_3).grid(row=1, column=2, padx=5, pady=5)
    tk.Button(button_frame, text="Query 2.4", command=query2_4).grid(row=1, column=3, padx=5, pady=5)
    tk.Button(button_frame, text="Query 2.5", command=query2_5).grid(row=1, column=4, padx=5, pady=5)
    tk.Button(button_frame, text="Query 3.1", command=query3_1).grid(row=2, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Query 3.2", command=query3_2).grid(row=2, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Query 3.3", command=query3_3).grid(row=2, column=2, padx=5, pady=5)
    tk.Button(button_frame, text="Query 3.4", command=query3_4).grid(row=2, column=3, padx=5, pady=5)
    tk.Button(button_frame, text="Query 3.5", command=query3_5).grid(row=2, column=4, padx=5, pady=5)

    # Create the Treeview widget
    tree = ttk.Treeview(root)
    tree.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
