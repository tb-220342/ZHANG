<!doctype html>
<html lang="ja">

<head>
<meta charset="UTF-8">
<title>5-1</title>
</head>

<body>
<?php
    // DB接続設定
    $dsn = 'mysql:dbname=データベース名;host=localhost';
	$user = 'ユーザー名'';
	$password = 'PASSWORD';
    $pdo = new PDO($dsn, $user, $password, array(PDO::ATTR_ERRMODE => PDO::ERRMODE_WARNING));

    
	$sql = "CREATE TABLE IF NOT EXISTS mission5_1"
	." ("
	. "id INT AUTO_INCREMENT PRIMARY KEY,"
	. "name char(32),"
    . "comment TEXT,"
    . "date TEXT,"
    . "pass TEXT"
	.");";
    $stmt = $pdo->query($sql);

    
         
         if(!empty($_POST["post_editnum"] && !empty($_POST["editpass"]))){
            $editnum=$_POST["post_editnum"];
            //抽出
            $sql = 'SELECT * FROM mission5_1';
            $stmt = $pdo->query($sql);
            $results = $stmt->fetchAll();
            foreach ($results as $row){
                 if($editnum==$row['id'] && $_POST["editpass"]==$row['pass'] &&
                    $row['comment']!==""){
                    $send_editnum=$row['id'];
                    $editname=$row['name'];
                    $editcomment=$row['comment'];
                    $txt="編集";
                    break;
                 }else{
                    $editname="";
                    $editcomment="";
                 }
            }
        }
    
        //名前とコメントが送信されたとき
        elseif(!empty($_POST["name"]) && !empty($_POST["comment"])){
        
            //編集用パスワードが同時に送信されたとき
            if(!empty($_POST["send_editnum"])){
                $editname=$_POST["name"];
                $editcomment=$_POST["comment"];
                date_default_timezone_set("Asia/Tokyo");
                $date=date("Y年/m月/n日　H時/i分/s秒");

                //入力したデータレコードを抽出
                 $sql = 'SELECT * FROM mission5_1';
                 $stmt = $pdo->query($sql);
                 $results = $stmt->fetchAll();
                 foreach ($results as $row){
                     //$rowの中にはテーブルのカラム名が入る
                    $id = $_POST["send_editnum"]; //変更する投稿番号
	                $name = $editname;
                    $comment = $editcomment;
                    $date = $date;
	                $sql = 'UPDATE mission5_1 SET name=:name,comment=:comment,date=:date WHERE id=:id';
	                $stmt = $pdo->prepare($sql);
	                $stmt->bindParam(':name', $name, PDO::PARAM_STR);
                    $stmt->bindParam(':comment', $comment, PDO::PARAM_STR);
                    $stmt->bindParam(':date', $date, PDO::PARAM_STR);
	                $stmt->bindParam(':id', $id, PDO::PARAM_INT);
                    $stmt->execute(); 
                }

            
            //新規の投稿を行うとき
            }else{
                    if(!empty($_POST["postpass"])){
                        $post_pass=$_POST["postpass"];
                    }
                $post_name=$_POST["name"];
                $post_comment=$_POST["comment"];
                date_default_timezone_set("Asia/Tokyo");
                $date_create=date("Y年/m月/n日　H時/i分/s秒");
                
                //データベースに書き込み
                $sql = $pdo -> prepare("INSERT INTO mission5_1 (name, comment, date, pass) VALUES (:name, :comment, :date, :pass)");
	            $sql -> bindParam(':name', $name, PDO::PARAM_STR);
                $sql -> bindParam(':comment', $comment, PDO::PARAM_STR);
                $sql -> bindParam(':date', $date, PDO::PARAM_STR);
                $sql -> bindParam(':pass', $pass, PDO::PARAM_STR);
                $name=$post_name;
                $comment=$post_comment;
                $date=$date_create;
                $pass=$post_pass;
                $sql -> execute();
                
                

            }

        }
    
        if(!empty($_POST["delnum"]) && !empty($_POST["delpass"]) && empty($_POST["name"]) &&
        empty($_POST["comment"])){
            $delnumber=$_POST["delnum"];
            $delpass=$_POST["delpass"];
            $sql = 'SELECT * FROM mission5_1';
            $stmt = $pdo->query($sql);
            $results = $stmt->fetchAll();
            $i=0;
            foreach($results as $row)
            {$i++;
            if($i==$_POST["delnum"]){
                if($_POST["delpass"]==$row["pass"]){
                    $id=$row["id"];
                    $sql = 'UPDATE mission5_1 SET name=:name,comment=:comment,date=:date,pass=:pass WHERE id=:id';
                    $stmt = $pdo->prepare($sql);
                    $stmt->bindParam(':name', $name, PDO::PARAM_STR);
                    $stmt->bindParam(':comment', $comment, PDO::PARAM_STR);
                    $stmt->bindParam(':date', $date, PDO::PARAM_STR);
                    $stmt->bindParam(':pass', $pass, PDO::PARAM_STR);
                    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
                    $stmt->execute();}
            }}
                    
                }
    

    //表示
    $sql = 'SELECT * FROM mission5_1';
	$stmt = $pdo->query($sql);
	$results = $stmt->fetchAll();
	foreach ($results as $row){
		echo $row['id'].' ';
        echo $row['name'].' ';
        echo $row['date'].' ';
        if(!empty($row['pass'])){
            echo "パスワード(不可視)"."<br>";
        }else{
            echo "<br>";
        }
        echo $row['comment']."<br>";
        echo "<br>";
	    echo "<hr>";
	}

