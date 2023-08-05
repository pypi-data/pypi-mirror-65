from disco.core.exceptions import GraphQLRequestException
from disco.models import JobDetails, Task

MockListJobsResponse = [
    JobDetails({'id': '5df8db9f099035000c7b0c87', 'status': 'Done', 'request': {'meta': {'name': 'dsfgfdsgs'}}}),
    JobDetails({'id': '5df8db7af6f866000c42f04e', 'status': 'Done', 'request': {'meta': {'name': 'asddfgssdfaasd'}}}),
    JobDetails({'id': '5df8d95f32d75f000c3afb8a', 'status': 'Listed', 'request': {'meta': {'name': 'kjhlkjlkhj'}}}),
    JobDetails({'id': '5df8d91032d75f000c3afb81', 'status': 'Listed', 'request': {'meta': {'name': 'jhkjkhjhkkju'}}}),
    JobDetails( {'id': '5df8d86a32d75f000c3afb75', 'status': 'Listed', 'request': {'meta': {'name': 'asffdasdf'}}}),
    JobDetails({'id': '5db18c2fa13a79000f002696', 'status': 'Working', 'request': {'meta': {'name': 'RadioEvent'}}}),
    JobDetails({'id': '5daff5f4e0f21e000a079948', 'status': 'Done','request': {'meta': {'name': 'Dng Territory'}}}),
    JobDetails({'id': '5daea8d0e0f21e000a079397', 'status': 'Done', 'request': {'meta': {'name': 'Caring Territory'}}}),
    JobDetails({'id': '5daea77fe0f21e000a07938f', 'status': 'Done', 'request': {'meta': {'name': 'Absorbing Clover'}}}),
    JobDetails({'id': '5d89ac6493a029000a34a077', 'status': 'Done', 'request': {'meta': {'name': 'Grumpy Teaching'}}}),
    JobDetails({'id': '5d89ac0ffc4015000dd1e94f', 'status': 'Done', 'request': {'meta': {'name': 'Harmonious Boy'}}}),
    JobDetails({'id': '5d88b54afc4015000dd1e3b1', 'status': 'Done', 'request': {'meta': {'name': 'Funny Grape'}}}),
    JobDetails({'id': '5d887bd993a029000a349940', 'status': 'Done', 'request': {'meta': {'name': 'Uplifting Circle'}}}),
    JobDetails({'id': '5d887bac8d9278000a507995', 'status': 'Done', 'request': {'meta': {'name': 'Able Income'}}}),
    JobDetails({'id': '5d66595208edfa000a250dda', 'status': 'Done', 'request': {'meta': {'name': 'Cool Humor'}}})
]

MockViewJobResponse = JobDetails(
    {'id': '5df8db9f099035000c7b0c87', 'request': {'meta': {'name': 'dsfgfdsgs'}}, 'status': 'Done',
     'tasksSummary': {'queued': 0, 'running': 0, 'failed': 1, 'success': 0, 'stopped': 0,
                      'timeout': 0, 'all': 1}})

MockViewStoppedJobResponse = JobDetails(
    {'id': '5e5512465b63c9000ebb3621', 'request': {'meta': {'name': 'job to cancel'}}, 'status': 'Stopped',
     'archived': False,
     'tasksSummary': {'queued': 0, 'running': 0, 'failed': 0, 'success': 2, 'stopped': 2,
                      'timeout': 0, 'all': 4}})

MockLoginResponse = {'login': {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI1ZDY2NTkyMTRmM'
             'jAzMjAwMGI4ZmU4NzYiLCJwcm9maWxlSWQiOiI1ZDY2NTkyMTRmMjAzMjAwMGI4ZmU4'
             'NzkiLCJyb2xlcyI6WyJDb25zb2xlIl0sImlhdCI6MTU3NjY2MzUzNSwiZXhwIjoxNTc'
             '3MjY4MzM1LCJhdWQiOlsiQ29uc29sZSJdLCJzdWIiOiJBdXRoIn0.QFCLt-PMNfzpkg'
             'zNxA2F3FJKClcroECICNclrhoPIrc'}}

MockBadIdException = GraphQLRequestException("", [
    {'message': 'Cast to ObjectId failed for value "5df8db9f099035000c7b0c87afdasdsa" at path "_id" for model "Job"',
     'locations': [{'line': 2, 'column': 13}], 'path': ['fetchJob'], 'extensions': {'code': 'INTERNAL_SERVER_ERROR',
                                                                                    'exception': {'errors': [{
                                                                                        'message': 'Cast to ObjectId '
                                                                                                   'failed for value '
                                                                                                   '"5df8db9f099035000c7b0c87afdasdsa" at path "_id" for model "Job"',
                                                                                        'locations': [],
                                                                                        'path': [
                                                                                            'fetchJob']}]}}}])

MockListTasksResponse = [
    Task({'id': '5e4bef1942abec000cab2a71', 'status': 'Success', 'stats': {'duration': 17602}, 'request':
        {'inputFile': {'id': '5e4beee087b4b2000edc6f2e', 'name': 'Desktop/job-examples/primes/Data/range01.txt'}}, 'result': {'artifactIds': ['5e53a8cc5ccc95000cfffa1d']}}),
    Task({'id': '5e4bef1942abec000cab2a72', 'status': 'Success', 'stats': {'duration': 1023}, 'request':
        {'inputFile': {'id': '5e4beee987b4b2000edc6f30', 'name': 'Desktop/job-examples/primes/Data/range02.txt'}}, 'result': {'artifactIds': ['5e53a8bc3b64ee000b87d4a4']}}),
    Task({'id': '5e4bef1942abec000cab2a73', 'status': 'Success', 'stats': {'duration': 1008}, 'request':
        {'inputFile': {'id': '5e4beef687b4b2000edc6f32', 'name': 'Desktop/job-examples/primes/Data/range03.txt'}}, 'result': {'artifactIds': ['5e53a8b85ccc95000cfffa1b']}}),
    Task({'id': '5e4bef1942abec000cab2a74', 'status': 'Success', 'stats': {'duration': 3626}, 'request':
        {'inputFile': {'id': '5e4beefd2bb7d7000b92cdf8', 'name': 'Desktop/job-examples/primes/Data/range04.txt'}}, 'result': {'artifactIds': ['5e53a8c03b64ee000b87d4a6']}})
]
