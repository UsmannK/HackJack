$(document).ready(function() {
	render();
	resize();
});

var resize = function() {
	$('.card').each(function(index, el) {
		$(el).height($(el).width()*1.4);
	});
	$('.cards .wrapper').each(function(index, el) {
		var extraHeight = ($(el).children('.card').length-2) * 36;
		$(el).height(extraHeight + $(el).children('.card').height());
	});
}

var render = function() {
	$('.rendercard').each(function(index, el) {
		var value = $(el).data('value').charAt(0);
		var suit = $(el).data('value').charAt(1);
		console.log('value: ' + value + ', suit: ' + suit);
		if (suit === 'H' || suit === 'D')
			$(el).addClass('redCard');
		else
			$(el).addClass('blackCard')
		$(el).append('<span>'+value+getSuitSymbol(suit)+'</span><span>'+value+getSuitSymbol(suit)+'</span>');
	});


}

var getSuitSymbol = function(ch) {
	switch (ch) {
		case 'H':
			return '&hearts;'
		case 'S':
			return '&spades;'
		case 'D':
			return '&diams;'
		case 'C':
			return '&clubs;'
		default:
			return
	}
}