<?php 
	function add_msg_to_db($msg) {
		if(mb_strlen($msg) > 200){
			return false;
		}
		try {
			$dbopts = parse_url(getenv('DATABASE_URL'));
			$pdo = new PDO('pgsql:host='.$dbopts["host"].'; dbname='.ltrim($dbopts["path"],'/'), $dbopts["user"], $dbopts["pass"]);
			//var_dump("connection succeeded\n");
			$rows = $pdo->query("SELECT * from message");
			if(count($rows) >= 100) return false;
			$stmt = $pdo ->prepare("INSERT INTO message $row_cont VALUES (?,?)");
			$stmt->bindValue(1, date('Y年m月d日　H時i分s秒'));
			$stmt->bindValue(2, $_POST["message"]);
			$stmt->execute();
		} catch (PDOException $e) {
			var_dump($e->getMessage());
		}
		return true;
	}
	$ok = add_msg_to_db($_POST['message']);	
?>
<html>
<head>
	<meta name="viewport" content="width=device-width,initial-scale=1" charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge" />
	<meta name="description" content="YouTubeのチャンネル（投稿者）のまとめです。各チャンネルの最新の動画も載せてます。" />
	<link rel="icon" href="https://img.icons8.com/nolan/64/000000/video-call.png" sizes="16x16" type="image/png" />
	<?php
	echo '<meta http-equiv="refresh" content="2; URL='."{$_POST['category']}/{$_POST['mode']}" . '">';
	?>
    <title>チャンネルずかん</title>
</head>
<body>
<?php
	if($ok)echo '<h2>メッセージの送信が完了しました。</h2>';
	else  echo '<h2>メッセージの送信に失敗しました。</h2>';
?>
</body>
</html>