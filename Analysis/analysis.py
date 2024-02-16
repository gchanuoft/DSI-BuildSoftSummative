import matplotlib

def Analysis():

    def __init__(analysis_config:str):
        # load config here
        print('__init__')
    
    def load_data():
        # load data here
        print('load_data()')

    def compute_analysis() -> dict:
        # compute_analysis
        print('compute_analysis()')
    
    def notify_done(message: str) -> None:
        # notify user analysis is complete
        print('notify_done()')

    def plot_data(save_path:Optional[str] = None) -> matplotlib.Figure:
        # pot using matplotlib
        print('plot_data()')