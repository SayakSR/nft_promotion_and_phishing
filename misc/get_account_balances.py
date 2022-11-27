# Given the ETH addresses, query the database to get the balances

import os
import sys
import sqlalchemy
import multiprocessing

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
    connection = engine.connect()
    return connection

# Read ETH addresses (newline-separated) from file
def read_addresses(eth_addr_file):
    with open(eth_addr_file, 'r') as f:
        eth_addresses = f.readlines()
        eth_addresses = [x.strip() for x in eth_addresses]
        return eth_addresses

# Query the database to get the balance
def get_balance(eth_address):
    print(eth_address)
    query = f"SELECT \
                COALESCE(ROUND(SUM(value) / 1000000000000000000, 3), 0) AS eth, \
                COUNT(*) AS tx \
            FROM transactions \
            WHERE receiver = '{eth_address}'"
    result = connection.execute(query).first()
    return eth_address, result[0], result[1]

# Query the database to get the balances
def get_balances(eth_addresses, is_mp=False):
    if is_mp:
        with multiprocessing.Pool(32) as pool:
            balances = pool.map(get_balance, eth_addresses)
            return balances
    else:
        balances = []
        for eth_address in eth_addresses:
            balances.append(get_balance(eth_address))
        return balances

# Write the balances to file
def write_balances(balances, output_file):
    with open(output_file, 'w') as f:
        f.write('eth_address,eth_balance,tx_count\n')
        for balance in balances:
            f.write(f'{balance[0]},{balance[1]},{balance[2]}\n')

# arg1: path to file containing newline-separated ETH addresses
# arg2: path to file to write balances to
if __name__ == '__main__':
    # Check number of arguments
    if len(sys.argv) != 3:
        print('Usage: python3 get_account_balances.py <eth_addr_file> <output_file>')
        exit(1)
    
    eth_addr_file = sys.argv[1]
    output_file = sys.argv[2]

    eth_addresses = read_addresses(eth_addr_file)
    connection = connect_db()

    # Query database to get balances
    balances = get_balances(eth_addresses)

    # Write balances to file
    write_balances(balances, output_file)
