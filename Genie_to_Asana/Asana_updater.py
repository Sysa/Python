import asana
import cfg
from Genie_to_Asana_adapter import Genie

"""
get_asana_info:
        get_all_tasks:
            input: asana API connection instance, Asana project ID
            output: generator of list with
        find_tasks_with_defects:
            input: asana task ID and name
            output: iterable list of Defect's IDs in task names
            
update_asana_info:
        desc_sep - separator between current description and block that Asana bot will update.
        update_task_description - updates task description with given block of info.
        
defect_info_block:
    generate_info - generates new dict with Asana Task IDs as keys and Defect IDs as values.
"""

class get_asana_info:

    def get_all_tasks(self, asana_connector, project_id):
        return asana_connector.tasks.find_by_project(project_id, params={
            'opt_fields': 'id,completed,completed_at,name,notes,modified_at','completed_since':'now'})

    def find_tasks_with_defects(self, task_id, task_name):
        dict_of_IDs = {}
        for ch in task_name.split(" "):
            defect_number = ""
            for c in ch:
                try:
                    int(c)
                    defect_number += str(c)
                except:
                    pass
            if defect_number != None and len(defect_number) == 10 :
                #print(str(task_id) + " -> " + defect_number)
                try:
                    dict_of_IDs.setdefault(task_id, [])
                    dict_of_IDs[task_id].append(defect_number)
                except:
                    pass
        if dict_of_IDs:
            return dict_of_IDs

            #print(a)
            #for a1 in a.get(task_id):
            #for a1 in a[task_id]:
                #print(a1)

class update_asana_info:

    desc_sep = "\n ---------- \n" # 10 of '-'

    def update_task_description(self, asana_connector,
                                task_id, current_description,
                                new_description_block, description_separator=desc_sep):
        updated_desciption = current_description + description_separator + new_description_block
        update_result = asana_connector.tasks.update(task_id, params={'notes': updated_desciption})
        print(update_result)


class defect_info_block:

    def generate_info(self, list_of_defect_id):
        new_dict_of_defects = ""
        for asana_id in list_of_defect_id:
            for defect_IDs in list_of_defect_id[asana_id]:
                # new_dict_of_defects += update_asana_info.desc_sep + str(defect_IDs) + " Tratata"
                defect_info = Genie.get_defect_info_by_id(Genie(), Genie.conn.cursor(), defect_IDs)
                # print(defect_info)
                if(defect_info != "No info for such ID"):
                    new_dict_of_defects += Genie.combine_defect_results(Genie(), defect_info)
                # new_dict_of_defects += update_asana_info.desc_sep + str(defect_IDs) + " TFV: " + defect_info['target_fix'] + " Deadline: " + defect_info['due_date'].strftime("%x")
        # print(new_dict_of_defects)
        return new_dict_of_defects

        # Genie.get_defect_info_by_id()
        # db_connector = Genie.conn.cursor()
        # cursor = db_connector
    def compare_info(self, current_description, new_description_block):
        print(current_description.split(update_asana_info.desc_sep)[-1:][0])
        print(new_description_block)
        #print(current_description.split(update_asana_info.desc_sep)[:1][0])
        if (current_description.split(update_asana_info.desc_sep)[-1:][0] != new_description_block):
            #print("not matched")
            compare_result = current_description.split(update_asana_info.desc_sep)[:1][0]
            if compare_result:
                return compare_result
            else:
                return " "
            #return True
        else:
            #print("matched")
            return False
        #for blocks in current_description.split(update_asana_info.desc_sep):
            #print(blocks)



asana_connect = asana.Client.access_token(cfg.asana_info.token)
try:
    for proj_id in cfg.asana_info.project_ids:
        asana_result = get_asana_info().get_all_tasks(asana_connect, proj_id)
        #print(type(asana_result))
        for as_res in asana_result:
                dict_of_defects = get_asana_info.find_tasks_with_defects(asana_connect, as_res['id'], as_res['name'])
                if dict_of_defects is not None:
                    #print(dict_of_defects)
                    #for defect_id in dict_of_defects[as_res['id']]:
                        ###generate new block for description here!
                    defect_info_block.generate_info(defect_info_block(), dict_of_defects)
                        #print(defect_id)
                    compare_result = defect_info_block.compare_info(defect_info_block(), as_res['notes'],
                                                   defect_info_block.generate_info(defect_info_block(), dict_of_defects))
                    if (compare_result):
                        update_asana_info().update_task_description(asana_connect, as_res['id'], compare_result,
                                            defect_info_block.generate_info(defect_info_block(), dict_of_defects))
                        # asana_update = update_asana_info().update_task_description(asana_connect,
                        #                                                            as_res['id'],
                        #                                                            as_res['notes'],
                        #                                                            defect_id)
                #print(as_res['notes'])
                #asana_update = update_asana_info().update_task_description(asana_connect, as_res['id'], as_res['notes'],"MyOwnComment")
except:
    print("error for project_ids")
    pass