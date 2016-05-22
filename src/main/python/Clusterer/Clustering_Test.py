# Copyright (C) 2015 Siavoosh Payandeh Azad

import Clustering_Reports


def double_check_ctg(tg, ctg):
    """
    Checks if the clusters info in TG matches with the information in the CTG.
    :param tg: Task Graph
    :param ctg: Clustered Task Graph
    :return: True if CTG information is the same as TG, False if otherwise
    """
    for task in tg.nodes():
        cluster = tg.node[task]['task'].cluster
        if cluster in ctg.nodes():
            if task not in ctg.node[cluster]['TaskList']:
                print ("DOUBLE CHECKING CTG with TG: \t\033[31mFAILED\033[0m")
                print ("TASK", task, "DOES NOT EXIST IN CLUSTER:", cluster)
                Clustering_Reports.report_ctg(ctg, "CTG_DoubleCheckError.png")
                return False
            else:
                # print "DOUBLE CHECKING CTG with TG: OK!"
                pass
        else:
            print ("DOUBLE CHECKING CTG with TG: \t\033[31mFAILED\033[0m")
            print ("CLUSTER", cluster, " DOESNT EXIST...!!!")
            Clustering_Reports.report_ctg(ctg, "CTG_DoubleCheckError.png")
            raise ValueError("DOUBLE CHECKING CTG with TG FAILED")
    return True