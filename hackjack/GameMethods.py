from hackjack import db
from hackjack.models import *
from hackjack.consts import *
import hackjack.mongo_to_dict as jsonHelper
import json
from threading import Timer
from random import randint

def authenticate(passed_uname, passed_pwd):
	users = User.objects
	admins = Admin.objects
	for user in users:
		if user.display_name == passed_uname:
			if user.passphrase == passed_pwd:
				return True
	for admin in admins:
		if admin.display_name == passed_uname:
			if admin.passphrase == passed_pwd:
				return True
	return False

def table_exists(table_name):
	tables = Table.objects
	for table in tables:
		if table_name == table.table_name:
			return True
	return False

def find_table(table_name):
	tables = Table.objects
	for table in tables:
		if table_name == table.table_name:
			return table
	return None

def is_player_turn(passed_uname, table):
	return passed_uname == table.turn_name

def is_in_table(username, table):
	for player in table.players:
		if player.display_name == username:
			return True
	return False

def deal_cards(table):
	for player in table.players:
		player.card = []
		player.cards.append(new_card(table))
		player.cards.append(new_card(table))
		player.save()
	dealer = Dealer()
	dealer.cards = []
	dealer.cards.append(new_card(table))
	dealer.cards.append(new_card(table))
	dealer.flipped = True
	table.dealer = dealer
	dealer.save()
	table.save()

def check_bets_and_continue(table):
	if table.table_status_code == 1:
		players = table.players

		for player in players:
			if player.status_code == 1:
				player.status_code=3
				player.status=player_status_codes[player.status_code]
				if player.bet == 0:
					player.bet = table.min_bet
					player.money -= player.bet
				player.save()

	table.save()
	deal_cards(table)
	first_player = table.players[table.curStart]
	first_player.status_code=2
	first_player.status=player_status_codes[first_player.status_code]
	first_player.save()
	table.save()

def create_player(username):
	player = Player()
	player.display_name = username
	player.money = 100
	player.cards = []
	player.status_code=0
	player.status = player_status_codes[player.status_code]
	player.bet=0
	player.doubled_down=False
	return player

#Finish testing following methods on local branch before pushing

def create(username, table_name):
	#Initialize table admin
	table_admin = Player()
	table_admin.display_name = username
	table_admin.money = 100
	table_admin.cards = []
	table_admin.status_code=0
	table_admin.status = player_status_codes[table_admin.status_code]
	table_admin.bet=0
	table_admin.doubled_down=False

	#Initialize table
	table = Table()
	table.table_name = table_name
	table.table_admin_name = username
	table.table_status_code = 0
	table.table_status = table_status_codes[table.table_status_code]
	table.players = [table_admin]
	table.turn_index=0
	table.turn_name=table_admin.display_name
	table.curStart=0
	table.min_bet=5
	table.drawn_cards=[]
	table.save()
	return serialize_table(table)

def start(username, table):
	players = table.players

	for player in players:
		player.status_code=1
		player.status=player_status_codes[player.status_code]
		#player.save()

	table.table_status_code=1
	table.table_status = table_status_codes[table.table_status_code]

	table.save()

	t = Timer(15.0, check_bets_and_continue(table))
	t.start()
	return json.dumps(success_table_started)

def join(username, table):
	# table = find_table(table_name)
	if not table.table_status_code == 0:
		return json.dumps(game_in_progress_join)

	table.players.append(create_player(username))
	table.save()
	return serialize_table(table)

def hit(username, table):
	cur_player = None
	for player in table.players:
		if player.display_name == username:
			cur_player = player

	if not cur_player.status_code == 2:
		return json.dumps(cant_hit)

	#Give cur Cards
	cur_player.cards.append(new_card(table))

	if card_eval(cur_player.cards) > 21:
		cur_player.status_code = 6
		cur_player.status=player_status_codes[player.status_code]
	else:
		cur_player.status_code = 3
		cur_player.status=player_status_codes[player.status_code]

	cur_player.save()
	table.save()

	next_turn(table)

def stay(username, table):
	cur_player = None
	for player in table.players:
		if player.display_name == username:
			cur_player = player

	if not cur_player.status_code == 2:
		return json.dumps(cant_stay)

	cur_player.status_code = 4
	cur_player.status=player_status_codes[cur_player.status_code]
	cur_player.save()
	table.save()

	next_turn(table)


def bet(username, amount, table):
	cur_player = None
	for player in table.players:
		if player.display_name == username:
			cur_player = player
	if table.status_code != 1:
		return json.dumps(cant_bet_placed)
	if amount > cur_player.money:
		return json.dumps(cant_bet_too_little_money)
	if amount < table.min_bet and amount != cur_player.money:
		return json.dumps(cant_bet_below_minimum)
	cur_player.money -= amount
	cur_player.bet = amount

	player.status_code=3
	player.status=player_status_codes[player.status_code]
	player.save()

