# The header contains the following fields:
#     MSB                                           LSB
#
#                                     1  1  1  1  1  1
#       0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |                      ID                       |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |QR|   Opcode  |AA|TC|RD|RA| Z|  AD |   RCODE   |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |                    QDCOUNT                    |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |                    ANCOUNT                    |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |                    NSCOUNT                    |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#     |                    ARCOUNT                    |
#     +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# where:

# ID              A 16 bit identifier assigned by the program that
#                 generates any kind of query.  This identifier is copied
#                 the corresponding reply and can be used by the requester
#                 to match up replies to outstanding queries.

# QR              A one bit field that specifies whether this message is a
#                 query (0), or a response (1).

# OPCODE          A four bit field that specifies kind of query in this
#                 message.  This value is set by the originator of a query
#                 and copied into the response.  The values are:

#                 0               a standard query (QUERY)

#                 1               an inverse query (IQUERY)

#                 2               a server status request (STATUS)

#                 3-15            reserved for future use

# AA              Authoritative Answer - this bit is valid in responses,
#                 and specifies that the responding name server is an
#                 authority for the domain name in question section.

#                 Note that the contents of the answer section may have
#                 multiple owner names because of aliases.  The AA bit

from DNSManager import DNSManager

class DNSMessageManager:
    def __init__(self):
        pass
    
    @staticmethod
    def getId(data):
        id = (data[0] << 8) + data[1]
        return int(id)
        
    @staticmethod
    def getFlags(data):
        flags = dict()
        flags["QR"] = data[2] >> 7
        flags["Opcode"] = (data[2] >> 3) & 0b1111
        flags["AA"] = (data[2] >> 2) & 0b1
        flags["TC"] = (data[2] >> 1) & 0b1
        flags["RD"] = data[2] & 0b1
        flags["RA"] = data[3] >> 7
        
        flags["Z"] = (data[3] >> 6) & 0b1
        flags["AD"] = (data[3] >> 4) & 0b11
        flags["RCODE"] = data[3] & 0b1111
        
        print(data[2])
        print(data[3])
        
        return flags
        
    @staticmethod
    def getQDCount(data):
        QDCount = (data[4] << 8) + data[5]
        return QDCount
    
    @staticmethod
    def getANCount(data):
        QDCount = (data[6] << 8) + data[7]
        return QDCount
        
    @staticmethod
    def getNSCount(data):
        NSCount = (data[8] << 8) + data[9]
        return NSCount
        
    @staticmethod
    def getARCount(data):
        ARCount = (data[10] << 8) + data[11]
        return ARCount


    @staticmethod
    def buildResponse(data):
        flags = DNSMessageManager.getFlags(data)
        if flags["QR"]:
            # not a query so must be ignored
            return bytes(0)
        
        flags["QR"] = 1
        flags["RA"] = flags["RD"]
        flags["AD"] = 0
        flags["CD"] = 1
        # change QDCount
        dt = bytearray(data)
        dt[4] = 0
        dt[5] = 1
        dt[6] = 0
        dt[7] = 1
        dt[8] = 0
        dt[9] = 0
        dt[10] = 0
        dt[11] = 0
        msg = DNSMessageManager.modifyHeader(dt, flags)
        msg = b"".join((
            msg,
            DNSMessageManager.buildStaticResponse(data)
        ))

        return bytes(msg)
    
    @staticmethod
    def modifyHeader(data, flags):
        data[2] ^= (flags["QR"] << 7)
        data[2] ^= (flags["Opcode"] << 3)
        data[2] ^= (flags["AA"] << 2)
        data[2] ^= (flags["TC"] << 1)
        data[2] ^= (flags["RD"])
        data[3] ^= (flags["RA"] << 7)
        data[3] ^= (flags["Z"] << 6)
        data[3] ^= (flags["AD"] << 4)
        data[3] ^= (flags["RCODE"])
        
        return data

    @staticmethod
    def buildStaticResponse(data):
        
        # TODO: Implement query extraction from the message
        query = DNSMessageManager.getQuery(data)
        ttl = bytes(60)
        rdlength = bytes(4)
        
        hostname = ".".join(query["hostparts"])
        host = DNSManager.getHostByName(hostname)
        pt = host.split(".")
        pt = [int(n) for n in pt]
        hostbytes = bytearray(pt)
        
        res = b"".join((
            b"\xc0\xc0",
            bytes(query["rrtype"]),
            bytes(query["qclass"]),
            ttl,
            rdlength,
            bytes(hostbytes)
            ))
        return res

    # TODO: Make this function implementation
    # def to_bytes(self):
    #     return b"".join((
    #         super(Response, self).to_bytes(),
    #         b"\xc0\x0c",                      # Pointer/Offset
    #         int_to_bytes(self.query.rrtype),  # TYPE: A
    #         int_to_bytes(self.query.qclass),  # CLASS: IN
    #         int_to_bytes(self.ttl, 8),        # TTL: 60
    #         int_to_bytes(4),                  # RDLENGTH: 4 octets
    #         _bytes(int(octet) for octet in self.address.split('.')),
    #     ))
    
    # DONE: Extract the query from the request
    # def from_bytes(cls, data):
    #     ini = 12
    #     lon = _intify(data[ini])
    #     labels = []
    #     while lon != 0:
    #         part = data[ini + 1:ini + lon + 1]
    #         labels.append(part.decode("latin-1"))
    #         ini += lon + 1
    #         lon = _intify(data[ini])
    #     rrtype = bytes_to_int(data[ini + 1:ini + 3])
    #     qclass = bytes_to_int(data[ini + 3:ini + 5])
    #     return cls(rrtype, tuple(labels), qclass)
    
    @staticmethod
    def getQuery(data):
        begin = 12
        messageSize = int(data[12])
        labels = []
        query = dict()
        
        while messageSize != 0:
            part = data[begin + 1: begin + messageSize + 1]
            labels.append(part.decode("latin-1"))
            begin += messageSize + 1
            messageSize = int(data[begin])
        
        rrtype = (data[begin + 1] << 8) + data[begin + 2]
        qclass = (data[begin + 3] << 8) + data[begin + 4]
        
        # python rules because that's a dict to anything
        query["rrtype"] = rrtype
        query["qclass"] = qclass
        query["hostparts"] = labels
        
        return query
    
    