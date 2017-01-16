Level = {};
Level.words = [];
Level.letters = [];

Level.loadJSON = function(fileName, callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', '/levels/level_' + fileName + '.json', true);
    xobj.onreadystatechange = function() {
        if (xobj.readyState == 4 && xobj.status == "200") {
            var response = JSON.parse(xobj.responseText);
            Level.words = response.words;
            Level.letters = response.letters;
            callback();
        }
    };
    xobj.send(null);
}