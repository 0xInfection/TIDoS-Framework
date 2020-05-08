from __future__ import absolute_import

import struct
import zlib
from io import DEFAULT_BUFFER_SIZE

from ._urllib2_fork import BaseHandler
from .polyglot import is_py2


CRC_MASK = 0xffffffff
if is_py2:
    CRC_MASK = long(CRC_MASK)


def gzip_prefix():
    # See http://www.gzip.org/zlib/rfc-gzip.html
    return b''.join((
        b'\x1f\x8b',  # ID1 and ID2: gzip marker
        b'\x08',  # CM: compression method
        b'\x00',  # FLG: none set
        # MTIME: 4 bytes, set to zero so as not to leak timezone information
        b'\0\0\0\0',
        b'\x02',  # XFL: max compression, slowest algo
        b'\xff',  # OS: unknown
    ))


def compress_readable_output(src_file, compress_level=6):
    crc = zlib.crc32(b"")
    size = 0
    zobj = zlib.compressobj(compress_level, zlib.DEFLATED, -zlib.MAX_WBITS,
                            zlib.DEF_MEM_LEVEL, zlib.Z_DEFAULT_STRATEGY)
    prefix_written = False
    while True:
        data = src_file.read(DEFAULT_BUFFER_SIZE)
        if not data:
            break
        size += len(data)
        crc = zlib.crc32(data, crc)
        data = zobj.compress(data)
        if not prefix_written:
            prefix_written = True
            data = gzip_prefix() + data
        yield data
    yield zobj.flush() + struct.pack(b"<LL", crc & CRC_MASK, size)


def read_amt(f, amt):
    ans = b''
    while len(ans) < amt:
        extra = f.read(amt - len(ans))
        if not extra:
            raise EOFError('Unexpected end of compressed stream')
        ans += extra
    return ans


class UnzipWrapper:
    def __init__(self, fp):
        self.__decoder = zlib.decompressobj(-zlib.MAX_WBITS)
        self.__data = b''
        self.__crc = zlib.crc32(self.__data) & CRC_MASK
        self.__fp = fp
        self.__size = 0
        self.__is_fully_read = False

    def read(self, sz=-1):
        amt_read = 0
        ans = []
        if self.__data:
            if sz < 0 or len(self.__data) < sz:
                ans.append(self.__data)
                amt_read += len(self.__data)
                self.__data = b''
            else:
                self.__data, ret = self.__data[sz:], self.__data[:sz]
                return ret

        if not self.__is_fully_read:
            while not self.__decoder.unused_data and (sz < 0 or amt_read < sz):
                chunk = self.__fp.read(1024)
                if chunk:
                    if self.__decoder.unconsumed_tail:
                        chunk = self.__decoder.unconsumed_tail + chunk
                    chunk = self.__decoder.decompress(chunk)
                    ans.append(chunk)
                    amt_read += len(chunk)
                    self.__size += len(chunk)
                    self.__crc = zlib.crc32(chunk, self.__crc)
                else:
                    if not self.__decoder.unused_data:
                        raise ValueError(
                            'unexpected end of compressed gzip data,'
                            ' before reading trailer')
                    break

            if self.__decoder.unused_data:
                # End of compressed stream reached
                tail = self.__decoder.unused_data
                if len(tail) < 8:
                    tail += read_amt(self.__fp, 8 - len(tail))
                # ignore any extra bytes after end of compressed stream
                self.__fp.read()
                # check CRC, ignore size mismatch
                crc, size = struct.unpack(b'<LL', tail)
                if (crc & CRC_MASK) != (self.__crc & CRC_MASK):
                    raise ValueError(
                        'gzip stream is corrupted, CRC does not match')
                self.__is_fully_read = True

        ans = b''.join(ans)
        if len(ans) > sz and sz > -1:
            ans, self.__data = ans[:sz], ans[sz:]
        return ans

    def readline(self, sz=-1):
        # Dont care about making this efficient
        data = self.read()
        idx = data.find(b'\n')
        if idx > 0:
            if sz < 0 or idx < sz:
                line, self.__data = data[:idx + 1], data[idx + 1:]
            else:
                line, self.__data = data[:sz], data[sz:]
        else:
            if sz > -1:
                line, self.__data = data[:sz], data[sz:]
            else:
                line = data
        return line

    def close(self):
        self.__fp.close()

    def fileno(self):
        return self.__fp.fileno()

    def __iter__(self):
        ans = self.readline()
        if ans:
            yield ans

    def next(self):
        ans = self.readline()
        if not ans:
            raise StopIteration()
        return ans


def create_gzip_decompressor(zipped_file):
    prefix = read_amt(zipped_file, 10)
    if prefix[:2] != b'\x1f\x8b':
        raise ValueError('gzip stream has incorrect magic bytes: %r' %
                         prefix[:2])
    if prefix[2:3] != b'\x08':
        raise ValueError('gzip stream has unknown compression method: %r' %
                         prefix[2])
    flag = ord(prefix[3:4])
    if flag & 4:  # extra
        extra_amt = read_amt(zipped_file, 2)
        extra_amt = ord(extra_amt[0]) + 256 * ord(extra_amt[1])
        if extra_amt:
            read_amt(zipped_file, extra_amt)
    if flag & 8:  # filename
        while read_amt(zipped_file, 1) != b'\0':
            continue
    if flag & 16:  # comment
        while read_amt(zipped_file, 1) != b'\0':
            continue
    if flag & 2:  # crc
        read_amt(zipped_file, 2)
    return UnzipWrapper(zipped_file)


class HTTPGzipProcessor(BaseHandler):
    handler_order = 200  # response processing before HTTPEquivProcessor

    def __init__(self, request_gzip=False):
        self.request_gzip = request_gzip

    def __copy__(self):
        return self.__class__(self.request_gzip)

    def http_request(self, request):
        if self.request_gzip:
            existing = [
                x.strip()
                for x in request.get_header('Accept-Encoding', '').split(',')
            ]
            if sum('gzip' in x for x in existing) < 1:
                existing.append('gzip')
                request.add_header("Accept-Encoding",
                                   ', '.join(filter(None, existing)))
        return request

    def http_response(self, request, response):
        # post-process response
        h = response.info()
        enc_hdrs = h.getheaders("Content-encoding")
        for enc_hdr in enc_hdrs:
            if "gzip" in enc_hdr:
                response._set_fp(create_gzip_decompressor(response.fp))
                del h['Content-encoding']
                del h['Content-length']
        return response

    https_response = http_response
    https_request = http_request
