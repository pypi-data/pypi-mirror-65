import struct, socket, threading, json, os, pickle
from essentials import tokening
import essentials
import copy
import time

def SocketDownload(sock):
    """
        Helper function for Socket Classes
    """
    try:
        data = b""
        payload_size = struct.calcsize(">L")
        while len(data) < payload_size:
            data += sock.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += sock.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        try:
            xData = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            return xData
        except:
            print("EOF Error Caught.")
    except:
        raise ConnectionError("Connection Error")

def SocketUpload(sock, data):
    """
        Helper function for Socket Classes
    """
    try:
        data = pickle.dumps(data, 0)
        size = len(data)
        sock.sendall(struct.pack(">L", size) + data)
    except:
        raise ConnectionError("Connection Error")

def HostServer(HOST, PORT, connections=5, SO_REUSEADDR=True):
    """
        Helper function for Socket Classes
    """
    PORT = int(os.getenv('PORT', PORT))
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    if SO_REUSEADDR == True:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST,PORT))
    sock.listen(connections)
    return sock

def ConnectorSocket(HOST, PORT):
    """
        Helper function for Socket Classes
    """
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))
    return  clientsocket

class Socket_Server_Host:
    def __init__(self, HOST, PORT, on_connection_open, on_data_recv, on_question, on_connection_close=False, daemon=True, autorun=True, connections=5, SO_REUSEADDR=True):
        """Host your own Socket server to allows connections to this computer.

        Parameters
        ----------
        HOST (:obj:`str`): Your hosting IP Address for this server.

        PORT (:obj:`int`): Which port you'd like to host this server on.

        on_connection_open (:obj:`def`): The function to call when you get a new connection. Gives Socket_Server_Client Class

        on_data_recv (:obj:`def`): The function to call when you receive data from a connection.

        on_question (:obj:`def`): The function to call when you receive a question from a connection.

        on_connection_close (:obj:`def`, optional): The function to call when a connection is closed.

        daemon (:obj:`bool`, optional): If you'd like the server to close when the python file closes or is interrupted. 

        autorun (:obj:`bool`, optional): Will run the server on init.

        connections (:obj:`int`, optional): How many connections to allow at one time. To be used with autorun = True

        Attributes
        ----------

        running (:obj:`bool`): Is the server still running.

        connections (:obj:`dict`): Holds all connection threads.

        on_connection_open (:obj:`def`): Holds the function you specified to use, can be over written. NOTE: Overwriting this will not overwrite old connection values.

        on_connection_close (:obj:`def`): Holds the function you specified to use, can be over written. NOTE: Overwriting this will not overwrite old connection values.

        on_data_recv (:obj:`def`): Holds the function you specified to use, can be over written. NOTE: Overwriting this will not overwrite old connection values.

        """
        self.on_connection_open = on_connection_open
        self.on_connection_close = on_connection_close
        self.on_data_recv = on_data_recv
        self.HOST = HOST
        self.PORT = PORT
        self.connections = {}
        self.on_question = on_question
        self.running = False
        if autorun:
            self.Run(connections, daemon, SO_REUSEADDR)
        
    def Run(self, connections=5, daemon=True, SO_REUSEADDR=True):
        """
        Will start the server on the specified host, port and listening count.

        This setup allows you to shutdown, change, and restart the server.

        Parameters
        ----------

        connections (:obj:`int`): How many connections to accept at one time


        :rtype: None

        """
        self.server = HostServer(self.HOST, self.PORT, connections, SO_REUSEADDR)
        self.running = True
        self.broker = threading.Thread(target=self.ConnectionBroker, daemon=daemon)
        self.broker.start()

    def ConnectionBroker(self):
        """
        Server background task for accepting connections, you'll not need to use this.

        :rtype: None

        """
        while self.running:
            try:
                conn, addr = self.server.accept()
                if self.running == False:
                    conn.close()
                conID = tokening.CreateToken(12, self.connections)
                connector = Socket_Server_Client(conn, addr, conID, self.on_data_recv, on_question=self.on_question, on_close=self.close_connection)
                self.connections[conID] = connector
                self.on_connection_open(connector)
                time.sleep(0.05)
            except Exception as e:
                self.running = False
                raise e
                
    def close_connection(self, connection):
        """
        Server background task for clearing connections and notifying the parent file, you'll not need to use this.

        :rtype: None

        """
        try:
            self.on_connection_close(connection)
        except:
            pass
        del self.connections[connection.conID]

    def Shutdown(self):
        """
        Shutdown the server and close all connections.

        :rtype: None

        """
        self.running = False
        keys = list(self.connections.keys())
        for con in keys:
            try:
                self.connections[con].shutdown()
            except:
                pass
        self.connections = {}
        try:
            self.server.close()
        except:
            pass

    def CloseConnection(self, conID):
        """
        Shortcut to close a certain connection.

        Can also be used as Server.connections[conID].shutdown()

        :rtype: None

        """
        self.connections[conID].shutdown()

