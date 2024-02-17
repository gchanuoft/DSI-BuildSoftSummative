from typing import Any, Optional, Final
import matplotlib.pyplot as plt
import pandas as pd
import yaml
import requests
import datetime
import logging


class Analysis():

    STUDIY_ID: Final = 201
    INIT_LOG_FILE_NAME_PREFIX: Final = 'dsiBuildSoftSummative'
    DATA_URL: Final = f'https://osdr.nasa.gov/osdr/data/osd/files/{STUDIY_ID}'
    rawJsonData = None
    studiesBySubCat = None
    dataComputed = False

    def __init__(self, analysis_config: str) -> None:

        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        config = {}
        # load each config file and update the config dictionary
        for path in paths:
            try:
                with open(path, 'r') as f:
                    this_config = yaml.safe_load(f)
                    config.update(this_config)   
            except FileNotFoundError as e:    
                e.add_note(f'{self._timeStamp()} The file {path} cannot be found')
                raise e
            except Exception as e:
                e.add_note(f'{self._timeStamp()} Error while loading configuration files')
                raise e             
        self.config = config

        # Init logging
        try:
            logging_level = logging.DEBUG if config['verbose_log'] else logging.WARNING
            # Initialize logging module
            now = datetime.datetime.now()
            logFileName = f'{self.INIT_LOG_FILE_NAME_PREFIX}_{now.strftime("%Y_%m_%d_%H%M")}.log'
            logging.basicConfig(
                level=logging_level,
                handlers=[logging.StreamHandler(),
                          logging.FileHandler(logFileName)])
        except Exception as e:
            e.add_note(f'{self._timeStamp()} Error initializing log file')
            raise e   

    def load_data(self) -> None:
        logging.debug(f'{self._timeStamp()} Starting loading data from Data API: {self.DATA_URL}')

        # Load data from NASA API
        try:
            self.rawJsonData = requests.get(url=f'{self.DATA_URL}?api_key={self.config['api_key']}').json()
        except Exception as e:
            logging.error(f'{self._timeStamp()} Error Loading Data from API: {self.DATA_URL}')
            e.add_note(f'{self._timeStamp()} Error Loading Data from API: {self.DATA_URL}')
            raise e   
        logging.debug(f'{self._timeStamp()} Done loading data from Data API: {self.DATA_URL}')

    def compute_analysis(self) -> Any:
        assert self.rawJsonData != None, 'Cannot compute analysis when no data is loaded'
        
        # Log the analysis start time
        logging.debug(f'{self._timeStamp()} Starting compute_analysis()')
        start = datetime.datetime.now()
        logging.info(f'{self._timeStamp()} Analysis Start time {start.timestamp()}')

        # create data frame and analysis data from json
        studiesPD = pd.DataFrame(self.rawJsonData['studies'][f'OSD-{self.STUDIY_ID}']['study_files'])
        self.studiesBySubCat = studiesPD.groupby('subcategory').agg(Num_of_Studies_Per_Subcateglory=('file_name', 'count'))
        self.studiesBySubCat= self.studiesBySubCat.iloc[1: , :]

        # Log analysis end time
        end = datetime.datetime.now()
        logging.info(f'{self._timeStamp()} Analysis end time {end.timestamp()}')
        logging.info(f'{self._timeStamp()} Analysis End time')

        # Mark computation as done and send done message through ntfy
        self.dataComputed = True
        self.notify_done(f'Analysis done start: - {start.strftime("%Y %m %d, %H:%M:%S")} | end: - {end.strftime("%Y %m %d, %H:%M:%S")}')        
        logging.debug(f'{self._timeStamp()} Done compute_analysis()')

    def plot_data(self, save_path: Optional[str] = None) -> plt.Figure:
        ''' 
        Analyze and plot data

        Generates a plot, display it to screen, and save it to the path in the parameter `save_path`, or 
        the path from the configuration file if not specified.

        Parameters
        ----------
        save_path : str, optional
            Save path for the generated figure

        Returns
        -------
        fig : matplotlib.Figure

        '''
        assert self.dataComputed, 'Cannot plot data when data has not been computed'
        logging.debug(f'{self._timeStamp()} Starting saving plot: {save_path}')

        fig, ax = plt.subplots()

        ax.set_title(self.config['plot_config']['title'])
        ax.set_xlabel(self.config['plot_config']['xlabel'])
        ax.set_ylabel(self.config['plot_config']['ylabel'])
        ax.set_axisbelow(True)
        ax.grid(alpha=0.3)

        subCat = ax.scatter(self.studiesBySubCat.index, self.studiesBySubCat['Num_of_Studies_Per_Subcateglory'])
    
        ax.legend([subCat],
                  ['Sub Categories'],
                  bbox_to_anchor=(1, 1),
                  loc='upper left')
        
        pngFileName = 'stub.png'

        logging.info(f'{self._timeStamp()} Creating image file {pngFileName}')
        fig.autofmt_xdate(rotation=45)
        fig.savefig(pngFileName, bbox_inches='tight')
        logging.debug(f'{self._timeStamp()} Done saving plot: {save_path}')

        return fig

    def notify_done(self, message: str) -> None:
        assert self.dataComputed, 'Cannot send done message when data has not been computed'
        logging.debug(f'{self._timeStamp()} Done sending message to ntfy')
        try:
            requests.post("https://ntfy.sh/dsiBuildSoftSummative",
                          data=message.encode(encoding='utf-8'))
        except Exception as e:
            logging.error(f'{self._timeStamp()} Error calling ntfy')
            e.add_note(f'{self._timeStamp()} Error calling ntfy')
            raise e   
        logging.debug(f'{self._timeStamp()} Done sending message to ntfy')

    def _timeStamp(self) -> str:
        now = datetime.datetime.now()
        return now.strftime("%Y %m %d, %H:%M:%S")
        