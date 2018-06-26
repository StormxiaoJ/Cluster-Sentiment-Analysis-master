#Set node IP addresses, electing the first as "master node" and admin credentials
export declare nodes=(115.146.95.90,115.146.95.87)
export masternode=`echo ${nodes} | cut -f1 -d' '`
export othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export size=${#nodes[@]}
export user=admin
export pass=admin

#Create Docker containers
for node in ${nodes[@]}}; do docker create couchdb:2.1.1 -–ip=${node}; done
#Put in conts the Docker container IDs
declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

#Start the containers

for cont in "${conts[@]}"; do docker start ${cont}; done
sleep 3

#Write the cookie name and node name to the CouchDB configuration on every node

for (( i=0; i<${size}; i++ )); do
    docker exec ${conts[${i}]} \
      bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
    docker exec ${conts[${i}]} \
      bash -c "echo \"-name couchdb@${nodes[${i}]}\" >> /opt/couchdb/etc/vm.args"
done

#Restart containers to pick-up changes to CouchDB configurations

for cont in "${conts[@]}"; do docker restart ${cont}; done
sleep 3

#Set the CouchDB cluster (deleting the default nonode@nohost node from the configuration)

for node in "${nodes[@]}"; do     
    curl -XPUT "http://${node}:5984/_node/_local/_config/admins/${user}" --data "\"${pass}\""    
    curl -XPUT "http://${user}:${pass}@${node}:5984/_node/couchdb@${node}/_config/chttpd/bind_address" --data '"0.0.0.0"'
done
for node in "${nodes[@]}"; do     
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \
        \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"5984\", \
        \"remote_node\": \"${node}\", \
        \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
done
for node in "${nodes[@]}"; do     
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"add_node\", \"host\":\"${node}\", \
        \"port\": \"5984\", \"username\": \"${user}\", \"password\":\"${pass}\"}"
done
curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}" 
rev=`curl -XGET "http://172.17.0.2:5986/_nodes/nonode@nohost" --user "${user}:${pass}" | sed -e 's/[{}"]//g' | cut -f3 -d:`
curl -X DELETE "http://172.17.0.2:5986/_nodes/nonode@nohost?rev=${rev}"  --user "${user}:${pass}"

#Check the correct cluster configuration

for node in "${nodes[@]}"; do  curl -X GET "http://${user}:${pass}@${node}:5984/_membership"; done


#Adding a database to one node of the cluster cause it to be created on all other nodes as well

curl -XPUT "http://${user}:${pass}@${masternode}:5984/twitter"
for node in "${nodes[@]}"; do  curl -X GET "http://${user}:${pass}@${node}:5984/_all_dbs"; done
