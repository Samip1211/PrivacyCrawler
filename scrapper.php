<html>
<head><title>Website Privacy Scraper</title><head>
<body>
Beginning to Scrape:

<?php

$domain = $_POST['domain'];
echo $domain;

$command = 'python scrapper.py ' . $domain;
$output = passthru($command);

echo $output;
?>
<p></p>
<p></p>
<a href="index.php">View Results</a>
</html>
