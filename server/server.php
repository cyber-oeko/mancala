<?php
header('Content-Type: application/json');
require_once("db_connect.php");
$mysqli = new mysqli($db_host, $db_user, $db_pass, $db_name);
if ($mysqli->connect_error) {
  echo json_encode(["success" => false]);
}
$data = json_decode(file_get_contents('php://input'), true);
if(isset($data["write"])){
    if($data["write"] == "move"){
        $type = $data["type"];
        $game_id = $data["game_id"];
        $player = $data["player"];
        $x = $data["x"];
        $y = $data["y"];
        $data = $data["data"];
        $sql = "INSERT INTO moves (type, game_id, player, x, y, data) VALUES ($type, $game_id, '$player', $x, $y, $data)";
        if ($mysqli->query($sql) === TRUE) {
          $insert_id = $mysqli->insert_id;
          echo json_encode(["success" => true, "move_id" => $insert_id]);
        } else {
          echo json_encode(["success" => false, "error" => $mysqli->error]);
        }
    }elseif($data["write"] == "newgame"){
        $player = $data["player"];
        $sql = "INSERT INTO `games` (`player1`) VALUES ('$player');";
        if ($mysqli->query($sql) === TRUE) {
          $insert_id = $mysqli->insert_id;
          echo json_encode(["success" => true, "game_id" => $insert_id]);
        } else {
          echo json_encode(["success" => false, "error" => $mysqli->error]);
        }
    }elseif($data["write"] == "joingame"){
        $player = $data["player"];
        $game_id = $data["game_id"];
        $sql = "UPDATE `games` SET `player2`='$player' WHERE `id`=$game_id AND `player2` IS NULL ORDER BY `id` DESC LIMIT 1;";
        if ($mysqli->query($sql) === TRUE) {
        } else {
          echo json_encode(["success" => false, "error" => $mysqli->error]);
        }
        $sql = "SELECT * FROM `games` WHERE `id`=$game_id ORDER BY `id` DESC LIMIT 1";
        $result = $mysqli->query($sql);
        if ($result->num_rows > 0) {
            $row = $result->fetch_assoc();
            $row["success"] = true;
            echo json_encode($row);
        }else{
          echo json_encode(["success" => false, "error" => ""]);
        }
    }
}elseif(isset($_GET["game_id"])){
    if(isset($_GET["check_joined"])){
        $game_id = $_GET["game_id"];
        $sql = "SELECT * FROM `games` WHERE `id`=$game_id ORDER BY `id` DESC LIMIT 1";
        $result = $mysqli->query($sql);
        if ($result->num_rows > 0) {
            $row = $result->fetch_assoc();
            $row["success"] = true;
            echo json_encode($row);
        }else{
          echo json_encode(["success" => false, "error" => "game not existent"]);
        }
    }else{
        $game_id = $_GET["game_id"];
        $sql = "SELECT * FROM `moves` WHERE `game_id`=$game_id ORDER BY `id` DESC LIMIT 1";
        $result = $mysqli->query($sql);
        if ($result->num_rows > 0) {
            $row = $result->fetch_assoc();
            $row["success"] = true;
            echo json_encode($row);
        }else{
            echo json_encode(["success"=>true, "id"=>-2]);
        }
    }
}
$mysqli->close();
?>
