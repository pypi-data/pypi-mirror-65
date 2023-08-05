from thompcoutils.log_utils import get_logger
from thompcoutils.config_utils import ConfigManager
import logging
import sqlobject
import os
import sshtunnel
import mysql.connector


class DBConfig:
    def __init__(self, cfg_mgr=None, db_type=None, sqlite_file=None, db_host=None, db_username=None, db_password=None,
                 schema=None, db_port=None, rebuild=None, section="DB CONNECTION", ssh_username=None, ssh_password=None,
                 use_ssh=False, ssh_host=None, ssh_timeout=None, ssh_tunnel_timeout=None):
        self.ssh_tunnel = None
        if cfg_mgr is None:
            self.type = db_type
            self.sqlite_file = sqlite_file
            self.db_host = db_host
            self.db_username = db_username
            self.db_password = db_password
            self.schema = schema
            self.db_port = db_port
            self.rebuild = rebuild
            self.ssh_username = ssh_username
            self.ssh_password = ssh_password
            self.use_ssh = use_ssh
            self.ssh_host = ssh_host
            self.ssh_timeout = ssh_timeout
            self.ssh_tunnel_timeout = ssh_tunnel_timeout
        else:
            self.type = cfg_mgr.read_entry(section, "type", default_value="mysql")
            self.sqlite_file = cfg_mgr.read_entry(section, "sqlite file", default_value="licenseserver.sqlite")
            self.db_host = cfg_mgr.read_entry(section, "db_host", default_value="localhost")
            self.db_username = cfg_mgr.read_entry(section, "db_username", default_value="my db user name")
            self.db_password = cfg_mgr.read_entry(section, "db_password", default_value="my db user password")
            self.schema = cfg_mgr.read_entry(section, "schema", default_value="my db schema")
            self.db_port = cfg_mgr.read_entry(section, "db_port", default_value=3306)
            self.rebuild = cfg_mgr.read_entry(section, "rebuild", default_value=False)
            self.ssh_username = cfg_mgr.read_entry(section, "ssh_username", default_value="")
            self.ssh_password = cfg_mgr.read_entry(section, "ssh_password", default_value="")
            self.ssh_host = cfg_mgr.read_entry(section, "ssh_host", default_value="localhost")
            self.use_ssh = cfg_mgr.read_entry(section, "use_ssh", default_value=False)
            self.ssh_timeout = cfg_mgr.read_entry(section, "ssh_timeout", default_value=5.0)
            self.ssh_tunnel_timeout = cfg_mgr.read_entry(section, "ssh_tunnel_timeout", default_value=5.0)


class DbUtils:
    def __init__(self, db_cfg=None, db_type=None, db_host=None, db_username=None, db_password=None, schema=None,
                 db_port=None, sqlite_file=None, use_ssh=False, ssh_username=None, ssh_password=None, ssh_timeout=None,
                 ssh_tunnel_timeout=None):
        logger = get_logger()
        self.connection = None
        self.ssh_tunnel = None
        self.tables = []
        if db_cfg is not None:
            db_type = db_cfg.type
            db_host = db_cfg.db_host
            db_username = db_cfg.db_username
            db_password = db_cfg.db_password
            schema = db_cfg.schema
            db_port = db_cfg.db_port
            use_ssh = db_cfg.use_ssh
            ssh_username = db_cfg.ssh_username
            ssh_password = db_cfg.ssh_password
            ssh_timeout = db_cfg.ssh_timeout
            ssh_tunnel_timeout = db_cfg.ssh_tunnel_timeout
        if db_type == "sqlite":
            if sqlite_file is None:
                raise RuntimeError("--sqlite requires --sqlite-dir")
            else:
                logger.debug("Using {} Sqlite database".format(sqlite_file))
                self._connect_sqlite(sqlite_file)
        elif db_type == "postgres":
            logger.debug('Using postgress database {} at {}'.format(schema, db_host))
            self._connect_postgres(db_username, db_password, schema, db_host, db_port)
        elif "mysql" in db_type:
            logger.debug('Using mysql database {} at {}'.format(schema, db_host))
            self._connect_mysql(db_username, db_password, schema, db_host, db_port, use_ssh, db_cfg.ssh_host,
                                ssh_username, ssh_password, ssh_timeout, ssh_tunnel_timeout)
        elif db_type == "odbc":
            raise RuntimeError("ODBC not implemented yet")
        else:
            raise RuntimeError("No database type selected")

    def _connect_uri(self, uri):
        self.connection = sqlobject.sqlhub.processConnection = sqlobject.connectionForURI(uri)

    def _connect_sqlite(self, file_path):
        uri = "sqlite:" + file_path
        self._connect_uri(uri)

    def _connect_postgres(self, username, password, database, host, db_port):
        port_str = ""
        if db_port is not None:
            port_str = ":" + str(db_port)
        uri = "postgres://" + username + ":" + password + "@" + host + port_str + "/" + database
        self._connect_uri(uri)

    def _connect_mysql(self, db_username, db_password, schema, db_host, db_port, use_ssh=False, ssh_host=None,
                       ssh_username=None, ssh_password=None, ssh_timeout=None, ssh_tunnel_timeout=None):
        if use_ssh:
            if ssh_username == '':
                ssh_username = None
            if ssh_password == '':
                ssh_password = None
            sshtunnel.SSH_TIMEOUT = ssh_timeout
            sshtunnel.TUNNEL_TIMEOUT = ssh_tunnel_timeout
            try:
                self.ssh_tunnel = sshtunnel.SSHTunnelForwarder(db_host,
                                                               ssh_username=ssh_username, ssh_password=ssh_password,
                                                               remote_bind_address=(db_host, db_port))
                self.ssh_tunnel.daemon_forward_servers = True
                self.ssh_tunnel.start()
                self.connection = mysql.connector.connect(user=db_username, password=db_password,
                                                          host=ssh_host, port=self.ssh_tunnel.local_bind_port,
                                                          database=schema)
            except sshtunnel.BaseSSHTunnelForwarderError as e:
                raise Exception(e)
        else:
            port_str = ""
            if db_port is not None:
                port_str = ":" + str(db_port)
            uri = "mysql://" + db_username + ":" + db_password + "@" + db_host + port_str + "/" + schema
            self._connect_uri(uri)

    def add_table(self, table):
        self.tables.append(table)

    def set_tables(self, tables):
        self.tables = tables

    def shutdown(self):
        if self.ssh_tunnel is not None:
            self.ssh_tunnel.stop()

    def create_table(self, table):
        logger = get_logger()
        if not self.connection.tableExists(table.q.tableName):
            logger.debug("creating table {}".format(str(table)))
            table.createTable()

    def create_tables(self, tables=None):
        logger = get_logger()
        logger.debug("Creating tables...")
        if tables is None:
            tables = self.tables
        for table in tables:
            self.create_table(table)

    def drop_tables(self, tables=None):
        logger = get_logger()
        logger.debug("Dropping tables...")
        if tables is None:
            tables = self.tables
        for table in tables:
            logger.debug("dropping table {}".format(str(table)))
            table.dropTable(cascade=True, ifExists=True)


def main():
    create_file = False
    logging.config.fileConfig('logging.ini')
    temp_filename = "testing DbConfig only.ini"
    if create_file:
        if os.path.isfile(temp_filename):
            os.remove(temp_filename)
    cfg_mgr = ConfigManager(temp_filename, create=create_file)
    db_cfg = DBConfig(cfg_mgr=cfg_mgr)
    if create_file:
        cfg_mgr.write(temp_filename)
    db_utils = DbUtils(db_cfg)
    db_utils.shutdown()


if __name__ == "__main__":
    main()
