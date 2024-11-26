import struct
import socket

def build_response(transaction_id, domain_name, ip):
    # Header
    flags = 0x8180  # Response with no error
    qdcount = 1
    ancount = 1
    nscount = 0
    arcount = 0

    header = struct.pack("!HHHHHH", transaction_id, flags, qdcount, ancount, nscount, arcount)

    # Question
    question = build_question(domain_name, 1, 1)  # A record, IN class

    # Answer
    name = 0xC00C  # Pointer to the domain name in the question section
    type_ = 1      # A record
    class_ = 1     # IN class
    ttl = 300      # Time to live
    rdlength = 4   # Length of IP address
    rdata = socket.inet_aton(ip)  # Convert IP to bytes

    answer = struct.pack("!HHHLH4s", name, type_, class_, ttl, rdlength, rdata)

    return header + question + answer

def build_question(domain_name, qtype, qclass):
    parts = domain_name.split(".")
    question = b"".join(bytes([len(part)]) + part.encode() for part in parts)
    question += b"\x00"  # End of domain name
    question += struct.pack("!HH", qtype, qclass)
    return question

def build_error_response(transaction_id):
    flags = 0x8183  # Response with NXDOMAIN error
    qdcount = 1
    ancount = 0
    nscount = 0
    arcount = 0

    return struct.pack("!HHHHHH", transaction_id, flags, qdcount, ancount, nscount, arcount)
