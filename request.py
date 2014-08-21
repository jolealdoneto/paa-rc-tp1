import httplib
import json
import sys
from pymongo import MongoClient
import time

client = MongoClient()
db = client.vk_crawl
nodes = db.nodes
edges = db.edges

MAX_N_FRIENDS = int(sys.argv[2]) if len(sys.argv) > 2 else 10

def vk_request(method, argstr):
    conn = httplib.HTTPSConnection("api.vk.com")
    conn.request("GET", "/method/%s?access_token=64fd7e36eb3a1a8c77ef94542176829eb51627dd28e738dcefbf3e17fc2a6300ec9fb1ee9826dfb3e2da2%s" % (method, argstr))
    r1 = conn.getresponse()
    print r1.status, r1.reason
    data1 = r1.read()
    return json.loads(data1)


def get_friends(uid):
    return vk_request("getFriends", "&uid=%s" % uid)['response']
def get_profiles(uids):
    return vk_request("getProfiles", "&uids=%s" % ",".join("{}".format(i) for i in uids))['response']
def add_node(node):
    nodes.insert(node)
def gen_friend_tuple(n1, n2):
    return [n1, n2] if n1 > n2 else [n2, n1]
def add_friendship(n1, n2):
    if not friend_tuple_exists(n1, n2):
        friend_tuple = gen_friend_tuple(n1, n2)
        edges.insert({ 'eid': str(friend_tuple), 'friend_tuple': friend_tuple })
def friend_tuple_exists(n1, n2):
    return edges.find_one({ 'eid': gen_friend_tuple(n1, n2) }) != None
def node_visited(node):
    return nodes.find_one({ 'uid': node }) != None
def number_nodes():
    return nodes.count()


def do_BSF(seed):
    crawl_queue = [seed]
    while len(crawl_queue) > 0 and number_nodes() < MAX_N_FRIENDS:
        time.sleep(3)
        try:
            node = crawl_queue.pop(0)
            if not node_visited(node):
                print "node %s not visited" % node
                node_info = get_profiles([node])
                print "got profile. adding"
                print node_info

                add_node(node_info)
                #get friends that were not visited
                friends = [i for i in get_friends(node) if not node_visited(i)]
                if len(crawl_queue) < MAX_N_FRIENDS:
                    crawl_queue.extend(friends[: MAX_N_FRIENDS-len(crawl_queue)] )
                for friend in friends:
                    add_friendship(node, friend)
                print crawl_queue
        except Exception as e:
            print e
            pass

#get_profiles(["8923113"])

seed = int(sys.argv[1])
do_BSF(seed)

