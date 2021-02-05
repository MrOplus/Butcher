from typing import Optional

from dnslib import QTYPE, CLASS, DNSRecord, DNSQuestion, A, NS, RR, SOA, DNSLabel, AAAA, TXT, CNAME


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

    def get_a_answer(self, answers):
        reply = self.record.reply()
        if type(answers) is list:
            for x in answers:
                reply.add_answer(RR(rname=self.get_question().get_qname(), rtype=QTYPE.A, ttl=x['ttl'], rdata=A(x['value'])))
        elif type(answers) is dict:
            reply.add_answer(RR(rname=self.get_question().get_qname(), rtype=QTYPE.A, ttl=answers['ttl'], rdata=A(answers['value'])))
        return reply

    def get_aaaa_answer(self, answers):
        reply = self.record.reply()
        if type(answers) is list:
            for x in answers:
                reply.add_answer(RR(rname=self.get_question().get_qname(), rtype=QTYPE.AAAA, ttl=x['ttl'], rdata=AAAA(x['value'])))
        elif type(answers) is dict:
            reply.add_answer(
                RR(rname=self.get_question().get_qname(), rtype=QTYPE.AAAA, ttl=answers['ttl'], rdata=AAAA(answers['value'])))
        return reply

    def get_txt_answer(self, answers):
        reply = self.record.reply()
        if type(answers) is list:
            for x in answers:
                reply.add_answer(
                    RR(rname=self.get_question().get_qname(), rtype=QTYPE.TXT, ttl=x['ttl'], rdata=TXT(x['value'])))
        elif type(answers) is dict:
            reply.add_answer(
                RR(rname=self.get_question().get_qname(), rtype=QTYPE.TXT, ttl=answers['ttl'], rdata=TXT(answers['value'])))
        return reply

    def get_soa_answer(self, ttl: int, domain: str, email: str, times: tuple):
        reply = self.record.reply()
        reply.add_answer(
            RR(rname=self.get_question().get_qname(), rtype=QTYPE.SOA, ttl=ttl, rdata=SOA(domain, email, times)))
        return reply

    def get_ns_answer(self, answers):
        reply = self.record.reply()
        if type(answers) is list:
            for x in answers:
                reply.add_answer(
                    RR(rname=self.get_question().get_qname(), rtype=QTYPE.NS, ttl=x['ttl'], rdata=NS(x['value'])))
        elif type(answers) is dict:
            reply.add_answer(
                RR(rname=self.get_question().get_qname(), rtype=QTYPE.NS, ttl=answers['ttl'], rdata=NS(answers['value'])))
        return reply

    def get_rtype(self):
        return DNSParser.QTYPE[self.get_question().qtype]

    def null_response(self):
        reply = self.record.reply()
        return reply.pack()

    def get_cname_answer(self, answers):
        reply = self.record.reply()
        if type(answers) is list:
            for x in answers:
                reply.add_answer(
                    RR(rname=self.get_question().get_qname(), rtype=QTYPE.CNAME, ttl=x['ttl'], rdata=CNAME(x['value'])))
        elif type(answers) is dict:
            reply.add_answer(
                RR(rname=self.get_question().get_qname(), rtype=QTYPE.CNAME, ttl=answers['ttl'], rdata=CNAME(answers['value'])))
        return reply
