tests_sapna_search = [
  ################################################/catalogs########################################################
  # search authors.  Status: Done
  {
    "test_name": "search_author",
    "test_type": "sapna",
    "test_base_url": "shop/search/{author}/search_tag/author",
    "test_function": "search",
    "test_params": {
    },
    "test_repl": {
      "author": ["Chetan Bhagat"]
    },
    "test_expected":{
      "rowcount":72,
      "author": "Chetan Bhagat",
      "name": "2 States",
      "url": "sapnaonline.com",
      "specific":"author"
    }
  },
  ## search publishers.  Status: Done
  #{
  #  "test_name": "search_publisher",
  #  "test_type": "sapna",
  #  "test_base_url": "shop/search/{publisher}/search_tag/publisher",
  #  "test_function": "search",
  #  "test_params": {
  #  },
  #  "test_repl": {
  #    "publisher": ["mcgraw"]
  #  },
  #  "test_expected":{
  #    "rowcount":72,
  #    "publisher": "Mcgraw-hill",
  #    "name": "2 States",
  #    "url": "sapnaonline.com",
  #    "specific":"specs"
  #  }
  #},
  ## search product.  Status: Done
  #{
  #  "test_name": "search_term",
  #  "test_type": "sapna",
  #  "test_base_url": "shop/search/{term}/page/{page_num}",
  #  "test_function": "search",
  #  "test_params": {
  #  },
  #  "test_repl": {
  #    "term": ["batman"],
  #    "page_num": ["5"]
  #  },
  #  "test_expected":{
  #    "rowcount":72,
  #    "name": "batman",
  #    "url": "sapnaonline.com",
  #    "specific":"term"
  #  }
  #},
  ## Refine search books based on categories.  Status: Done
  #{
  #  "test_name": "search_book_categories",
  #  "test_type": "sapna",
  #  "test_base_url": "shop/books/{category}/page/{page}",
  #  "test_function": "search",
  #  "test_params": {
  #  },
  #  "test_repl": {
  #      "category": ["activity","accounting",],
  #      "page": ["1"],
  #  },
  #  "test_expected":{
  #    "rowcount":72,
  #    "specific":"specs"
  #  },
  #  "output_mode": "a+"
  #},
  ## Refine search books based on categories.  Status: Done
  #{
  #  "test_name": "search_widget",
  #  "test_type": "sapna",
  #  "test_base_url": "shop/widget/{category}/widget_sub_name/books/page/{page_num}",
  #  "test_function": "search",
  #  "test_params": {
  #  },
  #  "test_repl": {
  #      "category": ["women-s-day-special",],
  #      "page_num": ["1"],
  #  },
  #  "test_expected":{
  #    "rowcount":72,
  #    "specific":"specs"
  #  },
  #  "output_mode": "a+"
  #},  
]