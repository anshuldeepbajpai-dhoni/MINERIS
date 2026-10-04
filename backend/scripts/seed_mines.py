from sqlalchemy import text

from app.db.session import SessionLocal


MINES = [
    {
        "name": "Balaghat Manganese Mine",
        "location": "Balaghat, Madhya Pradesh",
        "description": (
            "Demo manganese mining zone representing the Balaghat "
            "manganese belt for MINERIS analysis."
        ),
        "area_hectares": 1250.0,
        "boundary": (
            "MULTIPOLYGON (((80.10 21.85, "
            "80.14 21.85, "
            "80.14 21.88, "
            "80.10 21.88, "
            "80.10 21.85)))"
        ),
    },
    {
        "name": "Nagpur Manganese Zone",
        "location": "Nagpur, Maharashtra",
        "description": (
            "Demo manganese prospectivity zone used for "
            "geospatial and production analysis."
        ),
        "area_hectares": 980.0,
        "boundary": (
            "MULTIPOLYGON (((79.05 21.15, "
            "79.09 21.15, "
            "79.09 21.18, "
            "79.05 21.18, "
            "79.05 21.15)))"
        ),
    },
    {
        "name": "Keonjhar Mineral Zone",
        "location": "Keonjhar, Odisha",
        "description": (
            "Demo mineral zone representing a manganese-rich "
            "geological environment for MINERIS."
        ),
        "area_hectares": 1430.0,
        "boundary": (
            "MULTIPOLYGON (((85.45 21.60, "
            "85.49 21.60, "
            "85.49 21.63, "
            "85.45 21.63, "
            "85.45 21.60)))"
        ),
    },
]


def seed_mines():
    db = SessionLocal()

    try:
        for mine in MINES:
            query = text(
                """
                INSERT INTO mines
                (
                    name,
                    location,
                    description,
                    area_hectares,
                    boundary,
                    created_at
                )
                VALUES
                (
                    :name,
                    :location,
                    :description,
                    :area_hectares,
                    ST_GeomFromText(
                        :boundary,
                        4326
                    ),
                    NOW()
                )
                """
            )

            db.execute(query, mine)

        db.commit()

        print("Successfully seeded MINERIS demo mines.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_mines()