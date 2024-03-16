import azure.cosmos.cosmos_client as cosmos_client
import azure.functions as func
import os
import json

#load config
with open('config.json', 'r') as f:
    config = json.load(f)

def main(req: func.HttpRequest) -> func.HttpResponse:
    endpoint = config["CosmosDBEndpoint"]
    key = config["CosmosDBKey"]
    database_name = config["database_name"]
    container_name = config["container_name"]
    
    client = cosmos_client.CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    item = container.read_item(item='visitor_count', partition_key='visitor_count')
    current_count = item.get('count', 0)

    #increment the visitor count
    updated_count = current_count + 1
    container.upsert_item({'id': 'visitor_count', 'count': updated_count})

    return func.HttpResponse(f"Visitor count: {updated_count}", status_code=200)
