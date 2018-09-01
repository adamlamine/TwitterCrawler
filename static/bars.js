var input1 = document.getElementById("input1");
var input2 = document.getElementById("input2");

var tweets1box = document.getElementById("tweets1");
var tweets2box = document.getElementById("tweets2");
var score1box = document.getElementById("score1");
var score2box = document.getElementById("score2");

var init = function(tweets1, tweets2, score1, score2){
	
	
	
	if (score1 < 0) {score1 = 0;}
	if (score2 < 0) {score2 = 0;}
	
	score1 *= 33;
	score2 *= 33;
	
	if (tweets1 > 90) {tweets1 = 90;}
	if (tweets2 > 90) {tweets2 = 90;}
	if (score1 > 90) {score1 = 90;}
	if (score2 > 90) {score2 = 90;}
	
	
	
	
	tweets1box.style.width = tweets1 + "%";
	tweets2box.style.width = tweets2 + "%";
	score1box.style.width = score1 + "%";
	score2box.style.width = score2 + "%";
}

var refresh = function(){
	var i1 = document.getElementById("input1").value;
	var i2 = document.getElementById("input2").value;
	
	var url = i1 + "&" + i2 + "&1";
	window.location.replace(url);
	
}

window.onkeyup = function(e) {
   var key = e.keyCode ? e.keyCode : e.which;

   if (key === 13) {
       refresh();
   }
}