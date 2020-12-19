lte = "now/m"
gte = "now-15m/m"


def get_5xx_query():
    body = {"query": {
        "bool": {
          "must": [],
          "filter": [
            {
              "bool": {
                "should": [
                  {
                    "range": {
                      "response_code": {
                        "gte": 500
                      }
                    }
                  }
                ],
                "minimum_should_match": 1
              }
            },
            {
              "range": {
                "@timestamp": {
                  "gte": gte,
                  "lte": lte,
                  "format": "strict_date_optional_time"
                }
              }
            }
          ],
          "should": [],
          "must_not": []
        }
      }
    }
    return body


def get_5xx_target(log):
    body = {"query": {
        "bool": {
          "must": [],
          "filter": [
            {
              "bool": {
                "filter": [
                  {
                    "bool": {
                      "should": [
                        {
                          "range": {
                            "response_code": {
                              "gte": 500
                            }
                          }
                        }
                      ],
                      "minimum_should_match": 1
                    }
                  },
                  {
                    "bool": {
                      "should": [
                        {
                          "match_phrase": {
                            "log.file.path": log
                          }
                        }
                      ],
                      "minimum_should_match": 1
                    }
                  }
                ]
              }
            },
            {
              "range": {
                "@timestamp": {
                  "gte": gte,
                  "lte": lte,
                  "format": "strict_date_optional_time"
                }
              }
            }
          ],
          "should": [],
          "must_not": []
        }
      }
    }
    return body


def get_4xx_query():
    body = {"query": {
        "bool": {
          "must": [],
          "filter": [
            {
              "bool": {
                "filter": [
                  {
                    "bool": {
                      "should": [
                        {
                          "range": {
                            "response_code": {
                              "gte": 400
                            }
                          }
                        }
                      ],
                      "minimum_should_match": 1
                    }
                  },
                  {
                    "bool": {
                      "filter": [
                        {
                          "bool": {
                            "should": [
                              {
                                "range": {
                                  "response_code": {
                                    "lt": 499
                                  }
                                }
                              }
                            ],
                            "minimum_should_match": 1
                          }
                        },
                        {
                          "bool": {
                            "must_not": {
                              "bool": {
                                "should": [
                                  {
                                    "query_string": {
                                      "fields": [
                                        "message"
                                      ],
                                      "query": "*forecast*"
                                    }
                                  }
                                ],
                                "minimum_should_match": 1
                              }
                            }
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            },
            {
              "range": {
                "@timestamp": {
                  "gte": gte,
                  "lte": lte,
                  "format": "strict_date_optional_time"
                }
              }
            }
          ],
          "should": [],
          "must_not": []
        }
      }
    }
    return body


def get_4xx_target(log):
    body = {"query": {
        "bool": {
          "must": [],
          "filter": [
            {
              "bool": {
                "filter": [
                  {
                    "bool": {
                      "should": [
                        {
                          "match_phrase": {
                            "log.file.path": log
                          }
                        }
                      ],
                      "minimum_should_match": 1
                    }
                  },
                  {
                    "bool": {
                      "filter": [
                        {
                          "bool": {
                            "should": [
                              {
                                "range": {
                                  "response_code": {
                                    "gte": 400
                                  }
                                }
                              }
                            ],
                            "minimum_should_match": 1
                          }
                        },
                        {
                          "bool": {
                            "filter": [
                              {
                                "bool": {
                                  "should": [
                                    {
                                      "range": {
                                        "response_code": {
                                          "lt": 499
                                        }
                                      }
                                    }
                                  ],
                                  "minimum_should_match": 1
                                }
                              },
                              {
                                "bool": {
                                  "must_not": {
                                    "bool": {
                                      "should": [
                                        {
                                          "query_string": {
                                            "fields": [
                                              "message"
                                            ],
                                            "query": "*forecast*"
                                          }
                                        }
                                      ],
                                      "minimum_should_match": 1
                                    }
                                  }
                                }
                              }
                            ]
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            },
            {
              "range": {
                "@timestamp": {
                  "gte": gte,
                  "lte": lte,
                  "format": "strict_date_optional_time"
                }
              }
            }
          ],
          "should": [],
          "must_not": []
        }
      }
     }
    return body


def get_4xx_top5(log):
    body = {"aggs": {
        "2": {
          "terms": {
            "field": "url.keyword",
            "order": {
              "_count": "desc"
            },
            "size": 5
          }
        }
      },
      "size": 0,
      "stored_fields": [
        "*"
      ],
      "script_fields": {},
      "docvalue_fields": [
        {
          "field": "@timestamp",
          "format": "date_time"
        }
      ],
      "_source": {
        "excludes": []
      },
      "query": {
        "bool": {
          "must": [],
          "filter": [
            {
              "bool": {
                "filter": [
                  {
                    "bool": {
                      "should": [
                        {
                          "match_phrase": {
                            "log.file.path": log
                          }
                        }
                      ],
                      "minimum_should_match": 1
                    }
                  },
                  {
                    "bool": {
                      "filter": [
                        {
                          "bool": {
                            "should": [
                              {
                                "range": {
                                  "response_code": {
                                    "gte": 400
                                  }
                                }
                              }
                            ],
                            "minimum_should_match": 1
                          }
                        },
                        {
                          "bool": {
                            "filter": [
                              {
                                "bool": {
                                  "should": [
                                    {
                                      "range": {
                                        "response_code": {
                                          "lt": 499
                                        }
                                      }
                                    }
                                  ],
                                  "minimum_should_match": 1
                                }
                              },
                              {
                                "bool": {
                                  "must_not": {
                                    "bool": {
                                      "should": [
                                        {
                                          "match_phrase": {
                                            "message": "forecast"
                                          }
                                        }
                                      ],
                                      "minimum_should_match": 1
                                    }
                                  }
                                }
                              }
                            ]
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            },
            {
              "range": {
                "@timestamp": {
                  "gte": gte,
                  "lte": lte,
                  "format": "strict_date_optional_time"
                }
              }
            }
          ],
          "should": [],
          "must_not": []
        }
      }
    }
    return body
