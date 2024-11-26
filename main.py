import socket
from resolver import resolve_domain
from packet_parser import parse_question
from packet_builder import build_response, build_error_response
import logging


logging.basicConfig(
    filename="logs/dns_logs.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

def start_dns_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
    server_socket.bind(("0.0.0.0", 53))
    print("DNS server started on port 53...")
    logging.info("DNS server started on port 53...")

    while True:
        try:
            print("Waiting for query...")
            data, addr = server_socket.recvfrom(512)  # Max UDP packet size
            print(f"Received query from {addr}")
            logging.info(f"Received query from {addr}")

            transaction_id, domain_name, qtype = parse_question(data)

            print(f"Transaction ID: {transaction_id}")
            print(f"Domain Name: {domain_name}, Query Type: {qtype}")
            logging.info(f"Transaction ID: {transaction_id}")
            logging.info(f"Domain Name: {domain_name}, Query Type: {qtype}")

            ip = resolve_domain(domain_name)

            if ip:
                print(f"Resolved {domain_name} to {ip}")
                logging.info(f"Resolved {domain_name} to {ip}")
                response = build_response(transaction_id, domain_name, ip)
            else:
                print(f"Domain {domain_name} not found!")
                logging.warning(f"Domain {domain_name} not found!")
                response = build_error_response(transaction_id)

            server_socket.sendto(response, addr)
            print("Response sent.")
            logging.info("Response sent.")
        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error: {e}")

if __name__ == "__main__":
    try:
        start_dns_server()
    except KeyboardInterrupt:
        print("DNS server stopped.")
        logging.info("DNS server stopped.")
