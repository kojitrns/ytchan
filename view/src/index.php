<html><body><h1>hello world</h1>
<?php
// phpinfo();
$dbopts = parse_url(getenv('DATABASE_URL'));
// header('Content-Type: application/json');
try {
    // $pdo = new PDO('pgsql:host=localhost; dbname=d34ajosp96vv38', 'koji', 'mukku');
	$pdo = new PDO( 'pgsql:host='.$dbopts["host"].'; dbname='.ltrim($dbopts["path"],'/'), $dbopts["user"], $dbopts["pass"] );
	// var_dump("接続に成功しました\n");
    foreach($pdo->query('SELECT * from channels') as $row) {
		echo '<a href=https://www.youtube.com/channel/'.$row['channelid'].' target=_blank title='.$row['channeltitle'].'>';
		echo '<img src="'.$row['thumbnail_url'].'"></a>';
    }
    $sth = null;
    $dbh = null;
}
catch(PDOException $e) {
	var_dump($e->getMessage());
}
?>

</body></html>