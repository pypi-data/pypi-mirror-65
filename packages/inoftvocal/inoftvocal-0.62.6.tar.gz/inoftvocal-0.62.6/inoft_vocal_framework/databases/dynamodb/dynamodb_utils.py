import json

def dynamodb_to_python(dynamodb_item_value_or_dict_or_list):
    from decimal import Decimal
    if isinstance(dynamodb_item_value_or_dict_or_list, Decimal):
        if dynamodb_item_value_or_dict_or_list % 1 > 0:
            return float(dynamodb_item_value_or_dict_or_list)
        else:
            return int(dynamodb_item_value_or_dict_or_list)

    elif isinstance(dynamodb_item_value_or_dict_or_list, list):
        for i, item in enumerate(dynamodb_item_value_or_dict_or_list):
            dynamodb_item_value_or_dict_or_list[i] = dynamodb_to_python(item)
        return dynamodb_item_value_or_dict_or_list

    elif isinstance(dynamodb_item_value_or_dict_or_list, dict):
        for item_key, item_value in dynamodb_item_value_or_dict_or_list.items():
            dynamodb_item_value_or_dict_or_list[item_key] = dynamodb_to_python(item_value)
        return dynamodb_item_value_or_dict_or_list

    else:
        return dynamodb_item_value_or_dict_or_list

def dict_to_dynamodb(item_object: dict):
    from decimal import Decimal
    if (isinstance(item_object, int) or isinstance(item_object, float)) and not isinstance(item_object, bool):
        # Before turning the object to a decimal, we need to check that it is not of bool instance, because
        # an int is not necessarily of bool instance, where a bool is both of type bool and int (seriously).
        # And we need to insert the bool to DynamoDB, not its equivalent in int and Decimal.
        return Decimal(item_object)

    elif isinstance(item_object, str) and item_object.replace("'", "").replace("\"", "") == "":
        return None

    elif isinstance(item_object, list):
        items_to_remove = list()
        for i, item in enumerate(item_object):
            nested_item = dict_to_dynamodb(item)
            if nested_item is not None:
                item_object[i] = nested_item
            else:
                items_to_remove.append(nested_item)

        for item_to_remove in items_to_remove:
            item_object.remove(item_to_remove)
        return item_object

    elif isinstance(item_object, dict):
        keys_to_pop = list()
        for item_key, item_value in item_object.items():
            nested_item = dict_to_dynamodb(item_value)
            if nested_item is not None:
                item_object[item_key] = nested_item
            else:
                keys_to_pop.append(item_key)

        for key_to_pop in keys_to_pop:
            item_object.pop(key_to_pop)
        return item_object

    else:
        return item_object

import boto3
dynamodb = boto3.resource("dynamodb", region_name="eu-west-3")
table = dynamodb.Table("skill_hello-world_users-data")
item = dict_to_dynamodb({'id': '5dde17b6-3c1a-4458-a702-3a94a5a6e164', 'lastSessionId': 'projects/cite-des-sciences/agent/sessions/ABwppHFhDnYQIioEG0qH6fXI74MBvSa3acZZK1wf5hqRps6wBHmjVhEufTZqV3287gpr_LpLc5HBSz7x1hSBMhM', 'lastInteractionTime': 1585866296, 'smartSessionAttributes': {'lastIntentHandler': 'LaunchRequestHandler'}, 'persistentAttributes': {'alphaBravoCharlieInfos': {'hasEaredExplanationsAtLeastOnce': False}}})
table.put_item(Item=item)
