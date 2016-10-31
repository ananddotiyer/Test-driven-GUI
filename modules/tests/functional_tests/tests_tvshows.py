tests_tvshows = [
  ################################################/tvshows########################################################
  #All TV Shows.  Status: Done
  {
    "test_name": "tvshows_page_recommended",
    "test_type": "dittotv",
    "test_base_url": "tvshows",
    "test_function": "tvshow_page",
    "test_params": {
    },
    "test_repl": {
      
    },
    "test_expected":{
      "rowcount":30,
      "title": "Colors",
      "specific":"recommended"
    }
  },
]