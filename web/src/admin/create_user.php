<?php

if (isset($_POST['id']) && isset($_POST['pass'])) {
    //パスワードの暗号化
    $hash_pass = password_hash($_POST['pass'], PASSWORD_DEFAULT);

    try {
        // データベースへの接続開始
        $dbopts = parse_url(getenv('DATABASE_URL'));
        $pdo = new PDO('pgsql:host='.$dbopts["host"].'; dbname='.ltrim($dbopts["path"],'/'), $dbopts["user"], $dbopts["pass"]);
        // bindParamを利用したSQL文の実行
        $sql = 'INSERT INTO usrinfo (id, pass) VALUES(:id, :pass);';
        $sth = $pdo->prepare($sql);
        $sth->bindParam(':id', $_POST['id']);
        $sth->bindParam(':pass', $hash_pass);
        $sth->execute();

        // データベースへの接続に失敗した場合
    } catch (PDOException $e) {
        print('接続失敗:' . $e->getMessage());
        die();
    }
}
?>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>ユーザ情報の登録画面</title>
</head>
<body>

<p>ユーザ情報</p>
<form action="create_user.php" method="post">
ID:<input type="text" name="id"><br>
PASS:<input type="text" name="pass">
<input type="submit" value="送信">
</form>

</body>
</html>