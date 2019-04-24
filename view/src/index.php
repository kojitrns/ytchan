<html>
<head>
	<meta name="viewport" content="width=device-width,initial-scale=1" charset="UTF-8">
	<link rel="stylesheet" type="text/css" href="css/main.css">
</head>
<body>
<?php
// phpinfo();
$youtube_url = 'https://www.youtube.com/channel/';
// header('Content-Type: application/json');

function get_channel_cont($chan_data=null)
{
	global $youtube_url;
	$cont = sprintf('<a href="%s%s" target=_blank title="%s"><img src="%s"></a>', $youtube_url, $chan_data['channelid'],
		$chan_data['channeltitle'], $chan_data['thumbnailurl']);
	return '<div class="chan_box">'. $cont .'</div>';
}

function set_channel_database(&$category_list)
{
	try {
	    // $pdo = new PDO('pgsql:host=localhost; dbname=d34ajosp96vv38', 'koji', 'mukku');
		$dbopts = parse_url(getenv('DATABASE_URL'));
		$pdo = new PDO( 'pgsql:host='.$dbopts["host"].'; dbname='.ltrim($dbopts["path"],'/'), $dbopts["user"], $dbopts["pass"] );
		// var_dump("connection succeeded\n");
		foreach($pdo->query('SELECT * from channel') as $row) {
			$category_list[$row['maincategory']][$row['subcategory']][] = $row;
	    }
	    $sth = null;
	    $dbh = null;
	} catch (PDOException $e) {
		var_dump($e->getMessage());
	}
}

// function init() {
// }
// $main_categories = file(__DIR__.'/main_category.txt', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

$category_list = array();
set_channel_database($category_list);

foreach ($category_list as $maincategory => $sub_categories) {
	echo "<div class=\"main_category_panel\"><h2>$maincategory</h2>";
	foreach ($sub_categories as $subcategory => $rows) {
		echo "<div class=\"chan_container clearfix\"><h3>$subcategory</h3>";
		foreach ($rows as $row) {
			echo get_channel_cont($row);
		}
		echo '</div>';
	}
	echo '</div>';
}
?>

</body></html>