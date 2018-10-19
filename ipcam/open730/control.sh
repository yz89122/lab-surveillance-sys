#! /bin/bash

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] ;
then
  echo "Usage: $0 <hostname> <http-port> <username> [password]"
  exit 1
fi

HOST=$1
PORT=$2
USER=$3
PASS=$4

echo "Hostname: [$HOST]"
echo "HttpPort: [$PORT]"
echo "Username: [$USER]"
echo "Password: [$PASS]"

send_command() {
  curl "$HOST:$PORT/decoder_control.cgi?command=$1" --user "$USER:$PASS"
}

key_to_code() {
  echo -n $1 | grep -E '\[A' && return 0
  echo -n $1 | grep -E '\[B' && return 2
  echo -n $1 | grep -E '\[C' && return 4
  echo -n $1 | grep -E '\[D' && return 6
  return 1
}

while :
do
  read -sn3 key
  key_to_code $key
  command=$?
  echo -n command $command' '
  send_command $(echo -n $command)
done
