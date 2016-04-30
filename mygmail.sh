#!/bin/bash

dirIds='INBOX'
q='is:unread'

function usage
{
    echo "usage: mygmail [[[-q is:unread ] [-d INBOX]] | [-h]]"
}

while [ "$1" != "" ]; do
    case $1 in
        -q | --query )
            shift
            if [ ! -z "$1" ]; then
                q=$1
            fi
            ;;
        -d | --directory )
            shift
            if [ ! -z "$1" ]; then
                dirIds=$1
            fi
            ;;
        -h | --help )
            usage
            exit
            ;;
        * )
            usage
            exit 1
    esac
    shift
done

PYTHON=`which python`
$PYTHON ~/Programming/Python/terminalgmail/mygmail.py "$q" "$dirIds"

