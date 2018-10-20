#! /bin/bash

ESC=$(echo -ne '\x1b')

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
  echo -n $1 | grep -E '\[F' && return 1
  return 1
}

echo Press arrow key to control the rotating direction
echo Press \[End\] key to send stop signal

while :
do
  until read -sN1 k1 && [ "$k1" = "$ESC" ]; do false; done
  read -sN2 k2
  key_to_code $k1$k2
  command=$?
  echo -n sending command $command' '
  send_command $(echo -n $command)
done
