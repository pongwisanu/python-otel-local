# Python Opentelemetry with local exporter

## Install
```
pip install flask opentelemetry-distro opentelemetry-exporter-otlp

opentelemetry-bootstrap -a install
```

## Show result on local
```
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name dice-server \
    flask run -p 8080
``` 

## Running collector
> Copy config  ```cp otel-collector-config.yaml /tmp```
```
docker run -p 4317:4317 \
    -v /tmp/otel-collector-config.yaml:/etc/otel-collector-config.yaml \
    otel/opentelemetry-collector:latest \
    --config=/etc/otel-collector-config.yaml
```

## Show result on exporter
```
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument --logs_exporter otlp flask run -p 8080
```