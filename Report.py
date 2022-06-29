import sqlite3

def lpad(length, inputStr, padStr):
    padLength = length - len(inputStr)
    return padStr * padLength + inputStr

conn = sqlite3.connect("pfreshdesk.db")
cur = conn.cursor()

sqlStr = "SELECT ticket_id \
, CASE WHEN status = 'Open' THEN '12' \
  ELSE 'N/A' END AS \"time_spent_open\" \
, CASE WHEN sold_datetime IS NULL THEN 'UNSOLD' ELSE strftime('%s', sold_datetime) - strftime('%s', create_datetime) END AS time_spent_waiting_on_customer \
, CASE WHEN pending_start_datetime IS NOT NULL THEN round((strftime('%s.%f', pending_end_datetime) - strftime('%s.%f', pending_start_datetime)) * 1000) \
  ELSE 0 END AS time_spent_waiting_for_response \
, CASE WHEN pending_end_datetime IS NULL THEN 0 ELSE strftime('%s', pending_end_datetime) - strftime('%s', create_datetime) END AS time_till_resolution \
, CASE WHEN cust_start_queue_datetime IS NULL THEN 0 ELSE round(strftime('%s', greeting_datetime) - strftime('%s', cust_start_queue_datetime)) END AS time_to_first_response \
FROM R_TKT_ACTIVITY"

cur.execute(sqlStr)
resultList = cur.fetchall()
cur.close()
conn.close
title = "| ticket_id | time_spent_open | times_spent_waiting_on_customer | time_spent_waiting_for_response | time_till_resolution |\
 time_to_first_response |" 
print(title)
print("-----------------------------------------------------------------------------------------------------------------------------\
----------------------")
for result in resultList:
    ticketId, spentOpen, waitingcust, waitingResponse, resolution, firstResponse = result
    print("   ",lpad(7, str(ticketId), ' '),"\t\t", spentOpen, "\t\t\t", waitingcust, "\t\t\t\t", int(waitingResponse), "\t\t\t\t", resolution, "\t\t\t", int(firstResponse))