<?php
session_start();
// session_unset($_SESSION);
// print($_SESSION);

if (isset($_SESSION['auth'])) {
    $_SESSION['auth'] = false;
}

$error = "";

if (isset($_POST['userid']) && isset($_POST['password'])) {
    try {
        // データベースへの接続開始
        $dbopts = parse_url(getenv('DATABASE_URL'));
        $pdo = new PDO('pgsql:host='.$dbopts["host"].'; dbname='.ltrim($dbopts["path"],'/'), $dbopts["user"], $dbopts["pass"]);

        // bindParamを利用したSQL文の実行
        $cmd = 'SELECT pass FROM usrinfo WHERE id = :id;';
        $sth = $pdo->prepare($cmd);
        $sth->bindParam(':id', $_POST['userid']);
        $sth->execute();
        $pass = $sth->fetch();
        // print($_POST['password']);
        //認証処理
        if(password_verify($_POST['password'], $pass['pass'])){
            session_regenerate_id(true);
            $_SESSION['auth'] = true;
            $_SESSION['username'] = $_POST['userid'];
            // print '認証成功';
        }else{
            $error = 'ユーザーIDかパスワードに誤りがあります';
            print '認証失敗';
        }
    // データベースへの接続に失敗した場合
    } catch (PDOException $e) {
        print('接続失敗:' . $e->getMessage());
        die();
    }
}
elseif(isset($_SESSION['username'])){
    $_SESSION['auth'] = true;
}
if ($_SESSION['auth'] !== true) {
?>

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ログイン</title>
    <style>
        .container {
            width: 100%;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="login">
            <h1>認証フォーム</h1>
            <?php 
                if($error) echo '<p style="color:red;">'.$error.'</p>';
            ?>
            <form action="admin.php" method="post">
                <dl>
                    <dt><label for="userid">ユーザーID:</label></dt>
                    <dd><input type="text" name="userid" value=""></dd>
                </dl>
                <dl>
                    <dt><label for="password">パスワード：</label></dt>
                    <dd><input type="password" name="password" id="password" value=""></dd>
                </dl>
                <input type="submit" name="submit" value="ログイン">
            </form>
        </div>
    </div>
</body>
</html>

<?php
    exit();
}
?>
<html>
  <head>
    <meta name="viewport" content="width=device-width,initial-scale=1,shrink-to-fit=no"" charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="css/main.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script> 
    <script src="https://unpkg.com/react@16/umd/react.development.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@16/umd/react-dom.development.js" crossorigin></script>
    <script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
    <script type="text/babel" src="./js/channelManager.js"></script>
  </head>

  <body>
    <div id="chanManager"></div>
  </body>
</html>