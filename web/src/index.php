<html>
<head>
	<meta name="viewport" content="width=device-width,initial-scale=1" charset="UTF-8">
	<link rel="stylesheet" type="text/css" href="css/main.css">
    <title>チャンネルずかん</title>
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
		$description = "<span class=\"description\"><img id=\"desc-img\" src=\"https://img.icons8.com/ios/50/000000/questions.png\" /> <p>{$chan_data['description']}</p></span>";
	}
	$social_blade = "<a href=\"https://socialblade.com/youtube/channel/{$chan_data['channelid']}\" target=_blank> <img id=\"sb-img\" src =\"img/sb.png\"/></a>";
	$viewcount = digit_handler($chan_data['viewcount']);
	$videocount = digit_handler($chan_data['videocount']);
	$subscribercount = digit_handler($chan_data['subscribercount']);

	$chan_detail = "<div class=\"detail-box\">$description$social_blade</div>";

	$chan_info = "<div class=\"counter-box\"><p>$viewcount</p><p>$subscribercount</p><p>$subscribercount</p></div>$chan_detail";
	$cont = sprintf('<img src="%s"><div class="chan-info-box">%s</div><div class ="chan-title-box"><a href="%s%s" target=_blank title="%s">%s</a></div>', $chan_data['thumbnailurl'], $chan_info, $youtube_url, $chan_data['channelid'], $chan_data['channeltitle'] ,$chan_data['channeltitle']);
	return '<div class="chan-box">'. $cont .'</div>';
}

function get_video_cont($video_data=null)
{
	$pub_data = preg_split("/[T]/", $video_data['published_at'])[0];
	$view_count = $video_data['view_count']+ " views  ";
    return 
    "<div class=\"video-box\">
      <a href=\"https://www.youtube.com/watch?v={$video_data['video_id']}\" target=\"_blank\">
      <img src = \"{$video_data['thumbnail']}\" />
      <p>{$video_data['video_title']}</p></a>
      <a href=\"https://www.youtube.com/channel/{$video_data['channel_id']}\" target=\"_blank\" title=\"{$video_data['channel_title']}\">
      <p>{$video_data['channel_title']}</p></a>
      <span> $view_count views</span> <span>$pub_data</span>
    </div>";
}

function set_channel_database(&$category_list, $table_name)
{
	try {
		$dbopts = parse_url(getenv('DATABASE_URL'));
		$pdo = new PDO('pgsql:host='.$dbopts["host"].'; dbname='.ltrim($dbopts["path"],'/'), $dbopts["user"], $dbopts["pass"]);
		//var_dump("connection succeeded\n");
		if($table_name=='channel')
		foreach($pdo->query("SELECT * from $table_name") as $row) {
			$category_list[$row['maincategory']][$row['subcategory']][] = $row;
	    }
	    else
		foreach($pdo->query("SELECT * from $table_name") as $row) {
			$category_list[$row['main_category']][$row['sub_category']][] = $row;
	    }
	} catch (PDOException $e) {
		var_dump($e->getMessage());
	}
}

function show_header(&$category_list) {
	echo '<header class="site-header"><nav><b>カテゴリ:</b>';
	$mode = '';
	if(isset($_GET['mode']))
		$mode = $_GET['mode'];
	foreach ($category_list as $maincategory => $sub_categories) {
		echo "<a href=\"{$_SERVER["SCRIPT_NAME"]}?cur_category=$maincategory&mode=$mode\">$maincategory</a> ";
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

$category_list = array();
$cur_category = '';

if(!isset($_GET['mode']) || $_GET['mode']=='channel') {
	set_channel_database($category_list, 'channel');
} else {
	set_channel_database($category_list, 'video');
}

show_header($category_list);

if(isset($_GET['cur_category'])) {
	$cur_category = $_GET['cur_category'];
} else {
	$cur_category = 'ニュース';
}

show_left_panel(array_keys($category_list[$cur_category]));

echo "<div class=\"main-category-panel\"><h2>$cur_category</h2>";
$mode_cont = '';
if(isset($_GET['mode']) && $_GET['mode'] == 'video') {
	$mode_cont = "<a href=\"{$_SERVER["SCRIPT_NAME"]}?cur_category=$cur_category&mode=channel\">
	  チャンネル</a> / 最近の動画";
} else {
	$mode_cont = " チャンネル / <a href=\"{$_SERVER["SCRIPT_NAME"]}?cur_category=$cur_category&mode=video\">
      最近の動画</a>";
}
echo "<div class=\"mode-selector\">$mode_cont</div>";

$sub_categories = $category_list[$cur_category];

if(!isset($_GET['mode']) || $_GET['mode']=='channel')
foreach ($sub_categories as $subcategory => $rows) {
	echo "<div class=\"chan-container clearfix\"><h3 id=\"$subcategory\">■$subcategory</h3>";
	sort_chan_rows($rows, 'viewcount');
	foreach ($rows as $row) {
		echo get_channel_cont($row);
	}
	echo '</div>';
}
else {
	foreach ($sub_categories as $subcategory => $rows) {
	echo "<div class=\"clearfix\"><h3 id=\"$subcategory\">■$subcategory</h3>";
	foreach ($rows as $row) {
		echo get_video_cont($row);
	}
	echo '</div>';
}

}

echo '</div>';
?>
</body></html>