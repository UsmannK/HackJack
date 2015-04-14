import os
import logging
from flask import Flask, request, abort
from hackjack.models import *
import json
from hackjack.consts import *
from hackjack.GameMethods import *


app = Flask(__name__)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)


@app.route("/tables/<table_name>", methods=['POST', 'GET'])
def tables(table_name):
	# if not authenticate(request.form['username'], request.form['password']):
	# 	abort(401)

	requested_table = find_table(table_name)

	#GET routing
	if request.method == 'GET':
		if requested_table is None:
			return json.dumps(table_not_found)
		else:
			return serialize_table(table_name)

	#POST routing
	if request.method == 'POST':
		cmd = request.form['command']

		if requested_table is None:
			if cmd is 'create':
				return create(request.form['username'], table_name)
			return json.dumps(table_not_found)

		#implicit else:
		if not is_player_turn(request.form['username'], requested_table):
			if cmd is 'join':
				join(request.form['username'], requested_table) #TODO: FIXIT: Make table states: not_started, betting, between_rounds
			if is_in_table(request.form['username'], requested_table):
				return json.dumps(wait_your_damn_turn)
			return json.dumps(join_the_game)

		#implicit else
		if cmd == 'hit':
			return hit(request.form['username'], requested_table)
		elif cmd == 'stay':
			return stay(request.form['username'], requested_table)
		elif cmd == 'bet':
			return bet(request.form['username'], request.form['bet_amt'], requested_table)
		elif cmd == 'start':
			return start(request.form['username'], requested_table)
		elif cmd == 'double down':
			return double_down(request.form['username'], requested_table)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
# def create_table(table_num)