#! /bin/bash

ESC=$(echo -ne '\x1b')

# if the arguments doesn't satisfied
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]
then
  echo "Usage: $0 <hostname> <http-port> <username> [password]"
  exit 1
fi

# variables
HOST=$1
PORT=$2
USER=$3
PASS=$4

# PORT value check
if [[ ! "$PORT" =~ ^[0-9]+$ ]]
then
  echo 'The parameter <http-port> should be a positive integer'
  echo "[$PORT] entered"
  exit 1
fi

# PORT check
if [ "$PORT" -gt 65535 ]
then
  echo 'The port number is too large'
  echo "[$PORT] entered"
  exit 1
fi

# prints the info
echo "Hostname: [$HOST]"
echo "HttpPort: [$PORT]"
echo "Username: [$USER]"
echo "Password: [$PASS]"

send_command() {
  # web interface provided by the camera
  curl "$HOST:$PORT/decoder_control.cgi?command=$1" --user "$USER:$PASS"
}

key_to_code() {
  echo -n $1 | grep -E '\[F' && return 1 # end
  echo -n $1 | grep -E '\[A' && return 0 # up
  echo -n $1 | grep -E '\[B' && return 2 # down
  echo -n $1 | grep -E '\[C' && return 4 # right
  echo -n $1 | grep -E '\[D' && return 6 # left
  return 1 # default
}

# tell user how to use this script
echo 'Press arrow key to control the rotating direction'
echo 'Press [End] key to send stop signal'
echo 'Ctrl+C to end this script'

while :
do
  # ignore non-control key pressed
  until read -sN1 k1 && [ "$k1" = "$ESC" ]; do false; done
  # read the remaining characters
  read -sN2 k2
  # translate key to actual control code
  key_to_code $k1$k2
  # send the control code to camera
  command=$?
  # prints message
  echo -n sending command $command' '
  # use $(echo -n $command) in order to convert integer to string
  send_command $(echo -n $command)
done
