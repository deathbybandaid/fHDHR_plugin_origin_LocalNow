import json


class Plugin_OBJ():

    def __init__(self, plugin_utils):
        self.plugin_utils = plugin_utils

        self.base_api = 'https://localnow.com/api/dsp/live/epg'
        self.stream_url_post = "https://localnow.com/api/ln/get-video"
        self.creds = self.get_creds()

    @property
    def tuners(self):
        return self.plugin_utils.config.dict["localnow"]["tuners"]

    @property
    def stream_method(self):
        return self.plugin_utils.config.dict["localnow"]["stream_method"]

    def get_creds(self):
        creds = {}
        cookies = self.plugin_utils.web.session.get("https://localnow.com/channels/newsy").cookies.get_dict()
        creds["guid"] = cookies["_ln_guid"]

        self.plugin_utils.web.session.options("https://prod.localnowapi.com/gis/api/v1/City/Search?Text=%s" % self.postalcode).json()
        location_json = self.plugin_utils.web.session.get("https://prod.localnowapi.com/gis/api/v1/City/Search?Text=%s" % self.postalcode).json()
        print(location_json)

        return creds

    @property
    def postalcode(self):
        if self.plugin_utils.config.dict["localnow"]["postalcode"]:
            return self.plugin_utils.config.dict["localnow"]["postalcode"]
        try:
            postalcode_url = 'http://ipinfo.io/json'
            postalcode_req = self.plugin_utils.web.session.get(postalcode_url)
            data = postalcode_req.json()
            postalcode = data["postal"]
        except Exception as e:
            self.plugin_utils.logger.info("Unable to automatically optain postalcode: %s" % e)
            postalcode = None
        return postalcode

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

        try:
            channel_stream_json = self.plugin_utils.web.session.post(self.stream_url_post, data=json.dumps(channel_post)).json()
        except json.JSONDecodeError as err:
            print(err)
            return None
        print(channel_stream_json)

        streamurl = channel_stream_json['url']

        stream_info = {"url": streamurl}

        return stream_info

    def get_channel_dict(self, chanlist, keyfind, valfind):
        return next(item for item in chanlist if item[keyfind] == valfind)
