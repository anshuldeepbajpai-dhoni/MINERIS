from datetime import datetime

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.mine import Mine
from app.models.production import ProductionRecord


PRODUCTION_DATA = {
    "Balaghat Manganese Mine": [
        (2022, 82000, 76000, 90000),
        (2023, 85000, 81000, 92000),
        (2024, 90000, 87000, 95000),
        (2025, 95000, 91000, 99000),
    ],

    "Nagpur Manganese Zone": [
        (2022, 68000, 62000, 73000),
        (2023, 72000, 67000, 76000),
        (2024, 76000, 71000, 80000),
        (2025, 80000, 75000, 85000),
    ],

    "Keonjhar Mineral Zone": [
        (2022, 105000, 98000, 108000),
        (2023, 110000, 104000, 112000),
        (2024, 115000, 108000, 118000),
        (2025, 120000, 113000, 125000),
    ],
}


def seed_production():
    db = SessionLocal()

    try:
        inserted = 0
        skipped = 0

        for mine_name, records in PRODUCTION_DATA.items():

            mine = db.scalar(
                select(Mine).where(
                    Mine.name == mine_name
                )
            )

            if mine is None:
                print(
                    f"WARNING: Mine not found: {mine_name}"
                )
                continue

            print(
                f"Found {mine.name} "
                f"(ID: {mine.id})"
            )

            for year, planned, actual, demand in records:

                existing = db.scalar(
                    select(ProductionRecord).where(
                        ProductionRecord.mine_id == mine.id,
                        ProductionRecord.year == year,
                    )
                )

                if existing:
                    skipped += 1
                    continue

                production = ProductionRecord(
                    mine_id=mine.id,
                    year=year,
                    planned_production=planned,
                    actual_production=actual,
                    demand=demand,
                    created_at=datetime.utcnow(),
                )

                db.add(production)
                inserted += 1

        db.commit()

        print()
        print("Production seeding completed.")
        print(f"Inserted: {inserted}")
        print(f"Skipped: {skipped}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_production()