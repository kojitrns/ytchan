<?php
	$dbopts = parse_url(getenv('DATABASE_URL'));
	// header('Content-Type: application/json');
	try {
		$pdo = new PDO( 'pgsql:host='.$dbopts["host"].'; dbname='.ltrim($dbopts["path"],'/'), $dbopts["user"], $dbopts["pass"] );
	}
	catch(PDOException $e) {
	    var_dump($e->getMessage());
	}

	if ($_SERVER['REQUEST_METHOD'] == 'POST')
	{
		$params = json_decode(file_get_contents('php://input'), true);
		if($params['opType'] == 'delete') {
			$stmt = $pdo->prepare("DELETE FROM channel WHERE channelid = ?");
			$stmt->bindValue(1, $params['channelid']);
			$stmt->execute();
		}
		elseif($params['opType'] == 'move') {
			$stmt = $pdo->prepare("UPDATE channel SET maincategory = ?, subcategory = ? WHERE channelid = ?");
			$stmt->bindValue(1, $params['maincategory']);
			$stmt->bindValue(2, $params['subcategory']);
			$stmt->bindValue(3, $params['channelid']);
			$stmt->execute();
		}
		elseif($params['opType'] == 'add') {
			$row_cont =  "(maincategory, subcategory, channelid ,channeltitle, viewcount, videocount,subscribercount,thumbnailurl,description,keywords,uploadsid, publishdate)";
			$row_array = array('maincategory','subcategory','channelid','title','viewcount',
			'videocount','subscribercount','thumbnail_url','description','keywords','uploads_id',
			'publish_date');
			$stmt = $pdo ->prepare("INSERT INTO channel $row_cont VALUES (?,?,?,?,?,?,?,?,?,?,?,?)");
			foreach ($row_array as $key => $value) {
				$stmt->bindValue($key+1, $params[$value]);
			}
			$stmt->execute();			
		}
		else{//fetch all data
			$sql = "SELECT * FROM {$params['table']}";
			$res = $pdo->query($sql);
			$array[] = array();

			foreach ($res as $data) {
				$array[] = $data;
			}

			echo json_encode($array);
		}
	}
?>