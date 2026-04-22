let wrapper = document.getElementById('wrapper');
let button = wrapper.querySelector('button');
let loader = document.getElementById('loader');
let warning = document.getElementById('warning');
let cards = wrapper.getElementsByClassName('card');
let i = 0;

function foward(){
	if(i > cards.length - 2) return;

	cards[++i].style.transform = "translateY(-"+ 390*i +"px)";
	wrapper.style.transform = "translateY(-"+10*i+"px)";
	cards[i].style.opacity = 1;
	loader.style.width = 100*i/(cards.length-1) + "%";
}

function backwards(){
	if(i <= 0) return;

	cards[i].style.opacity = 1;
	cards[i].style.transform = "translateY("+ 430*i--/cards.length +"vh)";
	cards[i].style.opacity = 1;
	wrapper.style.transform = "translateY(-"+2*i+"vh)";
	loader.style.width = 100*i/(cards.length-1) + "%";
}

button.onclick = function(){
	warning.style.opacity = 0;
	warning.style.transform = "translateY(-200px)";

	window.onkeydown = function(e){
		if(e.keyCode == 32 || e.keyCode == 40 || e.keyCode == 13 || e.keyCode == 83)
			foward();
		if(e.keyCode == 38 || e.keyCode == 87)
			backwards()
	}

	window.onclick = foward;
}