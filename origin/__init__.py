import json


class Plugin_OBJ():

    def __init__(self, plugin_utils):
        self.plugin_utils = plugin_utils

        self.base_api = 'https://localnow.com/api/dsp/live/epg'
        self.stream_url_post = "https://localnow.com/api/ln/get-video"
        self.cookie = self.get_cookie()

    def get_cookie(self):
        cookies = self.plugin_utils.web.session.get("https://localnow.com/channels/newsy").cookies
        for cookie in cookies:
            print(cookie)

    def get_channels(self):

        channel_list = []

        channels_json = self.plugin_utils.web.session.get(self.base_api).json()["data"]["channels"]
        for channel_dict in channels_json:

            clean_station_item = {
                                 "name": channel_dict["name"],
                                 "callsign": channel_dict["slug"],
                                 "id": channel_dict["id"],
                                 "thumbnail": channel_dict["logo"],
                                 }
            channel_list.append(clean_station_item)

        return channel_list

    def get_channel_stream(self, chandict, stream_args):

        channels_json = self.plugin_utils.web.session.get(self.base_api).json()["data"]["channels"]
        origin_chandict = self.get_channel_dict(channels_json, "id", chandict["origin_id"])

        channel_post = {
                        "playback": {
                                    "url": "https://prod.localnowapi.com/vod/api/v2/Video/GetPlayback",
                                    "AssetId": "miMarquette_WeatherToday",
                                    "Version": 1612205496
                                    }
                        }

        channel_stream_json = self.plugin_utils.web.session.post(self.stream_url_post, data=json.dumps(channel_post)).json()
        print(channel_stream_json)

        streamurl = channel_stream_json['url']

        stream_info = {"url": streamurl}

        return stream_info

    def get_channel_dict(self, chanlist, keyfind, valfind):
        return next(item for item in chanlist if item[keyfind] == valfind)
