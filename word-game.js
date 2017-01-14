/*
 * For testing, run python -m SimpleHTTPServer
 * Then go to http://localhost:8000/
 * 
 **/

var Game = {};
// canvas variables
Game.$answerCanvas = null;
Game.answerContext = null;
Game.$letterCanvas = null;
Game.letterContext = null;
Game.canvasWidth = 0;
Game.canvasHeight = 0;
// level variables
Game.currentLevel = 1;
Game.isDragging = false;

Game.initialize = function() {
    console.log('init');
    Game.$answerCanvas = $('#answer-canvas');
    Game.answerContext = Game.$answerCanvas[0].getContext('2d');
    Game.$letterCanvas = $('#letter-canvas');
    Game.letterContext = Game.$letterCanvas[0].getContext('2d');

    Game.initCanvases();

    // setInterval(() => Game.loadLevel(Game.currentLevel++), 3000);
    Game.loadLevel(Game.currentLevel);
};

//#region Initialization

Game.initCanvases = function() {
    // fill the browser window dynamically
    window.addEventListener('resize', Game.resizeCanvas, false);
    // using touch events to work with mobile, we can add some mouse events here later to work with desktop
    Game.$letterCanvas.on('mousedown', () => {
        this.isDragging = true;
    });
    window.addEventListener('mousemove', () => {
        if (this.isDragging) {
            console.log('dragging');
        }
    })
    window.addEventListener('mouseup', () => {
        this.isDragging = false;
    });
    Game.resizeCanvas();
};

Game.resizeCanvas = function() {
    Game.canvasWidth = window.innerWidth;
    Game.canvasHeight = window.innerHeight / 2;
    Game.$answerCanvas.attr('width', Game.canvasWidth);
    Game.$answerCanvas.attr('height', Game.canvasHeight);
    Game.$letterCanvas.attr('width', Game.canvasWidth);
    Game.$letterCanvas.attr('height', Game.canvasHeight);

    // on resize, we need to redraw all canvases
    Game.redrawAll();
};

//#endregion Initialization

//#region Canvas Drawing

Game.redrawAll = function() {
    Game.drawAnswers();
    Game.drawLetters();
};

Game.drawAnswers = function() {
    Game.answerContext.clearRect(0, 0, Game.canvasWidth, Game.canvasHeight);
    Game.answerContext.font = '48px Lucida Sans Unicode, Lucida Grande, sans-serif';
    Game.answerContext.fillStyle = 'white';
    Game.answerContext.fillText(Level.words.toString(), 10, 50);
};

Game.drawLetters = function() {
    Game.letterContext.clearRect(0, 0, Game.canvasWidth, Game.canvasHeight);
    Game.letterContext.font = '48px Lucida Sans Unicode, Lucida Grande, sans-serif';
    Game.letterContext.fillStyle = 'white';
    Game.letterContext.fillText(Level.letters.toString(), 10, 50);

    Game.letterContext.beginPath();
    Game.letterContext.arc(Game.canvasWidth / 2, Game.canvasHeight / 2, Game.canvasHeight / 2 - 10, 0, 2 * Math.PI);
    Game.letterContext.stroke();
};

Game.letterCanvasDrag = function() {
    console.log('dragging')
};

//#endregion Canvas Drawing

Game.loadLevel = function(levelNumber) {
    Level.loadJSON(Game.padLevelNumber(levelNumber), function() {
        console.log(Level.words);
        console.log(Level.letters);

        Game.drawAnswers();
        Game.drawLetters();
    });
};

Game.padLevelNumber = function(level) {
    var s = '0000000000' + level;
    return s.substr(s.length - 3);
};

$(document).on('ready', function() {
    Game.initialize();
});