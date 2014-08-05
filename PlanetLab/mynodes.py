#!/usr/bin/env python

def read_nodes(node_file, offset):
    nodes = list()
    for line in open(node_file, 'rb'):
        line = line.strip('\r\n ')
        if line != '' and not line[0] == '#':
            node_name = line.split(',')[offset]
            nodes.append(node_name)
    return nodes

if __name__ == '__main__':
    nodes = read_nodes('deploy_nodes.txt', 0)
    open('mynodes', 'wb').write('\n'.join(nodes))
