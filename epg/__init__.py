

class Plugin_OBJ():

    def __init__(self, channels, plugin_utils):
        self.plugin_utils = plugin_utils

        self.channels = channels

        self.origin = plugin_utils.origin
        self.base_api = 'https://localnow.com/api/dsp/live/epg'

    def update_epg(self):
        programguide = {}

        channels_json = self.plugin_utils.web.session.get(self.base_api).json()["data"]["channels"]
        for channel_dict in channels_json:

            chan_obj = self.channels.get_channel_obj("origin_id", channel_dict["id"], self.plugin_utils.namespace)

        return programguide
