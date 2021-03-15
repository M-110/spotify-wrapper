s = """
self._album_type: str = json_dict['album_type']
        self._artists: List[ArtistObject] = json_dict['artists']
        self._available_markets: List[str] = json_dict['available_markets']
        self._copyrights: List[CopyrightObject] = json_dict['copyrights']
        self._external_ids: ExternalIdObject = json_dict['external_ids']
        self._external_urls: ExternalUrlObject = json_dict['external_urls']
        self._genres: List[str] = json_dict['genres']
        self._href: str = json_dict['href']
        self._id: str = json_dict['id']
        self._images: List[ImageObject] = json_dict['images']
        self._label: str = json_dict['label']
        self._name: str = json_dict['name']
        self._popularity: int = json_dict['popularity']
        self._release_date: str = json_dict['release_date']
        self._release_date_precision: str = json_dict['release_date_precision']
        self._restrictions: Optional[AlbumRestrictionObject] = json_dict.get('restrictions')
        self._tracks: PagingObject[SimplifiedTrackObject] = json_dict['tracks']
        self._type: str = json_dict['type']
        self._uri: str = json_dict['uri']
"""

template = '''
@property
def {name}(self) -> {type_}:
    """
    T
    """
    return self._{name}
'''

def code_writer(s: str):
    properties =[]
    things = s.split('\n')[1:-1]
    for thing in things:
        start = thing.find('_')
        end = thing.find(':')
        properties.append(thing[start+1:end])
    for property_ in properties:
        print(template.format(name=property_, type_='str'))
    
code_writer(s)