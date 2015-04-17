var previousData;

$(document).ready(function() {
	render();
	resize();
	livereload();
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
		var value = $(el).data('value').substring(0, $(el).data('value').length - 1);;
		var suit = $(el).data('value').charAt($(el).data('value').length-1);
		console.log('value: ' + value + ', suit: ' + suit);
		if (suit === 'H' || suit === 'D')
			$(el).addClass('redCard');
		else
			$(el).addClass('blackCard')
		$(el).html('').append('<span>'+value+getSuitSymbol(suit)+'</span><span>'+value+getSuitSymbol(suit)+'</span>');
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

var livereload = function() {
	getData();
	var interval = window.setInterval(function() {
		getData();
	}, 1000);
}

var getData = function(cb) {
	$.post(window.location.href, function( data ) {
		if (data != previousData) {
			previousData = data;
			refresh(JSON.parse(data));
		}
	});
}

var refresh = function(data) {
	$('.json-beautify').html($('.json-beautify').html() + '\n========\n' + JSON.stringify(data, undefined, 4));

	$('#dealerBox').html(renderDealerHtml(data.dealer));
	render();
	resize();
	$('.players').html('');
	data.players.forEach(function(el, index, array) {
		$('.players').append(renderPlayerHtml(el));
		render();
		resize();
	});
}

var renderDealerHtml = function(dealer) {
	var dealerHtml = '';
	dealerHtml += '<div class="box">';
	dealerHtml += '	<div class="box-header">';
	dealerHtml += '		<h2 class="title">DEALER</h2>';
	dealerHtml += '	</div>';
	dealerHtml += '	<div class="box-body">';
	if (dealer && dealer.cards) {
		dealerHtml += '			<div class="cards">';
		dealerHtml += '				<div class="wrapper">';
		dealer.cards.forEach(function(card, index, array) {
			if (card === 'secret')
				dealerHtml += '					<div class="card hidden"></div>';
			else if (index < 2)
				dealerHtml += '					<div class="card rendercard" data-value="'+card+'"></div>';
			else
				dealerHtml += '					<div class="card rendercard" style="top: '+36*(index-1)+'px;" data-value="'+card+'"></div>';
		});
		dealerHtml += '				</div>';
		dealerHtml += '			</div>';
	}
	dealerHtml += '	</div>';
	dealerHtml += '</div>';
	return dealerHtml;
}

var renderPlayerHtml = function(el) {
	var playerHtml = '';
	playerHtml += '<div class="box">';
	playerHtml += '	<div class="box-header';
	if (el.status === 'currently turn')
		playerHtml += ' b-orange';
	playerHtml += '">';
	playerHtml += '		<h2 class="title">'+el.display_name+'&nbsp;&nbsp;&nbsp;</h2>';
	playerHtml += '     <p><span class="chips">$'+el.money+'</span> <span class="chips bet">($'+el.bet+')</span></p>';
	playerHtml += '	</div>';
	playerHtml += '	<div class="box-body';
	if (el.status === 'currently turn')
		playerHtml += ' b-sunflower';
	playerHtml += '">';
	if (el.cards) {
		playerHtml += '			<div class="cards">';
		playerHtml += '				<div class="wrapper">';
		el.cards.forEach(function(card, index, array) {
			if (index < 2)
				playerHtml += '					<div class="card rendercard" data-value="'+card+'"></div>';
			else
				playerHtml += '					<div class="card rendercard" style="top: '+36*(index-1)+'px;" data-value="'+card+'"></div>';
		})
		playerHtml += '				</div>';
		playerHtml += '			</div>';
	}
	playerHtml += '	</div>';
	playerHtml += '</div>';
	return playerHtml;
}