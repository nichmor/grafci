from ci import repo_observer

def test_all_good():
    arg_string = ["--dispatcher-server", "localhost:8888" , "test_repo"]
    repo_observer.parse_args(arg_string)
    assert True