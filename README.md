# 양덕관 (Deokkwan Yang)

**기술이 왜 등장했는지부터 이해하고 쓰는 백엔드 개발자**

[![Email](https://img.shields.io/badge/deokkwan.y@gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:deokkwan.y@gmail.com)
[![Blog](https://img.shields.io/badge/Blog-isle--blu.github.io-222222?style=flat-square&logo=githubpages&logoColor=white)](https://isle-blu.github.io)

<br/>

## 요즘 하는 일

반려동물과의 평범한 오늘을 기록하고 오래 간직하도록 돕는 서비스 **[pawmento](#pawmento)** 를 만들고 있습니다.

<br/>

## 프로젝트

### showmoa

<!-- TODO: 대표 이미지 (assets/showmoa.png) -->

전국 공연을 검색·지도·캘린더로 찾고, 관심 공연을 저장해 외부 예매처까지 연결하는 공연 정보 서비스입니다. 4인 팀에서 **CTO**를 맡아 API 설계, KOPIS 공연 데이터 동기화, 서버 배포·운영, 모니터링·성능 측정을 담당했습니다.

- **되돌릴 수 있는 것과 없는 것을 나눴습니다.** 배포가 실패하면 앱은 이전 이미지로 자동 롤백되지만, DB 스키마는 그렇게 되돌릴 수 없습니다. 그래서 스키마를 바꾸는 커밋이 들어오면 배포 스크립트가 아무것도 바꾸지 않고 멈추게 했습니다.
- **최적화보다 측정을 먼저 했습니다.** k6로 조회 API의 성능 기준선을 잡았습니다(동시 사용자 10명, p95 약 200ms, 오류 0%). 인덱스나 캐시를 바꿀 때는 이 값과 비교합니다.

`Java 21` `Spring Boot 4.1` `PostgreSQL + PostGIS` `Valkey` `Docker Compose` `Caddy` `k6`

[Backend 저장소](https://github.com/dawn-guys/showmoa-backend) · [Frontend 저장소](https://github.com/dawn-guys/showmoa-frontend)

<br/>

### test-moa

<!-- TODO: 대표 이미지 (assets/test-moa.png) -->

개발자와 테스터를 연결하는 소프트웨어 테스터 모집 플랫폼입니다. 조건에 맞는 테스터를 모집하고, 항목별 피드백을 받고, 피드백에 크레딧으로 보상합니다. 모인 피드백은 AI가 묶어 개선 우선순위를 매깁니다.

<!-- TODO: 맡은 부분 -->
<!-- TODO: "왜" 문장 1~2개 -->

`Java 21` `Spring Boot 4.1` `Spring Security` `JPA` `PostgreSQL` `Next.js` `Docker` `GitHub Actions`

[저장소](https://github.com/likelion-backendschool-9th/test-moa) · [테스트 서버](https://test-moa.newlecture.com)

<br/>

### pawmento

<!-- TODO: 대표 이미지 (assets/pawmento.png) -->

반려동물의 사진·영상·음성·글을 한곳에 보관하고, 하루 한 질문으로 평범한 일상을 쉽게 기록하도록 돕는 PWA 기반 웹·모바일 서비스입니다. 보호자가 준비되었을 때 홈 화면을 함께하는 오늘(ACTIVE)에서 기억의 정원(GARDEN)으로 직접 전환할 수 있고, 커뮤니티에서 반려 생활·돌봄·장례·추모 경험을 나눌 수 있습니다.

<!-- TODO: 맡은 부분 -->
<!-- TODO: "왜" 문장 1~2개 -->

`Java 21` `Spring Boot` `PostgreSQL` `Testcontainers` `Next.js` `PWA` `Docker`

[저장소](https://github.com/likelion-backendschool-9th/pawmento)

<br/>

## 기술 스택

**Backend**<br/>
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white)
![Spring Security](https://img.shields.io/badge/Spring_Security-6DB33F?style=flat-square&logo=springsecurity&logoColor=white)
![JPA](https://img.shields.io/badge/JPA-59666C?style=flat-square&logo=hibernate&logoColor=white)

**Database**<br/>
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![PostGIS](https://img.shields.io/badge/PostGIS-5A8DB8?style=flat-square)
![Redis (Valkey)](https://img.shields.io/badge/Redis_%28Valkey%29-DC382D?style=flat-square&logo=redis&logoColor=white)

**Infra**<br/>
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![nginx](https://img.shields.io/badge/nginx-009639?style=flat-square&logo=nginx&logoColor=white)
![Caddy](https://img.shields.io/badge/Caddy-1F88C0?style=flat-square&logo=caddy&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)

**Test**<br/>
![JUnit5](https://img.shields.io/badge/JUnit5-25A162?style=flat-square&logo=junit5&logoColor=white)
![Testcontainers](https://img.shields.io/badge/Testcontainers-291A3F?style=flat-square)
![k6](https://img.shields.io/badge/k6-7D64FF?style=flat-square&logo=k6&logoColor=white)

**Frontend (협업)**<br/>
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
