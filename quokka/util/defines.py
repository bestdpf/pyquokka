class Defines(object):
    proxy_busy = 200
    proxy_base_delay = 1
    proxy_max = 500
    proxy_speed = 200

    ids_busy = 200
    ids_base_delay = 5
    ids_max = 500
    ids_speed = 200    

    gateway_busy = 200
    gateway_base_delay = 1
    gateway_max = 500
    gateway_speed = 200

    nat_busy = 200
    nat_base_delay = 2
    nat_max = 500
    nat_speed = 200

    firewall_busy = 200
    firewall_base_delay = 5
    firewall_max = 500
    firewall_speed = 200 

    general_base_delay = 1
    general_busy = 200
    general_max = 500
    general_speed = 200

    INF = 1000000000

    mb_select_num = 10
    mb_max_num = 10
    mb_type = 5
    mb_add_step = 1
    max_delay = 200
    max_delay_ratio = 0.01
    max_chain_len = 5
    mb_lst = ['firewall', 'nat', 'ids', 'gateway', 'proxy']
    mb_id = {'firewall':0, 'nat':1, 'ids':2, 'gateway':3, 'proxy':4}

    outFlowRatio = 0.56
    shortSmallRatio = 57.2
    shortLargeRatio = 59.8
    longSmallRatio = 91.6
    longLargeRatio = 8.4
    hostRatio = 0.8    

    flow_num = 2000
