"""Module providing a function to run a FastAPI application"""
import uvicorn
import os
import yaml
import logging
import time

if __name__ == '__main__':
    # use GMT to format datetime instead of local
    logging.Formatter.converter = time.gmtime
    # Load logging configuration from the YAML file
    with open('logging_config.yaml', 'r') as config_file:
        config_dict = yaml.safe_load(config_file)
        handlers = config_dict.get('handlers', {})
        for handler in handlers.values():
            if handler.get('class') == 'logging.handlers.RotatingFileHandler':
                log_filename = handler.get('filename')
                log_directory = os.path.dirname(log_filename)

                # Create the directory if it doesn't exist
                if not os.path.exists(log_directory):
                    os.makedirs(log_directory)
        logging.config.dictConfig(config_dict)

    uvicorn.run("app.entry:app", host="0.0.0.0", port=int(os.environ.get("APP_PORT", 8080)))
