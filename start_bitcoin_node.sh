#!/bin/bash

# Configuration for Bitcoin Core daemon and CLI
RPC_USER="Cornbread78"
RPC_PASS="26a78aea33835e4d74654ce25e3e8b51a0706d8e55353f92b98c73f7ec33f416"

echo "=================================================="
echo " STARTING BITCOIN DAEMON (bitcoind)"
echo "=================================================="

# Start bitcoind in daemon mode with custom credentials if not already running
if pgrep -x "bitcoind" > /dev/null; then
    echo "[+] bitcoind is already running."
else
    bitcoind -daemon -rpcuser="$RPC_USER" -rpcpassword="$RPC_PASS"
    echo "[+] bitcoind launched successfully in the background."
    sleep 3
fi

echo "=================================================="
echo " RUNNING BITCOIN-CLI HEALTH & STATUS CHECK"
echo "=================================================="

# Test connection using bitcoin-cli
bitcoin-cli -rpcuser="$RPC_USER" -rpcpassword="$RPC_PASS" getblockchaininfo
