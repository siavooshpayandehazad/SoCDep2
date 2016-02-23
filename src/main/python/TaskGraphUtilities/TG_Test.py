# Copyright (C) 2015 Siavoosh Payandeh Azad
import networkx


def check_acyclic(tg,logging):
    if not networkx.is_directed_acyclic_graph(tg):
        raise ValueError('TASK GRAPH HAS CYCLES..!!!')
    else:
        logging.info("TG IS AN ACYCLIC DIRECTED GRAPH... ALL IS GOOD...")
    return None