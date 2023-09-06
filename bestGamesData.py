import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('database.sql')
cursor = connection.cursor()

# Retrieve data from the database
cursor.execute('''
    SELECT g.game_title, g.release_date, p.name AS platform_name, g.metascore, g.user_score, g.gamerank_score
    FROM games AS g
    LEFT JOIN platform AS p ON g.platform_id = p.id
    ORDER BY g.gamerank_score DESC
    LIMIT 100;
''')

# Fetch the first row to get column names
columns = [description[0] for description in cursor.description]

# Fetch all the data rows
rows = cursor.fetchall()

# Generate HTML
html = '<table border="1">\n<tr>'
# Create table headers
for column in columns:
    html += f'<th>{column}</th>'
html += '</tr>\n'

# Create table rows
for row in rows:
    html += '<tr>'
    for value in row:
        html += f'<td>{value}</td>'
    html += '</tr>\n'

html += '</table>'

# Close the database connection
connection.close()

# Write the HTML to a file or display it as needed
with open('topGames.html', 'w', encoding='utf-8') as file:
    file.write(html)

print("HTML table generated and saved as 'topGames.html'")
