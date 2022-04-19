from protocol.messages.clientHello import ClientHelloMessage

packets = {
    10100: ClientHelloMessage
}

class MessageFactory:
    def create_message_by_type(m_type):
        if m_type in packets:
            return packets[m_type]()
        return None