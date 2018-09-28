from graphviz import Digraph, Graph
import re
import math
import operator
import pytablewriter

class VZ(object):
    def __init__(self, path, way):
        self.path = path
        self.way = way
        if self.way > 0:
            self.arrowhead='teetee'
            self.arrowtail='crowodot'
        else:
            self.arrowhead='crowodot'
            self.arrowtail='teetee'
        self.pairs = set()


    def icons_to_FKs(self, cols, this_tbl, num_of_icons, icons_to_FKs, numerated_FKs):
        # STYLE='ROUNDED' removed
        cd = self.icons_dic()
        n = num_of_icons
        # numerated_FKs = {}
        # for k, v in sorted(numerated_FKs.iteritems()):
        #     print v, k
        if num_of_icons != 0:
            for c in sorted(cols):
                # print this_tbl + "." + c
                try:
                    icons_to_FKs[this_tbl + "." + c]
                except:
                    numerated_FKs[this_tbl + "." + c] = n
                    try:
                        icons_to_FKs[this_tbl + "." + c] = cd[numerated_FKs[this_tbl + "." + c]]
                    except:
                        if n > len(cd.keys()):
                            n = int(len(cd.keys())/2)
                            numerated_FKs[this_tbl + "." + c] = n
                            icons_to_FKs[this_tbl + "." + c] = cd[n]
                    n +=1
        # core table:  
        else:
            # generate icons dictionarry for the core table and pass number of icons (n) used:
            print "------- start with '"+this_tbl+"'----------"
            for c in sorted(cols):
                try:
                    numerated_FKs[this_tbl + "." + c]
                except:
                    numerated_FKs[this_tbl + "." + c] = n
                    n += 1
            # print "core", this_tbl, " ------------" , cols, icons_to_FKs            
            for c in sorted(cols):
                try: 
                    # icons_to_FKs[this_tbl + "." + c] += cd[numerated_FKs[this_tbl + "." + c]]
                    if cd[numerated_FKs[this_tbl + "." + c]] not in icons_to_FKs[this_tbl + "." + c]:
                        icons_to_FKs[this_tbl + "." + c] += cd[numerated_FKs[this_tbl + "." + c]]
                except:
                    icons_to_FKs[this_tbl + "." + c] = cd[numerated_FKs[this_tbl + "." + c]]

        return numerated_FKs, n, icons_to_FKs

    def icons_dic(self):
        return {0: u" \u2600", 1: u" \u2602", 2: u" \u2605",  3: u" \u260A", 4: u" \u2618", 5: u" \u2622", 6: u" \u265B", 7: u" \u266C", 
                8: u" \u2692", 9: u" \u2696", 10: u" \u265C", 11: u" \u26FF", 12: u" \u26B5", 13: u" \u2698", 14: u" \u2612", 15: u" \u262D", 
                16: u" \u2603", 17: u" \u2638", 18: u" \u2623", 19: u" \u2625", 20: u" \u2628", 21: u" \u2699", 22: u" \u2663", 23: u" \u2665",
                24: u" \u2666", 25: u" \u267C", 26: u" \u267B", 27: u" \u266F", 28: u" \u267D", 29: u" \u2694", 30: u" \u26B9",
                31: u" \u26BD", 32: u" \u26C3", 33: u" \u26C7", 34: u" \u26D1", 35: u" \u26D2", 
                36: u" \u263D", 37: u" \u26D6", 38: u" \u26DB", 39: u" \u22A1", 40: u" \u26E2", 41: u" \u26E8", 42: u" \u229B", 43: u" \u26EF",
                44: u" \u26F1", 45: u" \u262A", 46: u" \u26F7", 47: u" \u22B0", 48: u" \u26FC", 49: u" \u2691", 50: u" \u2689",
                51: u" \u2670", 52: u" \u265A", 53: u" \u263B", 54: u" \u2630", 55: u" \u262F", 
                56: u" \u262B", 57: u" \u262A", 58: u" \u2629", 59: u" \u2615", 60: u" \u22D5", 61: u" \u260E", 62: u" \u26C1", 63: u" \u2127",
                64: u" \u26C8", 65: u" \u26E2", 66: u" \u26E7", 67: u" \u26EC", 68: u" \u26B6", 69: u" \u203B", 70: u" \u058D",
                71: u" \u2318", 72: u" \u235D", 73: u" \u2332", 74: u" \u2D32", 75: u" \u3020", 
                76: u" \u2182", 77: u" \u21A2", 78: u" \u21A5", 79: u" \u21AF", 80: u" \u21C5", 81: u" \u21C7", 82: u" \u1C22", 83: u" \u1C15",
                84: u" \u1BFD", 85: u" \u13B2", 86: u" \u1BFE", 87: u" \u1C03", 88: u" \u1C07", 89: u" \u1C17", 90: u" \u1C20",
                91: u" \u1BD6", 92: u" \u1BE3", 93: u" \u1BE4", 94: u" \u1BE5", 95: u" \u2BCD", 
                96: u" \u1C14", 97: u" \u1C1C", 98: u" \u1C66", 99: u" \u1BCC", 100: u" \u1C6F", 101: u" \u1C75", 102: u" \u23F3", 103: u" \u2B16",
                104: u" \u2B57", 105: u" \u24DE", 106: u" \u25A3", 107: u" \u25A6", 108: u" \u25C9", 109: u" \u25D1", 110: u" \u25E9",
                111: u" \u25EE", 112: u" \u25C8", 113: u" \u25EC",
                114: u" \u2708", 115: u" \u2704", 116: u" \u2720", 117: u" \u2731", 118: u" \u2756", 119: u" \u23CF", 120: u" \u2764",                
                121: u" \u2736", 122: u" \u272A", 123: u" \u271A",
                124: u" \u27F0", 125: u" \u29D1", 126: u" \u2CED", 127: u" \u2D53", 128: u" \u2E99", 129: u" \u2ED9", 130: u" \u2BCC",                
                131: u" \u2C03", 132: u" \u2C16", 133: u" \u2C17",
                134: u" \u2A00", 135: u" \u2C14", 136: u" \u2C2D", 137: u" \u2D65", 138: u" \u2E90", 139: u" \u2EB5", 140: u" \u2EB8",
                141: u" \u2A02", 142: u" \u29FB", 143: u" \u29D7",
                144: u" \u2235", 145: u" \u2726", 146: u" \u271B", 147: u" \u2C00", 148: u" \u25CE", 149: u" \u24C4", 150: u" \u1C6C",
                151: u" \u2200", 152: u" \u2206", 153: u" \u2207", 154: u" \u2205", 155: u" \u220B", 156: u" \u2211", 157: u" \u2217", 158: u" \u221E", 159: u" \u2222", 160: u" \u222E",
                161: u" \u222F", 162: u" \u2237", 163: u" \u2234", 164: u" \u223A", 165: u" \u223E", 166: u" \u224B", 167: u" \u224D", 168: u" \u224E", 169: u" \u2263", 170: u" \u1CEA",
                171: u" \u2327", 172: u" \u2180", 173: u" \u218B", 174: u" \u21A3", 175: u" \u21BA", 176: u" \u21BB", 177: u" \u21C8", 178: u" \u21CA", 179: u" \u219D", 180: u" \u219F",
                181: u" \u13A7", 182: u" \u13BA", 183: u" \u13CC"
                }   #2670 262E   

    def colors_list(self):
        return ["#c6ecd7", "#b3e6ff", "#f2e6ff", "#ffe6cc", "#ffcce6", "#e6e6ff", "#ebccff", "#e0e0d1", "#ccccff", "#f2ffcc", "#80ffff", "#d1d1e0", "#ffeecc", "#c6d9ec", "#ffcc99", "#c2f0c2",
        "#c6ecd7", "#b3e6ff", "#f2e6ff", "#ffe6cc", "#ffcce6", "#e6e6ff", "#ebccff", "#e0e0d1", "#ccccff", "#f2ffcc", "#80ffff", "#d1d1e0", "#ffeecc", "#c6d9ec", "#ffcc99", "#c2f0c2",
        "#c6ecd7", "#b3e6ff", "#f2e6ff", "#ffe6cc", "#ffcce6", "#e6e6ff", "#ebccff", "#e0e0d1", "#ccccff", "#f2ffcc", "#80ffff", "#d1d1e0", "#ffeecc", "#c6d9ec", "#ffcc99", "#c2f0c2"]

    def table_styling(self, this_tbl, icons_to_FKs, nodes):

        # STYLE='ROUNDED' removed
        title = "<<TABLE STYLE='ROUNDED' BORDER='1' CELLBORDER='0' CELLSPACING='0' CELLPADDING='2' BGCOLOR='#EAF0F6' COLOR='#808080'><TR><TD COLSPAN='2' BGCOLOR='#A8C7EF' STYLE='ROUNDED' BORDER='1' SIDES='B'><FONT FACE='arial' POINT-SIZE='12'>%s</FONT></TD></TR>" % this_tbl
        t_formated = ""
        for fk in sorted(icons_to_FKs.keys()):
            t, c = fk.split(".")
            if t == this_tbl:
                t_formated += "<TR><TD ALIGN='LEFT' CELLSPACING='3'><FONT FACE='arial' POINT-SIZE='11'>%s</FONT></TD><TD ALIGN='RIGHT' CELLSPACING='4'><FONT POINT-SIZE='11' COLOR='#555555'>%s</FONT></TD></TR>" % (c, icons_to_FKs[fk])
        table = title + t_formated + "</TABLE>>" 
        return table

    def gather_edges(self, fk, t1, t2, args, icon, edges):
        if t1 == 0:    
            return edges
        edge = "-".join([fk, t1, t2])
        try:
            edges[edge]
        except:
            edges.update({ edge : [args, icon] })
        return edges

    def gather_nodes(self, node, args, cluster, nodes, numerated_FKs, icons_to_FKs):
        if node == 0:
            return nodes
        try:
            nodes[node]            
            nodes[node][0]['label'] = self.table_styling(node, icons_to_FKs, nodes)
        except:
            args['label'] = self.table_styling(node, icons_to_FKs, nodes)
            nodes[node] = [args, cluster]
        return nodes

    def graph_core(self, tables, this_tbl, dot, level, num_of_icons, t_cols_r, icons_to_FKs, numerated_FKs, prnt_tbl, edges, nodes):
        # print "#1", num_of_icons
        cd = self.icons_dic()
        numerated_FKs, num_of_icons, icons_to_FKs = self.icons_to_FKs(tables[this_tbl].keys(), this_tbl, num_of_icons, icons_to_FKs, numerated_FKs)
        # print "#2", num_of_icons
        # if there is several connections from the same table to the same column:
        this_tbl_children = []
        for c, [t_r, c_r] in sorted(tables[this_tbl].iteritems()):
            this_tbl_children.append(t_r)

        prnt_tbl_children = []
        if prnt_tbl != "init":
            for c, [t_r, c_r] in sorted(tables[prnt_tbl].iteritems()):
                prnt_tbl_children.append(t_r)

        # icons for references between kids:
        # c here is a FK in this_tbl:
        for c, [t_r, c_r] in sorted(tables[this_tbl].iteritems()):
            try:
                # if there are relations between children tables then we generate icons dictionary for them:
                for i_c, [i_t_r, i_c_r] in tables[t_r].iteritems():
                    if i_t_r in this_tbl_children or i_t_r == this_tbl or i_t_r in prnt_tbl_children:
                            # if t_r != this_tbl:  # - to not mess into already generated for this_tbl icons
                            if t_r != this_tbl:  # - to not mess into already generated for this_tbl icons
                                try: 
                                    numerated_FKs[t_r + "." + i_c]
                                except:    
                                    numerated_FKs[t_r + "." + i_c] = num_of_icons
                                    num_of_icons += 1
                            try:
                                numerated_FKs[i_t_r + "." + i_c_r] # the same icon for ref
                            except:
                                numerated_FKs[i_t_r + "." + i_c_r] = num_of_icons
                                num_of_icons += 1

                            try:
                                numerated_FKs[t_r + "." + c_r] # the same icon for ref
                            except:
                                numerated_FKs[t_r + "." + c_r] = num_of_icons
                                num_of_icons += 1

                            if i_t_r == t_r:
                                numerated_FKs[i_t_r + "." + i_c_r] = numerated_FKs[t_r + "." + i_c]
            except:
                pass
        for cln, [t_r, c_r] in sorted(tables[this_tbl].iteritems()):
            t_cols = [c_r]
            try:
                # if there are relations between children tables:print "#3", num_of_icons
                # if there is a connection back:
                for i_c, [i_t_r, i_c_r] in tables[t_r].iteritems():
                    if i_t_r in this_tbl_children or i_t_r == this_tbl or i_t_r in prnt_tbl_children:
                        t_cols.append(i_c)
                        headlabel = cd[numerated_FKs[t_r + "." + i_c]]
                        # icon for i_c should be different!
                        icons_to_FKs[t_r + "." + i_c] = cd[numerated_FKs[t_r + "." + i_c]] # ! important !
                        # self-connection:
                        style = "dashed"
                        if i_c == i_c_r == "id" or i_c.split(u" \u2190 ")[0] == i_c_r == "id":
                            style = "solid"
                        # dot.edge(i_t_r, t_r, style="invis")
                        if i_t_r == this_tbl and i_t_r not in this_tbl_children:
                            # print t_r + "." + i_c, " - [EDGE] back to: ", i_t_r + "." + i_c_r 
                            # headlabel = cd[numerated_FKs[i_t_r + "." + i_c_r]]
                            args = {"arrowhead": self.arrowtail, "arrowtail": self.arrowhead, "dir": 'both', "arrowsize": '0.5', "penwidth": '0.5', "headlabel": " " + headlabel, "labelfontsize": '14', "color": '#2F4F4F', "weight": '0', "style": style}
                            edges = self.gather_edges(i_c_r, i_t_r, t_r, args, headlabel, edges)
                        else:
                            args = {"arrowhead": self.arrowhead, "arrowtail": self.arrowtail, "dir": 'both', "arrowsize": '0.5', "penwidth": '0.5', "headlabel": " " + headlabel, "labelfontsize": '14', "color": '#2F4F4F', "weight": '0', "style": style}
                            edges = self.gather_edges(i_c, t_r, i_t_r, args, headlabel, edges)
                        # update icons sets for c_r in t_r if the icon is not already there as a column may self-reference the same table:            
                        if (i_t_r != t_r and t_r != this_tbl):
                            try: 
                                if headlabel not in icons_to_FKs[i_t_r + "." + i_c_r]:
                                    icons_to_FKs[i_t_r + "." + i_c_r] = headlabel + icons_to_FKs[i_t_r + "." + i_c_r]
                            except:
                                icons_to_FKs[i_t_r + "." + i_c_r] = headlabel
                        # update icons sets for i_c_r in i_t_r=this_tbl and for i_c in t_r if the icon is not already there as a column may self-reference the same table:
                        if i_t_r == this_tbl:
                            try:
                                if headlabel not in icons_to_FKs[t_r + "." + i_c]:
                                    icons_to_FKs[t_r + "." + i_c] = headlabel + icons_to_FKs[t_r + "." + i_c]
                            except:
                                icons_to_FKs[t_r + "." + i_c] = headlabel

            except Exception, e:
                pass
                print this_tbl + " ran out of ER level for: " + t_r, e
            # all clns with connections in t_r:
            t_cols_r[t_r] = t_cols
            # update icons sets for cln in this_tbl if the icon is not already there as a column may self-reference the same table:
            ## [this_tbl , cln] -> [t_r , c_r]
            try: 
                if cd[numerated_FKs[this_tbl + "." + cln]] not in icons_to_FKs[t_r + "." + c_r]:
                    icons_to_FKs[t_r + "." + c_r] = cd[numerated_FKs[this_tbl + "." + cln]] + icons_to_FKs[t_r + "." + c_r]
            except Exception, e:
                icons_to_FKs[t_r + "." + c_r] = cd[numerated_FKs[this_tbl + "." + cln]]

            try: # icon_cols[t_r + "." + c_r] exists
                try:
                    # update icons sets for this column if the icon is not already there as a column may self-reference the same table:
                    if cd[numerated_FKs[t_r + "." + c_r]] not in icons_to_FKs[t_r + "." + c_r]:
                        icons_to_FKs[t_r + "." + c_r] = cd[numerated_FKs[t_r + "." + c_r]] + c_set[t_r + "." + c_r]
                except:
                    try:
                        icons_to_FKs[t_r + "." + c_r] += cd[numerated_FKs[t_r + "." + c_r]] # ! important !
                    except Exception, E: 
                        # print "----  </// ----", e
                        icons_to_FKs[t_r + "." + c_r] = cd[numerated_FKs[t_r + "." + c_r]]
            except Exception, e:
                # print "----  <> ----", e
                pass
        n_args = {"shape" : "plaintext", "penwidth" : '0.5'}
        nodes = self.gather_nodes(this_tbl, n_args, 0, nodes, 0, icons_to_FKs)
        for c, [t_r, c_r] in sorted(tables[this_tbl].iteritems()):  
            t_cols = t_cols_r[t_r]
            this_numerated_FKs, num_of_icons, icons_to_FKs = self.icons_to_FKs(t_cols_r[t_r], t_r, num_of_icons, icons_to_FKs, numerated_FKs)

            n_args = {"shape" : "plaintext", "penwidth" : '0.5'}
            if this_tbl == t_r:
                nodes = self.gather_nodes(t_r, n_args, level, nodes, numerated_FKs, icons_to_FKs)
            if this_tbl != t_r:
                cluster = 1
                if level > 2:
                    cluster = 2
                nodes = self.gather_nodes(t_r, n_args, cluster, nodes, numerated_FKs, icons_to_FKs)
                style = "dashed"
                if c == c_r == "id" or c.split(u" \u2190 ")[0] == c_r == "id":
                    style = "solid"
                args = {"arrowhead" : self.arrowhead, "arrowtail" : self.arrowtail, "dir" : 'both', "arrowsize": '0.5', "penwidth" : '0.5', 
                          "headlabel" : " " + cd[numerated_FKs[this_tbl + "." + c]], "color" : '#204A87', "labelfontsize" : '14', "style" : style}
                edges = self.gather_edges(c, this_tbl, t_r, args, cd[numerated_FKs[this_tbl + "." + c]], edges)
        # to not break args/label this loop should go separately:
        # check for already collected args['label'] node which might have updates in icons_to_FKs due to backward connections from the next level:
        for c, [t_r, c_r] in sorted(tables[this_tbl].iteritems()):  
            if this_tbl != t_r:
                if level > 2:
                    cluster = 2
                    if t_r not in prnt_tbl_children:
                        for i_c, [i_t_r, i_c_r] in tables[t_r].iteritems():
                            if i_t_r in prnt_tbl_children and i_t_r != this_tbl:
                                print "- - - -", i_t_r 
                                args = {"shape" : "plaintext", "penwidth" : '0.5'}
                                # numerated_FKs, num_of_icons, icons_to_FKs = self.icons_to_FKs(t_cols_r[i_t_r], i_t_r, num_of_icons, icons_to_FKs, numerated_FKs)
                                args['label'] = self.table_styling(i_t_r, icons_to_FKs, nodes)
                                nodes[i_t_r][0] = args
            # n_args = {"shape" : "plaintext", "penwidth" : '0.5'}
            # this_numerated_FKs, num_of_icons, icons_to_FKs = self.icons_to_FKs(t_cols_r[t_r], t_r, num_of_icons, icons_to_FKs, numerated_FKs)
            # nodes = self.gather_nodes(t_r, n_args, cluster, nodes, numerated_FKs, icons_to_FKs)


        c_t = {}
        # num_of_icons += 1
        for c, [n_t_r, c_r] in sorted(tables[this_tbl].iteritems()):  
            if level == 2:
                if n_t_r != this_tbl:
                    try:
                        c_t[n_t_r]
                    except:    
                        c_t[n_t_r] = 1
                        try:
                            print "--- going with", n_t_r, level, num_of_icons
                            next_level = level + 1
                            dot, edges, nodes, this_num_of_icons = self.graph_core(tables, n_t_r, dot, next_level, num_of_icons, t_cols_r, icons_to_FKs, numerated_FKs, this_tbl, edges, nodes)
                            print "--- end with", n_t_r, level, num_of_icons
                        except Exception, e:
                            # this_tbl_r has no FKs
                            print "--- end for ", n_t_r
                            print "out of its level:", e
                            # pass
                        # to make sure icons are not the same in the restart of collecting them for a new node:
                        num_of_icons += math.ceil(len(edges)/2.0)
        return dot, edges, nodes, num_of_icons


    def draw_to_cluster(self, dot, num, attrs, tbl, color):
        with dot.subgraph(name="cluster_" + num) as lvl:
            for k, v in attrs.iteritems():
                lvl.node_attr[k] = v
            lvl.node(tbl)
            lvl.attr(color=color,  style='filled')
        return dot


    def diagram_draw(self, tables, level):
        # tables are: tables[t_c] = {c_c: [t_p, c_p]}
        for this_tbl in tables.keys():
            # this_tbl = "appointments"
            # this_tbl = "employment_contracts"
            # this_tbl = "payments"
            # this_tbl = "patients"
            # this_tbl = "legal_entity"            
            dot = Digraph()
            if level == 1:
                dot.attr(rankdir="TB")
            else:
                dot.attr(rankdir="LR")
            # dictionary of columns(FKs) of tables: 
            t_cols_r = {}
            icons_to_FKs = {}
            numerated_FKs ={}
            edges = {}
            nodes = {}
            # level - is a levels number, 
            # num_of_icons - number of icons appended to FKs, starts with 0 here
            # t_cols_r - FKs to tables
            dot, edges, node, num_of_icons = self.graph_core(tables, this_tbl, dot, level, 0, t_cols_r, icons_to_FKs, numerated_FKs, "init", edges, nodes)
            """
            draw nodes:
            """
            cluster_1 = []
            nodes = self.gather_nodes(0,0,0,nodes,0,0)
            print len(nodes), ": number of nodes"
            for tbl in sorted(nodes.keys()):
                attrs = nodes[tbl]
                if attrs[1] == 0:
                    with dot.subgraph(name="cluster_" + str(attrs[1])) as lvl:
                        for k, v in attrs[0].iteritems():
                            lvl.node_attr[k] = v
                        lvl.node(tbl)
                        lvl.attr(color="white",  style='filled') 

            first_cluster_tables = []
            for tbl in sorted(nodes.keys()):
                attrs = nodes[tbl]
                if attrs[1] == 1:
                    first_cluster_tables.append(tbl)
                    # print "1 +++++++++++++++", tbl, attrs[0]
                    dot = self.draw_to_cluster(dot, str(attrs[1]), attrs[0], tbl, "#DBE3EE")            

            if level != 1:
                # align nodes of the first_cluster_tables in a row:
                with dot.subgraph(name="cluster_1") as lvl:
                    c = Digraph()
                    for nd in first_cluster_tables:
                        c.node(nd)
                    c.attr(rank='same')
                    lvl.subgraph(c)    

            for tbl in sorted(nodes.keys()):
                attrs = nodes[tbl]
                if attrs[1] == 2:
                    # print "2 +++++++++++++++", tbl, attrs[0]
                    dot = self.draw_to_cluster(dot, str(attrs[1]), attrs[0], tbl, "#DEF2EA")
            """
            draw edges:
            """
            print len(self.gather_edges(0,0,0,0,0,edges).keys()), ": number of edges"
            
            for e, attrs in self.gather_edges(0,0,0,0,0,edges).iteritems():
                fk, t1, t2 = e.split("-")
                if t1 == this_tbl:
                    with dot.subgraph() as lvl: 
                        for k, v in attrs[0].iteritems():
                            lvl.edge_attr[k] = v
                        lvl.edge(t1, t2)

            for e, attrs in self.gather_edges(0,0,0,0,0,edges).iteritems():
                fk, t1, t2 = e.split("-")
                if t1 != this_tbl and t2 != this_tbl:   
                    with dot.subgraph() as lvl: 
                        for k, v in attrs[0].iteritems():
                            lvl.edge_attr[k] = v
                        lvl.edge(t1, t2)

            dot.format = 'png'
            dot.render(self.path + this_tbl)
            print "diagram and png image with the core table '%s' is generated in %s" % (this_tbl, self.path)


    def reduce_graph(self, tables, b_tables, fertiles_numbered, fertiles, lessers):
        if len(lessers.keys()) > 0:
            fat_t = ""
            for t in fertiles.keys():
                if fertiles_numbered[t] == 1:
                    fat_t = t
            fertiles.pop(fat_t)
            fertiles_numbered.pop(fat_t)
            for t in lessers.keys() + fertiles.keys():
                try:
                    listed = lessers[t].remove(fat_t)
                    lessers[t] = listed
                except:
                    pass
        
            new_tables = {}
            new_b_tables = {}
            for tbl in tables.keys():
                for c, [t_r, c_r] in tables[tbl].iteritems():
                    if t_r != fat_t:
                        try:
                            new_tables[tbl].update({c: [t_r, c_r]})
                        except:
                            new_tables[tbl] = {c: [t_r, c_r]}
            tables = new_tables

            for tbl in b_tables.keys():
                for c, [t_r, c_r] in b_tables[tbl].iteritems():
                    if t_r != fat_t:
                        try:
                            new_b_tables[tbl].update({c: [t_r, c_r]})
                        except:
                            new_b_tables[tbl] = {c: [t_r, c_r]}
            b_tables = new_b_tables

        return tables, b_tables, fertiles_numbered, fertiles, lessers


    def make_tables_graph(self, tables, b_tables, tbl, graph):
        try:
            graph[tbl]
        except:
            graph[tbl] = []
        for t in tables, b_tables:
            try:
                for c, [t_r, c_r] in t[tbl].iteritems():
                    if t_r != tbl and t_r not in graph[tbl]:
                        graph[tbl].append(t_r)
            except:
                pass
        return graph


    def find_paths(self, graph, start, end, length, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = self.find_paths(graph, node, end, length, path)
                for newpath in newpaths:
                    if len(newpath) < length + 1:
                        paths.append(newpath)
        return paths


    def closest_rels(self, graph, t1, t2, fertiles, g_closest_rels = [], iterated = []):
        while len(g_closest_rels) < 15: # this threshold is defined by the most connected tables having 10 and more connections + some lapse to make sure isolated clusters are encompassed
            try:
                g_closest_rels.index(t2)
                return g_closest_rels
            except:
                iterated = iterated + [t1]
                try: 
                    for this in graph[t1]:
                        if this not in g_closest_rels: 
                            g_closest_rels.append(this)
                except:
                    pass
                if t1 not in g_closest_rels:
                    g_closest_rels.append(t1)
                else:
                    return g_closest_rels
                # print "rels", len(graph[t1]), t1, g_closest_rels
                for t in g_closest_rels: 
                    if not fertiles.has_key(t) and t not in iterated:
                        g_closest_rels = self.closest_rels(graph, t, t2, fertiles, g_closest_rels, iterated)
        return g_closest_rels


    def table_output(self, matrix, num):
      writer = pytablewriter.MarkdownTableWriter()
      writer.table_name = 'the most connected tables:' 
      writer.header_list = ["num", "table", "number of in/out connections"]
      writer.value_matrix = matrix
      writer.margin = 1
      writer.write_table()

    def graph_clusters(self, fertiles_numbered, fertiles, seconds, dot, this_tables, drawn_nodes, drawn_edges, clean, dr):
        for tbl, k in sorted(fertiles_numbered.iteritems(), key=lambda x: x[1], reverse=True):
            cluster = str(k + 1)
            try:
                for c, [t_r, c_r] in this_tables[tbl].iteritems():
                    edge = [t_r, tbl] 
                    arrowhead='teetee'
                    arrowtail='crowodot'
                    if dr == -1:
                        edge = [tbl, t_r]
                        arrowhead='crowodot'
                        arrowtail='teetee'
                    style = "dashed"
                    if re.search(u" \u2190 ", c):
                        c, tt = c.split(u" \u2190 ")
                    if c_r == c == "id":
                        style = "solid"
                    dd = Digraph()
                    if t_r not in fertiles.keys() and t_r not in drawn_nodes:
                        with dot.subgraph(name="cluster_" + cluster) as lvl:
                            dd.node(t_r, label=t_r, shape="box", penwidth='0.5', style="rounded,filled", fillcolor=self.colorscale(self.colors_list()[fertiles_numbered[tbl]], 1.1))
                            drawn_nodes.append(t_r)
                            seconds[cluster].append(t_r)
                            if [t_r, tbl] not in drawn_edges:
                                dd.edge(tbl, t_r, arrowhead=arrowhead, arrowtail=arrowtail, dir='both', arrowsize='0.5', penwidth ='1', style=style, color="#9900cc")
                                drawn_edges.append(edge)
                            lvl.subgraph(dd)
                    else:
                        if edge not in drawn_edges: # and (clean == 0 or (clean == 1 and fertiles_numbered[tbl] != 1)):
                            headlabel = "[ " + tbl + " ]\n"
                            if dr == -1:
                                headlabel = "[ " + t_r + " ]\n"
                            if clean == 1 or tbl == t_r:
                                headlabel = ""    
                            dot.edge(tbl, t_r, arrowhead=arrowhead, arrowtail=arrowtail, headlabel=headlabel, dir='both', arrowsize='0.5', 
                                    penwidth ='2', style=style, color=self.colorscale(self.colors_list()[fertiles_numbered[tbl]], 0.75), labelfontsize='9', labeldistance='1.5', labelangle="75")
                            drawn_edges.append(edge)
            except:
                pass
        return dot, drawn_nodes, drawn_edges, seconds


    def lesser_edges(self, lessers, seconds, dot, this_tables, drawn_edges, dr):
        for tbl in lessers.keys():
            try:
                for c, [t_r, c_r] in this_tables[tbl].iteritems():
                    edge = [t_r, tbl] 
                    arrowhead='teetee'
                    arrowtail='crowodot'
                    if dr == -1:
                        edge = [tbl, t_r]
                        arrowhead='crowodot'
                        arrowtail='teetee'
                    style = "dashed"
                    if re.search(u" \u2190 ", c):
                        c, tt = c.split(u" \u2190 ")
                    if c_r == c == "id":
                        style = "solid"
                    if edge not in drawn_edges:
                        color = "#33334d"
                        for lst in seconds.values(): 
                            if t_r in lst or tbl in lst:
                                color = "#438c50"
                        headlabel = "[ " + tbl + " ]\n"    
                        if dr == -1:
                            headlabel = "[ " + t_r + " ]\n"                                
                        dot.edge(tbl, t_r, arrowhead=arrowhead, arrowtail=arrowtail, headlabel=headlabel, dir='both', arrowsize='0.5', penwidth ='1', style=style, color=color, labelfontsize='9')
                        drawn_edges.append(edge)
            except:
                pass
        return dot, drawn_edges


    def clamp(self, val, minimum=0, maximum=255):
        if val < minimum:
            return minimum
        if val > maximum:
            return maximum
        return val

    def colorscale(self, hexstr, scalefactor):
        """
        [thanks to thadeusb.com/weblog/2010/10/10/python_scale_hex_color/]
        Scales a hex string by ``scalefactor``. Returns scaled hex string.
        To darken the color, use a float value between 0 and 1.
        To brighten the color, use a float value greater than 1.
        >>> colorscale("#DF3C3C", .5)
        #6F1E1E
        >>> colorscale("#52D24F", 1.6)
        #83FF7E
        >>> colorscale("#4F75D2", 1)
        #4F75D2
        """
        hexstr = hexstr.strip('#')
        if scalefactor < 0 or len(hexstr) != 6:
            return hexstr
        r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)
        r = self.clamp(r * scalefactor)
        g = self.clamp(g * scalefactor)
        b = self.clamp(b * scalefactor)
        return "#%02x%02x%02x" % (r, g, b)

    def paths_draw(self, tables, b_tables, couple, length, depth, clean):
        t1, t2 = couple
        # next_tables= self.make_closest_rels(tables, b_tables, next_t)
        this_level = {}
        # paths = {0 : t1 + " >> "}
        graph = {}
        for tbl in tables.keys() + b_tables.keys():
            graph = self.make_tables_graph(tables, b_tables, tbl, graph)

        print "\nnumber of all connected tables (our grapth):", len(graph.keys()), "\n"
        graph_size = {}
        for t in graph.keys():
            graph_size[t] = len(graph[t])

        # sorting by relations number:
        sorted_graph = sorted(graph_size.items(), key=operator.itemgetter(1), reverse=True)
        fertiles = {}
        lessers = {}
        matrix = []
        fertiles_numbered = {}
        num_f = 1
        for t, l in sorted_graph:
            if l >= depth:
                matrix.append(tuple([num_f,t,l]))
                fertiles[t] = graph[t]
                fertiles_numbered[t] = num_f
                num_f += 1
            else:
                lessers[t] = graph[t]
            if t == t1 or t == t2:
                lessers[t] = graph[t]

        # removing most connected node:
        if clean == 2:
            tables, b_tables, fertiles_numbered, fertiles, lessers = self.reduce_graph(tables, b_tables, fertiles_numbered, fertiles, lessers)
        
        self.table_output(matrix, 2)

        g_closest_rels = self.closest_rels(lessers, t1, t2, fertiles)

        print "closest relations for '" + t1 + "':", sorted(g_closest_rels + [t2])
        # print sorted(g_closest_rels).index(t1)
        min_graph = {}

        for t in graph.keys():
            if t in g_closest_rels or t in fertiles.keys():
                min_graph[t] = graph[t]
        print "found paths:\n"
        paths = self.find_paths(min_graph, t1, t2, length)
        if t2 in graph[t1]:
            paths.append([t1, t2])
        n = 0
        for p in paths:
            print n, ":", p
            n += 1

        print "drawing full connections graph:"
        dot = Digraph()
        dot.attr(pad=".1", ranksep="2.25", nodesep="0.25", rankdir="RL")
        drawn_nodes = []
        drawn_edges = []
        for tbl in fertiles.keys():
            attrs = {"label": tbl, "shape" : "rect", "penwidth" : '0.5'}
            dot = self.draw_to_cluster(dot, str(fertiles_numbered[tbl] + 1), attrs, tbl, self.colors_list()[fertiles_numbered[tbl]])
            dot.node(tbl, fillcolor=self.colorscale(self.colors_list()[fertiles_numbered[tbl]], 0.9), style="rounded,filled", margin='0.2')
            drawn_nodes.append(tbl)

        seconds = {}
        for nf in range(1, num_f+1):
            seconds[str(nf)] = []
        positions = ["n","ne","e","se","s","sw","w","nw","c","_"]

        # for tbl, k in sorted(fertiles_numbered.iteritems(), key=lambda x: x[1], reverse=True):
        dot, drawn_nodes, drawn_edges, seconds = self.graph_clusters(fertiles_numbered, fertiles, seconds, dot, tables, drawn_nodes, drawn_edges, clean, 1)
        dot, drawn_nodes, drawn_edges, seconds = self.graph_clusters(fertiles_numbered, fertiles, seconds, dot, b_tables, drawn_nodes, drawn_edges, clean, -1)                      

        for tbl in lessers.keys():
            if tbl not in drawn_nodes:
                dot.node(tbl, label=tbl, shape="box", penwidth='0.5', style="rounded,filled")
                drawn_nodes.append(tbl)

        dot, drawn_edges = self.lesser_edges(lessers, seconds, dot, tables, drawn_edges, 1)
        dot, drawn_edges = self.lesser_edges(lessers, seconds, dot, b_tables, drawn_edges, -1)

        dot.format = 'pdf'
        dot.render(self.path + "DB" + str(depth) + "_" + str(clean))

        print "if the table name contains $-sign, put it like 'table_name' (in single-quotes)"
