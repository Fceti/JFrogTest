import argparse
from CF import CloudFlareHelper


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--token', '-t', help='Token')


if __name__ == '__main__':
    args = arg_parser.parse_args()

    cf = CloudFlareHelper(token=args.token)

    account_id = cf.get_account_id()
    if not account_id:
        raise RuntimeError("Can\'t get account ID")

    with open("filename.txt", "r") as file:
        for zone in file:
            zone_id = cf.get_zone_id_by_name(account_id, zone.strip())
            print(zone_id)
            r = cf.cf.zones.bot_management.put(zone_id, data={"fight_mode": True})
            print(r)


