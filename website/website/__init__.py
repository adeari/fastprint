# fix_mysql_version.py
import pymysql

# Monkey patch to fix version issue
pymysql.version_info = (2, 2, 1, "final", 0)

# Install as MySQLdb
pymysql.install_as_MySQLdb()

print("✅ PyMySQL patched to version 2.2.1")

