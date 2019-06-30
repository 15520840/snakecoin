from flask import Flask
from flask import request
node = Flask(__name__)


this_node_transactions = []

@node.route('/txion',methods = ['POST'])
def transaction():
        if request.method == 'POST':
                # Extract the transaction data on each new POST request
                new_txion = request.get_json()
                this_node_transactions.append(new_txion)

                print("New transaction")
                print("From: {}".format(new_txion['from']))
                print("To: {}".format(new_txion['to']))
                print("Amount: {}".format(new_txion['amount']))

                return "Transaction submission successful\n"

node.run()
