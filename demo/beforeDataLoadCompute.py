from dsiBuildSoftSummative import Analysis

analysis_obj = Analysis.Analysis('configs/job_config.yml')

analysis_output = analysis_obj.compute_analysis()
