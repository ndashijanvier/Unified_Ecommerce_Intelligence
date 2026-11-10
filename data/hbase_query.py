import happybase

# Connect to HBase Thrift Server
connection = happybase.Connection(host='ecommerce_hbase', port=9090)
connection.open()
table = connection.table('user_sessions')

# We select a target user id from the synthetic dataset pool to test retrieval
target_user = "user_000000" 
print(f"Scanning HBase for active chronological session streams for: {target_user}...\n")

# Use a row prefix scan to quickly catch all rows starting with this user's ID
user_records = table.scan(row_prefix=target_user.encode())

record_count = 0
for key, data in user_records:
    record_count += 1
    print(f"Row Key: {key.decode()}")
    print(f"  -> Session ID: {data[b'info:session_id'].decode()}")
    print(f"  -> Duration: {data[b'info:duration'].decode()} seconds")
    print(f"  -> Conversion Status: {data[b'info:conversion'].decode()}")
    print(f"  -> Device/OS: {data[b'activity:device'].decode()} ({data[b'activity:os'].decode()})")
    print("-" * 50)
    if record_count >= 3: # Limit terminal output to avoid flood
        print("... Truncated for readability ...")
        break

if record_count == 0:
    print(f"No explicit records found for {target_user}. Trying an alternative scan match...")
    # Fallback to display the first row available in the database table
    for key, data in table.scan(limit=1):
        print(f"Found Alternative Entry Row Key: {key.decode()}")

connection.close()
