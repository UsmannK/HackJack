from hackjack import db
from hackjack.models import *
from hackjack.consts import *
import hackjack.mongo_to_dict as jsonHelper
import json
from threading import Timer

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
		if table_name == table.name:
			return True
	return False

def find_table(table_name):
	tables = Table.objects
	for table in tables:
		if table_name == table.name:
			return table
	return None

def is_player_turn(passed_uname, table):
	return passed_uname == table.players[table.turn_index].display_name

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
	table.turn_index=[0]
	table.turn_name=table_admin.display_name
	table.curStart=0
	table.min_bet=5
	table.save()
	return table

def start(username, table_name):
	table = find_table(table_name)
	players = table.players

	for player in players:
		player.status_code=1
		player.status=player_status_codes[player.status_code]

	table.status_code=1
	table.table_status = table_status_codes[table.table_status_code]

	t = Timer(10.0, check_bets_and_continue(table))
	t.start() # after 10 seconds, unplaced bets will be minimum

def join():
	pass

def hit():
	pass

def stay():
	pass

def bet():
	pass

def double_down():
	pass

def check_bets_and_continue(table):
	if table.status_code == 1:
		players = table.players

		for player in players:
			player.status_code=3
			player.status=player_status_codes[player.status_code]
			if player.bet == 0:
				player.bet = table.min_bet
				player.money -= player.bet


	

def serialize_table(table_name):
	cur_table = table_name
	cur_table_dict = {}
	cur_table_dict['name'] = cur_table.table_name
	cur_table_dict['status'] = cur_table.table_status
	cur_table_dict['current_starting_player'] = cur_table.curStart
	cur_table_dict['turn'] = cur_table.started
	player_list = []
	for player in cur_table.players:
		player_list.append(jsonHelper.jsonify(player))
	cur_table_dict['players'] = player_list
	return cur_table_dict

	#Sample Output
	# {"status": "not_started", "turn": 0, "players": [{"status": "stay", "money": 400, "cards": ["AH", "2S"], "display_name": "Usmann2", "bet": 100}, {"status": "stay", "money": 900, "cards": ["AH", "2S"], "display_name": "Usmann1", "bet": 100}], "name": "scrubTable", "current_starting_player": 0}