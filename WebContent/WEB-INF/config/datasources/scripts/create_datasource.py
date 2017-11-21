# Licensed Materials - Property of IBM 
# 5724-O03
# (C) Copyright 2010. IBM Corp. All rights reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP
# Schedule Contract with IBM Corp.
#
# The Program may contain sample source code or programs, which illustrate programming techniques.
# You may only copy, modify, and distribute these samples internally. These samples have not been
# tested under all conditions and are provided to you by IBM without obligation of support of any
# kind.
#
# IBM PROVIDES THESE SAMPLES "AS IS" SUBJECT TO ANY STATUTORY WARRANTIES THAT CANNOT BE EXCLUDED.
# IBM MAKES NO WARRANTIES OR CONDITIONS, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NON-INFRINGEMENT REGARDING THESE SAMPLES OR TECHNICAL SUPPORT, IF ANY.


import os
import re
import sys

def fixupOsType():

    thisOs = java.lang.System.getProperty( "os.name" )
    print '***** JVM is reporting the OS name as %s *****' % (thisOs)

    windowsServerOsPattern = r"Windows.*(2003|2008|Vista|7)"
    
    if re.match( windowsServerOsPattern, thisOs ):
        print '***** Setting OS %s to be recognized at an NT derived system *****' % (thisOs)
        sys.registry.setProperty( "python.os", "nt" )

def getProviderID():

    # Test to see if the named provider has already been created.
    providerName = os.environ['providerName']
    providerID = AdminConfig.getid('/JDBCProvider:%s/' % (providerName))
    
    if len(providerID) == 0:
        print '***** Begin creating JDBC provider named %s *****' % (providerName)

        # Set the Node ID.
        server = '/Server:%s' % (os.environ['serverName'])
        serverID = AdminConfig.getid(server)
        print 'The target server ID is %s.' % (serverID)

        # Set the required attributes for the provider.
        name = ['name', providerName]
        implCN = ['implementationClassName', os.environ['implementationClassName']]
        description = ['description', os.environ['providerDescription']]
        providerClasspath = ['classpath', os.environ['providerClasspath']]
        providerType = ['providerType', os.environ['providerType']]
        providerAttrs = [name, implCN, description, providerClasspath, providerType]

        print 'The defined properties for the provider are:'
        for item in providerAttrs:
            print '%s = %s' % (item[0],item[1])

        # Create and save the JDBC provider.
        print 'Creating provider...'
        provider = AdminConfig.create('JDBCProvider', serverID, providerAttrs)
        
        providerID = AdminConfig.getid('/JDBCProvider:%s/' % (providerName))
        print 'Provider ID = %s' %(providerID)

        print 'Saving provider configuration...'
        AdminConfig.save()

        print '***** End creating JDBC provider named %s *****' % (providerName)
 
    else:
        print 'A JDBC provider named %s already exists; it will not be recreated.' % (providerName)

    return providerID

def createDataSource():

    # Test to see if the datasource already exists in the before creating.
    providerName = os.environ['providerName']
    datasourceName = os.environ['datasourceName']
    datasourceID = AdminConfig.getid('/JDBCProvider:%s/DataSource:%s/' % (providerName, datasourceName))
    
    if len(datasourceID) == 0:
        print '***** Begin creating JDBC datasource named %s in provider %s *****' % (datasourceName, providerName)
        
        # Get the associated provider.
        providerID = getProviderID()

        # Set the datasource attributes.
        name = ['name', datasourceName]
        jndiName = ['jndiName', os.environ['jndiName']]
        description = ['description', os.environ['datasourceDescription']]
        datasourceHelper = ['datasourceHelperClassname', os.environ['datasourceHelperClassname']]
        statementCacheSize = ['statementCacheSize', 0]
        datasourceAttrs = [name, jndiName, description, datasourceHelper, statementCacheSize]
    
        print 'The defined properties for the datasource are:'
        for item in datasourceAttrs:
            print '%s = %s' % (item[0],item[1])

        print 'Creating datasource...'
        datasource = AdminConfig.create('DataSource', providerID, datasourceAttrs)

        # Set custom properties for the datasource.
        print 'Adding custom properties to datasource...'
        propSet = AdminConfig.create('J2EEResourcePropertySet', datasource, [])
        value = os.environ['databaseName']
        if len(value) > 0:
            AdminConfig.create('J2EEResourceProperty', propSet, [['name', 'databaseName'], ['value', value]])
    
        print 'Saving datasource configuration...'
        AdminConfig.save()

        print '***** End creating JDBC datasource named %s in provider %s *****' % (datasourceName, providerName)

    else:
        print 'A JDBC datasource named %s already exists; it will not be recreated.' % (datasourceName)

    return datasource


try:
    fixupOsType()
    datasource = createDataSource()
    print '***** Begin testing datasource connection *****'
    print AdminControl.testConnection(datasource)
    print '***** End testing datasource connection *****'
except:
    print "***** Unexpected error while creating JDBC datasource:", sys.exc_info()[0], " *****"
    raise
