#!/usr/bin/env python3

from __future__ import print_function

import argparse,binascii,os,pprint,traceback,sys
from random import randrange
from dnslib import DNSRecord,DNSQuestion,QTYPE,DNSError

def fuzz_delete(b):
    """ Delete byte """
    f = b[:]
    del f[randrange(len(b))]
    return f

def fuzz_add(b):
    """ Add byte """
    f = b[:]
    f.insert(randrange(len(b)),randrange(256))
    return f

def fuzz_change(b):
    """ Change byte """
    f = b[:]
    f[randrange(len(b))] = randrange(256)
    return f

def fname(f):
    try:
        return f.func_name
    except AttributeError:
        return f.__name__

if __name__ == '__main__':

    a = argparse.ArgumentParser(description="DNS Fuzzer")
    a.add_argument("--server","-s",default="8.8.8.8",
                    help="DNS server address[:port] (default:8.8.8.8:53)")
    a.add_argument("--query","-q",default="google.com",
                   help="DNS query (default:google.com)")
    a.add_argument("--type","-t",default="A",
                   help="DNS query type (default:A)")
    a.add_argument("--debug","-d",action='store_true',default=False,
                   help="Print debug output")
    a.add_argument("--number","-n",type=int,default=200,
            help="Number of iterations (default:200)")
    a.add_argument("--tcp",action='store_true',default=False,
                    help="Use TCP (default: UDP)")
    args = a.parse_args()

    def p(*s):
        if args.debug:
            print(*s)

    uncaught = 0
    exceptions = []

    address,_,port = args.server.partition(':')
    port = int(port or 53)

    if args.query == 'google.com' and args.type == 'A':
        question = None
        packet = bytearray(binascii.unhexlify(b'55838180000100100000000006676f6f676c6503636f6d0000010001c00c000100010000012b00043efca994c00c000100010000012b00043efca998c00c000100010000012b00043efca9b7c00c000100010000012b00043efca99dc00c000100010000012b00043efca9acc00c000100010000012b00043efca9bbc00c000100010000012b00043efca9a3c00c000100010000012b00043efca9a8c00c000100010000012b00043efca9b1c00c000100010000012b00043efca9a7c00c000100010000012b00043efca999c00c000100010000012b00043efca9a2c00c000100010000012b00043efca9b6c00c000100010000012b00043efca9b2c00c000100010000012b00043efca9adc00c000100010000012b00043efca99e'))
    else:
        question = DNSRecord(q=DNSQuestion(args.query,getattr(QTYPE,args.type)))
        packet = bytearray(question.send(address,port,tcp=args.tcp))

    original = DNSRecord.parse(packet)

    if question:
        p("Question:")
        p(question.toZone(prefix="  | "))

    p("Original:")
    p(original.toZone(prefix="  | "))

    for f in (fuzz_delete,fuzz_add,fuzz_change):
        for i in range(args.number):
            try:
                fuzzed_pkt = f(packet)
                fuzzed = DNSRecord.parse(fuzzed_pkt)
                if original != fuzzed:
                    diff = original.diff(fuzzed)
                    p("[%s:parsed ok] >>> %d Diff Errors" % (fname(f),len(diff)))
                    p(pprint.pformat(diff))
            except DNSError as e:
                p("[%s:exception] >>> %s" % (fname(f),str(e)))
            except Exception as e:
                raise
                uncaught += 1
                exceptions.append((binascii.hexlify(fuzzed_pkt),traceback.format_exc(limit=1)))
                p(traceback.format_exc())

    p("-----------------------")
    print("Uncaught Exceptions: %d" % uncaught)

    if exceptions:
        pprint.pprint(exceptions)

