import json
import os
import sqlite3
import sys
import time

# Add repo root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import ui.database

# Patch DB file
ui.database.DB_FILE = "benchmark_chat_history.db"


def setup_data():
    if os.path.exists(ui.database.DB_FILE):
        os.remove(ui.database.DB_FILE)

    ui.database.init_db()

    user_id = "bench_user"
    conv_id = ui.database.create_new_conversation(user_id, "Benchmark Chat")

    print("Populating database with 1000 messages...")

    conn = sqlite3.connect(ui.database.DB_FILE)
    c = conn.cursor()

    data = []
    for i in range(1000):
        data.append(
            (
                conv_id,
                "user" if i % 2 == 0 else "assistant",
                f"This is message number {i}. It has some content.",
                json.dumps({"idx": i}),
                str(time.time()),
            )
        )

    c.executemany(
        "INSERT INTO messages (conversation_id, role, content, meta_json, timestamp) VALUES (?, ?, ?, ?, ?)",
        data,
    )
    conn.commit()
    conn.close()

    return conv_id


def benchmark():
    conv_id = setup_data()

    print("\n--- Benchmarking ---")

    # Test 1: Fetch All
    start_time = time.time()
    msgs = ui.database.get_conversation_messages(conv_id)
    end_time = time.time()
    print(f"Fetch All (1000 msgs): {(end_time - start_time)*1000:.2f} ms")
    print(f"Count: {len(msgs)}")

    # Test 2: Fetch Limit 50
    start_time = time.time()
    msgs_paged = ui.database.get_conversation_messages(conv_id, limit=50)
    end_time = time.time()
    print(f"Fetch Limit 50 (Real): {(end_time - start_time)*1000:.2f} ms")
    print(f"Count: {len(msgs_paged)}")

    # Check correctness
    # If we fetch limit 50, offset 0, we should get the last 50 messages (indices 950-999)
    # The function reverses them, so they should be in order 950 -> 999.
    first_msg = msgs_paged[0]
    last_msg = msgs_paged[-1]

    print(f"First message idx (should be ~950): {first_msg.get('idx')}")
    print(f"Last message idx (should be 999): {last_msg.get('idx')}")

    # Test 3: Offset
    msgs_offset = ui.database.get_conversation_messages(conv_id, limit=50, offset=50)
    print(f"Fetch Limit 50 Offset 50 Count: {len(msgs_offset)}")
    print(f"First message idx (should be ~900): {msgs_offset[0].get('idx')}")
    print(f"Last message idx (should be ~949): {msgs_offset[-1].get('idx')}")

    # Clean up
    if os.path.exists(ui.database.DB_FILE):
        os.remove(ui.database.DB_FILE)


if __name__ == "__main__":
    benchmark()
