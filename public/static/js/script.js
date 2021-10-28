import Modal from "./modal.js";

let dinosaurs_positions;
let number_dinosaurs;
let robot_position;
let grid_columns;
let grid_rows;
let dinosaurs;
let game = {};
let $header;
let $robot;
let $grid;

// Main functions
function renderGame() {
  $header.innerText = `Game ID: ${game.id}`;

  setDinosaursPosition();
  setRobotPosition();

  document.onkeydown = (event) => {
    switch (event.key) {
      case "ArrowLeft":
        moveRobot("left");
        break;
      case "ArrowRight":
        moveRobot("right");
        break;
      case "ArrowUp":
        moveRobot("front");
        break;
      case "ArrowDown":
        moveRobot("behind");
        break;
      case "Enter":
      case "Space":
      case " ":
        attack();
        break;
      default:
        break;
    }

    setDinosaursPosition();
    setRobotPosition();
  };
}

function finishGame() {
  document.onkeydown = () => {};
  $header.innerText = "";
  $grid.innerHTML = "";

  fetch(`http://localhost:8000/api/game/delete?id=${game.id}`);

  Modal.setModalContent(
    "Game over. You won!",
    `
    <div class="row w-100 h-100 gap-10">
        <div class="form-control w-100">
            <button class="primary w-100" id="create-game">Create a new game</button>
        </div>
        <div class="form-control w-100">
            <button class="w-100" id="join-game">Join a game</button>
        </div>
    </div>
    `
  );

  document.getElementById("create-game").onclick = getGameData;
  document.getElementById("join-game").onclick = joinGame;
}

function joinGame() {
  Modal.setModalContent(
    "Join a game",
    `
    <form class="cols w-100 gap-10" id="game-id-form">
        <div class="form-control">
            <label for="game-id">Enter game ID:</label>
            <input type="number" id="game-id" required autofocus>
        </div>
        <div class="form-control w-100">
            <button type="submit" class="w-20">Join</button>
        </div>
    </form>
    <section>
        <h4 class="error-message"></h4>
    </section>
    <a href="/" class="w-100"><- Back</a>
    `
  );
  const $game_id = document.getElementById("game-id");

  document.getElementById("game-id-form").onsubmit = (event) => {
    event.preventDefault();
    event.stopPropagation();

    game.id = $game_id.value;

    fetch(`http://localhost:8000/api/game?id=${game.id}`)
      .then((res) => res.json())
      .then((json) => {
        if (json.status != "success") {
          Modal.$modal.querySelector(".error-message").innerText = json.message;
          return;
        }

        Modal.hide();
        Modal.clearModalContent();

        grid_columns = json.grid_columns;
        grid_rows = json.grid_rows;

        renderGrid();

        dinosaurs = JSON.parse(json.dinosaurs);
        game.robot_id = json.robot_id;
        game.id = json.id;

        renderGame();
      });
  };
}

function getGameData() {
  Modal.setModalContent(
    "Set game data",
    `
    <form class="cols w-100 gap-10" id="game-data-form">
      <div class="row w-100 gap-10">
        <div class="form-control h-100">
          <label for="number-dinosaurs">* Number of dinosaurs:</label>
          <input type="number" id="number-dinosaurs" min="5" max="1250" autofocus>

          <div class="h-60 cols scroll-y" id="dinosaurs-positions">
          </div>
        </div>
        <div class="form-control h-100">
          <label for="grid-columns">* Number of grid columns:</label>
          <input type="number" id="grid-columns" min="10" max="50">

          <label for="grid-rows">* Number of grid rows:</label>
          <input type="number" id="grid-rows" min="10" max="50">

          <label>* Robot position:</label>
          <div class="row gap-8">
              <input type="number" placeholder="Column" id="robot-pos-x">
              <input type="number" placeholder="Row" id="robot-pos-y">
          </div>
        </div>
      </div>
      <div class="form-control w-100">
        <button type="submit" class="w-20">Start</button>
      </div>
    </form>

    <section>
        <h4 class="error-message"></h4>
    </section>

    <a href="/" class="w-100"><- Back</a>
    `
  );
  const $number_dinosaurs = document.getElementById("number-dinosaurs");
  const $grid_columns = document.getElementById("grid-columns");
  const $robot_pos_x = document.getElementById("robot-pos-x");
  const $robot_pos_y = document.getElementById("robot-pos-y");
  const $grid_rows = document.getElementById("grid-rows");

  $number_dinosaurs.onchange = () => {
    const $dinosaurs_positions = document.getElementById("dinosaurs-positions");
    $dinosaurs_positions.innerHTML = "";

    for (let i = 0; i < $number_dinosaurs.value; i++)
      $dinosaurs_positions.innerHTML += `
      <section>
        <label>* Dinosaur ${i + 1} position:</label>
        <div class="row gap-8">
            <input type="number" placeholder="Column" required>
            <input type="number" placeholder="Row" required>
        </div>
      </section>
      `;
  };

  document.getElementById("game-data-form").onsubmit = (event) => {
    event.preventDefault();
    event.stopPropagation();

    let robot_pos_x = parseInt($robot_pos_x.value);
    if (isNaN(robot_pos_x)) {
      Modal.$modal.querySelector(".error-message").innerText =
        "Robot position (Column) must be an integer number.";
      return;
    }
    let robot_pos_y = parseInt($robot_pos_y.value);
    if (isNaN(robot_pos_y)) {
      Modal.$modal.querySelector(".error-message").innerText =
        "Robot position (Row) must be an integer number.";
      return;
    }

    dinosaurs_positions = [];
    number_dinosaurs = $number_dinosaurs.value;
    robot_position = [robot_pos_x, robot_pos_y];
    grid_columns = $grid_columns.value;
    grid_rows = $grid_rows.value;

    for (let i = 0; i < number_dinosaurs; i++) {
      const $dinosaur_position = document.querySelectorAll(
        "#dinosaurs-positions section"
      )[i];
      const X = parseInt($dinosaur_position.querySelectorAll("input")[0].value);
      const Y = parseInt($dinosaur_position.querySelectorAll("input")[1].value);

      if (isNaN(X) || isNaN(Y)) {
        Modal.$modal.querySelector(".error-message").innerText =
          "Dinosaur position (X and Y) must be integer numbers.";
        return;
      }

      dinosaurs_positions.push([X, Y]);
    }

    createGame();
  };
}

