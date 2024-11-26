def resolve_domain(domain_name):
    records = {
        "example.com": "93.184.216.34",
        "google.com": "142.250.64.14",
        "localhost": "127.0.0.1",
        "microsoft.com": "40.112.72.205",
    }
    return records.get(domain_name)
