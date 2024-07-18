import json
import pandas as pd
import sqlite3

def get_log(dbname="logs.db", table="chat_completions"):
    try:
        con = sqlite3.connect(dbname)
        query = f"SELECT * FROM {table}"
        data = pd.read_sql_query(query, con)
        con.close()
        return data
    except Exception as e:
        print(f"Error fetching log data: {e}")
        return pd.DataFrame()

def str_to_dict(s):
    return json.loads(s)

def calculate_costs(session_id, dbname="logs.db", table="chat_completions"):
    # Fetch log data
    log_data_df = get_log(dbname, table)

    if log_data_df.empty:
        print("No data retrieved from the database.")
        return None, None

    # Convert JSON strings to dictionaries and extract required fields
    log_data_df["total_tokens"] = log_data_df["response"].apply(lambda x: str_to_dict(x)["usage"]["total_tokens"])
    log_data_df["request"] = log_data_df["request"].apply(lambda x: str_to_dict(x)["messages"][0]["content"])
    log_data_df["response"] = log_data_df["response"].apply(lambda x: str_to_dict(x)["choices"][0]["message"]["content"])

    # Sum total tokens and cost for all sessions
    total_tokens = log_data_df["total_tokens"].sum()
    total_cost = log_data_df["cost"].sum()

    # Total tokens and cost for specific session
    session_tokens = log_data_df[log_data_df["session_id"] == session_id]["total_tokens"].sum()
    session_cost = log_data_df[log_data_df["session_id"] == session_id]["cost"].sum()

    return (total_tokens, round(total_cost, 4)), (session_tokens, round(session_cost, 4))

# Example usage
# session_id = "6366bb42-beb1-4cb6-ade2-309588a1f47c"
# (total_tokens, total_cost), (session_tokens, session_cost) = calculate_costs(session_id)

# if total_tokens is not None:
#     print(f"Total tokens for all sessions: {total_tokens}, total cost: {total_cost}")
#     print(f"Total tokens for session {session_id}: {session_tokens}, cost: {session_cost}")
