from hdbcli import dbapi
import pandas as pd
import time

def main(in_p):
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
        exit()

    # If no errors, print connected
    print('connected')

    # Select the user or users from input parameter
    sql_command = f"""SELECT user_name FROM "SYS"."USERS" WHERE user_name like '{in_p}%';"""
    df_users = pd.read_sql(sql_command, conn)

    # Prepare dataframes to be used
    df = pd.DataFrame()
    df_aux2 = pd.DataFrame()

    for ind, user in df_users.iterrows():
        # Get the objects and operations from expensive statements (limit 5K to save DB, considered enough sample) for each user
        # Tables: "OTBI"."TR_EXPENSIVE_STATEMENTS" , "_SYS_BIC"."KING.Monitors.Backup/CV_EXPENSIVE_STATEMENT"  (DB_USER = '{user['USER_NAME']}' )
        sql_command = f"""
            SELECT 
                SUB.STATEMENT_HASH,
                SUB.DB_USER,
                SUB.OBJECT_NAME,
                SUB.OPERATION
            FROM
                (
                    SELECT DISTINCT 
                        T.STATEMENT_HASH,
                        T.OBJECT_NAME,
                        T.DB_USER,
                        T.OPERATION,
                        T.START_TIME
                    FROM
                        "OTBI"."TR_EXPENSIVE_STATEMENTS" , "_SYS_BIC"."KING.Monitors.Backup/CV_EXPENSIVE_STATEMENT" T
                    JOIN (
                            SELECT
                                p.STATEMENT_HASH,
                                MAX(p.START_TIME) AS MAX_START_TIME
                            FROM
                                "OTBI"."TR_EXPENSIVE_STATEMENTS" , "_SYS_BIC"."KING.Monitors.Backup/CV_EXPENSIVE_STATEMENT" p
                            WHERE
                                p.START_TIME >= ADD_DAYS(CURRENT_DATE, -365)
                                --AND p.DB_USER = 'S_MSTRGY_EDW_CONTA'
                                and p.DB_USER = '{user['USER_NAME']}'
                            GROUP BY
                                p.STATEMENT_HASH
                        ) ULT
                ON
                        T.STATEMENT_HASH = ULT.STATEMENT_HASH
                        AND T.START_TIME = ULT.MAX_START_TIME
                        AND T.operation NOT IN ('AGGREGATED_EXECUTION','COMPILE')
                        AND T.object_name <> ''
                ) SUB
            GROUP BY
                SUB.STATEMENT_HASH,
                SUB.DB_USER,
                SUB.OBJECT_NAME,
                SUB.OPERATION;
                    """

        df_package = pd.read_sql(sql_command, conn)

        # Split the objects (obj1, obj2, ..., objn)
        df_object_name = df_package['OBJECT_NAME'].str.split(',', expand=True)

        for ind, object_name in df_object_name.iterrows():
            df_aux = pd.concat([pd.DataFrame({'statement_hash': [df_package.loc[ind, 'STATEMENT_HASH']], 'operation': [df_package.loc[ind, 'OPERATION']]}), object_name.dropna()], ignore_index=True, axis=1)
            df_aux2 = pd.concat([df_aux2, df_aux]).drop_duplicates()
            df_aux2['USER'] = user['USER_NAME']

        df = pd.concat([df, df_aux2]).drop_duplicates()

    df.columns = ['STATEMENT_HASH', 'OPERACION', 'TABLA', 'USER']
    df.to_excel('expensive_statements.xlsx', index=False)

    # # Write to Excel with multiple sheets if necessary  1048576
    # max_rows_per_sheet = 1000000
    # num_sheets = (len(df) // max_rows_per_sheet) + 1

    # with pd.ExcelWriter('expensive_statements.xlsx') as writer:
    #     for i in range(num_sheets):
    #         start_row = i * max_rows_per_sheet
    #         end_row = start_row + max_rows_per_sheet
    #         df.iloc[start_row:end_row].to_excel(writer, sheet_name=f'Sheet{i+1}', index=False)

    # while True:
    #         print("Executing ...")
    #         time.sleep(20) 

if __name__ == "__main__":
    user = input('Enter user_name or pattern: ')
    main(user)

