import json
import logging

log = logging.getLogger(__name__)


class Config:
    def __init__(self, token, ip, port, password, publish_channel_id, admin_channels, chat_channel_id,
                 count_channel_id, update_player_count_interval, rcon_keep_alive_interval,
                 log_connect_disconnect_notices, log_player_count_updates, log_rcon_messages, log_rcon_keep_alive,
                 include_timestamp, debug):
        self.token = token
        self.ip = ip
        self.port = port
        self.password = password
        self.publish_channel_id = publish_channel_id
        self.admin_channels = admin_channels
        self.chat_channel_id = chat_channel_id
        self.count_channel_id = count_channel_id
        self.update_player_count_interval = update_player_count_interval
        self.rcon_keep_alive_interval = rcon_keep_alive_interval
        self.log_connect_disconnect_notices = log_connect_disconnect_notices
        self.log_player_count_updates = log_player_count_updates
        self.log_rcon_messages = log_rcon_messages
        self.log_rcon_keep_alive = log_rcon_keep_alive
        self.include_timestamp = include_timestamp
        self.debug = debug

    @staticmethod
    def build_from(file_path):
        with open(file_path) as f:
            config = json.load(f)

        token = config['token']
        ip = config['rcon_ip']
        port = config['rcon_port']
        password = config['rcon_password']
        publish_channel_id = config.get('rcon_admin_log_channel')
        if publish_channel_id is None:
            publish_channel_id = config.get('rcon_publish_channel')
            if publish_channel_id is not None:
                log.warning('carim.json rcon_publish_channel is deprecated, use rcon_admin_log_channel instead')

        admin_channels = config.get('rcon_admin_channels', list())
        chat_channel_id = config.get('rcon_chat_channel')
        count_channel_id = config.get('rcon_count_channel')
        update_player_count_interval = config.get('update_player_count_interval', 300)
        rcon_keep_alive_interval = config.get('rcon_keep_alive_interval', 30)

        discord_logging_verbosity = config.get('log_events_in_discord', dict())

        log_connect_disconnect_notices = discord_logging_verbosity.get('connect_disconnect_notices', True)
        log_player_count_updates = discord_logging_verbosity.get('player_count_updates', True)
        log_rcon_messages = discord_logging_verbosity.get('rcon_messages', True)
        log_rcon_keep_alive = discord_logging_verbosity.get('rcon_keep_alive', True)
        include_timestamp = discord_logging_verbosity.get('include_timestamp', True)

        debug = config.get('debug', False)

        return Config(token, ip, port, password, publish_channel_id, admin_channels, chat_channel_id, count_channel_id,
                      update_player_count_interval, rcon_keep_alive_interval, log_connect_disconnect_notices,
                      log_player_count_updates, log_rcon_messages, log_rcon_keep_alive, include_timestamp, debug)


_config: Config = None


def get() -> Config:
    return _config


def set(config):
    global _config
    _config = config
