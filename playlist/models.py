from django.db import models
from django_neomodel import DjangoNode
from neomodel import db as db, ArrayProperty, StringProperty, IntegerProperty, Relationship, RelationshipFrom, \
    RelationshipTo, StructuredRel, UniqueIdProperty, StructuredNode, DateTimeProperty


class PlayList(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    playlist_title = StringProperty()
    type = StringProperty()

    has_tag = RelationshipTo('PlayListTag', 'HAS_TAG')
    has_track = RelationshipTo('PlayListTracks', 'HAS_TRACK')
    owns = RelationshipFrom('PlayListUser', 'OWNS')

    def merge_nodes(self):
        query = '''
            MERGE (tag:PlayListTag)<-[:HAS_TAG]-(tg:PlayList)-[:HAS_TRACK]->(track:PlayListTracks)
            MERGE (tg)<-[:OWNS]-(u:PlayListUser) '''

        self.cypher(query)

    def import_playlists(self):
        print("I'm in import_playlists")
        query = f'''RETURN 1

            '''
        self.cypher(query)

    class Meta:
        app_label = 'tracks'


class PlayListTracks(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    track_title = StringProperty()

    has_track = RelationshipFrom('PlayListTracks', 'HAS_TRACK')

    class Meta:
        app_label = 'tracks'


class PlayListTag(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    tag_name = StringProperty()
    tg_count = IntegerProperty()

    has_tag = RelationshipFrom('PlayList', 'HAS_TAG')
    top_track = RelationshipTo('PlayListTracks', 'TOP_TRACK')
    related_to = RelationshipTo('PlayListTag', 'RELATED')
    related_from = RelationshipFrom('PlayListTag', 'RELATED')

    def set_top_track(self):
        query = f'''
            MATCH (tag:PlayListTag)
            WHERE tag.name='{self.name}'
            WITH tag
            MATCH (tag:PlayListTag)<-[:HAS_TAG]-(tg:PlayList)-[:HAS_TRACK]->(track:PlayListTracks)
            MATCH (tg)<-[:OWNS]-(u:PlayListUser) 
            WITH tag as tag, track as track, count(DISTINCT u) as rank
            LIMIT 1
            MERGE (tag)-[:TOP_TRACK]->(track)
            '''
        self.cypher(query)

    class Meta:
        app_label = 'tracks'


class PlayListUser(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    user_name = StringProperty()

    owns = RelationshipTo('PlayList', 'OWNS')

    class Meta:
        app_label = 'tracks'


class PlayListCountry(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    country_name = StringProperty()

    in_country = RelationshipFrom('PlayListUser', 'IN_COUNTRY')

    class Meta:
        app_label = 'tracks'


class TrackGroup(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    title = StringProperty()
    type = StringProperty()

    has_tag = RelationshipTo('Tag', 'HAS_TAG')
    has_track = RelationshipTo('Track', 'HAS_TRACK')
    owns = RelationshipFrom('RUser', 'OWNS')

    def import_playlists():
        print("I'm in import_playlists")
        query = f'''RETURN 1

            '''
        self.cypher(query)

    class Meta:
        app_label = 'tracks'


class Tag(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    name = StringProperty()
    tg_count = IntegerProperty()

    has_tag = RelationshipFrom('TrackGroup', 'HAS_TAG')
    top_track = RelationshipTo('Track', 'TOP_TRACK')
    related_to = RelationshipTo('Tag', 'RELATED')
    related_from = RelationshipFrom('Tag', 'RELATED')

    def set_top_track(self):
        self.top_track.disconnect_all()
        query = f'''
            MATCH (tag:Tag)
            WHERE tag.name='{self.name}'
            WITH tag
            MATCH (tag:Tag)<-[:HAS_TAG]-(tg:TrackGroup)-[:HAS_TRACK]->(track:Track)
            MATCH (tg)<-[:OWNS]-(u:RUser) 
            WITH tag as tag, track as track, count(DISTINCT u) as rank
            LIMIT 1
            MERGE (tag)-[:TOP_TRACK]->(track)
            '''
        self.cypher(query)

    class Meta:
        app_label = 'tracks'


class Track(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    title = StringProperty()

    has_track = RelationshipFrom('Track', 'HAS_TRACK')

    class Meta:
        app_label = 'tracks'


class RUser(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    title = StringProperty()

    owns = RelationshipTo('TrackGroup', 'OWNS')

    class Meta:
        app_label = 'tracks'


class Country(DjangoNode):
    uuid = UniqueIdProperty(primary_key=True)
    name = StringProperty()

    in_country = RelationshipFrom('RUser', 'IN_COUNTRY')

    class Meta:
        app_label = 'tracks'


# a = PlayList()
# a.merge_nodes()