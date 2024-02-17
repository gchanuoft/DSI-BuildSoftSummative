from pytest import raises
import matplotlib.pyplot as plt
import pandas as pd

def test_exist_job_config_init():
    from dsiBuildSoftSummative import Analysis
    analysis_obj = Analysis.Analysis('configs/job_config.yml')


def test_does_not_exist_job_config_init():
    from dsiBuildSoftSummative import Analysis
    with raises(FileNotFoundError):
        analysis_obj = Analysis.Analysis('doesNotExist.yml')

def test_compute_analysis():
    from dsiBuildSoftSummative import Analysis
    analysis_obj = Analysis.Analysis('configs/user_config.yml')
    analysis_obj.load_data()
    analysis_output = analysis_obj.compute_analysis()
    assert isinstance(analysis_output , pd.DataFrame)

def test_plot_data():
    from dsiBuildSoftSummative import Analysis
    analysis_obj = Analysis.Analysis('configs/user_config.yml')
    analysis_obj.load_data()
    analysis_output = analysis_obj.compute_analysis()
    analysis_figure = analysis_obj.plot_data()
    assert isinstance(analysis_figure , plt.Figure)

def test_bad_config_format():
    from dsiBuildSoftSummative import Analysis
    with raises(ValueError):
        analysis_obj = Analysis.Analysis('configs/bad_config.yml')
        analysis_obj.load_data()
        analysis_output = analysis_obj.compute_analysis()
        analysis_figure = analysis_obj.plot_data()

def test_does_not_exist_output_path():
    from dsiBuildSoftSummative import Analysis
    with raises(FileNotFoundError):
        analysis_obj = Analysis.Analysis('configs/user_config.yml')
        analysis_obj.load_data()
        analysis_output = analysis_obj.compute_analysis()
        analysis_figure = analysis_obj.plot_data(['doesNotExist.yml'])
