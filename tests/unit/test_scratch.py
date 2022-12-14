# from src.models.scratch import Scratch

# def test_scratch_create():
#     scratch = Scratch(
#         author='@Miguel',
#         caption='My beautiful drawing :)'
#     )

#     assert scratch.author == '@Miguel'
#     assert scratch.caption == 'My beautiful drawing :)'
#     assert len(scratch.likes) == 0
#     assert len(scratch.comments) == 0

# def test_like_scratch():
#     scratch = Scratch(
#         author='@Brian',
#         caption='My other beautiful drawing :)'
#     )

#     # Ensure likes number == 0
#     assert len(scratch.likes) == 0

#     scratch.like_scratch(like_author='@Miguel')

#     assert len(scratch.likes) == 1
#     assert '@Miguel' in scratch.likes

#     # Try liking scratch again
#     scratch.like_scratch('@Miguel')

#     # Assert no presence of double liking
#     assert len(scratch.likes) == 1

# def test_unlike_scratch():
#     scratch = Scratch(
#         author='@Harshica',
#         caption='My other other beautiful drawing :)'
#     )

#     scratch.like_scratch(like_author='@Cesar')
#     assert len(scratch.likes) == 1
    
#     # Test unlike feature works
#     scratch.unlike_scratch(target_id='@Cesar')
#     assert len(scratch.likes) == 0

#     # Add multiple likes
#     scratch.like_scratch(like_author='@Varshita')
#     scratch.like_scratch(like_author='@Miguel')
#     assert len(scratch.likes) == 2

#     # Test removing like when multiple likes exist
#     scratch.unlike_scratch(target_id='@Varshita')
#     assert len(scratch.likes) == 1
#     assert '@Varshita' not in scratch.likes
#     assert '@Miguel' in scratch.likes

# def test_add_scratch_comment():
#     scratch = Scratch(
#         author='@Cesar',
#         caption='An amazing caption :o'
#     )

#     comment = Scratch(
#         author='@Miguel',
#         caption=''
#     )
    
#     assert len(scratch.comments) == 0

#     # Ensure adding comments works
#     scratch.add_comment(comment)
#     assert len(scratch.comments) == 1
#     assert comment in scratch.comments
#     assert scratch.comments[0].author == '@Miguel'

#     comment2 = Scratch(
#         author='@Brian',
#         caption='Cool post!!'
#     )

#     # Ensure adding a second comment works
#     scratch.add_comment(comment2)
#     assert len(scratch.comments) == 2
#     assert comment2 in scratch.comments
#     assert scratch.comments[0].author == '@Miguel'
