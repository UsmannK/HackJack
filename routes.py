import os
from flask import Flask
from hackjack.models import *

app = Flask(__name__)

@app.route("/tables/<int:table_num>", methods=['GET', 'POST'])
def tables(table_num):
	for table in Table.objects:
		if table.table_num == table_num:
			return "exists"
		else:
			return "should been created"
	if len(Table.objects) == 0:
		return "There are no tables"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)