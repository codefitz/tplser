// This pattern is in the public domain

tpl 1.0 module Wibble;

metadata
    origin := "Example";
	tree_path := 'Example', 'Wibble';
end metadata;

// We need the Apache Webserver from TKU to create the BAI herein
from ApacheBasedWebservers import ApacheBasedWebserver 1.2;

// Lookup product_version attribute for Appserver
table AppserverProductVersions 1.0
  '0.5'   -> 'Alpha';
  '2.6'   -> 'NG';
  '2.7'   -> 'NGi';
  '3.0'   -> 'Ultima';
  default -> 'Unknown';
end table;

//
// Generate SoftwareInstance for WibbleDatabase
//

pattern WibbleDatabase 1.0
  '''
  Pattern to capture WibbleDatabase SI. It detects the process and obtains version
  information by the 2 digits in the process name. The instance name is extracted
  from the process name after the "_".
  
  Supported Platforms:
    Unix
  
  To Do:
    Implement Windows version
  '''
  
  metadata
    publishers := 'Wibble Software Company Ltd';
    categories := 'Database Server Software';
    urls := 'http://www.wibble.com/';
  end metadata;
  
  overview
    tags Training3, Wibble;
  end overview;

  constants
    db_type := 'Wibble Database Server';
  end constants;

  triggers
    on process := DiscoveredProcess where cmd matches unix_cmd 'wibbleDB\d+_.*';
  end triggers;

  body
    host := model.host(process);
    
    // Extract instance; eg SLAVE from a command like "wibbleDB35_SLAVE"
    instance := regex.extract(process.cmd, regex 'wibbleDB\d+_(.*)', raw '\1');
    
    // Extract version; eg 3.5 from a command like "wibbleDB35_SLAVE"
    version := regex.extract(process.cmd, regex 'wibbleDB(\d)(\d+)', raw '\1.\2');
    
    // Create or update datastore
    model.SoftwareInstance(name := '%db_type% %version% instance "%instance%" on %host.name%',
                           type := db_type, instance := instance,
                           key := '%instance%/%db_type%/%host.key%',
                           version := version, product_version := version);
  end body;
end pattern;

//
// Generate SoftwareInstance for WibbleAppserver
//

pattern WibbleAppserver 1.0
  '''
  Pattern to capture WibbleAppserver SI. It detects the process and obtains version
  information by running "-v". The configuration file is extracted from the command
  line "-c" option, and interrogated for various attributes.
  
  Supported Platforms:
    Unix
  
  To Do:
    Implement Windows version
  '''
  
  metadata
    publishers := 'Wibble Software Company Ltd';
    categories := 'Application Server Software';
    urls := 'http://www.wibble.com/';
    known_versions := '0.5', '2.6', '2.7', '3.0';
  end metadata;
  
  overview
    tags Training3, Wibble;
  end overview;

  constants
    appserver_type := 'Wibble Application Server';
    db_type := 'Wibble Database Server';
  end constants;

  triggers
    on process := DiscoveredProcess where cmd matches unix_cmd 'wibbleAppServ';
  end triggers;

  body
    host := model.host(process);
    
    cmdResult := discovery.runCommand(host, process.cmd + ' -v');
    if not cmdResult then
      log.warn('Failed to run command %process.cmd% on host %host.name%');
      version := '';
      build := '';
      patch := '';
    else
      // Extract versions from command result like "Version 2.7.182 patch 69"
      version := regex.extract(cmdResult.result, regex 'Version (\d+\.\d+)', raw '\1');
      build := regex.extract(cmdResult.result, regex 'Version \d+\.\d+\.(\d+)', raw '\1');
      patch := regex.extract(cmdResult.result, regex 'patch (\d+)', raw '\1');
    end if;
    
    // Extract config file from argument: file after a "-c"
    cfgfilePath := regex.extract(process.args, regex '-c\s+(\S+)', raw '\1');
    
    // Extract instance from command path (last directory before file): eg SLAVE in "/.../wibble/SLAVE/config.xml"
    instance := regex.extract(cfgfilePath, regex '/(\w+)/[\w.]+$', raw '\1');
    
    // Get config file
    cfgfile := discovery.fileGet(host, cfgfilePath);
    portstr := '';
    edition := '';
    if not cfgfile then
      log.warn('Config file %cfgfilePath% not found');
    else
      // Extract edition
      edition := xpath.evaluate(cfgfile.content, raw '/config/engine/@edition');
      if not edition then
        edition := '';
      else
        edition := text.lower(edition[0]);
      end if;

      // Extract port information and generate a space-string
      // This example is contrived, as you could (and probably should) just attach a list to 
      // the host node, but it shows what can be done with a for loop.
      ports := xpath.evaluate(cfgfile.content, raw '/config/listeners/listener//@port');
      for port in ports do
        if portstr = '' then
          portstr := port;
        else
          portstr := '%portstr% %port%';
        end if;
      end for;    
    end if;
    
    // Get application version (the webapp that is running in the appserver, not the version of
    // the appserver itself) from startup file; qexpense.log in the same directory as the config file
    // This version is put in custom attribute qe_version, so it can be used by the BAI pattern.
    appfilePath := regex.extract(process.args, regex '-c\s+(\S+/)', raw '\1qexpense.log');
    
    // Get startup log file
    appfile := discovery.fileGet(host, appfilePath);
    if not appfile then
      log.warn('Appserver log file %appfilePath% not found');
      qe_version := '';
    else
      qe_maj := regex.extract(appfile.content, regex 'Major Release (\d+)', raw '\1');
      qe_min := regex.extract(appfile.content, regex 'Minor Release (\d+)', raw '\1');
      qe_version := '%qe_maj%.%qe_min%';
    end if;
    
    // Create or update datastore
    si := model.SoftwareInstance(name := '%appserver_type% %version% instance "%instance%" on %host.name%',
                                 type := appserver_type, instance := instance,
                                 key := '%instance%/%appserver_type%/%host.key%',
                                 version := version, product_version := AppserverProductVersions[version],
                                 patch := patch, build := build,
                                 ports := portstr, edition := edition,
								 _tw_meta_data_attrs := ['ports'],
                                 qe_version := qe_version);
    
    // Create dependency to database SI
    db_si := search(in host traverse Host:HostedSoftware:RunningSoftware:SoftwareInstance where
                    type = %db_type% and instance = %instance%);
                    
    if not db_si then
      log.warn('No database SIs found to link appserver to');
    else
      // We expect to have only have one DB present, so could take the first,
      // but might as well pass the whole list
      model.rel.Dependency(Dependant := si, DependedUpon := db_si);
    end if;
  end body;
