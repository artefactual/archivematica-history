#!/bin/bash

databaseName="MCP"
username="demo"
dpPassword="$1"

sudo mysql $dpPassword --execute="source /usr/share/transcoder/mysql" "$databaseName"
