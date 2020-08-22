from xml.etree import ElementTree as ET

f1=file('queue.txt','r').readlines()
ppp = ["capacity","maximum-capacity"]
for i in f1:
        if "---CON" in i:
                flag_c = f1.index(i)
        if "---PAR" in i:
                flag_p = f1.index(i)
        if "---QUE" in i:
                flag_q = f1.index(i)

partition = f1[flag_p+1].strip('\n').split(',')
qqq = ["user-limit-factor","accessible-node-labels","default-node-label-expression","acl_submit_applications","acl_administer_queue","state"]
title = qqq + partition
topo = {"root":[]}
configuration = ET.Element('configuration')
def add_property(name,value):
        global configuration
        property = ET.Element('property')
        ET.SubElement(property, 'name').text = name
        ET.SubElement(property, 'value').text = value
        configuration.append(property)

def put_in_topo(str):
        global topo
        ooo = str.split('.')
        if len(ooo) > 1:
                son = ooo.pop()
                father = '.'.join(ooo)
                if topo.has_key(father):
                        topo[father].append(son)
                else:
                        topo[father] = []
                        topo[father].append(son)

for i in f1[flag_c+1:]:
        if '=' not in i:
                break
        name,value = i.strip('\n').split('=')
        add_property("yarn.scheduler.capacity."+name,value)
        if '=' not in i:
                break




for line in f1[flag_q+1:]:
        config = line.strip('\n').split()
        queue_name = config[0]
        put_in_topo(queue_name)
        for i in range(0,len(title)):
                if i<len(qqq) :
                        name = "yarn.scheduler.capacity." + queue_name + '.' + title[i]
                        value = config[i+1]
                        add_property(name,value)

                else:
                        numbers = config[i+1].split("|")
                        for o in [0,1]:
                                if title[i] == "DEFAULT":
                                        name = "yarn.scheduler.capacity." + queue_name + '.' + ppp[o]
                                else:
                                        name = "yarn.scheduler.capacity." + queue_name + ".accessible-node-labels." + title[i] + '.' + ppp[o]
                                value = numbers[o]
                                add_property(name,value)

for i in topo:
        name = "yarn.scheduler.capacity." + i + ".queues"
        value = ','.join(topo[i])
        add_property(name,value)


ET.dump(configuration)
