# Docker

## Prerequisites

- Docker
- [Docker Compose](https://docs.docker.com/compose/install/#install-compose) v2.0.0+
- 5 GB of RAM

## Clone Repo

- Clone this repository:

```shell
git clone https://github.com/TelemetryHub/opentelemetry-demo.git
```

## Open Folder

- Navigate to the cloned folder:

```shell
cd opentelemetry-demo/
```

## Add Ingest Key
A custom `otelcol-config-extras.yml` file has been added to this repo which configures
pipelines to send to TelemetryHub. Just add your Ingest Key as described in
[BYOB](#bring-your-own-backend) below!

## Run Docker Compose

- Start the demo:

```shell
docker compose up --no-build
```

> **Note:** If you're running on Apple Silicon, please run `docker compose
> build` in order to create local images vs. pulling them from the repository.

**Note:** The `--no-build` flag is used to fetch released docker images from
[ghcr](http://ghcr.io/open-telemetry/demo) instead of building from source.
Removing the `--no-build` command line option will rebuild all images from
source. It may take more than 20 minutes to build if the flag is omitted.

## Verify the Webstore & the Telemetry

Once the images are built and containers are started you can access:

- Webstore: <http://localhost:8080/>
- Grafana: <http://localhost:8080/grafana/>
- Feature Flags UI: <http://localhost:8080/feature/>
- Load Generator UI: <http://localhost:8080/loadgen/>
- Jaeger UI: <http://localhost:8080/jaeger/ui/>

## Bring your own backend

Likely you want to use this as a demo application for an observability
backend you already have (e.g. TelemetryHub, right?).
OpenTelemetry Collector can be used to export telemetry data to multiple
backends. By default, the collector in the demo application will merge the
configuration from two files:

- otelcol-config.yml
- otelcol-config-extras.yml

**Edit otelcol-config-extras.yml and input your own Ingest Key to begin sending data to
TelemetryHub. The necessary pipelines have already been added.**

After updating the `otelcol-config-extras.yml`, start the demo by running
`docker compose up`. After a while, you should see the traces flowing into
your backend as well.
