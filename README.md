# Tibero Prometheus Exporter

티베로 데이터베이스의 메트릭을 수집하여 Prometheus 형식으로 제공하는 Exporter입니다.  
여러 개의 Tibero DB 인스턴스를 동시에 모니터링할 수 있으며, 메트릭 정의를 설정 파일을 통해 유연하게 구성할 수 있습니다.

---

## 수집하는 메트릭

`config.yaml` 파일 내 `metrics` 항목에 정의된 쿼리를 기반으로 메트릭을 수집합니다. 예시는 다음과 같습니다:

- `tibero_up`: 티베로 데이터베이스 연결 상태 (1: 연결됨, 0: 연결 안됨)
- `tibero_sessions_total`: 전체 세션 수
- `tibero_active_sessions`: 활성 세션 수

---

## API 엔드포인트

- `/metrics`: Prometheus 형식의 메트릭 데이터 제공
- `/health`: Exporter의 헬스 체크
- `/`: 기본 정보 페이지

---

## 설치 방법

```bash
pip install -r requirements.txt
```

---

## 설정 방법

### config.yaml

```yaml
default:
  log_level: "INFO"
  exporter:
    port: 9000

  databases:
    - name: HUNITEST
      host: 192.168.0.10
      port: 8000
      sid: HUNITEST
      username: ***********
      password: ***********
      jdbc_jar: lib/tibero6-jdbc.jar
      driver: com.tmax.tibero.jdbc.TbDriver

  metrics:
    tibero_up:
      name: tibero_up
      description: Tibero database is up and running
      labels: []
      query: "SELECT 1 FROM DUAL"

    tibero_sessions_total:
      name: tibero_sessions_total
      description: Total number of sessions
      labels: []
      query: "SELECT COUNT(*) FROM V$SESSION"

    tibero_active_sessions:
      name: tibero_active_sessions
      description: Number of active sessions
      labels: []
      query: "SELECT COUNT(*) FROM V$SESSION WHERE STATUS = 'ACTIVE'"
```

> 하나 이상의 DB 인스턴스를 `databases` 리스트에 추가할 수 있으며, 각 인스턴스에 대해 독립적인 메트릭 수집이 가능합니다.

---

## 실행 방법

```bash
python main.py
```

기본 포트는 `9000`이며, `config.yaml`에서 변경 가능합니다.

---

## Prometheus 설정 예시

```yaml
scrape_configs:
  - job_name: 'tibero'
    static_configs:
      - targets: ['localhost:9000']
```

SSL 기능은 기본적으로 비활성화되어 있으며, 별도로 설정하지 않으셔도 됩니다.

