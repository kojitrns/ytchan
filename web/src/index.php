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

function digit_handler($num) {
	if($num > 1000000000) return number_format(round($num/1000000)).' M';
	if($num > 100000) return number_format(round($num/1000)).' K';
	return number_format($num);
}

function get_channel_cont($chan_data=null)
{
	global $youtube_url;
	$description = '';
	$keywords = '';
	if (strlen($chan_data['description'])) {
		$description = "<span class=\"description\">説明 <p>{$chan_data['description']}</p></span>";
	}
	if (strlen($chan_data['keywords'])) {
		$keywords = "<span class=\"keywords\">関連語 <p>{$chan_data['keywords']}</p></span>";
	}
	$social_blade = "<a href=\"https://socialblade.com/youtube/channel/{$chan_data['channelid']}\" target=_blank> sbinfo</a>";
	$viewcount = digit_handler($chan_data['viewcount']);
	$videocount = digit_handler($chan_data['videocount']);
	$subscribercount = digit_handler($chan_data['subscribercount']);

	$chan_detail = "<div class=\"detail-box\">$description$keywords$social_blade</div>";

	$chan_info = "<div class=\"counter-box\"><p>$viewcount</p><p>$subscribercount</p><p>$subscribercount</p></div>$chan_detail";
	$cont = sprintf('<img src="%s"><div class="chan-info-box">%s</div><div class ="chan-title-box"><a href="%s%s" target=_blank title="%s">%s</a></div>', $chan_data['thumbnailurl'], $chan_info, $youtube_url, $chan_data['channelid'], $chan_data['channeltitle'] ,$chan_data['channeltitle']);
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
	echo '<header class="site-header"><nav><b>カテゴリ:</b>';
	foreach ($category_list as $maincategory => $sub_categories) {
		echo "<a href=\"{$_SERVER["SCRIPT_NAME"]}?cur_category=$maincategory\">$maincategory</a> ";
	}
	echo '</nav></header><div class="header-emb"></div>';
}


function show_left_panel(&$sub_categories) {
	echo '<div class="left-panel">';
	foreach ($sub_categories as $sub_category) {
		echo "<a href=\"#$sub_category\">・$sub_category</a></br> ";
	}
	echo '</div>';
}

function sort_chan_rows(&$chan_rows, $sort_target) {
	$sort;
	foreach ($chan_rows as $num => $row) {
		$sort[$num] = $row[$sort_target];
	}
	array_multisort($sort, SORT_DESC, $chan_rows);
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

show_left_panel(array_keys($category_list[$cur_category]));

echo "<div class=\"main-category-panel\"><h2>$cur_category</h2>";

$sub_categories = $category_list[$cur_category];

foreach ($sub_categories as $subcategory => $rows) {
	echo "<div class=\"chan-container clearfix\"><h3 id=\"$subcategory\">■$subcategory</h3>";
	sort_chan_rows($rows, 'viewcount');
	foreach ($rows as $row) {
		echo get_channel_cont($row);
	}
	echo '</div>';
}
echo '</div>';
?>
</body></html>