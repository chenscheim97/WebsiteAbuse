import logging
logging.basicConfig(filename='/Users/chenscheim/PycharmProjects/WebsiteAbuse/datasets/example.log',
                    level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too')
