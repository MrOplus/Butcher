import socketserver
import time
from config import RuntimeConfig
from dns import DNSParser, Utils
import binascii
from tld import get_tld
from database import Database
from logger import Logger


class PacketHandler(socketserver.DatagramRequestHandler):
    def handle(self) -> None:
        packet = self.rfile.read(512)
        Logger.log.debug("Accepting from {}".format(self.client_address[0]))
        packet = DNSParser(packet)
        if packet is None:
            return
        query = Utils.label_to_str(packet.get_question().get_qname())
        tld = get_tld(query, fix_protocol=True, as_object=True, fail_silently=True)
        if tld is None:
            self.wfile.write(packet.null_response())
            return
        fld = tld.fld
        zone = Database.get_memory_zone(fld)
        if zone is None:
            self.wfile.write(packet.null_response())
            return
        Logger.log.debug("Requested label : {}".format(packet.get_question().get_qname()))
        query_type = packet.get_rtype()
        if query_type == "SOA":
            if query == zone['name']:  # SOA only for root , who cares
                ns_record = Database.find_memory_record(zone, 'NS', '')
                if ns_record is None:
                    self.wfile.write(packet.null_response())
                    return
                owner = Utils.mail_to_label(zone['owner'])
                times = (zone['id'], 7200, 3600,
                         1209600, 60)
                if len(ns_record) > 0:
                    ns = ns_record[0]['value']
                else:
                    ns = ns_record['value']
                self.wfile.write(
                    packet.get_soa_answer(60, ns, owner, times).pack())
            else:
                self.wfile.write(packet.null_response())
        elif query_type == "AAAA" or query_type == "A" or query_type == "TXT" or query_type == "NS" or query_type == "CNAME":
            subdomain = '@' if tld.subdomain == '' else tld.subdomain
            record = Database.find_memory_record(zone, query_type, subdomain)
            if record is None:
                self.wfile.write(packet.null_response())
                return
            res = None
            if query_type == "A":
                res = packet.get_a_answer(record)
            elif query_type == "AAAA":
                res = packet.get_aaaa_answer(record)
            elif query_type == "TXT":
                res = packet.get_txt_answer(record)
            elif query_type == "NS" :
                res = packet.get_ns_answer(record)
            elif query_type == "CNAME":
                res = packet.get_cname_answer(record)
            if res is None:
                self.wfile.write(packet.null_response())
            else:
                self.wfile.write(res.pack())
        else:
            # not implemented
            self.wfile.write(packet.null_response())
