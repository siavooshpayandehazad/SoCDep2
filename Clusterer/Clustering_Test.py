# Copyright (C) 2015 Siavoosh Payandeh Azad

import ClusteringReports


def DoubleCheckCTG(TG, CTG):
    """
    Checks if the clusters info in TG matches with the information in the CTG.
    :param TG: Task Graph
    :param CTG: Clustered Task Graph
    :return:
    """
    for Task in TG.nodes():
        Cluster = TG.node[Task]['Cluster']
        if Cluster in CTG.nodes():
            if Task not in CTG.node[Cluster]['TaskList']:
                print ("DOUBLE CHECKING CTG with TG: \t\033[31mFAILED\033[0m")
                print ("TASK", Task, "DOES NOT EXIST IN CLUSTER:", Cluster)
                ClusteringReports.ReportCTG(CTG, "CTG_DoubleCheckError.png")
                return False
            else:
                print "DOUBLE CHECKING CTG with TG: OK!"
                pass
        else:
            print ("DOUBLE CHECKING CTG with TG: \t\033[31mFAILED\033[0m")
            print ("CLUSTER", Cluster, " DOESNT EXIST...!!!")
            ClusteringReports.ReportCTG(CTG, "CTG_DoubleCheckError.png")
            raise ValueError("DOUBLE CHECKING CTG with TG FAILED")
    return True