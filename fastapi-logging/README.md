# fastapi logging

## middleware
https://fastapi.tiangolo.com/tutorial/middleware/

fastapi의 middleware를 활용하면, 모든 request에 대해서 전/후 처리를 추가해줄 수 있습니다.

보통 백엔드 서버를 개발하게 되면, 모든 request에 대해서 로그를 남기는 작업을 middleware를 활용해서 구현할 수 있는데, Request 객체에 request에 대한 정보들도 들어있어서, 어떤 request인지와 헤더 정보 등등을 middleware에서 로깅하도록 구현하면 편하게 로깅을 구현할 수 있습니다.

## contextvars
https://docs.python.org/3/library/contextvars.html

fastapi가 등장한 이후로, python에서도 비동기로 구현하는 방식이 많이 활성화되고 있습니다.

멀티 스레딩으로 구현할 때는, thread의 context를 활용해서 로그를 남겨서 쉽게 모니터링 할 수 있었는데 비동기에서는 thread context가 없어서 해당 부분을 해소하기 위해서 등장한 것이 contextvars입니다.

contextvars는 최초 한 번 선언을 하고, set 함수를 호출하여 context를 설정해주면 get 함수를 호출해서 가져다 쓸 수 있습니다.

contextvars를 fastapi의 Middleware에서 처음에 context를 설정하게 구현하고 로그를 찍을 때 context를 항상 같이 출력하게 되면, api가 호출되어 응답이 나갈 때 까지 동일한 context로 출력이 되기 때문에, context를 기준으로 로그를 검색하면 api 한 번 호출에 대한 모든 로그를 한 눈에 볼 수 있습니다.