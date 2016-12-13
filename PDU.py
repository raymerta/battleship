class PDU:
    """ our data object to send via app layer protocol"""
    def __init__(self, data_raw):
    	data_split = data_raw.split('\r')

        #important
        try:
            request = data_split[0].split(" ")
            self.req_type = request[0]
            self.uri = request[1]
            self.protocol_name = request[2]

            host = data_split[1].split(":")
            self.host_address = host[1]
            self.host_port = host[2]

            #get content
            self.content = data_split[-1]
        except IndexError as ir:
            self.req_type = ""
            self.uri = ""
            self.protocol_name = ""
            self.host_address = ""
            self.host_port = ""


        #print data_split
    	self.data_split = data_split

    def __str__(self):
    	res = ""
    	return res
    	