function renderGrid() {
  for (let i = 0; i < grid_columns * grid_rows; i++)
    $grid.innerHTML += "<div></div>";

  $grid.style.gridTemplateColumns = `repeat(${grid_columns}, 1fr)`;
  $grid.style.gridTemplateRows = `repeat(${grid_rows}, 1fr)`;
}

function setRobotPosition() {
  $grid.querySelectorAll("div").forEach((elemento) => (elemento.id = ""));

  fetch(`http://localhost:8000/api/robot?id=${game.robot_id}`)
    .then((res) => res.json())
    .then((json) => {
      $robot = $grid.querySelectorAll("div")[json.X + json.Y * grid_columns];
      $robot.id = "robot";
    });
}

function setDinosaursPosition() {
  $grid
    .querySelectorAll("div")
    .forEach((element) => element.classList.remove("dinosaur"));

  fetch(`http://localhost:8000/api/game?id=${game.id}`)
    .then((res) => res.json())
    .then((json) => {
      console.log(json);

      // If there are not dinosaurs, the game has finished:
      if (json.dinosaurs == "{}") finishGame();

      dinosaurs = JSON.parse(json.dinosaurs);

      for (let dinosaur_position of Object.values(dinosaurs)) {
        const $dino =
          $grid.querySelectorAll("div")[
            dinosaur_position.X + dinosaur_position.Y * grid_columns
          ];
        $dino.classList.add("dinosaur");
      }
    });
}

function moveRobot(direction) {
  fetch(
    `http://localhost:8000/api/robot/move?id=${game.robot_id}&direction=${direction}`
  )
    .then((res) => res.json())
    .then((json) => {
      console.log(json);

      setRobotPosition();
    });
}

function attack() {
  console.log("attack");

  fetch(`http://localhost:8000/api/robot/attack?id=${game.robot_id}`)
    .then((res) => res.json())
    .then((json) => {
      console.log(json);

      setDinosaursPosition();
    });
}

function createGame() {
  fetch(
    `http://localhost:8000/api/game/create?grid_cols=${grid_columns}&grid_rows=${grid_rows}&num_dinos=${number_dinosaurs}&dinos_pos=${JSON.stringify(
      dinosaurs_positions
    )}&robot_pos=${JSON.stringify(robot_position)}`
  )
    .then((res) => res.json())
    .then((json) => {
      if (json.status != "success") {
        Modal.$modal.querySelector(".error-message").innerText = json.message;
        return;
      }

      Modal.hide();
      Modal.clearModalContent();

      renderGrid();

      dinosaurs = JSON.parse(json.dinosaurs);
      game.robot_id = json.robot_id;
      game.id = json.id;

      renderGame();
    });
}

function main() {
  $header = document.querySelector("header h1");
  $grid = document.querySelector("main");

  Modal.setModalContent(
    "Welcome",
    `
    <div class="row w-100 h-100 gap-10">
        <div class="form-control w-100">
            <button class="primary w-100" id="create-game">Create a new game</button>
        </div>
        <div class="form-control w-100">
            <button class="w-100" id="join-game">Join a game</button>
        </div>
    </div>
    `
  );

  document.getElementById("create-game").onclick = getGameData;
  document.getElementById("join-game").onclick = joinGame;
}

document.readyState == "complete"
  ? main()
  : document.addEventListener("DOMContentLoaded", main);
