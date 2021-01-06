from database import Database
from dns import DNSParser, Utils
import binascii
from tld import get_tld
import yaml
import threading,queue

a = queue.Queue()

def main():
    config_file = open('config.yaml', mode='r')
    config = yaml.load(config_file , yaml.FullLoader)
    packet = binascii.unhexlify(
        "00050100000100000000000006676f6f676c6503636f6d0000060001")
    packet = DNSParser(packet)
    database = Database(config['database']['connection_string'],
                        config['database']['database_name'])
    zones =  database.get_all_zones()
    print(packet.get_question())
    query = Utils.label_to_str(packet.get_question().get_qname())
    tld = get_tld(query, fix_protocol=True, as_object=True, fail_silently=True)
    if tld is None:
        # todo handle response
        return
    fld = tld.fld
    zone = database.get_zone(fld)
    if zone is None:
        # todo handle null response
        return
    query_type = packet.get_rtype()
    if query_type == "SOA":
        if Utils.label_to_str(query) == zone['zone']:
            ns_record = Database.get_prior_record(zone, "NS")
            owner = Utils.mail_to_label(zone['owner'])
            soa_record = Database.get_records(zone, 'SOA')[0]
            times = (soa_record['times']['serial'], soa_record['times']['refresh'], soa_record['times']['retry'],
                     soa_record['times']['expire'], soa_record['times']['ttl'])
            print(packet.get_soa_answer(soa_record['ttl'], Utils.list_to_label(ns_record['name'], zone['zone']), owner,
                                        times))


if __name__ == '__main__':
    main()
