from hdbcli import dbapi
import pandas as pd
import threading
import time

def print_status():
    while not stop_thread:
        print("El script se está ejecutando...")
        time.sleep(20)

def main(users, start_date, end_date):
    global stop_thread
    stop_thread = False

    # Start the status thread
    status_thread = threading.Thread(target=print_status)
    status_thread.start()

    # Establish connection to source system
    try:
        conn = dbapi.connect(
            address='hdbed1v.eci.geci', 
            port=30015, 
            database='ED1',
            user='KING', 
            password='30decED1'
        )
    except dbapi.Error as er:
        print('Connect failed, exiting')
        print(er)
        stop_thread = True
        status_thread.join()
        exit()

    # If no errors, print connected
    print('connected')

    # Convert the users input into a list
    user_list = users.split(',') if users else []

    # Prepare dataframes to be used
    df = pd.DataFrame()

    if not user_list:
        # If no users specified, get all users
        sql_command = f"""SELECT DISTINCT DB_USER, OBJECT_NAME, OPERATION, TO_DATE(START_TIME) AS START_TIME 
                          FROM "_SYS_BIC"."KING.Monitors.Backup/CV_EXPENSIVE_STATEMENT"
                          WHERE START_TIME >= TO_TIMESTAMP('{start_date} 00:00:00','YYYY-MM-DD HH24:MI:SS') 
                          AND START_TIME <= TO_TIMESTAMP('{end_date} 23:59:59','YYYY-MM-DD HH24:MI:SS') 
                          LIMIT 5000;"""
        df_package = pd.read_sql(sql_command, conn)
        df_package['USER'] = df_package['DB_USER']

        # Split the objects (obj1, obj2, ..., objn)
        df_object_name = df_package['OBJECT_NAME'].str.split(',', expand=True)

        for ind, object_name in df_object_name.iterrows():
            df_aux = pd.concat([pd.DataFrame({'start_time': [df_package.loc[ind, 'START_TIME']], 'operation': [df_package.loc[ind, 'OPERATION']]}), object_name.dropna()], ignore_index=True, axis=1)
            df_aux['USER'] = df_package.loc[ind, 'USER']
            df_aux['LINE'] = ind + 1  # Add line number
            df = pd.concat([df, df_aux]).drop_duplicates()
    else:
        for user in user_list:
            user = user.strip()  # Remove any leading/trailing whitespace
            # Get the objects and operations from expensive statements (limit 5K to save DB, considered enough sample) for each user
            sql_command = f"""SELECT DISTINCT OBJECT_NAME, OPERATION, TO_DATE(START_TIME) AS START_TIME 
                              FROM "_SYS_BIC"."KING.Monitors.Backup/CV_EXPENSIVE_STATEMENT"
                              WHERE DB_USER = '{user}' 
                              AND START_TIME >= TO_TIMESTAMP('{start_date} 00:00:00','YYYY-MM-DD HH24:MI:SS') 
                              AND START_TIME <= TO_TIMESTAMP('{end_date} 23:59:59','YYYY-MM-DD HH24:MI:SS') 
                              LIMIT 5000;"""

            df_package = pd.read_sql(sql_command, conn)
            df_package['USER'] = user

            # Split the objects (obj1, obj2, ..., objn)
            df_object_name = df_package['OBJECT_NAME'].str.split(',', expand=True)

            for ind, object_name in df_object_name.iterrows():
                df_aux = pd.concat([pd.DataFrame({'start_time': [df_package.loc[ind, 'START_TIME']], 'operation': [df_package.loc[ind, 'OPERATION']]}), object_name.dropna()], ignore_index=True, axis=1)
                df_aux['USER'] = user
                df_aux['LINE'] = ind + 1  # Add line number
                df = pd.concat([df, df_aux]).drop_duplicates()

    if not df.empty:
        df.columns = ['START_TIME', 'OPERACION', 'TABLA', 'USER', 'LINE']
        # Write to Excel with multiple sheets if necessary
        max_rows_per_sheet = 1048576
        num_sheets = (len(df) // max_rows_per_sheet) + 1

        with pd.ExcelWriter('expensive_statements.xlsx') as writer:
            for i in range(num_sheets):
                start_row = i * max_rows_per_sheet
                end_row = start_row + max_rows_per_sheet
                df.iloc[start_row:end_row].to_excel(writer, sheet_name=f'Sheet{i+1}', index=False)
    else:
        print("No data to write to Excel.")

    # Stop the status thread and print completion message
    stop_thread = True
    status_thread.join()
    print("El script ha terminado.")

if __name__ == "__main__":
    users = input('Enter user names separated by commas (leave empty for all users): ')
    #start_date = input('Enter start date (YYYY-MM-DDS_MSTRGY_EDW_CONTA): ')
   # end_date = input('Enter end date (YYYY-MM-DD): ')
   # main(users, start_date, end_date)

