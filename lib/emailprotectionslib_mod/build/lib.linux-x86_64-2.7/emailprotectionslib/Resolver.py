import dnslib
import sys

#A resolver wrapper around dnslib.py
# stolen wholesale from https://github.com/TheRook/subbrute
# thanks Rook
class resolver:
    #Google's DNS servers are only used if zero resolvers are specified by the user.
    pos = 0
    rcode = ""
    wildcards = {}
    failed_code = False
    last_resolver = ""

    def __init__(self, nameservers = ['8.8.8.8','8.8.4.4']):
        self.nameservers = nameservers

    def query(self, hostname, query_type = 'ANY', name_server = False, use_tcp = True):
        ret = []
        response = None
        if name_server == False:
            name_server = self.get_ns()
        else:
            self.wildcards = {}
            self.failed_code = None
        self.last_resolver = name_server
        query = dnslib.DNSRecord.question(hostname, query_type.upper().strip())
        try:
            response_q = query.send(name_server, 53, use_tcp)
            if response_q:
                response = dnslib.DNSRecord.parse(response_q)
            else:
                raise IOError("Empty Response")
        except Exception as e:
            #IOErrors are all conditions that require a retry.
            raise IOError(str(e))
        if response:
            self.rcode = dnslib.RCODE[response.header.rcode]
            for r in response.rr:
                try:
                    rtype = str(dnslib.QTYPE[r.rtype])
                except:#Server sent an unknown type:
                    rtype = str(r.rtype)
                #Fully qualified domains may cause problems for other tools that use subbrute's output.
                rhost = str(r.rname).rstrip(".")
                ret.append((rhost, rtype, str(r.rdata)))
            #What kind of response did we get?
            if self.rcode not in ['NOERROR', 'NXDOMAIN', 'SERVFAIL', 'REFUSED']:
                trace('!Odd error code:', self.rcode, hostname, query_type)
            #Is this a perm error?  We will have to retry to find out.
            if self.rcode in ['SERVFAIL', 'REFUSED', 'FORMERR', 'NOTIMP', 'NOTAUTH']:
                raise IOError('DNS Failure: ' + hostname + " - " + self.rcode)
            #Did we get an empty body and a non-error code?
            elif not len(ret) and self.rcode != "NXDOMAIN":
                raise IOError("DNS Error - " + self.rcode + " - for:" + hostname)
        return ret

    def was_successful(self):
        ret = False
        if self.failed_code and self.rcode != self.failed_code:
            ret = True
        elif self.rcode == 'NOERROR':
            ret = True
        return ret

    def get_returncode(self):
        return self.rcode

    def get_ns(self):
        if self.pos >= len(self.nameservers):
            self.pos = 0
        ret = self.nameservers[self.pos]
        # we may have metadata on how this resolver fails
        try:
            ret, self.wildcards, self.failed_code = ret
        except:
            self.wildcards = {}
            self.failed_code = None
        self.pos += 1
        return ret

    def add_ns(self, resolver):
        if resolver:
            self.nameservers.append(resolver)

    def get_authoritative(self, hostname):
        ret = []
        while not ret and hostname.count(".") >= 1:
            try:
                trace("Looking for nameservers:", hostname)
                nameservers = self.query(hostname, 'NS')
            except IOError:#lookup failed.
                nameservers = []
            for n in nameservers:
                #A DNS server could return anything.
                rhost, record_type, record = n
                if record_type == "NS":
                    #Return all A records for this NS lookup.
                    a_lookup = self.query(record.rstrip("."), 'A')
                    for a_host, a_type, a_record in a_lookup:
                        ret.append(a_record)
                #If a nameserver wasn't found try the parent of this sub.
            hostname = hostname[hostname.find(".") + 1:]
        return ret

    def get_last_resolver(self):
        return self.last_resolver

#Toggle debug output
verbose = False
def trace(*args, **kwargs):
    if verbose:
        for a in args:
            sys.stderr.write(str(a))
            sys.stderr.write(" ")
        sys.stderr.write("\n")
