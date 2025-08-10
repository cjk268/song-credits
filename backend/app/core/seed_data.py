from sqlalchemy.orm import Session
from app.core.database import engine
from app.core.schemas import Track, Role, Contributor, Credit


def seed():
    with Session(engine) as session:
        track = Track(
            title="Which One (feat. Central Cee)",
            spotify_id="5FMyXeZ0reYloRTiCkPprT",
        )
        session.add(track)
        session.flush()

        performers = Role(title="Performers")
        writers = Role(title="Writers")
        producers = Role(title="Producers")
        session.add_all([performers, writers, producers])
        session.flush()

        contributors = [
            Contributor(
                name="Central Cee",
                spotify_id="5H4yInM5zmHqpKIoMNAx4r",
                image_uri="https://i.scdn.co/image/ab677762000078e6afc079cda32d54850e82c385",
            ),
            Contributor(
                name="Drake",
                spotify_id="3TVXtAsR1Inumwj472S9r4",
                image_uri="https://i.scdn.co/image/ab677762000078e645c984e8c82f9ce15ebf1f51",
            ),
            Contributor(
                name="A. Graham",
                spotify_id="37iwVNNY8MxikC9RpAXQmN",
                image_uri="https://i.scdn.co/image/ab677762000078e6d2b377637d9f6ed34f1652e2",
            ),
            Contributor(
                name="O. Caesar - Su",
                spotify_id="7errNnlxPFWxmZSAq2Q0k9",
                image_uri="https://i.scdn.co/image/ab677762000078e6aae517f57fa4e9833b4bce9c",
            ),
            Contributor(
                name="O Lil Angel",
                spotify_id="53fnyGe5cBmfiLBzbedxFh",
                image_uri="https://i.scdn.co/image/ab677762000078e6afc079cda32d54850e82c385",
            ),
            Contributor(
                name="B4U",
                spotify_id="6vvV1xTiKlHbfzA8mWaEOu",
                image_uri="https://i.scdn.co/image/ab677762000078e6aae517f57fa4e9833b4bce9c",
            ),
            Contributor(
                name="OZ",
                spotify_id="5OLpzTqfOz7L1XKoFcifqN",
                image_uri="https://i.scdn.co/image/ab677762000078e6d2b377637d9f6ed34f1652e2",
            ),
        ]
        session.add_all(contributors)
        session.flush()

        credits = [
            Credit(track_id=track.id, contributor_id=contributors[0].id, role_id=performers.id, weight=6),
            Credit(track_id=track.id, contributor_id=contributors[1].id, role_id=performers.id, weight=7),
            Credit(track_id=track.id, contributor_id=contributors[2].id, role_id=writers.id, weight=5),
            Credit(track_id=track.id, contributor_id=contributors[3].id, role_id=writers.id, weight=4),
            Credit(track_id=track.id, contributor_id=contributors[4].id, role_id=producers.id, weight=3),
            Credit(track_id=track.id, contributor_id=contributors[5].id, role_id=producers.id, weight=2),
            Credit(track_id=track.id, contributor_id=contributors[6].id, role_id=producers.id, weight=1),
        ]
        session.add_all(credits)

        session.commit()
        print("Seed completed.")


if __name__ == "__main__":
    seed()
