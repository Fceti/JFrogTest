import ast
import sys

import CloudFlare
import click

TOKEN = 'wgKC7ELJaC8t6c6DkOttyQEr0bBZV5IQ1Cy8wKtd'
login = 'Zhenya'
password = 'ZhenyaLox'
def create_zone(cf, zone_name):
    print("Создаем зону")
    zone_id = ''
    zone_info = cf.zones.get()

    for item_zone_info in zone_info:
        if zone_name == item_zone_info["name"]:
            zone_id = item_zone_info["id"]
    if zone_id == '':
        try:
            zone_id = (cf.zones.post(data={'jump_start': False, 'name': zone_name})["id"])
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            sys.exit(f"При создании зоны {zone_name} возникли проблемы: " + str(e))

    return zone_id

def create_default_dns(cf, zone_id, zone_name, data):
    #cf.zones.dns_records.get(zone_id)
    print("Создаем DNS записи")
    print(data)
    for item_data in data:
        print(type(item_data))
        try:
            cf.zones.dns_records.post(zone_id, data=item_data)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
           sys.exit(f"При создании записей DNS для зоны {zone_name} прозошла ошибка: " + str(e))

#def pick_out_records(cf, ):

def create_firewallrules(cf, zone_id, data):
    print("Создаем правила фаервола")
    filters = cf.zones.filters(zone_id)
    rules = cf.zones.firewall.rules.get(zone_id)
    for item_data in data:
        if filters == []:
            try:
                filter_id = cf.zones.filters.post(zone_id, data=[{
                    "paused": False,
                    "expression": item_data["filter"]
                }])[0]["id"]
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                print(e)
        for item_filter in filters:
            if item_data["filter"] != item_filter["expression"]:
                print("Создаем фильтр " + item_data["filter"])
                try:
                    filter_id = cf.zones.filters.post(zone_id, data=[{
                                                            "paused": False,
                                                            "expression": item_data["filter"]
                                                        }])[0]["id"]
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    sys.exit(e)
            else:
                print("Фильтр " + item_data["filter"] + " уже есть!")
                filter_id = item_filter["id"]
        if rules == []:
            try:
                cf.zones.firewall.rules.post(
                    zone_id, data=[{"action": item_data["action"],
                                    "priority": item_data["priority"],
                                    "paused": item_data["paused"],
                                    "description": item_data["name"],
                                    "filter":
                                        {
                                            "id": filter_id,
                                            "paused": item_data["paused"],
                                        }}]
                )
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                sys.exit(e)
        for item_rule in rules:
            if item_data["name"] != item_rule["description"]:
                try:
                    cf.zones.firewall.rules.post(
                        zone_id, data=[{"action": item_data["action"],
                                        "priority": item_data["priority"],
                                        "paused": item_data["paused"],
                                        "description": item_data["name"],
                                        "filter":
                                            {
                                                "id": filter_id,
                                                "paused": item_data["paused"],
                                            }}]
                    )
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    sys.exit(e)

dns = [{"name": "@", "type": "A", "content": "8.13.56.100", "proxied": True}]

firewall_rules = [
        {"name": "Block DDoS UserAgent", "action": "block", "filter": "(http.user_agent contains \"Python\")",
         "priority": 1, "paused": False},
        {"name": "Allow Enterra list", "action": "allow", "filter": "(ip.src in $white_list_enterra)", "priority": 2, "paused": False},
        {"name": "Block ne MN", "action": "block", "filter": "(ip.geoip.country ne \"MN\")", "priority": 3, "paused": False}
    ]

@click.command()
@click.option(
    '--api_key', '-a',
    help='Апи токен доступа к CF(НЕ Global API Key, а индивидуально созданный)',
)
@click.option(
    '--file', '-f',
    help='Файл для парсинга значений для добавления',
)

@click.option(
    '--jenkins', '-j',
    help='Если скрипт запускается с Jenkins',
)

@click.option(
    '--test',
    help='Для тестов',
)


def main(api_key, file, jenkins, test):
    """
    Данная программа предназначена для автоматизации работы с CloudFlare
    """



    firewall_rules = [
        {"name": "Block DDoS UserAgent", "action": "block", "filter": "(http.user_agent contains \"Python\")",
         "priority": 1, "paused": False},
        {"name": "Allow Enterra list", "action": "allow", "filter": "(ip.src in $white_list_enterra)", "priority": 2,
         "paused": False},
        {"name": "Block ne MN", "action": "block", "filter": "(ip.geoip.country ne \"MN\")", "priority": 3,
         "paused": False}
    ]
    try:
        api_key
    except NameError:
        api_key = None

    try:
        file
    except NameError:
        file = None

    try:
        jenkins
    except NameError:
        jenkins = None

    try:
        test
    except NameError:
        test = None


    if not(api_key == None):
        TOKEN = api_key

    #if file != None:
     #   file_pars(file)

    if test != None:
        print(test)

    if jenkins != None:
        print(jenkins) 
        jenkins = ast.literal_eval(jenkins)
        print(jenkins)
        print(jenkins["records"], type(jenkins["records"]))
        # cf = CloudFlare.CloudFlare(token=jenkins["TOKEN"])
        # dns = []
        # dns_temp = {"name": "@", "type": "A", "proxied": True}
        # if jenkins["mongol"] == False:
        #     print("Not adding WAF rules")
        # elif jenkins["mongol"] == True:
        #     print("Adding default mongol rules")
        #     firewall_rules = [
        #         {"name": "Block DDoS UserAgent", "action": "block", "filter": "(http.user_agent contains \"Python\")",
        #          "priority": 1, "paused": False},
        #         {"name": "Allow Enterra list", "action": "allow", "filter": "(ip.src in $white_list_enterra)",
        #          "priority": 2,
        #          "paused": False},
        #         {"name": "Block ne MN", "action": "block", "filter": "(ip.geoip.country ne \"MN\")", "priority": 3,
        #          "paused": True}
        #     ]
        # for zone in jenkins["zone"]:
        #     zone_id = create_zone(cf, zone)
        #     dns_temp["content"] = jenkins["ipaddress"]
        #     dns.append(dns_temp)
        #     if zone not in jenkins["records"]:
        #         create_default_dns(cf, zone_id, jenkins["ipaddress"])

        # for dns in jenkins["records"]:
        #     create_default_dns(cf, zone_id, dns)
        #    create_firewallrules(cf, zone_id, firewall_rules)

if __name__ == "__main__":
    main()
