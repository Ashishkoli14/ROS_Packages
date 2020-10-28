#!/bin/bash

# Store URL in a variable
URL1="http://www.hivemq.com/demos/websocket-client/"
URL2="https://docs.google.com/spreadsheets/d/1VMJT3par-hYJDuJxzUXvyRzMpXCdWEVIUWPCANHVWLk/edit#gid=0"

# Print some message
echo "** Opening $URL1 and $URL2 in Firefox **"

# Use firefox to open the URL in a new window
firefox -new-window $URL1 
firefox -new-window $URL2