class Socket_Server_Client:

    def __init__(self, socket, addr, conID, on_data, on_question, on_close, Heart_Beat=True, Heart_Beat_Wait=20):
        """CLIENT for Socket_Server_Host"""
        self.socket = socket
        self.addr = addr
        self.conID = conID
        self.on_data = on_data
        self.on_close = on_close
        self.running = True
        self.meta = {}
        self.on_question = on_question
        self.__ask_list__ = {}
        self.created = essentials.TimeStamp()
        threading.Thread(target=self.__data_rev__, daemon=True).start()
        if Heart_Beat == True:
            self.heart_beat_wait = Heart_Beat_Wait
            threading.Thread(target=self.__heart_beat__, daemon=True).start()

    def __heart_beat__(self):
        while self.running:
            self.send({"heart_beat_function": True})
            time.sleep(self.heart_beat_wait)

    def shutdown(self):
        """
        Shuts down this connection and removes any place it is still stored. Completes the on_close event.

        :rtype: None

        """

        try:
            self.on_close(self)
        except:
            pass
        self.running = False
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        try:
            self.socket.close()
        except:
            pass
        

    def send(self, data):
        """
        Send data to the remote connection.

        :rtype: None

        """
        if self.running == False:
            raise ConnectionResetError("No Connection")

        try:
            SocketUpload(self.socket, data)
        except:
            self.shutdown()

    def ask(self, data, timeout=5):
        tok = essentials.CreateToken(20, self.__ask_list__)
        self.__ask_list__[tok] = False
        self.send({"function_ask_question": tok, "data": data})
        while self.__ask_list__[tok] == False:
            time.sleep(0.01)
            timeout -= 0.01
            if timeout <= 0:
                raise TimeoutError("No response within time.")
        copyed = copy.deepcopy(self.__ask_list__[tok])
        del self.__ask_list__[tok]
        return copyed['data']


    def __data_rev__(self):
        """
        Server background task for accepting data and run the on_data event, you'll not need to use this.

        :rtype: None

        """
        while self.running:
            try:
                data = SocketDownload(self.socket)
            except:
                self.shutdown()
                return
            if type(data) == type({}) and 'heart_beat_function' in data:
                pass
            elif type(data) == type({}) and 'function_ask_response' in data:
                self.__ask_list__[data['function_ask_response']] = data
            elif type(data) == type({}) and 'function_ask_question' in data:
                self.on_question(Socket_Question(data['data'], self, data['function_ask_question']))
            else:
                self.on_data(data, self)
            time.sleep(0.05)

class Socket_Question(object):
    def __init__(self, data, client, tok):
        self.data = data
        self.questioner = client
        self.__answer_token__ = tok
    
    def answer(self, data):
        self.questioner.send({"function_ask_response": self.__answer_token__, "data": data})

class Socket_Connector:

    def __init__(self, HOST, PORT, on_data_recv, on_question, on_connection_close, Heart_Beat=True, Heart_Beat_Wait=10, legacy=False, legacy_buffer_size=1024):
        """Host your own Socket server to allows connections to this computer.

        Parameters
        ----------
        HOST (:obj:`str`): The hosting IP Address for the server.

        PORT (:obj:`int`): The port the server is using.

        on_data_recv (:obj:`def`): The function to call when you receive data from a connection.

        on_question (:obj:`def`): The function to call when you receive Socket_Question from a connection.

        on_connection_close (:obj:`def`, optional): The function to call when a connection is closed.

        Attributes
        ----------

        running (:obj:`bool`): Is the server still running.

        on_connection_close (:obj:`def`): Holds the function you specified to use, can be over written.

        on_data_recv (:obj:`def`): Holds the function you specified to use, can be over written.

        """
        self.running = True
        self.HOST = HOST
        self.legacy = legacy
        self.legacy_buffer_size = legacy_buffer_size
        self.PORT = PORT
        self.__ask_list__ = {}
        self.on_question = on_question
        self.on_connection_close = on_connection_close
        self.socket = ConnectorSocket(HOST, PORT)
        self.on_data_recv = on_data_recv
        threading.Thread(target=self.__data_rev__, daemon=True).start()
        if Heart_Beat == True:
            self.heart_beat_wait = Heart_Beat_Wait
            threading.Thread(target=self.__heart_beat__, daemon=True).start()

    def __heart_beat__(self):
        while self.running:
            self.send({"heart_beat_function": True})
            time.sleep(self.heart_beat_wait)

    def ask(self, data, timeout=5):
        if self.legacy:
            print("Can't ask questions to legacy connections")
            return
        tok = essentials.CreateToken(20, self.__ask_list__)
        self.__ask_list__[tok] = False
        self.send({"function_ask_question": tok, "data": data})
        while self.__ask_list__[tok] == False:
            time.sleep(0.01)
            timeout -= 0.01
            if timeout <= 0:
                raise TimeoutError("No response within time.")
        copyed = copy.deepcopy(self.__ask_list__[tok])
        del self.__ask_list__[tok]
        return copyed['data']

    def send(self, data):
        """
        Send data to the remote connection.

        :rtype: None

        """
        if self.running == False:
            raise ConnectionResetError("No Connection")
        try:
            if self.legacy:
                self.socket.sendall(data)
            else:
                SocketUpload(self.socket, data)
        except Exception as e:
            print(e)
            self.shutdown()

    def shutdown(self):
        """
        Shuts down this connection. Completes the on_close event.

        :rtype: None

        """
        self.running = False
        self.on_connection_close(self)
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        try:
            self.socket.close()
        except:
            pass
    
    def __data_rev__(self):
        """
        Client background task for accepting data and run the on_data event, you'll not need to use this.

        :rtype: None

        """
        while self.running:
            if self.legacy:
                self.on_data_recv(self.socket.recv(self.legacy_buffer_size))
            else:
                try:
                    data = SocketDownload(self.socket)
                except:
                    self.shutdown()
                    return
                if type(data) == type({}) and 'heart_beat_function' in data:
                    pass
                elif type(data) == type({}) and 'function_ask_response' in data:
                    self.__ask_list__[data['function_ask_response']] = data
                elif type(data) == type({}) and 'function_ask_question' in data:
                    self.on_question(Socket_Question(data['data'], self, data['function_ask_question']))
                else:
                    self.on_data_recv(data)