def double_down(username, table):
	cur_player = None
	for player in table.players:
		if player.display_name == username:
			cur_player = player

	if (not player.status_code == 2) or len(player.cards) != 2:
		return json.dumps(cant_double_down)
	if player.money < player.bet:
		return json.dumps(cant_double_down)

	cur_player.cards.append(new_card(table))
	cur_player.money -= cur_player.bet
	cur_player.bet *= 2

	if card_eval(cur_player.cards) > 21:
		cur_player.status_code = 6
		cur_player.status=player_status_codes[player.status_code]
	else:
		cur_player.status_code = 7
		cur_player.status=player_status_codes[player.status_code]

	cur_player.save()
	table.save()

	next_turn(table)

def next_turn(table):
	if(len(table.players) == 1):
		end_round()
		return

	anyone_playing = False
	for player in table.players:
		if player.status_code == 3:
			anyone_playing = True

	if not anyone_playing:
		end_round(table)
		return

	for i in range(table.turn_index, len(table.players)):
		if table.players[i].status_code == 3:
			player = table.players[i]
			table.turn_index = i
			table.turn_name = player.display_name
			player.status_code = 2
			player.status=player_status_codes[player.status_code]
			player.save()
			table.save()
			return

	dealer_turn(table)

	for i in range(0, table.turn_index):
		if table.players[i].status_code == 3:
			player = table.players[i]
			table.turn_index = i
			table.turn_name = player.display_name
			player.status_code = 2
			player.status=player_status_codes[player.status_code]
			player.save()
			table.save()
			return

#def dealer_turn(table):

def new_card(table):
	card = card_vals[randint(0,len(card_vals)-1)] + card_suits[randint(0,len(card_suits)-1)]
	while table.drawn_cards.count(card) < 3:
		card = card_vals[randint(0,len(card_vals)-1)] + card_suits[randint(0,len(card_suits)-1)]
	table.drawn_cards.append(card)
	table.save()
	return card

def end_round(table):
	dealer = table.dealer
	dealer.flipped = False
	table.status_code=3
	table.table_status=table_status_code[table.status_code]

	while card_eval(dealer.cards) < 17:
		dealer.cards.append(new_card(table))

	dealer.save()

	dealerVal = card_eval(dealer.cards)

	for player in table.players:
		if player.status_code == 6:
			player.bet = 0
		else:
			playerVal = card_eval(dealer.cards)
			hasNatural = (playerVal == 21 and len(player.cards) == 2)

			if dealerVal > 21 or dealerVal < playerVal:
				if hasNatural:
					player.money += int(2.5*player.bet)
				else:
					player.money += 2*player.bet

			elif dealerVal == playerVal:
				player.money += player.bet

		player.bet = 0
		player.save()

	if table.curStart == len(table.players)-1:
		table.curStart = 0
	else:
		table.curStart += 1
	table.save()
	start_new_round(table) #TODO

def start_new_round(table):
	players = table.players

	if len(table.drawn_cards) <= 45:
		table.drawn_cards = []

	playersLeft = []

	for player in players:
		if player.money <= 0:
			player.status_code = 5
			player.status = player_status_codes[player.status]
			player.save()
		else:
			player.cards = []
			player.doubled_down = False
			player.status_code = 1
			player.status = player_status_codes[player.status]
			player.save()
			playersLeft.append(player)

	if len(playersLeft) == 1:
		playersLeft[0].status_code = 8
		playersLeft[0].status = player_status_codes[playersLeft[0].status_code]
		table.status_code = 4
		table.table_status = table_status_code[table.status_code]
		return

	table.min_bet += 5

	#deal_cards(table)
	check_bets_and_continue(table)

def card_eval(card_list):
	tot_val = 0
	num_ace = 0
	for card in card_list:
		if card[0] == 'A':
			num_ace += 1
			tot_val += 11
		elif len(card) == 2 and ord(card[0]) <= ord('9'):
			tot_val += ord(card[0])-ord('0')
		else:
			tot_val += 10
	if num_ace > 0 and tot_val > 21:
		tot_val -= 10
	return tot_val

def serialize_table(table):
	cur_table = table
	cur_table_dict = {}
	cur_table_dict['name'] = cur_table.table_name
	cur_table_dict['status'] = cur_table.table_status
	cur_table_dict['current_starting_player'] = cur_table.curStart
	cur_table_dict['turn'] = cur_table.turn_index
	player_list = []
	for player in cur_table.players:
		player_list.append(jsonHelper.jsonify(player))
	cur_table_dict['players'] = player_list

	if 'dealer' in cur_table_dict:
		cur_table_dict['dealer'] = jsonHelper.jsonify(cur_table.dealer)
		if cur_table.dealer.flipped:
			cur_table_dict['dealer'][cards][0] = 'secret'
	return json.dumps(cur_table_dict)

	#Sample Output
	# {"status": "not_started", "turn": 0, "players": [{"status": "stayed", "money": 400, "cards": ["AH", "2S"], "display_name": "Usmann2", "bet": 100}, {"status": "stayed", "money": 900, "cards": ["AH", "2S"], "display_name": "Usmann1", "bet": 100}], "name": "scrubTable", "current_starting_player": 0}