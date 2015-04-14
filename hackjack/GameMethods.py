from hackjack import db
from hackjack.models import *
from hackjack.errs import *
import hackjack.mongo_to_dict as jsonHelper
import json

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

def create():
	pass

def start():
	pass

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