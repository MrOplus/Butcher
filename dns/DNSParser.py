from typing import Optional

from dnslib import QTYPE, CLASS, DNSRecord, DNSQuestion, A, NS, RR, SOA, DNSLabel


class DNSParser:
    record: DNSRecord
    QTYPE = QTYPE
    QCLASS = CLASS

    def __init__(self, packet):
        self.record = DNSRecord.parse(packet)

    def get_question(self) -> Optional[DNSQuestion]:
        if len(self.record.questions) == 1:
            return self.record.questions[0]
        return None

    def get_a_answer(self, ip: str, ttl: int):
        reply = self.record.reply()
        reply.add_answer(RR(rname=self.get_question().get_qname(), rtype=QTYPE.A, ttl=ttl, rdata=A(ip)))
        return reply

    def get_soa_answer(self, ttl: int, domain: str, email: str, times: tuple):
        reply = self.record.reply()
        reply.add_answer(
            RR(rname=self.get_question().get_qname(), rtype=QTYPE.SOA, ttl=ttl, rdata=SOA(domain, email, times)))
        return reply

    def get_ns_record(self, ns_record: tuple, ttl: int):
        reply = self.record.reply()
        for ns in ns_record:
            reply.add_answer(
                RR(rname=self.get_question().get_qname(), rtype=QTYPE.NS, ttl=ttl, rdata=NS(ns))
            )
        return reply

    def get_rtype(self):
        return DNSParser.QTYPE[self.get_question().qtype]
