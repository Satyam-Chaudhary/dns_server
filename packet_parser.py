import struct

def parse_question(data):
    transaction_id = struct.unpack("!H", data[:2])[0]

    domain_name = []
    i = 12
    while data[i] != 0:
        length = data[i]
        domain_name.append(data[i + 1:i + 1 + length].decode())
        i += length + 1
    domain_name = ".".join(domain_name)

    qtype, _ = struct.unpack("!HH", data[i + 1:i + 5])

    return transaction_id, domain_name, qtype
