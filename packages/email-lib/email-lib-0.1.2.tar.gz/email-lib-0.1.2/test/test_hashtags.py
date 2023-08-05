from email_lib.hashtags import extract_hashtags


def test_extract_hashtags():
    result = extract_hashtags('#this is a#test to check #4 #matches http://test.com/index#faketag #tags')

    assert result == ['this', 'matches', 'tags']


    result = extract_hashtags('#one #two')

    assert result == ['one', 'two']
