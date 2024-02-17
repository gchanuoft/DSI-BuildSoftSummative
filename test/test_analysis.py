from pytest import raises

def test_exist_job_config_init():
    from dsiBuildSoftSummative import Analysis
    analysis_obj = Analysis.Analysis('configs/job_config.yml')


def test_does_not_exist_job_config_init():
    from dsiBuildSoftSummative import Analysis
    with raises(FileNotFoundError):
        analysis_obj = Analysis.Analysis('doesNotExist.yml')

def test_output_path_not_exist_from_config():
    from dsiBuildSoftSummative import Analysis
    with raises(FileNotFoundError):
        analysis_obj = Analysis.Analysis('configs/bad_config.yml')
        analysis_obj.load_data()

        analysis_output = analysis_obj.compute_analysis()
        print(analysis_output)

        analysis_figure = analysis_obj.plot_data()


#def test_pdAllStrToOneCol(monkeypatch):
#    monkeypatch.setattr('sys.argv', [sys.argv[0], 'user_config.yml', 'outputPNG'])
#    from dsiBuildSoftSummative import Analysis
#    testDataFrame =  pd.DataFrame({'A': [1, 2, 3, 4],
#                                   'B': [5, 6, 7, 8],
#                                   'C': ['Str1', 'Str2', 'Str3', 'Str4']})
#    assert len(pdAllStrToOneCol(testDataFrame).columns) == 1
    
#def test_pdAllStrToOneCol_errors(monkeypatch):
#    monkeypatch.setattr('sys.argv', [sys.argv[0], 'user_config.yml', 'outputPNG'])
#    from dsiBuildSoftSummative import Analysis
#    NotADataFrame = 0
    #with raises(TypeError):
     #   pdAllStrToOneCol(NotADataFrame)

   # emptyDataFrame =  pd.DataFrame()
   # with raises(ValueError):
    #    pdAllStrToOneCol(emptyDataFrame)
