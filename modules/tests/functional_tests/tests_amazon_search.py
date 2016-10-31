tests_amazon_search = [
  ################################################/catalogs########################################################
  # search keywords.  Status: Done
  {
    "test_name": "search_keywords",
    "test_type": "amazon",
    "test_base_url": "s?keywords={keyword}&page={page_no}",
    "test_function": "search",
    "test_params": {
    },
    "test_repl": {
      "keyword": ["poster"],
      "page_no": ["2"]
    },
    "test_expected":{
      "rowcount":16,
      "specific":"specs"
    },
    "output_mode": "a+"
  },
]