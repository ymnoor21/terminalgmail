#!/bin/bash

dirIds='INBOX'
q='is:unread'
charCounts=100

function usage
{
    echo "usage: mygmail [[[-q is:unread ] [-d INBOX] [-cc 100]] | [-h]]"
    echo "-q = query you want gmail to filter"
    echo "-d = directory you want search"
    echo "-cc = characters count"
}

if [ "$#" -eq 0 ]; then
    dirIds='ALL'
    q='is:unread'
fi

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
        -cc | --ccount )
            shift
            if [ ! -z "$1" ]; then
                charCounts=$1
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
$PYTHON ~/Programming/Python/terminalgmail/mygmail.py "$q" "$dirIds" "$charCounts"

