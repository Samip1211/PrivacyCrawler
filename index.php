html>
<head>
<style>
table, th, td {
    border: 1px solid black;
}</style>
</head>
<body>

<h1> Please enter the website you would like to scrape below</h1>

<form action="scrapper.php" method="post">
        <input type="text" value="domain" name="domain" />
        <input type="submit" value="Send" />
</form> 

<table style="width=100%">
<tr>
<th>id</th>
<th>Website URL</th>
<th>Website Privacy Link</th>
<th>Website Terms Of Service</th>

<?php

$db = new SQLite3('tos_scraper.db');

$results = $db->query("SELECT id, url, privacy, tos FROM website;");

 
while ($row = $results->fetchArray()) {
echo '<tr>';
echo '<td>' . $row['id'] . '</td><td>' . $row['url']  . '</td><td>' . $row['privacy'] . '</td><td>' . $row['tos'] . '</td>';
echo '</tr>';
}



?>
</tr>
</table>
</body>
</html>
