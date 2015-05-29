var Player = require('player');

if(process.argv.length <= 2) {
	console.log('Please give me a song!');
	process.exit();
}

var player = new Player(process.argv[2]);

player.play(function(err, player){
	console.log('End playback!');
});
