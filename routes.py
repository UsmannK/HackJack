import os
import logging
from flask import Flask, request, abort, render_template
from hackjack.models import *
import json
from hackjack.consts import *
from hackjack.GameMethods import *


app = Flask(__name__)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/viewer/<table_name>")
def viewer(table_name):

	requested_table = find_table(table_name)

	#If table doesn't exist
	if requested_table == None:
		return render_template('viewer.html', table=requested_table, table_exists=False)
	else:
		return render_template('viewer.html', table=requested_table, table_exists=True)


@app.route("/tables/<table_name>", methods=['POST', 'GET'])
def tables(table_name):

	requested_table = find_table(table_name)

	#GET routing
	if request.method == 'GET':
		if requested_table == None:
			return json.dumps(table_not_found)
		else:
			return serialize_table(requested_table)

	#POST routing
	if request.method == 'POST':
		if 'username' not in request.form or 'password' not in request.form:
			return json.dumps(provide_auth)
		if 'admin' in request.form and 'password' in request.form:
			if not authenticate(request.form['admin'], request.form['password']):
				abort(401)
		else:
			if not authenticate(request.form['username'], request.form['password']):
				abort(401)


		if not 'command' in request.form:
			return json.dumps(supply_command)
		cmd = request.form['command']

		if requested_table == None:
			if cmd == 'create':
				return create(request.form['username'], table_name)
			return json.dumps(table_not_found)

		#implicit else:
		if not is_player_turn(request.form['username'], requested_table):
			if cmd == 'join':
				join(request.form['username'], requested_table)
			if is_in_table(request.form['username'], requested_table):
				return json.dumps(wait_your_damn_turn)
			return json.dumps(join_the_game)
		#implicit else
		if cmd == 'hit':
			return hit(request.form['username'], requested_table)
		elif cmd == 'stay':
			return stay(request.form['username'], requested_table)
		elif cmd == 'bet':
			if not 'bet_amt' in request.form:
				return json.dumps(give_bet_amt)
			return bet(request.form['username'], request.form['bet_amt'], requested_table)
		elif cmd == 'start':
			return start(request.form['username'], requested_table)
		elif cmd == 'double down':
			return double_down(request.form['username'], requested_table)
		else:
			return serialize_table(requested_table)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
# def create_table(table_num)
