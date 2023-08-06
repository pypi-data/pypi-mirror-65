from acondbs.models import Map, Beam

# These tests are written primarily for the developer to understand
# how models in flask_sqlalchemy work.

# __________________________________________________________________||
def test_backref(app):

    # the operations here don't need be within the app context.

    # 1. create a map
    map1 = Map(name="map1")

    # no beams are associated with the map
    assert [] == map1.beams


    # 2. create a beam with the map
    beam1 = Beam(name="beam1", map=map1)

    # the map is associated with the beam
    assert map1 is beam1.map

    # the beam is referenced back by the map
    assert [beam1] == map1.beams

    # the beam has no child beam
    assert 0 == len(beam1.child_beams)


    # 3. create another beam with the map and the beam
    beam2 = Beam(name="beam2", map=map1, parent_beam=beam1)

    # the map is also associated with the 2nd beam
    assert map1 is beam2.map

    # the two beams are referenced back by the map
    assert [beam1, beam2] == map1.beams

    # the 1st beam is referenced by the 2nd beam
    assert beam1 is beam2.parent_beam

    # the 2nd beam is referenced back by the 1st beam
    assert [beam2] == beam1.child_beams

# __________________________________________________________________||
