<?php

$db = new SQLite3('tos_scraper.db');

$query = $db->query("SELECT id, url, privacy, tos FROM website;");


foreach ($query as $entry) {
    echo 'ID: ' . $entry['id'] . '  url: ' . $entry['url']  . '  privacy: ' . $entry['privacy'] . '  tos: ' . $entry['tos'];
}

?>