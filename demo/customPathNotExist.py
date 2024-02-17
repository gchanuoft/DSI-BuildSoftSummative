from dsiBuildSoftSummative import Analysis

analysis_obj = Analysis.Analysis('configs/job_config.yml')
analysis_obj.load_data()

analysis_output = analysis_obj.compute_analysis()
print(analysis_output)

analysis_figure = analysis_obj.plot_data(['NotExist'])