# 1. Movie Performance Reports
# 1.1 roll-up
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

# 1.2 drill-down
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
    dt.Location, dt.TheaterName, fm.Genre, fm.Title;

# 1.3 slice
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
    fm.Title, fm.MovieRating;

# 1.4 dice
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
    fm.Title, fm.MovieRating, dt.Location;
    
# 1.5 pivot
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
    fm.Title;
    
# 2 Actor Salary Reports
# 2.1 roll-up
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
	dage.AgentName, dact.Gender;
    
# 2.2 drill-down
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
	dact.Gender, dact.Nationality, dage.AgentName;

# 2.3 slice
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
	dact.ActorName, dact.Nationality;

# 2.4 dice
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
	dact.ActorName, dact.Nationality, dage.AgentName;
    
# 2.5 pivot
SELECT
    fm.Title,
    SUM(CASE WHEN fmc.ActorID = 'A0001' THEN fmc.Salary ELSE 0 END) AS AngelinaJolie,
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
	fm.Title;

# 3 Movie Rating Reports
# 3.1 roll-up
SELECT
    fm.Title,
    ROUND(AVG(fmr.ReviewRating),1) AS OverallRating
FROM
    factmoviereview fmr
JOIN
	factmovie fm ON fmr.MovieID = fm.MovieID
GROUP BY
	fm.Title;

# 3.2 drill-down
SELECT
    dr.ReviewerClass,
    fm.MovieRating,
    fm.Genre,
    ROUND(AVG(fmr.ReviewRating),1) AS OverallRating
FROM
    factmoviereview fmr
JOIN
	factmovie fm ON fmr.MovieID = fm.MovieID
JOIN
	dimreviewer dr ON fmr.ReviewerID = dr.ReviewerID
GROUP BY
	dr.ReviewerClass, fm.MovieRating, fm.Genre;

# 3.3 slice
SELECT
	fm.Title,
    fm.MovieRating,
    ROUND(AVG(fmr.ReviewRating),1) AS OverallRating
FROM
	factmoviereview fmr
JOIN
	factmovie fm ON fmr.MovieID = fm.MovieID
WHERE
	fm.MovieRating = 'R'
GROUP BY
	fm.Title, fm.MovieRating;

# 3.4 dice
SELECT
	fm.Title,
    fm.MovieRating,
    fm.Genre,
    ROUND(AVG(fmr.ReviewRating),1) AS OverallRating
FROM
	factmoviereview fmr
JOIN
	factmovie fm ON fmr.MovieID = fm.MovieID
WHERE
	fm.MovieRating = 'R'
AND
	fm.Genre = 'Thriller'
GROUP BY
	fm.Title, fm.MovieRating, fm.Genre;
    
# 3.5 pivot
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
	fm.Title;