#!/bin/bash
all_ips=$(hostname -i) 
my_local_ip=${all_ips%% *} 
echo $my_local_ip 
export MY_LOCAL_IP=$my_local_ip
