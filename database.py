"""
    Usage:
        database status [NAME] [--dbtype=DBS]
        database create [—-dbname=NAME]
            [—-dbtype=DBS]
            [--username=USERNAME]
            [—-passwd=PASSWD]
                        [—-nodes=NUM]
                        [--secgroup=SECGROUPs]
                        [—-tags=TAGS]
        database describe[—-dbname=NAME]
            [—dbtype=DBS]
        database delete[—-dbname=NAME]
            [—dbtype=DBS]
        database modify [—-dbname=NAME]
            [—dbtype=DBS]
            [—-passwd=PASSWD]
            [—-nodes=NUM]
            [--secgroup=SECGROUPs]
            [—-tags=TAGS]
        Arguments:
            NAME           database name. By default it is set to the name of last database.
        Options
            —-dbtype=DBS   the type of the cloud database (RedShift and others)
            --username=USERNAME   the username of the admin user of the database
            —-passwd=PASSWD   the password of the admin user of the database
            --secgroup=SECGROUP    security group name for the database
            --nodes=NUM    the count of nodes of the database
            —-tags=TAGS    the database tags
        Description:
            commands used to create, modify, delete, describe databases of a cloud
            database  status 
                Gets status of the database
            database  create [options…] 
                Creates a cloud database
            database  describe [options…] 
                Describes a cloud database, including options, details, and configuration
            database  delete [options…] 
                Deletes (and destroys) a cloud database
            database  modify [options…] 
                Modifies options in a cloud database 

""" 
from docopt import docopt

#if __name__ == '__main__':
#    options, arguments = docopt(__doc__)  # parse arguments based on docstring above

#    print(options)
#    print(arguments)

def main():
    # docopt saves arguments and options as key:value pairs in a dictionary
    args = docopt(__doc__, version='0.1')
    #verbose = args['--verbose']
    verbose = True
    name = args['<name>']
    if verbose:
        print('You are about to be reminded to document your code')
    # do the thing
    if args['--eternal']:
        if verbose:
            print('This may take a while...')
        while True:
            print(f'Document your code, {name}!')
    else:
        for _ in range(int(args['--n_reminders'])):
            print(f'Document your code, {name}')
    if verbose:
        print('You have been reminded to document your code')

if __name__=='__main__':
    main()
