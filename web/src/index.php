<html>
<head>
	<meta name="viewport" content="width=device-width,initial-scale=1" charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge" />
	<meta name="description" content="YouTubeの様々なチャンネル（投稿者）をジャンル別にまとめています。各チャンネルの最新動画の情報も載せてます。" />
	<link rel="icon" href="https://img.icons8.com/nolan/64/000000/video-call.png" sizes="16x16" type="image/png" />
	<link rel="stylesheet" type="text/css" href="https://ytchan.herokuapp.com/css/main.css">
    <title>チャンネルずかん</title>
</head>
<body>
<?php
// phpinfo();
$youtube_url = 'https://www.youtube.com/channel/';
$mode = 'channel';
$cur_category = 'ニュース';

$para = preg_split("/[\/]/", $_SERVER['REQUEST_URI']);
if(count($para) > 2) {
	$cur_category = urldecode($para[1]);
	$mode = $para[2];
}

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
		$description = "<span class=\"description\"><img id=\"desc-img\" src=\"https://img.icons8.com/ios/50/000000/questions.png\" /><p>{$chan_data['description']}</p></span>";
	}
	$social_blade = "<a href=\"https://socialblade.com/youtube/channel/{$chan_data['channelid']}\" target=_blank
	title=\"socialblade\"> <img id=\"sb-img\" src =\"img/sb.png\"/></a>";
	$view_count = digit_handler($chan_data['viewcount']);
	$video_count = digit_handler($chan_data['videocount']);
	$subscriber_count = digit_handler($chan_data['subscribercount']);

	$chan_detail = "<div class=\"detail-box\">$description$social_blade</div>";

	$chan_info = "<div class=\"counter-box\">
					<p title=\"ViewCount\"><img src=\"https://img.icons8.com/material-two-tone/24/000000/video.png\" id=\"view-img\">$view_count</p>
					<p title=\"VideoCount\"><img src=\"https://img.icons8.com/metro/26/000000/documentary.png\" id=\"video-img\">$video_count</p>
					<p title=\"SubscriberCount\"><img src=\"https://img.icons8.com/material-sharp/24/000000/user-group-man-man.png\" id=\"subscr-img\">$subscriber_count</p></div>$chan_detail";
	$cont = sprintf('<img src="%s"><div class="chan-info-box">%s</div><div class ="chan-title-box"><a href="%s%s" target=_blank title="%s">%s</a></div>', $chan_data['thumbnailurl'], $chan_info, $youtube_url, $chan_data['channelid'], $chan_data['channeltitle'] ,$chan_data['channeltitle']);
	return '<div class="chan-box">'. $cont .'</div>';
}

function get_video_cont($video_data=null)
{
	$pub_data = preg_split("/[T]/", $video_data['published_at'])[0];
	$view_count = $video_data['view_count']+ " views  ";
    return 
    "<div class=\"video-box\">
      <a href=\"https://www.youtube.com/watch?v={$video_data['video_id']}\" target=\"_blank\" title={$video_data['video_title']}>
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

	global $cur_category, $mode;
	echo '<header><div class="header-cont">
	<div class="site-title"><p>チャンネルずかん</p></div>';
	$mode_cont = '';
	if($mode == 'video') {
		$mode_cont = "<a href=\"/$cur_category/channel\">
		  チャンネル</a> / 最近の動画";
	} else {
		$mode_cont = " チャンネル / <a href=\"/$cur_category/video\">
	      最近の動画</a>";
	}
	echo "<div class=\"mode-selector\">$mode_cont</div>";
	echo '</div></header>';
}

function show_left_panel(&$category_list) {
	global $cur_category, $mode;
	$main_categories = array();
	foreach ($category_list as $maincategory => $subc) {
		$main_categories[] = $maincategory;
		// echo "<a href=\"{$_SERVER["SCRIPT_NAME"]}?cur_category=$maincategory&mode=$mode\">$maincategory</a> ";
	}
	sort($main_categories);

	$sub_categories = array_keys($category_list[$cur_category]);

	echo '<div class="left-panel"><p>カテゴリ</p><div class="category-zone">';
	foreach ($sub_categories as $sub_category) {
		echo "<a href=\"#$sub_category\">・$sub_category</a></br>";
	}
	foreach ($main_categories as $maincategory) {
		echo "<a href=\"/$maincategory/$mode\">$maincategory</a></br>";
	}
	echo '</div></div>';
}

function show_right_panel()
{
	echo '<div class="right-panel">
	<p>Youtubeのいろんなチャンネルをカテゴライズしてまとめてます。</p>
	</div>';
}

function show_footer() {
	// echo '<div class="footer"></div>';
	echo '<footer></footer>';
}

function sort_chan_rows(&$chan_rows, $sort_target) {
	$sort;
	foreach ($chan_rows as $num => $row) {
		$sort[$num] = $row[$sort_target];
	}
	array_multisort($sort, SORT_DESC, $chan_rows);
}

$category_list = array();

if($mode == 'channel') {
	set_channel_database($category_list, 'channel');
} else {
	set_channel_database($category_list, 'video');
}

show_header($category_list);
show_left_panel($category_list);
show_right_panel();

echo "<main><h2>$cur_category</h2>";
$sub_categories = $category_list[$cur_category];

if($mode == 'channel')
foreach ($sub_categories as $subcategory => $rows) {
	echo "<div class=\"subcategory-zone\"><h3 id=\"$subcategory\">■$subcategory</h3>";
	sort_chan_rows($rows, 'viewcount');
	foreach ($rows as $row) {
		echo get_channel_cont($row);
	}
	echo '</div>';
}
else {
	foreach ($sub_categories as $subcategory => $rows) {
	echo "<div class=\"subcategory-zone\"><h3 id=\"$subcategory\">■$subcategory</h3>";
	foreach ($rows as $row) {
		echo get_video_cont($row);
	}
	echo '</div>';
}

}

echo '</main>';
show_footer();
?>
</body></html>