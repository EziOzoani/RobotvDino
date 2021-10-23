const grid_columns = 20;
let game = {};
let $robot;
let $grid;

function setRobotPosition() {
    $grid.querySelectorAll('div').forEach(elemento => elemento.id = '');

    fetch(`http://localhost:8000/api/robot?id=${game.robot_id}`)
        .then(res => res.json())
        .then(json => {
            $robot = $grid.querySelectorAll('div')[json.X + json.Y * grid_columns];
            $robot.id = 'robot';
        });
}

function setDinosaursPosition() {
    $grid.querySelectorAll('div').forEach(element => element.classList.remove('dinosaur'));

    fetch(`http://localhost:8000/api/game?id=${game.robot_id}`)
        .then(res => res.json())
        .then(json => {
            dinosaurs = JSON.parse(json.dinosaurs);

            for (let dinosaur_position of Object.values(dinosaurs)) {
                const $dino = $grid.querySelectorAll(
                    'div'
                )[dinosaur_position.X + dinosaur_position.Y * grid_columns];
                $dino.classList.add('dinosaur')
            }
        });
}

function moveRobot(direction) {
    fetch(`http://localhost:8000/api/robot/move?id=${game.robot_id}&direction=${direction}`)
        .then(res => res.json())
        .then(json => {
            console.log(json);

            setRobotPosition();
        });
}

function attack() {
    console.log('attack')
    fetch(`http://localhost:8000/api/robot/attack?id=${game.robot_id}`)
        .then(res => res.json())
        .then(json => {
            console.log(json);

            setDinosaursPosition();
        });
}

function main() {
    $grid = document.querySelector('main');

    fetch('http://localhost:8000/api/game/create')
        .then(res => res.json())
        .then(json => {
            dinosaurs = JSON.parse(json.dinosaurs);
            game.robot_id = json.robot_id;
            game.id = json.id;

            for (let dinosaur_position of Object.values(dinosaurs)) {
                const $dino = $grid.querySelectorAll(
                    'div'
                )[dinosaur_position.X + dinosaur_position.Y * grid_columns];
                $dino.classList.add('dinosaur');
            }

            setRobotPosition();
        });

    document.addEventListener('keydown', event => {
        switch (event.key) {
            case 'ArrowLeft':
                moveRobot('left');
                break;
            case 'ArrowRight':
                moveRobot('right');
                break;
            case 'ArrowUp':
                moveRobot('front');
                break;
            case 'ArrowDown':
                moveRobot('behind');
                break;
            case 'Space':
            case ' ':
                attack();
                break;
            default:
                break;
        }

        setDinosaursPosition();
        setRobotPosition();
    });
}

document.readyState == 'complete'? main(): document.addEventListener('DOMContentLoaded', main);
