import requests
import json
import os
import re
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import boto3
import logging
from botocore.exceptions import ClientError



from tableauhyperapi import Connection, HyperProcess, SqlType, TableDefinition, \
    escape_string_literal, escape_name, NOT_NULLABLE, Telemetry, Inserter, CreateMode, TableName
from flask import Flask, request, render_template, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = os.urandom(24)

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    

    with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        print("The HyperProcess has started.")
        object_name=None
        file_name='TrivialExample.hyper'

        with Connection(hyper.endpoint, 'TrivialExample.hyper', CreateMode.CREATE_AND_REPLACE) as connection:
            print("The connection to the Hyper file is open.")
            connection.catalog.create_schema('Extract')
            example_table = TableDefinition(TableName('Extract','Extract'), [
                TableDefinition.Column('rowID', SqlType.big_int()),
                TableDefinition.Column('value', SqlType.big_int()),
            ])
            print("The table is defined.")
            connection.catalog.create_table(example_table)
            with Inserter(connection, example_table) as inserter:
                for i in range (1, 101):
                    inserter.add_row(
                        [ i, i ]
                )
                inserter.execute()
                print("The data was added to the table.")
                if object_name is None:
                    object_name = file_name
                s3_client = boto3.client('s3', aws_access_key_id=os.environ.get('aws_access_key_id'), 
                            aws_secret_access_key= os.environ.get('aws_secret_access_key'))
                try:
                    response = s3_client.upload_file('TrivialExample.hyper','hyperapi',object_name)
                except ClientError as e:
                    logging.error(e)
                    return False
            print("The connection to the Hyper extract file is closed.")
        print("The HyperProcess has shut down.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
