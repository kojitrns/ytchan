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
	$chan_info = "<p>{$chan_data['viewcount']}</p><p>{$chan_data['subscribercount']}</p><p>{$chan_data['videocount']}</p>";
	$cont = sprintf('<img src="%s"><div class="chan-info-box">%s</div><div class ="chan-title-box"><a href="%s%s" target=_blank title="%s">%s</a></div>', $chan_data['thumbnailurl'], $chan_info, $youtube_url, $chan_data['channelid'],
		$chan_data['channeltitle'] ,$chan_data['channeltitle']);
	return '<div class="chan-box">'. $cont .'</div>';
}

function set_channel_database(&$category_list)
{
	try {
	    // $pdo = new PDO('pgsql:host=localhost; dbname=d34ajosp96vv38', 'koji', 'mukku');
		$dbopts = parse_url(getenv('DATABASE_URL'));
		$pdo = new PDO('pgsql:host='.$dbopts["host"].'; dbname='.ltrim($dbopts["path"],'/'), $dbopts["user"], $dbopts["pass"]);
		//var_dump("connection succeeded\n");
		foreach($pdo->query('SELECT * from channel') as $row) {
			$category_list[$row['maincategory']][$row['subcategory']][] = $row;
	    }
	    $sth = null;
	    $dbh = null;
	} catch (PDOException $e) {
		var_dump($e->getMessage());
	}
}

function show_header(&$category_list) {
	echo '<header class="site-header"><nav><h4>カテゴリ</h4>';
	foreach ($category_list as $maincategory => $sub_categories) {
		echo "<a href=\"{$_SERVER["SCRIPT_NAME"]}?cur_category=$maincategory\">$maincategory</a> ";
	}
	echo '</nav></header><div class="header-emb"></div>';
}

// function init() {
// }
// $main_categories = file(__DIR__.'/main_category.txt', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

$category_list = array();
$cur_category = '';
set_channel_database($category_list);
show_header($category_list);

if(isset($_GET['cur_category'])) {
	$cur_category = $_GET['cur_category'];
} else {
	$cur_category = 'ニュース';
}

echo "<div class=\"main-category-panel\"><h2>$cur_category</h2>";
$sub_categories = $category_list[$cur_category];
foreach ($sub_categories as $subcategory => $rows) {
	echo "<div class=\"chan-container clearfix\"><h3>$subcategory</h3>";
	foreach ($rows as $row) {
		echo get_channel_cont($row);
	}
	echo '</div>';
}
echo '</div>';
?>
</body></html>