?>

<form action="" method="post">

<h1>入力フォーム</h1>
<!--編集番号が指定されたとき、その番号を受け取る-->
<input type="hidden" name="send_editnum" 
       value="<?php 
       if(!empty($_POST["post_editnum"]) && !empty($_POST["editpass"])){
             echo $send_editnum;
        }
             ?>"
>
<br>


<label>
    お名前：&emsp;
    <input type="txt" name="name" placeholder="お名前" 
           value="<?php 
           if(!empty($_POST["post_editnum"]) && !empty($_POST["editpass"])){
               echo $editname;
           }
                    ?>"
    >
    <br>
</label>

<!--コメントの入力エリアを作成-->
<labe">
    コメント:
    <input type="txt" name="comment" placeholder="コメント"
            value="<?php
            if(!empty($_POST["post_editnum"]) && !empty($_POST["editpass"])){
                echo $editcomment;
            }
                    ?>"
    >
    <br>
</label>

<label>
    パスワード：
    <input type="password" name="postpass" maxlength="10">
    <br>
</label> 
                    
<input type="submit" name="submit"
       value="<?php
       if(!empty($txt)){
        echo $txt;
       }else{
        echo "投稿";
       }
                ?>"
>
<br>
<br>
<h1>削除フォーム</h1>
<!--削除番号の入力エリア-->
<label>
    削除番号：
    <input type="number" name="delnum" min="1">
    <br>
</label>

<!--削除する際に入力するパスワードの入力エリア-->
<label>
    パスワード：
    <input type="password" name="delpass" maxlength="10">
    <br>
</label>

<!--削除番号とパスワードを送信-->
<input type="submit" name="delsubmit" value="削除">
<br>
<br>
<h1>編集フォーム</h1>
<!--編集する投稿番号の入力エリア-->
<label>
編集対象番号:
<input type="number" min=1 name="post_editnum">
<br>
</label>
            
<!--編集する際のパスワードを入力-->
<label>
パスワード：
<input type="password" name="editpass" maxlength="10">
<br>
</label>
            
<input type="submit" name="editsubmit" value="編集指定">
<br>
<br>

</form>



</body>

</html>
