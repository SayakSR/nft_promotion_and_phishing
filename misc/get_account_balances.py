# Given the ETH addresses, query the database to get the balances

import os
import argparse
import sqlalchemy
import multiprocessing

def execute(f, args, is_mp=False):
    if is_mp:
        with multiprocessing.Pool(32) as pool:
            results = pool.starmap(f, args)
            return results
    else:
        results = []
        for arg in args:
            results.append(f(*arg))
        return results

# Parse ~/.pgpass file to extract username, password, host and port
def parse_pgpass():
    with open(os.path.expanduser('~/.pgpass'), 'r') as f:
        line = f.readline()
        line = list(map(lambda x: x.strip(), line.split(':')))
        return line[3], line[4], line[0], line[1]

# Connect to postgres database
def connect_db():
    username, password, host, port = parse_pgpass()
    engine = sqlalchemy.create_engine(f'postgresql://{username}:{password}@{host}:{port}/mainnet', pool_size=32)
    return engine
    # connection = engine.connect()
    # return connection

# Read ETH addresses (newline-separated) from file
def read_addresses(eth_addr_file):
    with open(eth_addr_file, 'r') as f:
        eth_addresses = f.readlines()
        eth_addresses = [x.strip() for x in eth_addresses]
        return eth_addresses

# Read ETH addresses (newline-separated) from file
# Header: user_name, Twitter status, Market URL, Contract address
def read_addresses2(eth_addr_file):
    with open(eth_addr_file, 'r') as f:
        eth_addresses = f.readlines()
        eth_addresses = [x.split(',')[3].strip() for x in eth_addresses]

        # Filter out non-etherscan.io addresses
        eth_addresses = list(filter(lambda x: 'etherscan.io' in x, eth_addresses))

        # Extract ETH addresses from ethercan.io links
        eth_addresses = list(map(lambda x: os.path.split(x)[-1], eth_addresses))

        return eth_addresses

# Write the balances to file
def write_balances(balances, output_file):
    with open(output_file, 'w') as f:
        f.write('eth_address,total_eth_amount,tx_count\n')
        for balance in balances:
            f.write(f'{balance[0]},{balance[1]},{balance[2]}\n')

# Query the database to get the total amount of ETH sent
# through external transactions to a specific contract address
def get_eth_sent_thru_ext_tx(eth_address):
    print(eth_address)
    query = f"SELECT \
                COALESCE(ROUND(SUM(value) / 1000000000000000000, 3), 0) AS eth, \
                COUNT(*) AS tx \
            FROM transactions \
            WHERE receiver = '{eth_address}'"
    result = engine.execute(query).first()
    return eth_address, result[0], result[1]    # eth_address, total_eth_amount, tx_count

# Compute total sales of the phishing contracts, considers only external transactions
def get_total_phishing_sales(contract_addresses_file, output_file):
    contract_addresses = read_addresses(contract_addresses_file)
    args = list(map(lambda x: (x,), contract_addresses))

    # Query database to get total ETH sent to these contract addresses
    # only through external transactions. Internal transactions are not
    # considered as phishing tokens are assumed to not have legitimate
    # sales through marketplace contracts. Typically, they receive ETHs
    # directly from the users by tricking them sign mint transactions.
    balances = execute(get_eth_sent_thru_ext_tx, args, is_mp=True)

    # Write balances to file
    write_balances(balances, output_file)

# Query the database to get the total amount of ETH sent through both
# internal and external transactions to a specific contract address
#
# Dune Analytics (dune.com) query:
#
# SELECT 
#     ROUND(SUM(ethereum.transactions.value) / 1000000000000000000, 3) AS eth,
#     COUNT(*) AS tx
# FROM ethereum.traces
# INNER JOIN ethereum.transactions
# ON ethereum.transactions.hash = ethereum.traces.tx_hash
# WHERE ethereum.traces.to = '\xbCe3781ae7Ca1a5e050Bd9C4c77369867eBc307e';
# -- AND ethereum.traces.trace_address = '{}';
# -- Checking for empty INTEGER ARRAY to identify associated external transaction
#
# Merged query to compute ETH sent to multiple contract addresess
#
# SELECT
#    ethereum.traces.to,
#    ROUND(SUM(ethereum.transactions.value) / 1000000000000000000, 3) AS eth,
#    COUNT(*) AS tx
# FROM ethereum.traces
# INNER JOIN ethereum.transactions ON ethereum.transactions.hash = ethereum.traces.tx_hash
# WHERE ethereum.traces.to IN (...)
# GROUP BY ethereum.traces.to;
def get_eth_sent_thru_int_tx(eth_address):
    print(eth_address)
    query = f"SELECT \
                COALESCE(ROUND(SUM(transactions.value) / 1000000000000000000, 3), 0) AS eth, \
                COUNT(*) AS tx \
            FROM traces \
            INNER JOIN transactions \
            ON transactions.transaction_hash = traces.transaction_hash \
            WHERE traces.receiver = '{eth_address}'"
    result = engine.execute(query).first()
    return eth_address, result[0], result[1]    # eth_address, total_eth_amount, tx_count

# Compute total sales of the contracts, considers both internal and external transactions
def get_total_sales(contract_addresses_file, output_file):
    contract_addresses = read_addresses2(contract_addresses_file)
    args = list(map(lambda x: (x,), contract_addresses))

    # Query database to get total ETH sent to these contract addresses
    # through both internal and external transactions.
    balances = execute(get_eth_sent_thru_int_tx, args, is_mp=True)

    # Write balances to file
    write_balances(balances, output_file)

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='Get account balances')
    # Add subparsers
    subparsers = parser.add_subparsers(dest='cmd')
    # Add subparser for total phishing sales
    total_phishing_sales_parser = subparsers.add_parser('total-phishing-sales')
    total_phishing_sales_parser.add_argument('--contract-addresses', type=str, help='File containing newline-separated ETH addresses of phishing contracts')
    total_phishing_sales_parser.add_argument('--output', type=str, help='File to write balances to')
    # Add subparser for total sales
    total_sales_parser = subparsers.add_parser('total-sales')
    total_sales_parser.add_argument('--contract-addresses', type=str, help='File containing newline-separated ETH addresses of contracts')
    total_sales_parser.add_argument('--output', type=str, help='File to write balances to')
    # Parse arguments
    args = parser.parse_args()

    # Connect to database
    # connection = connect_db()
    engine = connect_db()
    
    # Dispatch to appropriate handler
    if args.cmd == 'total-phishing-sales':
        get_total_phishing_sales(args.contract_addresses, args.output)
    elif args.cmd == 'total-sales':
        get_total_sales(args.contract_addresses, args.output)
    else:
        print('Unknown command')
