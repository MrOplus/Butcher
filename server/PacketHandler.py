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
        query_type = packet.get_rtype()
        if query_type == "SOA":
            if query == zone['zone']:
                ns_record = Database.get_primary_ns_record(zone)
                owner = Utils.mail_to_label(zone['owner'])
                soa_record = zone['SOA']
                times = (soa_record['serial'], soa_record['refresh'], soa_record['retry'],
                         soa_record['expire'], soa_record['ttl'])
                self.wfile.write(
                    packet.get_soa_answer(soa_record['ttl'], ns_record, owner, times).pack())
            else:
                self.wfile.write(packet.null_response())
        elif query_type == "NS":
            self.wfile.write(packet.get_ns_record(sorted(zone['NS'], key=lambda x: x['order']), 60).pack())
        elif query_type == "AAAA" or query_type == "A" or query_type == "TXT":
            record = Database.find_memory_record(zone, query_type, tld.subdomain)
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
            if res is None:
                self.wfile.write(packet.null_response())
            else:
                self.wfile.write(res.pack())
        else:
            # not implemented
            self.wfile.write(packet.null_response())
