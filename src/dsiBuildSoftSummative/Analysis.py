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
    NTFY_URL: Final = 'https://ntfy.sh/'
    OUT_PUT_FILE_NAME: Final = 'SubCat.png'
    rawJsonData = None
    studiesBySubCat = None
    dataComputed = False
    apiKey = None
    ntfyTopic = None
    plotColor = None
    plotTitle = None
    plotXLabel = None
    plotYLabel = None
    plotSizeH = None
    plotSizeW = None
    outputPaths = None
    
    def __init__(self, analysis_config: str) -> None:
        ''' 
        Load config into an Analysis object

        Load system-wide configuration from `configs/system_config.yml`, user configuration from
        `configs/user_config.yml`, and the specified analysis configuration file

        Parameters
        ----------
        analysis_config : str
        Path to the analysis/job-specific configuration file

        Returns
        -------
        analysis_obj : Analysis
        Analysis object containing consolidated parameters from the configuration files

        Notes
        -----
        The configuration files should include parameters for:
        * GitHub API token
        * ntfy.sh topic
        * Plot color
        * Plot title
        * Plot x and y axis titles
        * Figure size
        * Default save path
        '''

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

        # Init logging
        try:
            logging_level = logging.DEBUG if config['verbose_log'] else logging.INFO
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
        
        # Only take the config values we want
        logging.info(f'{self._timeStamp()} Analysis init() config values')
        self.apiKey = config['api_key']
        self.ntfyTopic = config['ntfyTopic']
        logging.info(f'{self._timeStamp()} Notification will be sent to: {self.NTFY_URL}{self.ntfyTopic}')
        self.plotColor = config['plot_config']['color']
        self.plotTitle = config['plot_config']['title']
        self.plotXLabel = config['plot_config']['xlabel']
        self.plotYLabel = config['plot_config']['ylabel']
        self.plotSizeH = config['plot_config']['sizeH']
        self.plotSizeW = config['plot_config']['sizeW']
        self.outputPaths = config['output_paths']
        logging.info(f'{self._timeStamp()} Plots will be save to: {self.outputPaths}')
        
    def load_data(self) -> None:
        ''' 
        Retrieve data from the NASA Open API

        This function makes an HTTPS request to the NASA API and retrieves OSD Studies data. The data is
        stored in the Analysis object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        '''

        logging.debug(f'{self._timeStamp()} Starting loading data from Data API: {self.DATA_URL}')

        # Load data from NASA API
        try:
            self.rawJsonData = requests.get(url=f'{self.DATA_URL}?api_key={self.apiKey}').json()
        except Exception as e:
            logging.error(f'{self._timeStamp()} Error Loading Data from API: {self.DATA_URL}', exc_info=e)
            e.add_note(f'{self._timeStamp()} Error Loading Data from API: {self.DATA_URL}')
            raise e   
        logging.debug(f'{self._timeStamp()} Done loading data from Data API: {self.DATA_URL}')

    def compute_analysis(self) -> Any:
        '''
        Analyze previously-loaded data.

        This function sum the total of each OSD studyies subcateglory

        Parameters
        ----------
        None

        Returns
        -------
        analysis_output : Dataframe with the sum of each subcateglory 

        '''

        assert self.rawJsonData != None, 'Cannot compute analysis when no data is loaded'
        
        # Log the analysis start time
        logging.debug(f'{self._timeStamp()} Starting compute_analysis()')
        start = datetime.datetime.now()
        logging.info(f'{self._timeStamp()} Analysis Start time {start.timestamp()}')

        # create data frame and analysis data from json
        studiesPD = pd.DataFrame(self.rawJsonData['studies'][f'OSD-{self.STUDIY_ID}']['study_files'])
        analysis_output = studiesPD.groupby('subcategory').agg(Num_of_Studies_Per_Subcateglory=('file_name', 'count'))
        analysis_output = self.studiesBySubCat.iloc[1: , :]
        self.studiesBySubCat = analysis_output

        # Log analysis end time
        end = datetime.datetime.now()
        logging.info(f'{self._timeStamp()} Analysis End time {end.timestamp()}')

        # Mark computation as done and send done message through ntfy
        self.dataComputed = True
        self.notify_done(f'Analysis done start: - {start.strftime("%Y %m %d, %H:%M:%S")} | end: - {end.strftime("%Y %m %d, %H:%M:%S")}')        
        logging.debug(f'{self._timeStamp()} Done compute_analysis()')

        return analysis_output

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
        logging.debug(f'{self._timeStamp()} Starting saving plots')

        if save_path == None:
            plotOutputpaths = self.outputPaths
        else:
            plotOutputpaths = save_path

        fig, ax = plt.subplots()

        ax.set_title(self.plotTitle)
        ax.set_xlabel(self.plotXLabel)
        ax.set_ylabel(self.plotYLabel)
        ax.set_axisbelow(True)
        ax.grid(alpha=0.3)
        subCat = ax.bar(self.studiesBySubCat.index, self.studiesBySubCat['Num_of_Studies_Per_Subcateglory'], color=self.plotColor)
    
        ax.legend([subCat],
                  ['Sub Categories'],
                  bbox_to_anchor=(1, 1),
                  loc='upper left')
        
        for i in range(len(self.studiesBySubCat.index)):
            ax.text(i, self.studiesBySubCat['Num_of_Studies_Per_Subcateglory'].iloc[i], self.studiesBySubCat['Num_of_Studies_Per_Subcateglory'].iloc[i], ha = 'center')

        fig.autofmt_xdate(rotation=45)
        fig.set_size_inches(self.plotSizeW, self.plotSizeH)
        for path in plotOutputpaths:
            try:
                fullFileName = f'{path}/{self.OUT_PUT_FILE_NAME}'
                logging.info(f'{self._timeStamp()} Creating image file {fullFileName}')
                fig.savefig(fullFileName, bbox_inches='tight')
            except Exception as e:
                logging.error(f'{self._timeStamp()} Error saving file {fullFileName}', exc_info=e)
                e.add_note(f'{self._timeStamp()} Error saving file {fullFileName}')
                raise e   
        logging.debug(f'{self._timeStamp()} Done saving plot: {save_path}')

        return fig

    def notify_done(self, message: str) -> None:
        ''' 
        Notify the user that analysis is complete.

        Send a notification to the user through the ntfy.sh webpush service.

        Parameters
        ----------
        message : str
            Text of the notification to send

        Returns
        -------
        None

        '''

        assert self.dataComputed, 'Cannot send done message when data has not been computed'
        logging.debug(f'{self._timeStamp()} Done sending message to ntfy')
        try:
            requests.post(f'{self.NTFY_URL}{self.ntfyTopic}',
                          data=message.encode(encoding='utf-8'))
        except Exception as e:
            logging.error(f'{self._timeStamp()} Error calling ntfy', exc_info=e)
            e.add_note(f'{self._timeStamp()} Error calling ntfy')
            raise e   
        logging.debug(f'{self._timeStamp()} Done sending message to ntfy')

    def _timeStamp(self) -> str:
        ''' 
        Create a string that represent the current time in "%Y %m %d, %H:%M:%S" format

        Parameters
        ----------
        None
        
        Returns
        -------
        timeStr : str

        '''
        now = datetime.datetime.now()
        timeStr = now.strftime("%Y %m %d, %H:%M:%S")
        return timeStr
        