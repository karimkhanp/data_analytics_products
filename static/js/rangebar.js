
var slider = document.getElementById("myRange1");
var output = document.getElementById("demo1");
output.innerHTML = slider.value+"%";

slider.oninput = function() {
  output.innerHTML = this.value+"%";
}

var slider = document.getElementById("myRange2");
var output = document.getElementById("demo2");
output.innerHTML = slider.value+"%";

slider.oninput = function() {
  output.innerHTML = this.value+"%";
}


var slider = document.getElementById("myRange3");
var output = document.getElementById("demo3");
output.innerHTML = slider.value+"%";

slider.oninput = function() {
  output.innerHTML = this.value+"%";
}
