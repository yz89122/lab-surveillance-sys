#! /bin/bash

ESC=$(echo -ne '\x1b')
EOT=$(echo -ne '\x04')

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

move_direction=''
move_speed=10

send_move_command() {
    # prints message
    echo -n "sending move signal $move_direction... "
    # web interface provided by the camera
    curl "$HOST:$PORT/cgi-bin/view/cammove.cgi?move=$move_direction" \
            --user "$USER:$PASS" 1>/dev/null \
            1>/dev/null \
            2>/dev/null \
        && echo done \
        || echo error when sending command
}

send_set_speed_command() {
    [ $move_speed -gt 10 ] && move_speed=10
    [ $move_speed -lt 1 ] && move_speed=1
    echo -n "setting move speed to $move_speed... "
    curl "$HOST:$PORT/cgi-bin/view/ptzspeed.cgi?speed=$move_speed" \
            --user "$USER:$PASS" 1>/dev/null \
            1>/dev/null \
            2>/dev/null \
        && echo done \
        || echo error when sending command
}

arrow_key_to_code() {
    echo -n $1 | grep -E '\[A' && echo && move_direction='up' # up
    echo -n $1 | grep -E '\[B' && move_direction='down' # down
    echo -n $1 | grep -E '\[C' && move_direction='right' # right
    echo -n $1 | grep -E '\[D' && move_direction='left' # left
}

num_pad_control() {
    [ "$1" -eq 1 ] && move_direction='leftdown' && send_move_command
    [ "$1" -eq 2 ] && move_direction='down' && send_move_command
    [ "$1" -eq 3 ] && move_direction='rightdown' && send_move_command
    [ "$1" -eq 4 ] && move_direction='left' && send_move_command
    [ "$1" -eq 6 ] && move_direction='right' && send_move_command
    [ "$1" -eq 7 ] && move_direction='leftup' && send_move_command
    [ "$1" -eq 8 ] && move_direction='up' && send_move_command
    [ "$1" -eq 9 ] && move_direction='rightup' && send_move_command

    [ "$1" -eq 5 ] && move_direction='home' && send_move_command
}

parse_command() {
    cmd=()
    for part in $1
    do
        cmd+=($part)
    done
    case ${cmd[0]} in
        'speed')
            move_speed=${cmd[1]}
            send_set_speed_command
            ;;
        *)
            echo 'unknown command'
            ;;
    esac
}

trap 'echo Ctrl+C detected ; exit ;' 2

# tell user how to use this script
echo 'Press arrow key or NumPad to control the rotating direction'
echo '+ and - key to zoom in or zoom out'
echo 'Type `speed [value]` to change rotating speed'
echo 'Ctrl+C to end this script'

while :
do
    read -sN1 k1 || { echo EOF ; break ; }
    [ "$k1" = $EOT ] && { echo EOT ; break ; }
    if [ "$k1" = "$ESC" ]
    then
        # read the remaining characters
        read -sN2 k2 || { echo EOF ; break ; }
        # translate key to actual control code
        arrow_key_to_code $k1$k2
        send_move_command
    elif [ "$k1" = '+' ]
    then
        move_direction='rZoomIn'
        send_move_command
    elif [ "$k1" = '-' ]
    then
        move_direction='rZoomOut'
        send_move_command
    elif [[ "$k1" =~ ^[0-9]$ ]]
    then
        num_pad_control $k1
    elif [[ "$k1" =~ ^[a-z]$ ]]
    then
        echo -n "$k1"
        read k2 || { echo EOF ; break ; }
        parse_command "$k1$k2"
    else
        echo unkown command
    fi
done