end pattern;

//
// Generate SoftwareInstance for Wibble Exporter
//

pattern WibbleExporter 1.0
  '''
  Pattern to capture Wibble Exporter SI.
  Version information captured from the installed package
  No instance information is captured
  
  Supported Platforms:
    Unix
  
  To Do:
    Implement Windows version
  '''
  
  metadata
    publishers := 'Wibble Software Company Ltd';
    urls := 'http://www.wibble.com/';
  end metadata;
  
  overview
    tags Training3, Wibble;
  end overview;

  constants
    exp_type := 'Wibble Exporter Server';
  end constants;

  triggers
    on process := DiscoveredProcess where cmd matches unix_cmd 'wexportd';
  end triggers;

  body
    host := model.host(process);
    
    // Try to find version from installed package list
    packages := model.findPackages(host, [regex '^wibble$']);
    version := '';
    revision := '';
    if not packages then
      log.warn('Could not get version of %exp_type% from package list');
    else
      version := packages[0].version;
      revision := packages[0].revision;
    end if;
    
    // Create or update datastore
    model.SoftwareInstance(name := '%exp_type% %version% on %host.name%',
                           type := exp_type,
                           version := version, product_version := version,
                           revision := revision);
  end body;
end pattern;

//
// Generate BusinessApplicationInstance for QuickExpense
//

pattern QuickExpense 1.0
  '''
    Pattern to generate the QuickExpense Business Application
    
    It is triggered when the Wibble Application Server is detected, but only created when
    in addition, a suitable Web server is also found (Apache with version of at least 2.1).
    Associated database servers that support the application servers are linked in.
    Associated exporter servers are linked in.
  '''

  overview
    tags Training3, QuickExpense;
    requires ApacheBasedWebserver;
  end overview;
  
  constants
    appserver_type := 'Wibble Application Server';
    bai_type := 'QuickExpense Web Application';
    exp_type := 'Wibble Exporter Server';
    webserver_type := 'Apache Webserver';		// SI pattern from TKU
  end constants;
  
  triggers
    on si := SoftwareInstance created, modified where type = appserver_type;
  end triggers;

  body
    host := model.host(si);
    
    // Assume that any instance of Apache on this host is also part of the application
    // WARNING: string comparison of versions performed in search query  
    webserver_sis := search(in host traverse Host:HostedSoftware:RunningSoftware:SoftwareInstance where
                            type = %webserver_type% and product_version >= '2.1');
    if not webserver_sis then
       log.warn('No webserver SIs found, not creating BAI');
       stop;
    end if;
    
    
    // Create or update datastore with the BAI now we know we have both an Appserver and Webserver
    // WARNING: we assume the qe_version is the same, obtained from either appserver SI
    bai := model.BusinessApplicationInstance(name := '%bai_type% %si.qe_version% on %host.name%',
                                             type := bai_type,
                                             key := '%bai_type%/%host.key%',
                                             version := si.qe_version, product_version := si.qe_version);
    
    // Create a software containment relationship to appserver and webserver SIs (required for the BAI to exist)
    model.addContainment(bai, si);
    model.addContainment(bai, webserver_sis);
    
    // Create relationships to database SIs (the only dependency from the Appserver SI should be the DB SI)
    db_sis := search(in si traverse Dependant:Dependency:DependedUpon:SoftwareInstance);
    if not db_sis then
      log.warn('No database SIs found to link BAI to');
    else
      // We should only have one database present, but more that one would be handled too
      model.addContainment(bai, db_sis);
    end if;
    
    // Create relationships to exporter SIs
    exp_sis := search(in host traverse Host:HostedSoftware:RunningSoftware:SoftwareInstance where
                      type = %exp_type%);
    if not exp_sis then
      log.warn('No exporter SIs found to link BAI to');
    else
      // We may find more than one exporter
      model.addContainment(bai, exp_sis);
    end if;
    
  end body;
end pattern;

//
// Simple Identifier Matchers
//

// Simple identities matching cmd only
identify Servers_Wibble 1.0
  tags Training3, Wibble;
  DiscoveredProcess cmd -> simple_identity;
  
  unix_cmd 'wibbleAppServ' -> 'Wibble Application Server';
  unix_cmd 'wibbleDB\d+_.*' -> 'Wibble Database Server';
  unix_cmd 'wexportd' -> 'Wibble Exporter Server';
end identify;

// Simple identities matching cmd and args (wdog is too generic a name on its own)
identify Servers_Wibble_Watchdog 1.0
  tags Training3, Wibble;
  DiscoveredProcess cmd, args -> simple_identity;
  
  unix_cmd 'wdog', regex 'wibbleAppServ' -> 'Wibble Application Server Watchdog Service';
end identify;