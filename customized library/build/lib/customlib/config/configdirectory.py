from configparser import RawConfigParser # Can parse string with special symbol


def config_directory(filename, section):
    """
    the method is used to parse through the ini files which are stored in "dbfs:/init/" directory in order to obtain the configuration
    
    :param filename: str
                    The name of config file
    :param section: str
                    The name of section
    :return: the configuration dictionary
    
    """
    # create a parser
    parser = RawConfigParser()
    # read config file
    parser.read("/dbfs/init/"+ filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db