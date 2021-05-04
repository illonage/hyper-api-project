import requests
import json
import os
import re
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import boto3
import logging
from botocore.exceptions import ClientError
from pathlib import Path


from tableauhyperapi import Connection, HyperProcess, SqlType, TableDefinition, \
    escape_string_literal, escape_name, NOT_NULLABLE, Telemetry, Inserter, CreateMode, TableName
from flask import Flask, request, render_template, redirect, url_for, flash
app = Flask(__name__)
app.secret_key = os.urandom(24)

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

hyper_name = 'mealprep.hyper'

path_to_database = Path(hyper_name)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        request_data = request.get_json()
        print(request_data)
        print("The HyperProcess has started.")
        object_name="mealprep.hyper"
        file_name=os.environ.get('bucket_name')

        with Connection(hyper.endpoint, path_to_database, CreateMode.CREATE_AND_REPLACE) as connection:
            print("The connection to the Hyper file is open.")
            connection.catalog.create_schema('Extract')
            example_table = TableDefinition(TableName('Extract','Extract'), [
                TableDefinition.Column('Breakfast', SqlType.text()),
                TableDefinition.Column('Lunch', SqlType.text()),
                TableDefinition.Column('Dinner', SqlType.text()),
            ])
            print("The table is defined.")
            connection.catalog.create_table(example_table)
            with Inserter(connection, example_table) as inserter:
                for i in request_data['data']:
                    inserter.add_row(
                        [ i['breakfast'], i['lunch'], i['dinner'] ]
                    )

                inserter.execute()
                print("The data was added to the table.")
                if object_name is None:
                    object_name = file_name
                s3_client = boto3.client('s3', aws_access_key_id=os.environ.get('aws_access_key_id'), 
                            aws_secret_access_key= os.environ.get('aws_secret_access_key'))
                try:
                    response = s3_client.upload_file(str(path_to_database),file_name, object_name)
                except ClientError as e:
                    logging.error(e)
                    return False
            print("The connection to the Hyper extract file is closed.")
        print("The HyperProcess has shut down.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
