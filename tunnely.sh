#!/bin/bash

# Storing the flags options into variables
while getopts m:K:i:p:I:P: flag
do
    case "${flag}" in
        m) mode=${OPTARG};;
        K) key_path=${OPTARG};;
        i) remote_ip=${OPTARG};;
        p) remote_port=${OPTARG};;
        I) local_ip=${OPTARG};;
        P) local_port=${OPTARG};;
    esac
done

# Checking if the mode has been set
if [ -z $mode ];
then
    # If it hasn't, the script ends
    echo "Please specify the way Tunnely will run. (C for client or S for server)";
    exit;
fi

# Checking if the key path argument has been set
if [ -z $key_path ];
then
    # If it hasn't, the script ends
    echo "Please specify the file path for the key with the -K option. (Make sure it is inside a .txt file)";
    exit;
fi

# Validating the file containing the key
if ! [ -f $key_path ];
then 
    echo "Invalid file. Please specify a valid key file"
    exit;
fi

# Checking if the local ip address has been set
if [ -z $local_ip ];
then
    # If it hasn't, the script ends
    echo "Please specify the local IP address on which Tunnely will run with the -I option. (Make sure it is in the right format)";
    exit;
fi

# Checking if the local port has been set
if [ -z $local_port ];
then
    # If it hasn't, the script ends
    echo "Please specify the local port on which Tunnely will run with the -P option. (Make sure it is in the right format)";
    exit;
fi

# We check what mode Tunnely is running in
if [ $mode = "C" ]; 
then 
    echo "Tunnely will run as a client"

    # Checking if the remote ip address has been set
    if [ -z $remote_ip ];
    then
        # If it hasn't, the script ends
        echo "Please specify the remote IP address of the server with the -i option. (Make sure it is in the right format)";
        exit;
    fi

    # Checking if the remote port has been set
    if [ -z $remote_port ];
    then
        # If it hasn't, the script ends
        echo "Please specify the remote port of the server with the -p option. (Make sure it is in the right format)";
        exit;
    fi

    echo "$key_path";
    echo "$remote_ip";
    echo "$remote_port";
    echo "$local_port";
    echo "$local_ip";

    sudo ./client.py $key_path $local_ip $local_port $remote_ip $remote_port

elif [ $mode = "S" ];
then 
    echo "Tunnely will run as a server"
    
    echo "$key_path";
    echo "$local_port";
    echo "$local_ip";

    sudo ./server.py $key_path $local_ip $local_port
else 
    echo "Wrong mode. Please specify the way Tunnely will run. (C for client or S for server)"
fi