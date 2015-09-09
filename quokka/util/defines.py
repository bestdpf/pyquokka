class Defines(object):
    proxy_busy = 300
    proxy_base_delay = 10 
    proxy_max = 1000
    proxy_speed = 300

    ids_busy = 300
    ids_base_delay = 25
    ids_max =  1000
    ids_speed = 300    

    gateway_busy = 300
    gateway_base_delay = 10
    gateway_max = 1000
    gateway_speed = 300

    nat_busy = 300
    nat_base_delay = 15
    nat_max = 1000
    nat_speed = 300

    firewall_busy = 300
    firewall_base_delay = 15
    firewall_max = 1000
    firewall_speed = 300 

    general_base_delay = 10
    general_busy = 300
    general_max = 1000
    general_speed = 300

    INF = 1000000000

    
    random_max_delay = 10
    fattree_delay = 2 
    topo_delay = 2
    topo_host_num = 10   
 
    mb_select_num = 10
    mb_max_num = 100 
    mb_type = 5
    mb_add_step = 1
    max_delay = 350 
    max_delay_ratio = 0.01
    max_chain_len = 5
    mb_lst = ['firewall', 'nat', 'ids', 'gateway', 'proxy']
    mb_id = {'firewall':0, 'nat':1, 'ids':2, 'gateway':3, 'proxy':4}

    outFlowRatio = 0.56
    shortSmallRatio = 57.2
    shortLargeRatio = 59.8
    longSmallRatio = 91.6
    longLargeRatio = 100.0
    hostRatio = 0.8

    flow_num = 2000

class DCDefines(Defines):
    dcOutFlowRatio = 0.75
    dcRealTimeRatio = 0.50
    dcSoftRealTimeRatio = 0.60
    dcNoneRealTimeRatio = 1.00
    dcRealTimeLatency = 150
    dcSoftRealTimeLatency = 300
    dcNoneRealTimeLatency = 1000

