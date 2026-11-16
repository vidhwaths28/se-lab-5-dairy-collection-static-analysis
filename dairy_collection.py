"""Dairy cooperative milk collection ledger."""

import hashlib
import sqlite3


def create_connection() -> sqlite3.Connection:
    """Create a fresh in-memory ledger and its milk table."""
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE milk ("
        "id INTEGER PRIMARY KEY, farmer TEXT NOT NULL, litres REAL NOT NULL, "
        "fat REAL, day TEXT NOT NULL)"
    )
    return connection


def record_milk(
    connection: sqlite3.Connection,
    farmer: str,
    litres: float,
    fat: float | None,
    day: str,
) -> None:
    """Record a milk delivery."""
    if not farmer.strip():
        raise ValueError("farmer must not be empty")
    if litres <= 0:
        raise ValueError("litres must be greater than zero")
    if fat is not None and not 0 <= fat <= 10:
        raise ValueError("fat must be between 0 and 10")
    if not day.strip():
        raise ValueError("day must not be empty")

    connection.execute(
        "INSERT INTO milk (farmer, litres, fat, day) VALUES (?, ?, ?, ?)",
        (farmer, litres, fat, day),
    )
    connection.commit()


def farmer_token(farmer: str) -> str:
    """Return a stable SHA-256 digest for a farmer name."""
    return hashlib.sha256(farmer.encode("utf-8")).hexdigest()


def daily_total(connection: sqlite3.Connection, day: str) -> str:
    """Format the total litres collected on a given day."""
    row = connection.execute(
        "SELECT COALESCE(SUM(litres), 0) FROM milk WHERE day = ?", (day,)
    ).fetchone()
    return (
        f"Total: {row[0]:.1f} litres"
    )


def top_farmer(connection: sqlite3.Connection) -> str | None:
    """Return the farmer with the highest total delivery, if any."""
    row = connection.execute(
        "SELECT farmer, SUM(litres) AS total FROM milk "
        "GROUP BY farmer ORDER BY total DESC, farmer ASC LIMIT 1"
    ).fetchone()
    return None if row is None else str(row[0])


def print_slip(farmer: str) -> None:
    """Print a collection slip message without invoking a shell."""
    print(f"Printing slip for {farmer}")


def low_fat(connection: sqlite3.Connection) -> list[str]:
    """List farmers whose delivery is missing fat data or below 3.5%."""
    rows = connection.execute("SELECT farmer, fat FROM milk").fetchall()
    return [farmer for farmer, fat in rows if fat is None or fat < 3.5]


def main() -> None:
    """Run a small ledger demonstration."""
    connection = create_connection()
    try:
        record_milk(connection, "Gopal", 12.5, 4.1, "Mon")
        record_milk(connection, "Lata", 20.0, 3.2, "Mon")
        print(
            daily_total(connection, "Mon"),
            top_farmer(connection),
            low_fat(connection),
        )
        print_slip("Gopal")
        print(farmer_token("Lata"))
    finally:
        connection.close()


if __name__ == "__main__":
    main()
