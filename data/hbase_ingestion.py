import json
import happybase

print("Connecting to HBase Thrift Server...")
# Connect to the HBase container over the network
connection = happybase.Connection(host='ecommerce_hbase', port=9090)
connection.open()

table = connection.table('user_sessions')
print("Connected successfully. Starting ingestion...")

# Open the first sessions chunk file
with open('work/data/sessions_0.json', 'r') as file:
    sessions = json.load(file)

# Design Document Strategy: Row Key is user_id + start_time 
# This groups a user's chronological activity streams tightly in storage.
for session in sessions:
    row_key = f"{session['user_id']}_{session['start_time']}"
    
    # Pack flat metadata fields into the 'info' column family
    data = {
        b'info:session_id': str(session['session_id']).encode(),
        b'info:duration': str(session['duration_seconds']).encode(),
        b'info:conversion': str(session['conversion_status']).encode(),
        b'info:referrer': str(session['referrer']).encode(),
        b'activity:device': str(session['device_profile']['type']).encode(),
        b'activity:os': str(session['device_profile']['os']).encode()
    }
    
    # Put row into HBase
    table.put(row_key.encode(), data)

print(f"HBase Ingestion Complete! Successfully loaded {len(sessions)} session records.")
connection.close()
