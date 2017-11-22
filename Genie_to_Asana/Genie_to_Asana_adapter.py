import pyodbc
import cfg

class Genie:

    # conn = pyodbc.connect(r'DSN=SiebelFreeTDS;UID=UID;PWD=PWD')
    conn = pyodbc.connect(r'DSN=' + cfg.siebel_info.dsn +
                          ';UID=' + cfg.siebel_info.uid +
                          ';PWD=' + cfg.siebel_info.pwd)

    def __init__(self):
        print("New instance created")

    def db_connector(self):
        pass

    def get_defect_info_by_id(self, db_connection_string,
                              defect_id):
        #db_connection_string.conn.cursor()

        db_connection_string.execute("""
                        select
                            D.DEFECT_NUM AS id,
                            D.DEFECT_TYPE_CD as type,
                            D.ABSTRACT AS summary,
                            D.DESC_TEXT AS description,
                            D.CREATED as created,
                            D.DEFECT_AREA_CD as area,
                            D.DEFECT_SUB_AREA_CD as sub_area,
                            D.STATUS_CD as status,
                            D.SUB_STATUS_CD as sub_status,
                            D.SEVERITY_CD as severity,
                            D.MKTG_PRIORITY_CD as priority,
                            E.LOGIN as assigned_to,
                            ER.LOGIN as reported_by,
                            ED.LOGIN AS depended_on,
                            P_I2.NAME as found_version,
                            X.ATTRIB_34 as feature,
                            P_I.NAME as target_fix,
                            D.X_DUE_DATE as due_date
                        from
                            dbo.S_PROD_DEFECT as D
                            LEFT OUTER JOIN dbo.S_EMPLOYEE AS E ON D.OWNER_EMP_ID = E.ROW_ID
                            LEFT OUTER JOIN dbo.S_EMPLOYEE as ER on D.CREATED_BY = ER.ROW_ID
                            LEFT OUTER JOIN dbo.S_PROD_DEFECT_X AS X ON D.ROW_ID = X.ROW_ID
                            LEFT OUTER JOIN dbo.S_EMPLOYEE AS ED ON X.ATTRIB_04 = ED.ROW_ID
                            LEFT OUTER JOIN dbo.S_PROD_INT as P_I on D.X_PR_TAR_VER = P_I.ROW_ID
                            LEFT OUTER JOIN dbo.S_PROD_INT as P_I2 on D.X_PR_AFF_VER = P_I2.ROW_ID
                        where
                            D.DEFECT_NUM = '%s'
                        """ % defect_id)

        results = db_connection_string.fetchone()
        if results:
            res_dict = {}
            for indx, res in enumerate(results):
                res_dict[db_connection_string.description[indx][0]] = res

                # formatted_result = zip(cursor.description[indx][0], res)
                # print(cursor.description[indx][0])
            db_connection_string.close()
            return res_dict
        else:
            db_connection_string.close()
            return "No info for such ID"

    def combine_defect_results(self, defect_info):
        try:
            due_date = defect_info['due_date'].strftime("%x")
        except:
            due_date = defect_info['due_date'] = "somewhere in 2132..."
        if defect_info['assigned_to'] is not None:
            assignee = defect_info['assigned_to']
        else:
            assignee = "Mr.Nobody"
        if defect_info['target_fix'] is not None:
            tfv = defect_info['target_fix']
        else:
            tfv = "Not set"
        combined_result = defect_info['type'] + \
                          " " + defect_info['id'] + \
                          " " + defect_info['summary'] + \
                          "\n" + assignee + \
                          " - " + defect_info['status'] + " : " + \
                          defect_info['sub_status'] + "\n" + \
                          "TFV: " + tfv +\
                          ", deadline " + due_date + "\n\n"
        return combined_result


def main():

    #just for testing:
    db_connector = Genie.conn
    cursor = db_connector.cursor()
    def_id="1047029521"

    Genie_instance = Genie()
    defect_info = Genie.get_defect_info_by_id(Genie(), cursor, def_id)
    defect_info2 = Genie_instance.get_defect_info_by_id(cursor, "1111111")

    print(defect_info)
    print(defect_info2)

    # avaliable fields:
    # print(defect_info['id'])
    # print(defect_info['description'])
    # print(defect_info['due_date'].strftime("%x"))
    # id,type,created,description,summary,status,sub_status,priority,assigned_to,depended_on,found_version,target_fix etc.

    db_connector.close()

    if __name__ == "__main__":
        main()
