class DevelopmentConfig():
    DEBUG=True
    MYSQL_HOST='localhost'
    MYSQL_USER=''
    MYSQL_PASSWORD=''
    MYSQL_DB='pizzeria_db'
    MYSQL_CURSORCLASS ='Cursor'
    
config={
    'development':DevelopmentConfig
}

