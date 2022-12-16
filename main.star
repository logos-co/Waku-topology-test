IMAGE_NAME = "statusteam/nim-waku:deploy-status-prod"

# Waku RPC Port
RPC_PORT_ID = "rpc"
RPC_TCP_PORT = 8545

# Waku Matrics Port
PROMETHEUS_PORT_ID = "prometheus"
PROMETHEUS_TCP_PORT = 8008

GET_WAKU_INFO_METHOD = "get_waku_v2_debug_v1_info"
CONNECT_TO_PEER_METHOD = "post_waku_v2_admin_v1_peers"

def run(args):
    # in case u want to run each json separately, follow this cmd line arg format for main.star 
    #kurtosis run . --args '{"json_nw_name": "github.com/user/kurto-module/json_dir/abc.json"}'
    json_loc=args.json_nw_name
    file_contents = read_file(json_loc)
    #print(file_contents)
    decoded = json.decode(file_contents)
    services ={}

    # Get up all waku nodes
    for wakunode_name in decoded.keys():
        waku_service = add_service(
            service_id=wakunode_name,
            config=struct(
                image=IMAGE_NAME,
                ports={ 
                    RPC_PORT_ID: struct(number=RPC_TCP_PORT, protocol="TCP"),
                    PROMETHEUS_PORT_ID: struct(number=PROMETHEUS_TCP_PORT, protocol="TCP")
                    },
                entrypoint=[
                    "/usr/bin/wakunode", "--rpc-address=0.0.0.0", "--metrics-server-address=0.0.0.0"
                ],
                cmd=[
                    "--topics='" + " ".join(decoded[wakunode_name]["topics"]) + "'", '--rpc-admin=true', '--keep-alive=true',  '--metrics-server=true',
                ]
            )
        )
        services[wakunode_name] = waku_service
