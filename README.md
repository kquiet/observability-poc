# 可觀測性平台POC
可觀測性平台POC包含多個系統，統一以[docker compose](/scripts/docker-compose.yml)部署運行。

## POC各系統介紹
| 名稱 | 描述 |
|------|------|
|[Frontend](http://127.0.0.1:6080/)|前端系統，可透過點擊頁面內的button手動產生logs/metrics/traces等資料|
|Backend|後端系統，對外port未開通|
|[Grafana](http://127.0.0.1:3000/)|支援ldap帳號登入，主要用途是瀏覽平台的遙測資料。[Logs快速瀏覽](http://127.0.0.1:3000/a/grafana-lokiexplore-app/explore?patterns=%5B%5D&var-primary_label=service_name%7C%3D~%7C.%2B&from=now-15m&to=now&var-ds=d5D77Cc4-0bfE-7553-C0e2-c72CB69C5ba5&var-filters=&var-fields=&var-levels=&var-metadata=&var-patterns=&var-lineFilter=&refresh=&var-filters_replica=)、[Metrics快速瀏覽](http://127.0.0.1:3000/explore/metrics/trail?from=now-1h&to=now&timezone=browser&var-ds=8143b73E-7Fe5-4dE6-627e-4D8FfbD22b00&var-deployment_environment=&var-otel_resources=&var-filters=&metricPrefix=all)、[Logs查詢](http://127.0.0.1:3000/explore?schemaVersion=1&panes=%7B%22uw7%22:%7B%22datasource%22:%220EEa8C47-70cF-89DD-7a09-d917034F0120%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22expr%22:%22%22,%22queryType%22:%22range%22,%22datasource%22:%7B%22type%22:%22loki%22,%22uid%22:%22503f27fE-b7bB-F6C6-B541-2db6D420Beae%22%7D%7D%5D,%22range%22:%7B%22from%22:%22now-1h%22,%22to%22:%22now%22%7D%7D%7D&orgId=1)、[Metrics查詢](http://127.0.0.1:3000/explore?schemaVersion=1&panes=%7B%22g9u%22%3A%7B%22datasource%22%3A%228F0833d2-BCf2-D4C6-B16b-bED93cD0B6F9%22%2C%22queries%22%3A%5B%7B%22refId%22%3A%22A%22%2C%22expr%22%3A%22%22%2C%22range%22%3Atrue%2C%22instant%22%3Atrue%2C%22datasource%22%3A%7B%22type%22%3A%22prometheus%22%2C%22uid%22%3A%22cEda28b7-4DcC-9f85-A8F7-8AECa0C92bFc%22%7D%7D%5D%2C%22range%22%3A%7B%22from%22%3A%22now-1h%22%2C%22to%22%3A%22now%22%7D%7D%7D&orgId=1)、[Traces查詢](http://127.0.0.1:3000/explore?schemaVersion=1&panes=%7B%22ur2%22:%7B%22datasource%22:%22f91c72C9-31cE-3F79-186c-A10e8324B98E%22,%22queries%22:%5B%7B%22refId%22:%22A%22,%22datasource%22:%7B%22type%22:%22tempo%22,%22uid%22:%225BDf1CE7-0DaF-A8Ae-26B4-4fc5dE77B274%22%7D,%22queryType%22:%22traceqlSearch%22,%22limit%22:20,%22tableType%22:%22traces%22,%22filters%22:%5B%7B%22id%22:%224bc5c50c%22,%22operator%22:%22%3D%22,%22scope%22:%22resource%22,%22tag%22:%22service.name%22,%22value%22:%5B%5D%7D,%7B%22id%22:%22e67bdb83%22,%22operator%22:%22%3D%22,%22scope%22:%22span%22%7D%5D%7D%5D,%22range%22:%7B%22from%22:%22now-1h%22,%22to%22:%22now%22%7D%7D%7D&orgId=1)、[管理資料來源](http://127.0.0.1:3000/connections/datasources)、[管理/自訂儀表版](http://127.0.0.1:3000/dashboards)|
|[Prometheus](http://127.0.0.1:9090/)|主要用途是蒐集各系統的metrics|
|OtelCollector|主要用途是蒐集/轉送前端及後端系統產生的可觀測性資料，對外port未開通|
|Grafana-Loki|主要用途是儲存Logs，對外port未開通|
|Grafana-Tempo|主要用途是儲存Traces，對外port未開通|
|Grafana-Mimir|主要用途是儲存Metrics，對外port未開通|
|MariaDB|主要用途是儲存Grafana設定及後端系統API使用，對外port未開通|
|[Adminer](http://127.0.0.1:6082/)|網頁版的資料庫工具，主要用途是查看MariaDB資料|
|API Call Simulator|主要用途是模擬API呼叫，產生遙測資料|

## 啟動方式

### 前置條件
- 已安裝 Docker 與 Docker Compose

### 步驟

1. 在 `scripts/` 目錄下建立 `.env` 檔案，填入 LDAP 帳號資訊：
   ```
   LDAP_USERNAME=your_ldap_username
   LDAP_PASSWORD=your_ldap_password
   ```

2. 啟動所有服務：
   ```bash
   cd scripts
   docker compose up -d
   ```

3. 確認所有容器正常運行：
   ```bash
   docker compose ps
   ```

4. 停止所有服務：
   ```bash
   docker compose down
   ```

> 首次啟動時，MariaDB 需要初始化，Grafana 會等待 MariaDB 健康檢查通過後才啟動，請稍等片刻。

## 目錄結構

```
observability-poc/
├── backend/                        # POC後端應用程式 (Python/FastAPI)
│   ├── app/                        # 應用程式主體
│   ├── Dockerfile
│   ├── logging_config.yaml         # 日誌設定
│   └── pyproject.toml
├── docs/                           # 文件
│   └── plantuml/                   # PlantUML 圖檔原始碼
├── frontend/                       # POC前端應用程式 (Vue.js)
│   ├── src/                        # 前端原始碼
│   ├── resources/                  # nginx 設定
│   ├── Dockerfile
│   └── vite.config.js
├── library/                        # 可重用整合套件
│   ├── javascript/
│   │   └── otel-integration-lib/   # 前端 OpenTelemetry 整合套件
│   └── python/
│       └── fastapi_metrics_prometheus/  # FastAPI Prometheus metrics 套件
└── scripts/                        # 部署相關設定
    ├── docker-compose.yml          # 主要部署設定檔
    ├── grafana/                    # Grafana 設定 (ldap、provisioning)
    ├── grafana-loki/               # Loki 設定
    ├── grafana-mimir/              # Mimir 設定
    ├── grafana-tempo/              # Tempo 設定
    ├── mariadb/                    # MariaDB 初始化 SQL
    ├── otel-collector/             # OpenTelemetry Collector 設定
    ├── prometheus/                 # Prometheus 設定
    └── logs/                       # 應用程式 log 掛載目錄
```

## Log架構
![架構圖](https://www.plantuml.com/plantuml/png/dPDThjem48NVlOhP01leGmL-hzeTH1Cp2HR-SUq925NilIPoAUGQSs-U4ddEEUEPJzucniYJDIAWEk98i0l1Q8MilKlmHm14KenkD0G_K1sqezry3F3FCKJlcDo-IvV4P1DW0bkatR9Ol03As-0TERxxgxvPVNtgr-VlgtQbrkXM53NN1wrdCieRGufzhFPvKXJ_e0s1yMDtycQoLFNbSYhoPGqsUtzsc-zr4to3SzHCnTo-qDkeIFX_mzSQRFbvs78bRBaEjbm5MtuPjbm9MpPWorUmPHjswqALg2RigxY_-PzzedZ2NXlDbry6UV3HvdK-hcUCEA3377RKjobzw1wFQjfdMLRiaR77H60lwRSfvVbVm8CIDdcAHNw-_u4vL7Gb8GjOXTjKE6yZUKlTb6X6EGdnxgLCuNNJzkBRNZ4jnic5FlfpeYYsEMkovYy0)

## Metric架構
![架構圖](https://www.plantuml.com/plantuml/png/fPDDRi8m48NtFiLSW0kmgC3xghr1D34ciUeVrvuKeOgxrxAS4XT7GkaAcFdUcwU7V8Y4WIQZcKVnWOE4e_TQ2IJbR8Hl1X2a8BI3bl2AObHM7lCOG3ZZdPMMm97KmccTI1S08vX2TjKcg-Oxv-0iINlguZMIDB6IFIppnUhcZ3HrXNwOm-vb9HliOIJoMNYhWlRfSordlMl5B4HBzNlhrcgPFzqotzOotzWoNscPjrhc_s-PRsgPDrg-CJQVU-kZ35_OAwte-gwHpYwOR7mtzS4PIQESSXhdk_iWSISax35A60AUqM9db56XaDMiCYsRcblQcMlyr6MTlpC62nHs9tUngU0gpznhJGOrZ9JGsIbH939KQJDHHovsgR0_wFBzpAKNU1tbJw3jL_cCTrk0-LTCacwAClyl4sDJbYuwsaCVt2K1x93oJKR_0000)

## Trace架構
![架構圖](https://www.plantuml.com/plantuml/png/fP9DRiCW48Ntd68ku0jq4INig_O6rfXC7AlyK1WtYYhVlGG5jSYXIjEDRV6-nppys4R6mBFHmgDwmv5WvxsU5FBaR8HF0H18CTfH4poZEawMTdaPG3dZdINBu9YqSbedqWN02EPAzfMINMNE8JZBPFTzF4Sc4olRIimJgva5kUdBz9AVAmswsNURHaHuWYEphv8EwTqAMhHcpk9UkHefitHtoELMF_BkVkHZ_SW7-v6_z2CR_SZ_z2CVwaUs-YdI_I4NiGXHShuCaS873fEU-FogaGykc9peEyqOy80MUwQqSidaV5-jtQ9hBX5xP1mm4fXpVDTNENyB0JzGwFRkPBlDQaevGGs7QJnoeijcYMBbBqTitDFyavgR5vVycmip59sXVewKh_Cin0nTPKhu4Dmf0MAR-fgD_W80)