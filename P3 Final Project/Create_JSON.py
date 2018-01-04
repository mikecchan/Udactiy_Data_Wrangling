#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from collections import defaultdict

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

MAPPING = { "St": "Street",
            "St.": "Street",
            "Rd": "Road",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Trl": "Trail",
            "Trl.": "Trail",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Ct": "Court",
            "Ct.": "Court",
            "Ln": "Lane",
            "Ln.": "Lane",
            }
STREET = ["Street", "Road", "Avenue", "Drive", "Trail", "Boulevard", "Court", "Lane", "Highway", 
"Circle", "Way", "RailRoad", "Freeway", "Railway", "Parkway", "River", "Expressway", "Creek", "Railroad"]
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
ADDRESS = ["name", "highway", "county", "zip_left", "name_base", "reviewed", "building", "leisure"]
POSITION = ["lan", "lat"]

def shape_element(element):
    node = {}
    subnode = {}
    address_node = {}
    pos = []
    nd_list = []
    if element.tag == "way" or element.tag == "relation" or element.tag == "node":
        
        node["type"] = element.tag
        
        node["id"] = element.attrib["id"]
        
        for at in element.attrib:
            if at in CREATED:
                created = element.attrib[at]
                if at == "user":
                     created = split_user(created)
                subnode[at] = created
                node["created"] = subnode
            
        if element.tag == "node":
            pos.append(float(element.attrib["lat"]))
            pos.append(float(element.attrib["lon"]))
            node["pos"] = pos
            
        if element.tag == "way":
            
            for ref in element.iter("nd"):
                new_nd = ref.attrib["ref"]
                nd_list.append(new_nd)
            node["node_refs"] = nd_list
            
            for tag in element.iter("tag"):
                eval_k = tag.attrib['k']
                eval_v = tag.attrib['v']
                if "tiger:" in eval_k:
                      eval_k = eval_k.split("tiger:")[1:]
                      eval_k = eval_k[0]
                elif "addr:" in eval_k:
                      eval_k = eval_k.split("addr:")[1:]
                      eval_k = eval_k[0]
                if eval_k in ADDRESS:
                    for search_error in MAPPING:
                        if search_error in eval_v:
                            eval_v = re.sub(r'\b' + search_error + r'\b\.?', MAPPING[search_error], eval_v)
                    if eval_k == "zip_left":
                        eval_k = "zip"
                    if eval_k == "name":
                        is_street_name = False
                        for street_name in STREET:
                            if street_name in eval_v:
                                is_street_name = True
                        if is_street_name == False:        
                            eval_k = "businessName"
                        else:
                            eval_k = "streetName"
                    address_node[eval_k] = eval_v
                    node["address"] = address_node
        return node
    else:
        return None

def split_user(new_word):
    CHECK_NAME = {'MichaelGSmith':'Michael G Smith', 
                  'PurpleMustang':'Purple Mustang', 
                  'purpleduck':'purple duck', 
                  'dogblog':'dog blog',
                  'DougPeterson':'Doug Peterson',
                  'AaronAsAChimp':'Aaron As A Chimp',
                  'CanvecImports': 'Canvec Imports',
                  'MikeyCarter': 'Mikey Carter',
                  'AndrewSnow':'Andrew Snow',
                  'ChrisZontine':'Chris Zontine'}              
    for search_word in CHECK_NAME:
        if search_word in new_word:
            new_word = re.sub(search_word, CHECK_NAME[search_word], new_word) 
        
    if "tiger" in new_word:
        new_word = new_word.strip("tiger")
    if new_word == "Gone":
        new_word = None
    return new_word

def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "file_out_detroit3.json"
    data = []
    
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    
    
    return data

def test():
    
    data = process_map('file_in_detroit.osm', True)
    pprint.pprint(data)
    print "stopped"

if __name__ == "__main__":
    test()


