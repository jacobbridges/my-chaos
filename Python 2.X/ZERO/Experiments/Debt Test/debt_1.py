# BUILD and CLEAN database
# BUILD integrity database
# RUN debt minimizer loops
# ASSERT database validity
# SHOW the database legers

def main():
    database = get_database()
    database, credit_table = solve(database)
    show(database)

def solve(database):
    prune_zs(database)
    fix_negs(database)
    fix_loop_n_none(database)
    credit_table = credit_report(database)
    while True:
        # get loops and detect time to stop
        loops = get_database_loops(database)
        if not loops:
            break
        # make the processing order
        all_runs = []
        for runs in loops:
            for run in runs:
                # the last element is not needed
                all_runs.append(run[:-1])
        # sort the runs
        sorted_runs = sort_runs(all_runs)
        # prune the runs
        min_runs = prune_runs(sorted_runs)
        # process all of the runs
        for run in min_runs:
            min_debt = find_min_debt(database, run)
            sub_from_run(min_debt, database, run)
        # clean the database
        prune_zs(database)
        fix_loop_n_none(database)
    return database, check_validity(database, credit_table)

def check_validity(database, credit_table):
    new_report = credit_report(database)
    for debtor, credit in credit_table.items():
        # check the work
        if credit:
            assert credit == new_report[debtor]
        elif debtor in new_report:
            assert new_report[debtor] == 0
    return new_report

def show(database):
    for debtor in sorted(database.keys()):
        # print the results
        print '\n', debtor, 'owes the following:'
        creditors = database[debtor]
        for creditor in sorted(creditors.keys()):
            print '    %s to %s.' % (creditors[creditor], creditor)

################################################################################

# INPUT LOOPS

def get_database():
    database = {}
    while True:
        try:
            debtor = raw_input('New debtor? ')
            if not debtor:
                return database
            assert debtor not in database
            creditors = get_creditors()
            database[debtor] = creditors
        except:
            pass

def get_creditors():
    creditors = {}
    while True:
        try:
            debtor = raw_input('New creditor? ')
            if not debtor:
                return creditors
            assert debtor not in creditors
            creditor = get_debt()
            creditors[debtor] = creditor
        except:
            pass

def get_debt():
    while True:
        try:
            string = raw_input('Value? ')
            if not string:
                return 0
            creditor = int(string)
            return creditor
        except:
            pass

################################################################################

# DATABASE CLEANERS

def prune_zs(database):
    for creditors in database.values():
        for key, value in creditors.items():
            if value == 0:
                del creditors[key]

def fix_negs(database):
    for database_key, database_value in database.items():
        creditors = database_value
        for key, value in creditors.items():
            if value < 0:
                del creditors[key]
                creditors_key = key
                update(database, creditors_key, database_key, -value)

def update(database, database_key, creditors_key, value):
    if database_key not in database:
        database[database_key] = {}
    creditors = database[database_key]
    if creditors_key not in creditors:
        creditors[creditors_key] = 0
    creditors[creditors_key] += value

def fix_loop_n_none(database):
    for key, value in database.items():
        if key in value:
            del value[key]
        if not value:
            del database[key]

################################################################################

# INTEGRITY DATABASE

def credit_report(database):
    people = {}
    for debtor, creditors in database.items():
        for creditor, value in creditors.items():
            cr_help(people, creditor, value)
            cr_help(people, debtor, -value)
    return people

def cr_help(people, person, value):
    if person not in people:
        people[person] = 0
    people[person] += value

################################################################################

# DEBT LOOPS

def get_database_loops(database):
    loops = []
    for debtor, creditors in database.items():
        loop = get_creditors_loops(database, debtor, creditors)
        if loop:
            loops.append(loop)
    return loops

def get_creditors_loops(database, debtor, creditors):
    runs = []
    # pump init
    for creditor in creditors.keys():
        runs.append([debtor, creditor])
    # go over runs until dead end, debtor loop, or internal loop
    while True:
        cancel = 0
        for run in runs[:]:
            if run[0] == run[-1]:
                # this is a loop
                cancel += 1
                continue
            new_debtor = run[-1]
            if new_debtor not in database:
                # dead end -- no loop
                runs.remove(run)
            else:
                new_creditors = database[new_debtor]
                runs.remove(run)
                # new copies will be inserted
                for creditor in new_creditors.keys():
                    if creditor == run[0]:
                        # we have a loop; add it to runs
                        runs.append(run[:] + [creditor])
                    elif creditor in run:
                        # we have an internal loop; ignore
                        pass
                    else:
                        # build a new run
                        runs.append(run[:] + [creditor])
        if cancel == len(runs):
            return runs

################################################################################

# REMOVE DUPLICATES

def sort_runs(runs):
    sort = []
    for run in runs:
        mini = min(run)
        if mini != run[0]:
            min_index = run.index(mini)
            first = run[min_index:]
            second = run[:min_index]
            sort.append(first + second)
        else:
            sort.append(run)
    return sort

def prune_runs(runs):
    pruned = []
    for run in runs:
        if run not in pruned:
            pruned.append(run)
    return pruned

################################################################################

# DEBT MINIMIZER

def find_min_debt(database, run):
    min_debt = database[run[0]][run[1]]
    for index in range(1, len(run) - 1):
        value = database[run[index]][run[index+1]]
        min_debt = min(value, min_debt)
    value = database[run[-1]][run[0]]
    min_debt = min(value, min_debt)
    return min_debt

def sub_from_run(value, database, run):
    for index in range(len(run) - 1):
        creditors_key = run[index]
        debt_key = run[index + 1]
        database[creditors_key][debt_key] -= value
    database[run[-1]][run[0]] -= value

################################################################################
        
if __name__ == '__main__':
    main()
