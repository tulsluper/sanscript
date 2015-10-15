#!/usr/bin/env python3

import os
from settings import JSONDIR
from settings import logging
from defs import load_data, dump_data
from collections import OrderedDict


def f_graph(links, ports):

    def add_new_rel(graph, switch, port):
        if not switch in graph:
            graph[switch] = []
        if not port in graph[switch]:
            graph[switch].append(port)
        if not port in graph:
            graph[port] = []
        if not switch in graph[port]:
            graph[port].append(switch)
        return graph

    graph = OrderedDict()
    for record in links:
        if record['Reverse'] == False:

            switch1, index1 = record['Switch1'], record['Port1']
            switch2, index2 = record['Switch2'], record['Port2']
            
            if switch1 and switch2:

                port1 = ' '.join([switch1, str(index1)])
                graph = add_new_rel(graph, switch1, port1)

                port2 = ' '.join([switch2, str(index2)])
                graph = add_new_rel(graph, switch2, port2)

                graph[port1].append(port2)
                graph[port2].append(port1)

    for record in ports:
        port = ' '.join([record['Switch'], str(record['Index'])])
        graph = add_new_rel(graph, record['Switch'], port)

    return graph
 

def main():

    filepath = os.path.join(JSONDIR, 'link')
    links = load_data(filepath)
    filepath = os.path.join(JSONDIR, 'port')
    ports = load_data(filepath)

    data = f_graph(links, ports)
    filepath = os.path.join(JSONDIR, 'graph')
    dump_data(filepath, data)
    logging.info('%s | %s records' %('graph', len(data)))

    return


if __name__ == '__main__':
    main()
