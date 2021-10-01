class Episode:
    def __init__(self, data):
        self.id = data['id']
        self.season = data['airedSeason']
        self.episode_number = data['airedEpisodeNumber']
        self.episode_name = data['episodeName']
        self.air_date = data['firstAired']
        self.overview = data['overview']