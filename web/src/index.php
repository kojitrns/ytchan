<html>
<head>
	<meta name="viewport" content="width=device-width,initial-scale=1" charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge" />
	<meta name="description" content="YouTubeの様々なチャンネル（投稿者）をジャンル別にまとめています。各チャンネルの最新動画の情報も載せてます。" />
	<link rel="icon" href="https://img.icons8.com/nolan/64/000000/video-call.png" sizes="16x16" type="image/png" />
	<?php
	if($_SERVER['SERVER_NAME'] == 'localhost')
		echo '<link rel="stylesheet" type="text/css" href="../css/main.css">';
	else
		echo '<link rel="stylesheet" type="text/css" href="https://ytchan.herokuapp.com/css/main.css">';
	?>
	<!-- Global site tag (gtag.js) - Google Analytics -->
	<script async src="https://www.googletagmanager.com/gtag/js?id=UA-141605464-1"></script>
	<script>
	  window.dataLayer = window.dataLayer || [];
	  function gtag(){dataLayer.push(arguments);}
	  gtag('js', new Date());
	  gtag('config', 'UA-141605464-1');
	</script>
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
	$uplist = "<a href=\"https://youtube.com/channel/{$chan_data['channel_id']}/videos\" target=_blank
	title=\"videos\"> <img id=\"uplist-img\" src =\"https://ytchan.herokuapp.com/img/videos.png\"/></a>";
	$social_blade = "<a href=\"https://socialblade.com/youtube/channel/{$chan_data['channel_id']}\" target=_blank
	title=\"socialblade\"> <img id=\"sb-img\" src =\"https://ytchan.herokuapp.com/img/sb.png\"/></a>";

	$view_count = digit_handler($chan_data['view_count']);
	$video_count = digit_handler($chan_data['video_count']);
	$subscriber_count = digit_handler($chan_data['subscriber_count']);

	$chan_detail = "<div class=\"detail-box\">$description$uplist$social_blade</div>";
	$chan_title = $chan_data['channel_title'];
	$max_len = 34;
	if(mb_strlen($chan_title) > $max_len) {
		$chan_title = mb_substr($chan_title, 0, $max_len, "utf-8") ."...";
	}

	$chan_info = "<div class=\"counter-box\">
					<p title=\"ViewCount\"><img src=\"https://img.icons8.com/material-two-tone/24/000000/video.png\" id=\"view-img\">$view_count</p>
					<p title=\"VideoCount\"><img src=\"https://img.icons8.com/metro/26/000000/documentary.png\" id=\"video-img\">$video_count</p>
					<p title=\"SubscriberCount\"><img src=\"https://img.icons8.com/material-sharp/24/000000/user-group-man-man.png\" id=\"subscr-img\">$subscriber_count</p></div>$chan_detail";
	$cont = sprintf('<img src="%s"><div class="chan-info-box">%s</div><div class ="chan-title-box"><a href="%s%s" target=_blank title="%s">%s</a></div>', $chan_data['thumbnail_url'], $chan_info, $youtube_url, $chan_data['channel_id'], $chan_data['channel_title'], $chan_title);

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
	<img src="https://img.icons8.com/nolan/64/000000/video-call.png" width=40px height=40px><div class="site-title"><p>チャンネルずかん</p></div>';

	show_btns_on_header();

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
	<p>Youtubeのいろんなチャンネルをまとめてます。最近の動画はここ１週間でアップされたものです。ジャンルの分類、チャンネル追加など毎日更新。</p>
	</div>';
}

function show_btns_on_header() {
	echo '<a href="https://www.youtube.com/" target=_blank title="Youtube"><img src="https://img.icons8.com/windows/32/000000/youtube.png" class="yt-btn"></a>';

	global $cur_category;
	$text = "Youtube チャンネルずかん カテゴリ：$cur_category\"";
	$url = "https://ytchan.herokuapp.com". urlencode($_SERVER['REQUEST_URI']);
	echo '<span class="tw-btn"><a href="https://twitter.com/share?url='. $url  .'&text=' .$text. ' class="twitter-share-button" data-show-count="false">Tweet</a></span><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>';
}

function show_footer() {
	echo '<footer>
	<p>© Copyright 2019 チャンネルずかん All rights reserved.</p>
	</footer>';
}

function sort_rows(&$rows, $sort_target) {
	$sort;
	foreach ($rows as $num => $row) {
		$sort[$num] = $row[$sort_target];
	}
	array_multisort($sort, SORT_DESC, $rows);
}

$category_list = array();

if($mode == 'channel') {
	set_channel_database($category_list, 'channel');
} else {
	set_channel_database($category_list, 'video');
}

show_header($category_list);
show_left_panel($category_list);

echo "<main><h2>$cur_category</h2>";
$sub_categories = $category_list[$cur_category];

if($mode == 'channel') {
	foreach ($sub_categories as $subcategory => $rows) {
		echo "<div class=\"subcategory-zone\"><h3 id=\"$subcategory\">■$subcategory</h3>";
		sort_rows($rows, 'view_count');
		foreach ($rows as $row) {
			echo get_channel_cont($row);
		}
		echo '</div>';
	}
}
else {
	foreach ($sub_categories as $subcategory => $rows) {
		echo "<div class=\"subcategory-zone\"><h3 id=\"$subcategory\">■$subcategory</h3>";
		sort_rows($rows, 'published_at');
		foreach ($rows as $row) {
			echo get_video_cont($row);
		}
		echo '</div>';
	}
}

echo '</main>';
show_right_panel();
show_footer();
?>
</body></html>