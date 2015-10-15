#!/usr/bin/env python3
import sys
sys.setrecursionlimit(5000)

import os
from settings import logging
from settings import JSONDIR
from defs import load_data, dump_data
import itertools
import collections



def form_nodes(treads):
    nodes = collections.OrderedDict()
    for tread in sorted(treads):
        arrow = 'left'
        for node in tread:
            if ' ' in node:
                switch, port = node.split()
                if not switch in nodes:
                    nodes[switch] = {'left':[], 'right':[]}
                if not port in nodes[switch][arrow]:
                    nodes[switch][arrow].append(port)
                arrow = 'right' if arrow == 'left' else 'left'
    return nodes


def form_links(treads, linksD):
    unics = []
    links = []
    for tread in treads:
        for n in range(len(tread)-1):
            node1 = tread[n]
            node2 = tread[n+1]
            if ' ' in node1 and ' ' in node2:
                link = [node1, node2]
                if not link in unics:
                    s1,p1 = node1.split()
                    s2,p2 = node2.split()
                    link = linksD.get('%s %s %s %s' %(s1, p1, s2, p2))
                    record = {
                        'node1': node1.replace(' ', '_'),
                        'node2': node2.replace(' ', '_'),
                        'Speed': link['Speed'],
                        'TrunkId': link['TrunkId'],
                        'Master': link['Master'],
                        'E_Trunk': link['E_Trunk'],
                        'F_Trunk': link['F_Trunk'],
                        'F_Link': link['F_Link'],
                    }
                    unics.append(link)
                    links.append(record)
    return links



sw_treads = collections.OrderedDict()

def walk_graph(graph, treads, n2):
    if type(treads) == str:
        treads = [[treads]]
    finded = []
    new_treads = []
    for tread in treads:
        rel_nodes = graph.get(tread[-1], [])
        rel_nodes = set(rel_nodes) - set(tread)
        for node in rel_nodes:
            new_tread = tread+[node]
            if node == n2:
                if not new_tread in finded:
                    finded.append(new_tread)

                    sws = '%s %s' %(new_tread[1], new_tread[-2])
                    sws_tread = new_tread[1:-1]
                    if not sws in sw_treads:
                        sw_treads[sws] = []
                    if not sws_tread in sw_treads[sws]:
                        sw_treads[sws].append(sws_tread)
            else:
                new_treads.append(new_tread)
    if finded:
        return finded
    else:
        if new_treads:
            return walk_graph(graph, new_treads, n2)
        else:
            pass


def main():

    filepath = os.path.join(JSONDIR, 'graph')
    graph = load_data(filepath, {})

    filepath = os.path.join(JSONDIR, 'link')
    links = load_data(filepath, {})

    filepath = os.path.join(JSONDIR, 'rels')
    swports_rels = load_data(filepath, {})

    linksD = {'%s %s %s %s' %(r['Switch1'], r['Port1'], r['Switch2'], r['Port2']): r for r in links }

    records = []

    for swport1, swports in swports_rels.items():
        for swport2 in swports:

            sw1 = swport1.split()[0]
            sw2 = swport2.split()[0]
            sws = '%s %s' %(sw1, sw2)
            if not sws in sw_treads:
                treads = walk_graph(graph, swport1, swport2)
            else:
                treads = [[swport1] + tread + [swport2] for tread in sw_treads[sws]] 
            nodes = form_nodes(treads)
            links = form_links(treads, linksD)
          
            nodes = list(nodes.items())

            records.append({'Node1':swport1, 'Node2':swport2, 'Treads':treads, 'Nodes': nodes, 'Links': links})

    filepath = os.path.join(JSONDIR, 'path')
    dump_data(filepath, records)
    logging.info('%s | %s records' %('path', len(records)))

    return


if __name__ == '__main__':
    main()
