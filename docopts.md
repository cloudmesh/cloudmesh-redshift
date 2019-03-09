"""
        ::
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
