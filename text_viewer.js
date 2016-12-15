var texts = {123 : "Lause 1"};
var text_div = document.getElementById("text-box");
$(document).ready(function() {
    $('.dot').hover(function() {
      $(text_div).text(texts[$(this).attr('id')]);
      });
});




	
	

