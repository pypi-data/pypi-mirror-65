#coding:utf8
import pytest
import pymysql.cursors
import pathlib
import subprocess


def _setup_sqitch(args):
    def is_sqitch_project(path):
        try:
            return path.is_dir() and (path / "sqitch.plan").exists()
        except OSError:
            return False
    
    def arg_to_path(arg):
        # Test classes or functions can be appended to paths separated by ::
        arg = arg.split("::", 1)[0]
        return pathlib.Path(arg)

    def find_sqitch_path(args):
        args = map(str, args)
        args = [arg_to_path(x) for x in args if not x.startswith("-")]
        cwd = pathlib.Path.cwd()
        if not args:
            args.append(cwd)
        elif cwd not in args:
            args.append(cwd)
        for arg in args:
            if is_sqitch_project(arg):
                return arg
            
            for child in arg.glob('**/*'):
                if is_sqitch_project(child):
                    return child
        return None

    project_dir = find_sqitch_path(args)
    return project_dir

@pytest.fixture(scope="session")
def mysql(request):
    """
    Client fixture for MySQL server.

    #. Get django config
    #. Connect to mysql server.
    #. Drop database before tests
    #. Create database.
    #. Use proper database.
    #. Drop database after tests.

    :param FixtureRequest request: fixture request object

    :rtype: MySQLdb.connections.Connection
    :returns: connection to database
    """
    from django.conf import settings
    sqitch_file = _setup_sqitch([settings.BASE_DIR])
    sqitch_config = "test_sqitch"
    subprocess.run(["sqitch", "config", "core.registry", sqitch_config],cwd=sqitch_file)
    conf = settings.DATABASES['default']
    mysql_db = conf['TEST']['NAME']
    charset = 'utf8mb4'

    settings.DATABASES['default']['NAME'] = mysql_db
   
    connection = pymysql.connect(host=conf['HOST'],
                            user=conf["USER"],
                            password=conf["PASSWORD"],
                            charset=charset,
                            cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        cursor.execute("DROP DATABASE IF EXISTS %s" % sqitch_config)
        cursor.execute('DROP DATABASE IF EXISTS %s' % mysql_db)
        sql = ''' CREATE DATABASE {name}
            DEFAULT CHARACTER SET {charset}
        '''.format(name=mysql_db, charset=charset)
        cursor.execute(sql)
        cursor.execute('USE %s' % mysql_db)
        subprocess.run(["sqitch","deploy"],cwd=sqitch_file)
        

    def drop_database():
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS %s" % sqitch_config)
            cursor.execute('DROP DATABASE IF EXISTS %s' % mysql_db)
    request.addfinalizer(drop_database)

    return connection

