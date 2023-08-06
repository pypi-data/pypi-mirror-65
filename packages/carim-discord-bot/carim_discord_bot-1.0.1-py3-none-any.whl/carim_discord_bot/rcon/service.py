import asyncio
import logging
import re

from carim_discord_bot import config
from carim_discord_bot.rcon import protocol, registrar

log = logging.getLogger(__name__)
VALID_COMMANDS = ('players', 'admins', 'kick', 'bans', 'ban', 'removeBan', 'say', 'addBan')


def process_packet(packet, event_queue: asyncio.Queue, chat_queue: asyncio.Queue):
    if isinstance(packet.payload, protocol.Login):
        log.info(f'login was {"" if packet.payload.success else "not "}successful')
    else:
        if isinstance(packet.payload, protocol.Command):
            asyncio.get_event_loop().create_task(registrar.incoming(packet.payload.sequence_number, packet))
        elif isinstance(packet.payload, protocol.Message):
            message = packet.payload.message
            log.debug(f'message: {message}')
            connect = re.compile(r'Player .*connected')
            if connect.match(message):
                parts = message.split()
                status = parts[-1]
                if status == 'disconnected':
                    name = ' '.join(parts[2:-1])
                else:
                    name = ' '.join(parts[2:-2])
                login_message = f'{name} {status}'
                log.info(f'login event {login_message}')
                if config.get().log_connect_disconnect_notices:
                    asyncio.get_event_loop().create_task(put_in_queue(chat_queue, login_message))
            chat = re.compile(r'^\(Global\).*:.*')
            if chat.match(message):
                _, _, content = message.partition(' ')
                asyncio.get_event_loop().create_task(put_in_queue(chat_queue, content))
            if len(message) > 0:
                asyncio.get_event_loop().create_task(put_in_queue(event_queue, message))
            return generate_ack(packet.payload.sequence_number)
    return None


async def put_in_queue(queue, item):
    await queue.put(item)


def generate_login(password):
    return protocol.Packet(protocol.Login(password=password)).generate()


def generate_ack(received_sequence_number):
    return protocol.Packet(protocol.Message(received_sequence_number)).generate()


class RConProtocol(asyncio.DatagramProtocol):
    def __init__(self, future_queue, event_queue, chat_queue):
        self.transport = None
        self.future_queue = future_queue
        self.event_queue = event_queue
        self.chat_queue = chat_queue
        super().__init__()

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport
        data = generate_login(config.get().password)
        self.send_rcon_datagram(data)

    def datagram_received(self, data, addr):
        log.debug(f'received {data}')
        packet = protocol.Packet.parse(data)
        if packet is not None:
            response = process_packet(packet, self.event_queue, self.chat_queue)
            if response is not None:
                log.debug(f'responding {response}')
                self.send_rcon_datagram(response)

    def send_rcon_datagram(self, data):
        log.debug(f'sending {data}')
        self.transport.sendto(data)


async def process_futures(future_queue, rcon_protocol):
    while True:
        future, command = await future_queue.get()
        log.info(f'command received: {command}')
        if command == 'commands':
            future.set_result(VALID_COMMANDS)
        elif command.split()[0] in VALID_COMMANDS:
            seq_number = await registrar.get_next_sequence_number()
            packet = protocol.Packet(protocol.Command(seq_number, command=command))
            command_future = asyncio.get_running_loop().create_future()
            await registrar.register(packet.payload.sequence_number, command_future)
            rcon_protocol.send_rcon_datagram(packet.generate())
            try:
                await command_future
                future.set_result(command_future.result().payload.data)
            except asyncio.CancelledError:
                future.cancel()
        else:
            future.set_result('invalid command')


class ProtocolFactory:
    def __init__(self, future_queue, event_queue, chat_queue):
        self.future_queue = future_queue
        self.event_queue = event_queue
        self.chat_queue = chat_queue

    def get(self) -> RConProtocol:
        return RConProtocol(self.future_queue, self.event_queue, self.chat_queue)


async def start(future_queue, event_queue, chat_queue):
    loop = asyncio.get_running_loop()
    factory = ProtocolFactory(future_queue, event_queue, chat_queue)
    loop.create_task(keep_alive(factory))


async def keep_alive(factory):
    loop = asyncio.get_running_loop()
    while True:
        await registrar.reset()
        transport, rcon_protocol = await loop.create_datagram_endpoint(factory.get,
                                                                       remote_addr=(config.get().ip, config.get().port))
        task = loop.create_task(process_futures(factory.future_queue, rcon_protocol))
        rcon_protocol: RConProtocol = rcon_protocol
        while True:
            await asyncio.sleep(config.get().rcon_keep_alive_interval)
            seq_number = await registrar.get_next_sequence_number()
            packet = protocol.Packet(protocol.Command(seq_number))
            future = asyncio.get_running_loop().create_future()
            await registrar.register(packet.payload.sequence_number, future)
            rcon_protocol.send_rcon_datagram(packet.generate())
            try:
                await future
                if config.get().log_rcon_keep_alive:
                    asyncio.get_event_loop().create_task(put_in_queue(factory.event_queue, 'keep alive'))
            except asyncio.CancelledError:
                log.warning('keep alive timed out')
                await factory.event_queue.put('keep alive timed out')
                task.cancel()
                transport.close()
                break
