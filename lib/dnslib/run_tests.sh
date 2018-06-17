#!/bin/sh

export PYTHONPATH=$(pwd)

: ${VERSIONS:="python python3"}

for src in __init__.py bimap.py bit.py buffer.py label.py dns.py lex.py server.py digparser.py ranges.py test_decode.py
do
    echo "===" $src
    for py in $VERSIONS
    do
        echo "Testing:" $($py --version 2>&1)
        $py dnslib/$src
    done
done

for py in $VERSIONS
do
    echo "Fuzz:" $($py --version 2>&1)
    $py fuzz.py
done
