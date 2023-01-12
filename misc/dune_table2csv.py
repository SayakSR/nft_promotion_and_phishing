import sys

def dune_table2csv(dune_table_file, output_file):
    with open(dune_table_file, 'r') as f:
        lines = f.readlines()
    with open(output_file, 'w') as f:
        i = 0
        n = len(lines)

        while i < n:
            f.write(f'{lines[i].strip()},{lines[i + 1].strip()},{lines[i + 2].strip()}\n')
            i += 3


if __name__ == '__main__':
    dune_table_file = sys.argv[1]
    output_file = sys.argv[2]
    dune_table2csv(dune_table_file, output_file)