from .server import Server, server_list, BRAVO


def test_checkTop100():
    for server in server_list:

        # Read the top 100 info
        top100 = server.getTop100()

        # Quick check to ensure user data is being sent
        assert top100[0].get("nickname", None) != None



def test_userFetch():
    
    user = BRAVO.getUser("X-nor50")
    
    assert user != None
    assert user.uid == "deb5a20683d1890fdbed9185e6aea6ac"