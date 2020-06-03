window.onload = function() {
	var image = document.getElementById("active-game-image");

	function update_active_game() {
		image.src = image.src.split("?")[0] + "?" + new Date().getTime();
	}

	setInterval(update_active_game, 10000);
}