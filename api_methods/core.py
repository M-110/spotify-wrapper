
    def get_multiple_albums(self, ids: List[str], market: str = None) -> Union[List[Optional[AlbumObject]], ErrorObject]:
        """
        Get Spotify catalog information for multiple albums identified by their
    Spotify IDs.

    Args:
        ids: A list of strings of the Spotify IDs for the albums. Maximum: 20
          IDs.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/albums'
        query_params = {'ids': ids, 'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, AlbumObject)
    
    def get_an_album(self, id_: str, market: str = None) -> Union[Optional[AlbumObject], ErrorObject]:
        """
        Get Spotify catalog information for a single album.

    Args:
        id_: The Spotify ID of the album.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/albums/{id_}'
        query_params = {'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return AlbumObject(response.text)
    
    def get_an_albums_tracks(self, id_: str, market: str = None, limit: int = None, offset: int = None) -> Union[Optional[AlbumObject], ErrorObject]:
        """
        Get Spotify catalog information about an album’s tracks. Optional
    parameters can be used to limit the number of tracks returned.

    Args:
        id_: The Spotify ID of the album.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        limit: Optional; The maximum number of tracks to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first track to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/albums/{id_}/tracks'
        query_params = {'market': market, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return AlbumObject(response.text)
    
    def get_multiple_artists(self, ids: List[str]) -> List[Optional[ArtistObject]]:
        """
        Get Spotify catalog information for several artists based on their Spotify
    IDs.

    Args:
        ids: A list of strings of the Spotify IDs for the artists. Maximum: 50
          IDs.
        """
        url = f'https://api.spotify.com/v1/artists'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, ArtistObject)
    
    def get_an_artist(self, id_: str) -> Union[ArtistObject, ErrorObject]:
        """
        Get Spotify catalog information for a single artist identified by their
    unique Spotify ID.

    Args:
        id_: The Spotify ID of the artist.
        """
        url = f'https://api.spotify.com/v1/artists/{id_}'
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ArtistObject(response.text)
    
    def get_an_artists_top_tracks(self, id_: str, market: str) -> Union[List[TrackObject], ErrorObject]:
        """
        Get Spotify catalog information about an artist’s top tracks by country.

    Args:
        id_: The Spotify ID of the artist.
        market: An ISO 3166-1 alpha-2 country code or the string 'from_token'.
        """
        url = f'https://api.spotify.com/v1/artists/{id}/top-tracks'
        query_params = {'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, TrackObject)
    
    def get_an_artists_related_artists(self, id_: str) -> Union[List[ArtistObject], ErrorObject]:
        """
        Get Spotify catalog information about artists similar to a given artist.
    Similarity is based on analysis of the Spotify community’s listening
    history.

    Args:
        id_: The Spotify ID of the artist.
        """
        url = f'https://api.spotify.com/v1/artists/{id}/related-artists'
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, ArtistObject)
    
    def get_an_artists_albums(self, id_: str, include_groups: List[str] = None, market: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[SimplifiedAlbumObject], ErrorObject]:
        """
        Get Spotify catalog information about an artist’s albums.

    Args:
        id_: The Spotify ID of the artist.
        include_groups: Optional; A list of strings of the keywords that will
          be used to filter the response. If not supplied, all album types
          will be returned. Valid keywords are 'album', 'single',
          'appears_on', and 'compilation'.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        limit: Optional; The maximum number of albums to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first album to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/artists/{id}/albums'
        query_params = {'include_groups': include_groups, 'market': market, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
    def get_all_new_releases(self, country: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[SimplifiedAlbumObject], ErrorObject]:
        """
        Get a list of new album releases featured in Spotify (shown, for example,
    on a Spotify player’s “Browse” tab).

    Args:
        country: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        limit: Optional; The maximum number of albums to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first album to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/browse/new-releases'
        query_params = {'country': country, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
    def get_all_featured_playlists(self, country: str = None, locale: str = None, timestamp: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[SimplifiedPlaylistObject], ErrorObject]:
        """
        Get a list of Spotify featured playlists (shown, for example, on a Spotify
    player’s ‘Browse’ tab).

    Args:
        country: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        locale: Optional; The desired language, consisting of a lowercase ISO
          639-1 language code and an uppercase ISO 3166-1 alpha-2 country
          code, joined by an underscore. For example: es_MX, meaning “Spanish
          (Mexico)”. Provide this parameter if you want the results returned
          in a particular language (where available). Note that, if locale is
          not supplied, or if the specified language is not available, all
          strings will be returned in the Spotify default language (American
          English). The locale parameter, combined with the country parameter,
          may give odd results if not carefully matched.
        timestamp: Optional; A timestamp in ISO 8601 format: yyyy-MM-
          ddTHH:mm:ss. Use this parameter to specify the user’s local time to
          get results tailored for that specific date and time in the day. If
          not provided, the response defaults to the current UTC time.
          Example: “2014-10-23T09:00:00” for a user whose local time is 9AM.
          If there were no featured playlists (or there is no data) at the
          specified time, the response will revert to the current UTC time.
        limit: Optional; The maximum number of albums to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first album to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/browse/featured-playlists'
        query_params = {'country': country, 'locale': locale, 'timestamp': timestamp, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
    def get_all_categories(self, country: str = None, locale: str = None, timestamp: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[CategoryObject], ErrorObject]:
        """
        Get a list of categories used to tag items in Spotify (on, for example,
    the Spotify player’s “Browse” tab).

    Args:
        country: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        locale: Optional; The desired language, consisting of a lowercase ISO
          639-1 language code and an uppercase ISO 3166-1 alpha-2 country
          code, joined by an underscore. For example: es_MX, meaning “Spanish
          (Mexico)”. Provide this parameter if you want the results returned
          in a particular language (where available). Note that, if locale is
          not supplied, or if the specified language is not available, all
          strings will be returned in the Spotify default language (American
          English). The locale parameter, combined with the country parameter,
          may give odd results if not carefully matched.
        timestamp: Optional; A timestamp in ISO 8601 format: yyyy-MM-
          ddTHH:mm:ss. Use this parameter to specify the user’s local time to
          get results tailored for that specific date and time in the day. If
          not provided, the response defaults to the current UTC time.
          Example: “2014-10-23T09:00:00” for a user whose local time is 9AM.
          If there were no featured playlists (or there is no data) at the
          specified time, the response will revert to the current UTC time.
        limit: Optional; The maximum number of albums to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first category to return. Default:
          0.
        """
        url = f'https://api.spotify.com/v1/browse/categories'
        query_params = {'country': country, 'locale': locale, 'timestamp': timestamp, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
    def get_a_category(self, category_id: str, country: str = None, locale: str = None) -> Union[CategoryObject, ErrorObject]:
        """
        Get a single category used to tag items in Spotify (on, for example, the
    Spotify player’s “Browse” tab).

    Args:
        category_id: The Spotify category ID for the category.
        country: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        locale: Optional; The desired language, consisting of a lowercase ISO
          639-1 language code and an uppercase ISO 3166-1 alpha-2 country
          code, joined by an underscore. For example: es_MX, meaning “Spanish
          (Mexico)”. Provide this parameter if you want the results returned
          in a particular language (where available). Note that, if locale is
          not supplied, or if the specified language is not available, all
          strings will be returned in the Spotify default language (American
          English). The locale parameter, combined with the country parameter,
          may give odd results if not carefully matched.
        """
        url = f'https://api.spotify.com/v1/browse/categories/{category_id}'
        query_params = {'country': country, 'locale': locale}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return CategoryObject(response.text)
    
    def get_a_categorys_playlists(self, category_id: str, country: str = None, locale: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[SimplifiedPlaylistObject], ErrorObject]:
        """
        Get a list of Spotify playlists tagged with a particular category.

    Args:
        category_id: The Spotify category ID for the category.
        country: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        locale: Optional; The desired language, consisting of a lowercase ISO
          639-1 language code and an uppercase ISO 3166-1 alpha-2 country
          code, joined by an underscore. For example: es_MX, meaning “Spanish
          (Mexico)”. Provide this parameter if you want the results returned
          in a particular language (where available). Note that, if locale is
          not supplied, or if the specified language is not available, all
          strings will be returned in the Spotify default language (American
          English). The locale parameter, combined with the country parameter,
          may give odd results if not carefully matched.
        limit: Optional; The maximum number of albums to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first playlist to return. Default:
          0.
        """
        url = f'https://api.spotify.com/v1/browse/categories/{category_id}/playlists'
        query_params = {'country': country, 'locale': locale, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
    def get_recommendations(self, seed_artists: List[str], seed_genres: List[str], seed_tracks: List[str], limit: int = None, market: str = None, min_acousticness: float = None, max_acousticness: float = None, target_acousticness: float = None, min_danceability: float = None, max_danceability: float = None, target_danceability: float = None, min_duration_ms: int = None, max_duration_ms: int = None, target_duration_ms: int = None, min_energy: float = None, max_energy: float = None, target_energy: float = None, min_instrumentalness: float = None, max_instrumentalness: float = None, target_instrumentalness: float = None, min_key: int = None, max_key: int = None, target_key: int = None, min_liveness: float = None, max_liveness: float = None, target_liveness: float = None, min_loudness: float = None, max_loudness: float = None, target_loudness: float = None, min_mode: int = None, max_mode: int = None, target_mode: int = None, min_popularity: int = None, max_popularity: int = None, target_popularity: int = None, min_speechiness: float = None, max_speechiness: float = None, target_speechiness: float = None, min_tempo: float = None, max_tempo: float = None, target_tempo: float = None, min_time_signature: int = None, max_time_signature: int = None, target_time_signature: int = None, min_valence: float = None, max_valence: float = None, target_valence: float = None) -> Union[RecommendationsObject, ErrorObject]:
        """
        Recommendations are generated based on the available information for a
    given seed entity and matched against similar artists and tracks. If there
    is sufficient information about the provided seeds, a list of tracks will
    be returned together with pool size details.

    Args:
        seed_artists: A list of strings of Spotify IDs for seed artists. Up to
          5 seed values may be provided in any combination of seed_artists,
          seed_tracks and seed_genres.
        seed_genres: A list of strings of Spotify IDs for seed genres. Up to 5
          seed values may be provided in any combination of seed_artists,
          seed_tracks and seed_genres.
        seed_tracks: A list of strings of Spotify IDs for seed tracks. Up to 5
          seed values may be provided in any combination of seed_artists,
          seed_tracks and seed_genres.
        limit: Optional; The target size of the list of recommended tracks.
          For seeds with unusually small pools or when highly restrictive
          filtering is applied, it may be impossible to generate the requested
          number of recommended tracks. Debugging information for such cases
          is available in the response. Default: 20. Minimum: 1. Maximum: 100.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          from_token. Provide this parameter if you want to apply Track
          Relinking. Because min_*, max_* and target_* are applied to pools
          before relinking, the generated results may not precisely match the
          filters applied. Original, non-relinked tracks are available via the
          linked_from attribute of the relinked track response.
        min_acousticness: Optional; Restricts results to tracks with attribute
          greater than min. Acousticness is a confidence measure from 0.0 to
          1.0 of whether the track is acoustic. 1.0 represents high confidence
          the track is acoustic.
        max_acousticness: Optional; Restricts results to tracks with attribute
          less than max. Acousticness is a confidence measure from 0.0 to 1.0
          of whether the track is acoustic. 1.0 represents high confidence the
          track is acoustic.
        target_acousticness: Optional; Tracks near target attribute will be
          preferred. Acousticness is a confidence measure from 0.0 to 1.0 of
          whether the track is acoustic. 1.0 represents high confidence the
          track is acoustic.
        min_danceability: Optional; Restricts results to tracks with attribute
          greater than min. Danceability describes how suitable a track is for
          dancing based on a combination of musical elements including tempo,
          rhythm stability, beat strength, and overall regularity. A value of
          0.0 is least danceable and 1.0 is most danceable.
        max_danceability: Optional; Restricts results to tracks with attribute
          less than max. Danceability describes how suitable a track is for
          dancing based on a combination of musical elements including tempo,
          rhythm stability, beat strength, and overall regularity. A value of
          0.0 is least danceable and 1.0 is most danceable.
        target_danceability: Optional; Tracks near target attribute will be
          preferred. Danceability describes how suitable a track is for
          dancing based on a combination of musical elements including tempo,
          rhythm stability, beat strength, and overall regularity. A value of
          0.0 is least danceable and 1.0 is most danceable.
        min_duration_ms: Optional; Restricts results to tracks with duration
          greater than min duration (in milliseconds).
        max_duration_ms: Optional; Restricts results to tracks with duration
          less than max duration (in milliseconds).
        target_duration_ms: Optional; Tracks near target duration will be
          preferred (in milliseconds).
        min_energy: Optional; Restricts results to tracks with attribute
          greater than min. Energy is a measure from 0.0 to 1.0 and represents
          a perceptual measure of intensity and activity. Typically, energetic
          tracks feel fast, loud, and noisy. For example, death metal has high
          energy, while a Bach prelude scores low on the scale. Perceptual
          features contributing to this attribute include dynamic range,
          perceived loudness, timbre, onset rate, and general entropy.
        max_energy: Optional; Restricts results to tracks with attribute less
          than max. Energy is a measure from 0.0 to 1.0 and represents a
          perceptual measure of intensity and activity. Typically, energetic
          tracks feel fast, loud, and noisy. For example, death metal has high
          energy, while a Bach prelude scores low on the scale. Perceptual
          features contributing to this attribute include dynamic range,
          perceived loudness, timbre, onset rate, and general entropy.
        target_energy: Optional; Tracks near target attribute will be
          preferred. Energy is a measure from 0.0 to 1.0 and represents a
          perceptual measure of intensity and activity. Typically, energetic
          tracks feel fast, loud, and noisy. For example, death metal has high
          energy, while a Bach prelude scores low on the scale. Perceptual
          features contributing to this attribute include dynamic range,
          perceived loudness, timbre, onset rate, and general entropy.
        min_instrumentalness: Optional; Restricts results to tracks with
          attribute greater than min. Predicts whether a track contains no
          vocals. “Ooh” and “aah” sounds are treated as instrumental in this
          context. Rap or spoken word tracks are clearly “vocal”. The closer
          the instrumentalness value is to 1.0, the greater likelihood the
          track contains no vocal content. Values above 0.5 are intended to
          represent instrumental tracks, but confidence is higher as the value
          approaches 1.0.
        max_instrumentalness: Optional; Restricts results to tracks with
          attribute less than max. Predicts whether a track contains no
          vocals. “Ooh” and “aah” sounds are treated as instrumental in this
          context. Rap or spoken word tracks are clearly “vocal”. The closer
          the instrumentalness value is to 1.0, the greater likelihood the
          track contains no vocal content. Values above 0.5 are intended to
          represent instrumental tracks, but confidence is higher as the value
          approaches 1.0.
        target_instrumentalness: Optional; Tracks near target attribute will
          be preferred. Predicts whether a track contains no vocals. “Ooh” and
          “aah” sounds are treated as instrumental in this context. Rap or
          spoken word tracks are clearly “vocal”. The closer the
          instrumentalness value is to 1.0, the greater likelihood the track
          contains no vocal content. Values above 0.5 are intended to
          represent instrumental tracks, but confidence is higher as the value
          approaches 1.0.
        min_key: Optional; Restricts results to tracks with attribute greater
          than min. The key the track is in. Integers map to pitches using
          standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so
          on.
        max_key: Optional; Restricts results to tracks with attribute less
          than max. The key the track is in. Integers map to pitches using
          standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so
          on.
        target_key: Optional; Tracks near target attribute will be preferred.
          The key the track is in. Integers map to pitches using standard
          Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
        min_liveness: Optional; Restricts results to tracks with attribute
          greater than min. Detects the presence of an audience in the
          recording. Higher liveness values represent an increased probability
          that the track was performed live. A value above 0.8 provides strong
          likelihood that the track is live.
        max_liveness: Optional; Restricts results to tracks with attribute
          less than max. Detects the presence of an audience in the recording.
          Higher liveness values represent an increased probability that the
          track was performed live. A value above 0.8 provides strong
          likelihood that the track is live.
        target_liveness: Optional; Tracks near target attribute will be
          preferred. Detects the presence of an audience in the recording.
          Higher liveness values represent an increased probability that the
          track was performed live. A value above 0.8 provides strong
          likelihood that the track is live.
        min_loudness: Optional; Restricts results to tracks with attribute
          greater than min. The overall loudness of a track in decibels (dB).
          Loudness values are averaged across the entire track and are useful
          for comparing relative loudness of tracks. Loudness is the quality
          of a sound that is the primary psychological correlate of physical
          strength (amplitude). Values typical range between -60 and 0 db.
        max_loudness: Optional; Restricts results to tracks with attribute
          less than max. The overall loudness of a track in decibels (dB).
          Loudness values are averaged across the entire track and are useful
          for comparing relative loudness of tracks. Loudness is the quality
          of a sound that is the primary psychological correlate of physical
          strength (amplitude). Values typical range between -60 and 0 db.
        target_loudness: Optional; Tracks near target attribute will be
          preferred. The overall loudness of a track in decibels (dB).
          Loudness values are averaged across the entire track and are useful
          for comparing relative loudness of tracks. Loudness is the quality
          of a sound that is the primary psychological correlate of physical
          strength (amplitude). Values typical range between -60 and 0 db.
        min_mode: Optional; Restricts results to tracks with attribute greater
          than min. Mode indicates the modality (major or minor) of a track,
          the type of scale from which its melodic content is derived. Major
          is represented by 1 and minor is 0.
        max_mode: Optional; Restricts results to tracks with attribute less
          than max. Mode indicates the modality (major or minor) of a track,
          the type of scale from which its melodic content is derived. Major
          is represented by 1 and minor is 0.
        target_mode: Optional; Tracks near target attribute will be preferred.
          Mode indicates the modality (major or minor) of a track, the type of
          scale from which its melodic content is derived. Major is
          represented by 1 and minor is 0.
        min_popularity: Optional; Restricts results to tracks with attribute
          greater than min. The popularity of the track. The value will be
          between 0 and 100, with 100 being the most popular. The popularity
          is calculated by algorithm and is based, in the most part, on the
          total number of plays the track has had and how recent those plays
          are.
        max_popularity: Optional; Restricts results to tracks with attribute
          less than max. The popularity of the track. The value will be
          between 0 and 100, with 100 being the most popular. The popularity
          is calculated by algorithm and is based, in the most part, on the
          total number of plays the track has had and how recent those plays
          are.
        target_popularity: Optional; Tracks near target attribute will be
          preferred. The popularity of the track. The value will be between 0
          and 100, with 100 being the most popular. The popularity is
          calculated by algorithm and is based, in the most part, on the total
          number of plays the track has had and how recent those plays are.
        min_speechiness: Optional; Restricts results to tracks with attribute
          greater than min. Speechiness detects the presence of spoken words
          in a track. The more exclusively speech-like the recording (e.g.
          talk show, audio book, poetry), the closer to 1.0 the attribute
          value. Values above 0.66 describe tracks that are probably made
          entirely of spoken words. Values between 0.33 and 0.66 describe
          tracks that may contain both music and speech, either in sections or
          layered, including such cases as rap music. Values below 0.33 most
          likely represent music and other non-speech-like tracks.
        max_speechiness: Optional; Restricts results to tracks with attribute
          less than max. Speechiness detects the presence of spoken words in a
          track. The more exclusively speech-like the recording (e.g. talk
          show, audio book, poetry), the closer to 1.0 the attribute value.
          Values above 0.66 describe tracks that are probably made entirely of
          spoken words. Values between 0.33 and 0.66 describe tracks that may
          contain both music and speech, either in sections or layered,
          including such cases as rap music. Values below 0.33 most likely
          represent music and other non-speech-like tracks.
        target_speechiness: Optional; Tracks near target attribute will be
          preferred. Speechiness detects the presence of spoken words in a
          track. The more exclusively speech-like the recording (e.g. talk
          show, audio book, poetry), the closer to 1.0 the attribute value.
          Values above 0.66 describe tracks that are probably made entirely of
          spoken words. Values between 0.33 and 0.66 describe tracks that may
          contain both music and speech, either in sections or layered,
          including such cases as rap music. Values below 0.33 most likely
          represent music and other non-speech-like tracks.
        min_tempo: Optional; Restricts results to tracks with attribute
          greater than min. The overall estimated tempo of a track in beats
          per minute (BPM). In musical terminology, tempo is the speed or pace
          of a given piece and derives directly from the average beat
          duration.
        max_tempo: Optional; Restricts results to tracks with attribute less
          than max. The overall estimated tempo of a track in beats per minute
          (BPM). In musical terminology, tempo is the speed or pace of a given
          piece and derives directly from the average beat duration.
        target_tempo: Optional; Tracks near target attribute will be
          preferred. The overall estimated tempo of a track in beats per
          minute (BPM). In musical terminology, tempo is the speed or pace of
          a given piece and derives directly from the average beat duration.
        min_time_signature: Optional; Restricts results to tracks with
          attribute greater than min. An estimated overall time signature of a
          track. The time signature (meter) is a notational convention to
          specify how many beats are in each bar (or measure).
        max_time_signature: Optional; Restricts results to tracks with
          attribute less than max. An estimated overall time signature of a
          track. The time signature (meter) is a notational convention to
          specify how many beats are in each bar (or measure).
        target_time_signature: Optional; Tracks near target attribute will be
          preferred. An estimated overall time signature of a track. The time
          signature (meter) is a notational convention to specify how many
          beats are in each bar (or measure).
        min_valence: Optional; Restricts results to tracks with attribute
          greater than min. A measure from 0.0 to 1.0 describing the musical
          positiveness conveyed by a track. Tracks with high valence sound
          more positive (e.g. happy, cheerful, euphoric), while tracks with
          low valence sound more negative (e.g. sad, depressed, angry).
        max_valence: Optional; Restricts results to tracks with attribute less
          than max. A measure from 0.0 to 1.0 describing the musical
          positiveness conveyed by a track. Tracks with high valence sound
          more positive (e.g. happy, cheerful, euphoric), while tracks with
          low valence sound more negative (e.g. sad, depressed, angry).
        target_valence: Optional; Tracks near target attribute will be
          preferred. A measure from 0.0 to 1.0 describing the musical
          positiveness conveyed by a track. Tracks with high valence sound
          more positive (e.g. happy, cheerful, euphoric), while tracks with
          low valence sound more negative (e.g. sad, depressed, angry).
        """
        url = f'https://api.spotify.com/v1/recommendations'
        query_params = {'seed_artists': seed_artists, 'seed_genres': seed_genres, 'seed_tracks': seed_tracks, 'limit': limit, 'market': market, 'min_acousticness': min_acousticness, 'max_acousticness': max_acousticness, 'target_acousticness': target_acousticness, 'min_danceability': min_danceability, 'max_danceability': max_danceability, 'target_danceability': target_danceability, 'min_duration_ms': min_duration_ms, 'max_duration_ms': max_duration_ms, 'target_duration_ms': target_duration_ms, 'min_energy': min_energy, 'max_energy': max_energy, 'target_energy': target_energy, 'min_instrumentalness': min_instrumentalness, 'max_instrumentalness': max_instrumentalness, 'target_instrumentalness': target_instrumentalness, 'min_key': min_key, 'max_key': max_key, 'target_key': target_key, 'min_liveness': min_liveness, 'max_liveness': max_liveness, 'target_liveness': target_liveness, 'min_loudness': min_loudness, 'max_loudness': max_loudness, 'target_loudness': target_loudness, 'min_mode': min_mode, 'max_mode': max_mode, 'target_mode': target_mode, 'min_popularity': min_popularity, 'max_popularity': max_popularity, 'target_popularity': target_popularity, 'min_speechiness': min_speechiness, 'max_speechiness': max_speechiness, 'target_speechiness': target_speechiness, 'min_tempo': min_tempo, 'max_tempo': max_tempo, 'target_tempo': target_tempo, 'min_time_signature': min_time_signature, 'max_time_signature': max_time_signature, 'target_time_signature': target_time_signature, 'min_valence': min_valence, 'max_valence': max_valence, 'target_valence': target_valence}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return RecommendationsObject(response.text)
    
    def get_recommendation_genres(self) -> Union[RecommendationsObject, ErrorObject]:
        """
        Retrieve a list of available genres seed parameter values for
    recommendations.
        """
        url = f'https://api.spotify.com/v1/recommendations/available-genre-seeds'
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return RecommendationsObject(response.text)
    
    def get_multiple_episodes(self, ids: List[str], market: str = None) -> Union[List[Optional[EpisodeObject]], ErrorObject]:
        """
        Get Spotify catalog information for several episodes based on their
    Spotify IDs.

    Args:
        ids: A list of strings of the Spotify IDs for the episodes. Maximum:
          50 IDs.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/episodes'
        query_params = {'ids': ids, 'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, EpisodeObject)
    
    def get_an_episode(self, id_: str, market: str = None) -> Union[EpisodeObject, ErrorObject]:
        """
        Get Spotify catalog information for a single episode identified by its
    unique Spotify ID.

    Args:
        id_: The Spotify ID of the episode.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/episodes/{id_}'
        query_params = {'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return EpisodeObject(response.text)
    
@requires('user-follow-modify', 'playlist-modify-private')
    def follow_a_playlist(self, playlist_id: str, public: bool) -> Optional[ErrorObject]:
        """
        Add the current user as a follower of a playlist.

    Args:
        playlist_id: The Spotify ID of the playlist. Any playlist can be
          followed, regardless of its public/private status, as long as you
          know its playlist ID.
        public: If True the playlist will be included in user’s public
          playlists, if False it will remain private. Defaults to True.
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/followers'
        query_params = {}
        json_body = {'public': public}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('playlist-modify-public', 'playlist-modify-private')
    def unfollow_playlist(self, playlist_id: str) -> Optional[ErrorObject]:
        """
        Remove the current user as a follower of a playlist.

    Args:
        playlist_id: The Spotify ID of the playlist to be unfollowed.
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/followers'
        query_params = {}
        json_body = {}
        response, error = self._delete(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('playlist-read-private')
    def check_if_users_follow_a_playlist(self, playlist_id: str, ids: List[str]) -> Union[List[bool], ErrorObject]:
        """
        Check to see if one or more Spotify users are following a specified
    playlist.

    Args:
        playlist_id: The Spotify ID of the playlist.
        ids: A list of strings of Spotify User IDs; the ids of the users you
          want to check to see if they follow the playlist. Maximum: 5 ids.
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/followers/contains'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, ErrorObject)
    
@requires('user-follow-modify')
    def get_users_followed_artists(self, type_: str, after: str = None, limit: int = None) -> Union[PagingObject[ArtistObject], ErrorObject]:
        """
        Get the current user’s followed artists.

    Args:
        type_: The ID type: currently only 'artist' is supported.
        after: Optional; The last artist ID retrieved from the previous
          request.
        limit: Optional; The maximum number of artists to return.  Default:
          20. Minimum: 1. Maximum: 50.
        """
        url = f'https://api.spotify.com/v1/me/following'
        query_params = {'type_': type_, 'after': after, 'limit': limit}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
@requires('user-follow-modify')
    def follow_artists_or_users(self, type_: str, ids: List[str]) -> Optional[ErrorObject]:
        """
        Add the current user as a follower of one or more artists or other Spotify
    users.

    Args:
        type_: The ID type: 'artist' or 'user'.
        ids: A list of strings of Spotify IDs of the artists or users to be
          followed. A maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/following'
        query_params = {'type_': type_, 'ids': ids}
        json_body = {}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-follow-modify')
    def unfollow_artists_or_users(self, type_: str, ids: List[str]) -> Optional[ErrorObject]:
        """
        Remove the current user as a follower of one or more artists or other
    Spotify users.

    Args:
        type_: The ID type: 'artist' or 'user'.
        ids: A list of strings of Spotify IDs of the artists or users to be
          unfollowed. A maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/following'
        query_params = {'type_': type_, 'ids': ids}
        json_body = {}
        response, error = self._delete(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-follow-read')
    def get_following_state_for_artists_or_users(self, type_: str, ids: List[str]) -> Union[List[bool], ErrorObject]:
        """
        Check to see if the current user is following one or more artists or other
    Spotify users..

    Args:
        type_: The ID type: 'artist' or 'user'.
        ids: A list of strings of Spotify IDs of the artists or users to be
          checked. A maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/following/contains'
        query_params = {'type_': type_, 'ids': ids}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, ErrorObject)
    
@requires('user-library-read')
    def get_users_saved_albums(self, limit: int = None, offset: int = None, market: str = None) -> Union[PagingObject[SavedAlbumObject], ErrorObject]:
        """
        Get a list of the albums saved in the current Spotify user’s ‘Your Music’
    library.

    Args:
        limit: Optional; The maximum number of albums to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first album to return. Default: 0.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/me/albums'
        query_params = {'limit': limit, 'offset': offset, 'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
@requires('user-library-modify')
    def save_albums_for_current_user(self, ids: List[str]) -> Optional[ErrorObject]:
        """
        Save one or more albums to the current user’s ‘Your Music’ library.

    Args:
        ids: A list of strings of Spotify IDs of the albums to be saved. A
          maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/albums'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-library-modify')
    def remove_albums_for_current_user(self, ids: List[str]) -> Optioanl[ErrorObject]:
        """
        Remove one or more albums from the current user’s ‘Your Music’ library.

    Args:
        ids: A list of strings of Spotify IDs of the albums to be removed. A
          maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/albums'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._delete(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-library-read')
    def check_users_saved_albums(self, ids: List[str]) -> Union[List[bool], ErrorObject]:
        """
        Check if one or more albums is already saved in the current Spotify user’s
    ‘Your Music’ library.

    Args:
        ids: A list of strings of Spotify IDs of the albums to be checked. A
          maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/albums/contains'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, ErrorObject)
    
@requires('user-library-read')
    def get_users_saved_tracks(self, market: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[SavedTrackObject], ErrorObject]:
        """
        Get a list of the songs saved in the current Spotify user’s ‘Your Music’
    library.

    Args:
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        limit: Optional; The maximum number of tracks to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first track to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/me/tracks'
        query_params = {'market': market, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
@requires('user-library-modify')
    def save_tracks_for_users(self, ids: List[str]) -> Optional[ErrorObject]:
        """
        Save one or more tracks to the current user’s ‘Your Music’ library.

    Args:
        ids: A list of strings of Spotify IDs of the tracks to be saved. A
          maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/tracks'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-library-modify')
    def remove_users_saved_tracks(self, ids: List[str]) -> Optional[ErrorObject]:
        """
        Remove one or more tracks from the current user’s ‘Your Music’ library.

    Args:
        ids: A list of strings of Spotify IDs of the tracks to be removed. A
          maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/tracks'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._delete(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-library-read')
    def check_users_saved_tracks(self, ids: List[str]) -> Union[List[bool], ErrorObject]:
        """
        Check if one or more tracks is already saved in the current Spotify user’s
    ‘Your Music’ library.

    Args:
        ids: A list of strings of Spotify IDs of the tracks to be checked. A
          maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/tracks/contains'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, ErrorObject)
    
@requires('user-library-read')
    def get_users_saved_episodes(self, market: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[SavedEpisodeObject], ErrorObject]:
        """
        Get a list of the episodes saved in the current Spotify user’s library.
    (This API endpoint is in beta and could change without warning)

    Args:
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        limit: Optional; The maximum number of episodes to return.  Default:
          20. Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first episode to return. Default:
          0.
        """
        url = f'https://api.spotify.com/v1/me/episodes'
        query_params = {'market': market, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
@requires('user-library-modify')
    def save_tracks_for_users(self, ids: List[str]) -> Optional[ErrorObject]:
        """
        Save one or more episodes to the current user’s library. (This API
    endpoint is in beta and could change without warning)

    Args:
        ids: A list of strings of Spotify IDs of the episodes to be saved. A
          maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/episodes'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-library-modify')
    def remove_users_saved_tracks(self, ids: List[str]) -> Optional[ErrorObject]:
        """
        Remove one or more episodes from the current user’s library. (This API
    endpoint is in beta and could change without warning)

    Args:
        ids: A list of strings of Spotify IDs of the episodes to be removed. A
          maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/episodes'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._delete(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-library-read')
    def check_users_saved_tracks(self, ids: List[str]) -> Union[List[bool], ErrorObject]:
        """
        Check if one or more episodes is already saved in the current Spotify
    user’s ‘Your Episodes’ library. (This API endpoint is in beta and could
    change without warning)

    Args:
        ids: A list of strings of Spotify IDs of the episodes to be checked. A
          maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/episodes/contains'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, ErrorObject)
    
@requires('user-library-read')
    def get_users_saved_shows(self, market: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[SavedShowObject], ErrorObject]:
        """
        Get a list of shows saved in the current Spotify user’s library.

    Args:
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        limit: Optional; The maximum number of shows to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first show to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/me/shows'
        query_params = {'market': market, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
@requires('user-library-modify')
    def save_tracks_for_shows(self, ids: List[str]) -> Optional[ErrorObject]:
        """
        Save one or more shows to current Spotify user’s library.

    Args:
        ids: A list of strings of Spotify IDs of the shows to be saved. A
          maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/shows'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-library-modify')
    def remove_users_saved_shows(self, ids: List[str], market: str = None) -> Optional[ErrorObject]:
        """
        Delete one or more shows from current Spotify user’s library.

    Args:
        ids: A list of strings of Spotify IDs of the shows to be removed. A
          maximum of 50 IDs can be sent in one request.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/me/shows'
        query_params = {'ids': ids, 'market': market}
        json_body = {}
        response, error = self._delete(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-library-read')
    def check_users_saved_shows(self, ids: List[str]) -> Union[List[bool], ErrorObject]:
        """
        Check if one or more shows is already saved in the current Spotify user’s
    library.

    Args:
        ids: A list of strings of Spotify IDs of the shows to be checked. A
          maximum of 50 IDs can be sent in one request.
        """
        url = f'https://api.spotify.com/v1/me/shows/contains'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, ErrorObject)
    
    def get_avaliable_markets(self) -> Union[List[str], ErrorObject]:
        """
        Get the list of strings of the countries in which Spotify is available,
    identified by their ISO 3166-1 alpha-2 country code with additional
    country codes for special territories.
        """
        url = f'https://api.spotify.com/v1/markets'
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, ErrorObject)
    
@requires('user-top-read')
    def get_a_users_top_artists_and_tracks(self, type_: str, time_range: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[Union[ArtistObject, TrackObject]], ErrorObject]:
        """
        Get the current user’s top artists or tracks based on calculated affinity.

    Args:
        type_: The type of entity to return. Valid values: 'artists' or
          'tracks'.
        time_range: Optional; Over what time frame the affinities are
          computed. Valid values: 'long_term' (calculated from several years
          of data and including all new data as it becomes available),
          'medium_term' (approximately last 6 months), 'short_term'
          (approximately last 4 weeks). Default: 'medium_term'.
        limit: Optional; The maximum number of entities to return.  Default:
          20. Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first entity to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/me/top/{type_}'
        query_params = {'time_range': time_range, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
    def get_information_about_the_users_current_playback(self, market: str = None) -> Union[dict, ErrorObject]:
        """
        Get information about the user’s current playback state, including track
    or episode, progress, and active device.

    Args:
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/me/player'
        query_params = {'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-modify-playback-state')
    def transfer_a_users_playback(self, device_id: str, play: bool = None) -> Optional[ErrorObject]:
        """
        Transfer playback to a new device and determine if it should start
    playing.

    Args:
        device_id: ID of the device on which playback should be transferred
        play: Optional; If True, playback will be ensured on the new device.
          Otherwise it will keep the current playback state. Default: False.
        """
        url = f'https://api.spotify.com/v1/me/player'
        query_params = {}
        json_body = {'device_id': device_id, 'play': play}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-read-playback-state')
    def get_a_users_available_devices(self) -> Union[List[Optional[dict]], ErrorObject]:
        """
        Get a list of user's current available devices with information including
    their id, name, type, and volume percent.
        """
        url = f'https://api.spotify.com/v1/me/player/devices'
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, ErrorObject)
    
@requires('user-read-currently-playing', 'user-read-playback-state')
    def get_the_users_currently_playing_track(self, market: str) -> Union[Optional[dict]], ErrorObject]:
        """
        Get the object currently being played on the user’s Spotify account.

    Args:
        market: An ISO 3166-1 alpha-2 country code or the string 'from_token'.
        """
        url = f'	https://api.spotify.com/v1/me/player/currently-playing'
        query_params = {'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-modify-playback-state')
    def start_or_resume_a_users_playback(self, device_id: str = None, context_uri: str = None, uris: List[str] = None, offset: int = None, position_ms: int = None) -> Optional[ErrorObject]:
        """
        Start a new context or resume current playback on the user’s active
     device. A new context can be chosen by providing a value for the
     parameters context_uri or uris (note: you cannot provide both a
     context_uri and uris parameter).

    The context_uri is the uri code for a list object such as an album. The
     uris is a list of individual uri codes for individual objects such as
     tracks so it is like you are providing a playlist. Additionally offset
     and position_ms can be provided to choose which track to play within the
     context and the position to start it at.

    Warning: Due to the asynchronous nature of the issuance of the command,
    you should use the method get_information_about_the_users_current_playback
    to check that your issued command was handled correctly by the player.

    Args:
        device_id: Optional; The id of the device this command is targeting.
          If not supplied, the user’s currently active device is the target.
        context_uri: Optional; The uri of the context to be played. This can
          be any list type such as an album, playlist, show, etc.
        uris: Optional; A list of uris to be used as the context. These must
          be individual types like tracks or episodes.
        offset: Optional; The index of position to play within the context.
          For example if the context_uri were an album, an offset of 3 would
          begin play at the 4th track on the album. The index begins at 0.
          Default: 0.
        position_ms: Optional; The playback position in milliseconds to
          start/resume playback at. Default: 0.
        """
        url = f'https://api.spotify.com/v1/me/player/play'
        query_params = {'device_id': device_id}
        json_body = {'context_uri': context_uri, 'uris': uris, 'offset': offset, 'position_ms': position_ms}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-modify-playback-state')
    def pause_a_users_playback(self, device_id: str = None) -> Optional[ErrorObject]:
        """
        Pause the playback on the user's account.

    Warning: Due to the asynchronous nature of the issuance of the command,
    you should use the method get_information_about_the_users_current_playback
    to check that your issued command was handled correctly by the player.

    Args:
        device_id: Optional; The id of the device this command is targeting.
          If not supplied, the user’s currently active device is the target.
        """
        url = f'https://api.spotify.com/v1/me/player/pause'
        query_params = {'device_id': device_id}
        json_body = {}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-modify-playback-state')
    def skip_users_playback_to_next_track(self, device_id: str = None) -> Optional[ErrorObject]:
        """
        Skips to next track in the user’s queue.

    Warning: Due to the asynchronous nature of the issuance of the command,
    you should use the method get_information_about_the_users_current_playback
    to check that your issued command was handled correctly by the player.

    Args:
        device_id: Optional; The id of the device this command is targeting.
          If not supplied, the user’s currently active device is the target.
        """
        url = f'https://api.spotify.com/v1/me/player/next'
        query_params = {'device_id': device_id}
        json_body = {}
        response, error = self._post(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-modify-playback-state')
    def seek_to_position_in_currently_playing_track(self, position_ms: int, device_id: str = None) -> Optional[ErrorObject]:
        """
        Seeks to the given position in the user's currently playing track.

    Warning: Due to the asynchronous nature of the issuance of the command,
    you should use the method get_information_about_the_users_current_playback
    to check that your issued command was handled correctly by the player.

    Args:
        position_ms: The position in milliseconds to seek to. Must be a
          positive number. Passing in a position that is greater than the
          length of the track will cause the player to start playing the next
          song.
        device_id: Optional; The id of the device this command is targeting.
          If not supplied, the user’s currently active device is the target.
        """
        url = f'https://api.spotify.com/v1/me/player/seek'
        query_params = {'position_ms': position_ms, 'device_id': device_id}
        json_body = {}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-modify-playback-state')
    def set_repeat_mode_on_users_playback(self, state: str, device_id: str = None) -> Optional[ErrorObject]:
        """
        Set the repeat mode for the user’s playback. Options are repeat-track,
     repeat-context, and off.

    Warning: Due to the asynchronous nature of the issuance of the command,
    you should use the method get_information_about_the_users_current_playback
    to check that your issued command was handled correctly by the player.

    Args:
        state: The state to set the repeat mode to. Valid values are 'track',
          'context' and 'off'. 'track' will repeat the current track.
          'context' will repeat the current context. 'off' will turn repeat
          off.
        device_id: Optional; The id of the device this command is targeting.
          If not supplied, the user’s currently active device is the target.
        """
        url = f'https://api.spotify.com/v1/me/player/repeat'
        query_params = {'state': state, 'device_id': device_id}
        json_body = {}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-modify-playback-state')
    def set_volume_for_users_playback(self, volume_percent: int, device_id: str = None) -> Optional[ErrorObject]:
        """
        Set the volume for the user's current playback device.

    Warning: Due to the asynchronous nature of the issuance of the command,
    you should use the method get_information_about_the_users_current_playback
    to check that your issued command was handled correctly by the player.

    Args:
        volume_percent: The volume to set. Must be a value from 0 to 100
          inclusive.
        device_id: Optional; The id of the device this command is targeting.
          If not supplied, the user’s currently active device is the target.
        """
        url = f'https://api.spotify.com/v1/me/player/volume'
        query_params = {'volume_percent': volume_percent, 'device_id': device_id}
        json_body = {}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-modify-playback-state')
    def toggle_shuffle_for_users_playback(self, state: bool, device_id: str = None) -> Optional[ErrorObject]:
        """
        Toggle shuffle on or off for user’s playback.

    Warning: Due to the asynchronous nature of the issuance of the command,
    you should use the method get_information_about_the_users_current_playback
    to check that your issued command was handled correctly by the player.

    Args:
        state: The state to set the shuffle mode to. If True, shuffle will be
          turned on. If False, shuffle will be turned off.
        device_id: Optional; The id of the device this command is targeting.
          If not supplied, the user’s currently active device is the target.
        """
        url = f'https://api.spotify.com/v1/me/player/shuffle'
        query_params = {'state': state, 'device_id': device_id}
        json_body = {}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('user-modify-playback-state')
    def get_current_users_recently_played_tracks(self, limit: int = None, after: int = None, before: int = None) -> Union[PagingObject[PlayHistoryObject], ErrorObject]:
        """
        Get tracks from the current user’s recently played tracks. Note: Currently
    does not support podcast episodes.

    Args:
        limit: Optional; The maximum number of items to return.  Default: 20.
          Minimum: 1. Maximum: 50.
        after: Optional; A Unix timestamp in milliseconds. Returns all items
          after (but not including) this cursor position. If after is
          specified, before must not be specified.
        before: Optional; A Unix timestamp in milliseconds. Returns all items
          before (but not including) this cursor position. If before is
          specified, after must not be specified.
        """
        url = f'https://api.spotify.com/v1/me/player/recently-played'
        query_params = {'limit': limit, 'after': after, 'before': before}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
@requires('user-modify-playback-state')
    def add_an_item_to_queue(self, uri: str, device_id: str = None) -> Optional[ErrorObject]:
        """
        Add an item to the end of the user’s current playback queue.

    Args:
        uri: The uri of the item to add to the queue. Must be a track or an
          episode uri.
        device_id: Optional; The id of the device this command is targeting.
          If not supplied, the user’s currently active device is the target.
        """
        url = f'https://api.spotify.com/v1/me/player/queue'
        query_params = {'uri': uri, 'device_id': device_id}
        json_body = {}
        response, error = self._post(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('playlist-read-private', 'playlist-read-collaborative')
    def get_a_list_of_current_users_playlists(self, limit: int = None, offset: int = None) -> Union[PagingObject[SimplifiedPlaylistObject], ErrorObject]:
        """
        Get a list of the playlists owned or followed by the current Spotify user.

    Args:
        limit: Optional; The maximum number of playlists to return.  Default:
          20. Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first playlist to return. Default:
          0.
        """
        url = f'https://api.spotify.com/v1/me/playlists'
        query_params = {'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
@requires('playlist-read-private', 'playlist-read-collaborative')
    def get_a_list_of_a_users_playlists(self, user_id: str, limit: int = None, offset: int = None) -> Union[PagingObject[SimplifiedPlaylistObject], ErrorObject]:
        """
        Get a list of the playlists owned or followed by a Spotify user.

    Args:
        user_id: The user's Spotify user ID.
        limit: Optional; The maximum number of playlists to return.  Default:
          20. Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first playlist to return. Default:
          0.
        """
        url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
        query_params = {'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
@requires('playlist-modify-public', 'playlist-modify-private')
    def create_a_playlist(self, user_id: str, name: str, public: bool = None, collaborative: bool = None, description: str = None) -> Union[PlaylistObject, ErrorObject]:
        """
        Create an empty playlist for a Spotify user.

    Args:
        user_id: The user's Spotify user ID.
        name: The name for the new playlist, for example "Your Coolest
          Playlist". This name does not need to be unique; a user may have
          several playlists with the same name.
        public: Optional; If True, the playlist will be public. If False, the
          playlist will be private. Default: True.
        collaborative: Optional; If True, the playlist will be collaborative.
          If False, it won't be collaborative. Default: False. Note: To create
          a collaborative playlist you must also set public to False.
        description: Optional; The playlist description that will be displayed
          on Spotify clients.
        """
        url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
        query_params = {}
        json_body = {'name': name, 'public': public, 'collaborative': collaborative, 'description': description}
        response, error = self._post(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PlaylistObject(response.text)
    
    def get_a_playlist(self, playlist_id: str, market: str = None, fields: str = None) -> Union[PlaylistObject, ErrorObject]:
        """
        Get a playlist owned by a Spotify user.

    Args:
        playlist_id: The Spotify ID for the playlist.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        fields: Optional; Filters for the query: a comma-separated list of the
          fields to return. If omitted, all fields are returned. For example,
          to get just the playlist’’s description and URI:
          fields=description,uri. A dot separator can be used to specify non-
          reoccurring fields, while parentheses can be used to specify
          reoccurring fields within objects. For example, to get just the
          added date and user ID of the adder:
          fields=tracks.items(added_at,added_by.id). Use multiple parentheses
          to drill down into nested objects, for example:
          fields=tracks.items(track(name,href,album(name,href))). Fields can
          be excluded by prefixing them with an exclamation mark, for example:
          fields=tracks.items(track(name,href,album(!name,href))).
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
        query_params = {'market': market, 'fields': fields}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PlaylistObject(response.text)
    
@requires('playlist-modify-public', 'playlist-modify-private')
    def change_a_playlists_details(self, playlist_id: str, name: str, public: bool = None, collaborative: bool = None, description: str = None) -> Optional[ErrorObject]:
        """
        Change a playlist's name and public private state. The user must own the
    playlist.

    Args:
        playlist_id: The Spotify ID for the playlist.
        name: The new name for the playlist, for example "Your Coolest
          Playlist Version 2". This name does not need to be unique; a user
          may have several playlists with the same name.
        public: Optional; If True, the playlist will be public. If False, the
          playlist will be private. Default: True.
        collaborative: Optional; If True, the playlist will be collaborative.
          If False, it won't be collaborative. Default: False. Note: To create
          a collaborative playlist you must also set public to False.
        description: Optional; The playlist description that will be displayed
          on Spotify clients.
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
        query_params = {}
        json_body = {'name': name, 'public': public, 'collaborative': collaborative, 'description': description}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
    def get_a_playlists_items(self, playlist_id: str, market: str = None, fields: str = None, limit: int = None, offset: int = None) -> Union[PagingObject[Union[TrackObject, EpisodeObject]], ErrorObject]:
        """
        Get full details of the items of a playlist owned by a Spotify user.

    Args:
        playlist_id: The Spotify ID for the playlist.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        fields: Optional; Filters for the query: a comma-separated list of the
          fields to return. If omitted, all fields are returned. For example,
          to get just the playlist’’s description and URI:
          fields=description,uri. A dot separator can be used to specify non-
          reoccurring fields, while parentheses can be used to specify
          reoccurring fields within objects. For example, to get just the
          added date and user ID of the adder:
          fields=tracks.items(added_at,added_by.id). Use multiple parentheses
          to drill down into nested objects, for example:
          fields=tracks.items(track(name,href,album(name,href))). Fields can
          be excluded by prefixing them with an exclamation mark, for example:
          fields=tracks.items(track(name,href,album(!name,href))).
        limit: Optional; The maximum number of items to return.  Default: 100.
          Minimum: 1. Maximum: 100.
        offset: Optional; The index of the first item to return. Default: 0.
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        query_params = {'market': market, 'fields': fields, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
@requires('playlist-modify-public', 'playlist-modify-private')
    def add_items_to_a_playlist(self, playlist_id: str, market: str = None, position: int = None, uris: List[str] = None) -> Optional[ErrorObject]:
        """
        Add one or more items to a user’s playlist.

    Args:
        playlist_id: The Spotify ID for the playlist.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        position: Optional; The position to insert the items, a zero-based
          index. For example, to insert the items in the first position:
          position=0; to insert the items in the third position: position=2 .
          If omitted, the items will be appended to the playlist. Items are
          added in the order they are listed in the uris.
        uris: Optional; A list of Spotify URIs to be added. They can be tracks
          or episode URIs. A maximum of 100 items can be added per request.
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        query_params = {'market': market, 'position': position}
        json_body = {'uris': uris}
        response, error = self._post(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('playlist-modify-public', 'playlist-modify-private')
    def reorder_or_replace_a_playlists_items(self, playlist_id: str, uris: List[str] = None, range_start: int = None, insert_before: int = None, range_length: int = None, snapshot_id: str = None) -> Union[str, ErrorObject]:
        """
        Either reorder or replace items in a playlist depending on the request’s
     parameters. To reorder items, include range_start, insert_before,
     range_length and snapshot_id in the request’s body. To replace items,
     include uris as either a query parameter or in the request’s body.
     Replacing items in a playlist will overwrite its existing items. This
     operation can be used for replacing or clearing items in a playlist.

    Note: Replace and reorder are mutually exclusive operations which share
    the same endpoint, but have different parameters. These operations cannot
    be applied together in a single request.

    Args:
        playlist_id: The Spotify ID for the playlist.
        uris: Optional; A list of Spotify URIs to replace the playlist with.
          They can be tracks or episode URIs. A maximum of 100 items can be
          added per request.
        range_start: Optional; The position of the first item to be reordered.
        insert_before: Optional; The position where the items should be
          inserted. To reorder the items to the end of the playlist, simply
          set insert_before to the position after the last item. To reorder
          the first item to the last position in a playlist with 10 items, set
          range_start to 0, and insert_before to 10. To reorder the last item
          in a playlist with 10 items to the start of the playlist, set
          range_start to 9, and insert_before to 0.
        range_length: Optional; The amount of items to be reordered. Default:
          1.
        snapshot_id: Optional; The playlist's snapshot ID against which you
          want to make the changes.
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        query_params = {}
        json_body = {'uris': uris, 'range_start': range_start, 'insert_before': insert_before, 'range_length': range_length, 'snapshot_id': snapshot_id}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
@requires('playlist-modify-public', 'playlist-modify-private')
    def remove_items_from_a_playlist(self, playlist_id: str, tracks: List[str] = None, snapshot_id: str = None) -> Union[str, ErrorObject]:
        """
        Remove one of more items from a user's playlist.

    Args:
        playlist_id: The Spotify ID for the playlist.
        tracks: Optional; A list of Spotify URIs to be removed. They can be
          tracks or episode URIs. A maximum of 100 items can be removed per
          request.
        snapshot_id: Optional; The playlist’s snapshot ID against which you
          want to make the changes. The API will validate that the specified
          items exist and in the specified positions and make the changes,
          even if more recent changes have been made to the playlist.
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        query_params = {}
        json_body = {'tracks': tracks, 'snapshot_id': snapshot_id}
        response, error = self._delete(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ErrorObject(response.text)
    
    def get_a_playlist_cover_image(self, playlist_id: str) -> Union[ImageObject, ErrorObject]:
        """
        Get the current image associated with a specific playlist.

    Args:
        playlist_id: The Spotify ID for the playlist.
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/images'
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ImageObject(response.text)
    
@requires('ugc-image-upload', 'playlist-modify-public', 'playlist-modify-private')
    def upload_a_custom_playlist_cover_image(self, playlist_id: str, image: ImageObject) -> Union[ImageObject, ErrorObject]:
        """
        Replace the image used to represent a specific playlist.

    Args:
        playlist_id: The Spotify ID for the playlist.
        image: The image to be uploaded.
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/images'
        query_params = {}
        json_body = {}
        response, error = self._put(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ImageObject(response.text)
    
    def search_for_an_item(self, q: str, type_: List[str], market: str = None, limit: int = None, offset: int = None, include_external: str = None) -> Union[PagingObject[Union[ArtistObject, SimplifiedAlbumObject, TrackObject, SimplifiedShowObject, SimplifiedEpisodeObject]], ErrorObject]:
        """
        Get Spotify Catalog information about albums, artists, playlists, tracks,
    shows or episodes that match a keyword string.

    Args:
        q: Search query keywords and optional field filters and operators
        type_: A list of strings of the item types to search across. Valid
          types are: 'album', 'artist', 'playlist', 'track', 'show' and
          'episode'.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        limit: Optional; Maximum number of results to return. Default: 20.
          Minimum: 1. Maximum: 50. Note: The limit is applied within each
          type, not the total response. For example, if the limit value is 3
          and the type is ['artist', 'album'], the response contains 3 artists
          and 3 albums.
        offset: Optional; The index of the first result to return. Default: 0.
          Maximum: 1,000. Use with limit to get the next page of search
          results.
        include_external: Optional; Possible values: 'audio'. If 'audio' is
          specified the response will include any relevant audio content that
          is hosted externally. By default external content is filtered out
          from responses.
        """
        url = f'https://api.spotify.com/v1/search'
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return PagingObject(response.text)
    
    def get_multiple_shows(self, ids: List[str], market: str = None) -> Union[List[Optional[SimplifiedShowObject]], ErrorObject]:
        """
        Get Spotify catalog information for several shows based on their Spotify
    IDs.

    Args:
        ids: A list of strings of the Spotify IDs for the shows. Maximum: 50
          IDs.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/shows'
        query_params = {'ids': ids, 'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, SimplifiedShowObject)
    
    def get_a_show(self, id_: str, market: str = None) -> Union[ShowObject, ErrorObject]:
        """
        Get Spotify catalog information for a single show identified by its unique
    Spotify ID.

    Args:
        id_: The Spotify ID of the show.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/shows/{id_}'
        query_params = {'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return ShowObject(response.text)
    
    def get_a_shows_episodes(self, id_: str, market: str = None, limit: int = None, offset: int = None) -> Union[PagingObect[SimplifiedEpisodeObject], ErrorObject]:
        """
        Get Spotify catalog information about a show’s episodes. Optional
    parameters can be used to limit the number of episodes returned.

    Args:
        id_: The Spotify ID of the show.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        limit: Optional; The maximum number of episodes to return.  Default:
          20. Minimum: 1. Maximum: 50.
        offset: Optional; The index of the first episode to return. Default:
          0.
        """
        url = f'https://api.spotify.com/v1/shows/{id_}/episodes'
        query_params = {'market': market, 'limit': limit, 'offset': offset}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return SimplifiedEpisodeObject(response.text)
    
    def get_several_tracks(self, ids: List[str], market: str = None) -> Union[List[Optional[TrackObject]], ErrorObject]:
        """
        Get Spotify catalog information for multiple tracks based on their Spotify
    IDs.

    Args:
        ids: A list of strings of the Spotify IDs for the tracks. Maximum: 50
          IDs.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/tracks'
        query_params = {'ids': ids, 'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, TrackObject)
    
    def get_a_track(self, id_: str, market: str = None) -> Union[TrackObject, ErrorObject]:
        """
        Get Spotify catalog information for a single track identified by its
    unique Spotify ID.

    Args:
        id_: The Spotify ID of the track.
        market: Optional; An ISO 3166-1 alpha-2 country code or the string
          'from_token'.
        """
        url = f'https://api.spotify.com/v1/tracks/{id}'
        query_params = {'market': market}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return TrackObject(response.text)
    
    def get_audio_features_for_several_tracks(self, ids: List[str]) -> Union[List[Optional[AudioFeaturesObject]], ErrorObject]:
        """
        Get audio features for multiple tracks based on their Spotify IDs.

    Args:
        ids: A list of strings of the Spotify IDs for the tracks. Maximum: 100
          IDs.
        """
        url = f'https://api.spotify.com/v1/audio-features'
        query_params = {'ids': ids}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return self._convert_array_to_list(response.text, AudioFeaturesObject)
    
    def get_audio_features_for_a_track(self, id_: str) -> Union[AudioFeaturesObject, ErrorObject]:
        """
        Get audio feature information for a single track identified by its unique
    Spotify ID.

    Args:
        id_: The Spotify ID of the track.
        """
        url = f'https://api.spotify.com/v1/audio-features/{id}'
        query_params = {'id_': id_}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return AudioFeaturesObject(response.text)
    
    def get_audio_analysis_for_a_track(self, id_: str) -> Union[AudioAnalysisObject, ErrorObject]:
        """
        Get a detailed audio analysis for a single track identified by its unique
    Spotify ID.

    Args:
        id_: The Spotify ID of the track.
        """
        url = f'https://api.spotify.com/v1/audio-analysis/{id}'
        query_params = {'id_': id_}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return AudioAnalysisObject(response.text)
    
@requires('user-read-email', 'user-read-private')
    def get_current_users_profile(self) -> Union[UserObject, ErrorObject]:
        """
        Get detailed profile information about the current user (including the
    current user’s username).
        """
        url = f'https://api.spotify.com/v1/me'
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return UserObject(response.text)
    
    def get_a_users_profile(self, id_: str) -> Union[UserObject, ErrorObject]:
        """
        Get public profile information about a Spotify user.

    Args:
        id_: The Spotify ID of the user.
        """
        url = f'https://api.spotify.com/v1/users/{user_id}'
        query_params = {}
        json_body = {}
        response, error = self._get(url, query_params, json_body)
        if error:
            return ErrorObject(response.text)
        return UserObject(response.text)
    