from debt_1 import *

##for each creditor
##    create a queue of debtors names
##        for each debtor
##            create a list of children
##            sort list > by value owed
##            while money is owed to creditor and for each child
##                if child debt < debtor debt
##                    remove child from debtor's record
##                    add child debt to detors
##                    sub child debt from debtor's debt
##                elif child debt > debtor debt
##                    remove debtor from cred.'s record
##                    add debtor's debt to cred.'s record as child
##                    sub debtor's debt from debtor's record of child
##                else
##                    # child debt = debtor debt
##                    remove child from debtor's record
##                    add child debt to detors
##                    remove debtor from cred.'s record

def main():
    debtors = get_database()
    debtors, credit_table = solve(debtors)
    creditors = remap(debtors)
    # for each creditor
    for debtors in creditors.values():
        # create a queue of debtors names
        d_names = debtors.keys()
        # for each debtor
        while d_names:
            debtor = d_names.pop()
            if debtor in creditors:
                # create a list of children
                children = creditors[debtor].items()
                # sort list < by value owed
                children.sort(lambda x, y: cmp(x[1], y[1]))
                # for each child
                for child, child_debt in children:
                    if debtor not in debtors:
                        break
                    debtor_debt = debtors[debtor]
                    # while money is owed
                    if not debtor_debt:
                        break
                    if child_debt < debtor_debt:
                        # remove child from debtor's record
                        del creditors[debtor][child]
                        # add child debt to debtors
                        d_names.insert(0, child)
                        if child not in debtors:
                            debtors[child] = 0
                        debtors[child] += child_debt
                        # sub child debt from debtor's debt
                        debtors[debtor] -= child_debt
                    elif child_debt > debtor_debt:
                        # remove debtor from cred.'s record
                        del debtors[debtor]
                        # add debtor's debt to cred.'s record as child
                        d_names.insert(0, child)
                        if child not in debtors:
                            debtors[child] = 0
                        debtors[child] += debtor_debt
                        # sub debtor's debt from debtor's record of child
                        creditors[debtor][child] -= debtor_debt
                    else:
                        # child debt = debtor debt
                        # remove child from debtor's record
                        del creditors[debtor][child]
                        # add child debt to detors
                        d_names.insert(0, child)
                        if child not in debtors:
                            debtors[child] = 0
                        debtors[child] += child_debt
                        # remove debtor from cred.'s record
                        del debtors[debtor]
    debtors = remap(creditors)
    check_validity(debtors, credit_table)
    show(debtors)
                    
def remap(database):
    new_map = {}
    for debtor, creditors in database.items():
        for creditor, value in creditors.items():
            if creditor not in new_map:
                new_map[creditor] = {}
            creditor = new_map[creditor]
            if debtor not in creditor:
                creditor[debtor] = 0
            creditor[debtor] += value
    return new_map

if __name__ == '__main__':
    main()
