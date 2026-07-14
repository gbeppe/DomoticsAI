#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="/home/giuseppe/AndroidStudioProjects/DomoticsAI"
GATEWAY_DIR="$PROJECT_ROOT/gateway"
CORE_SCRIPT="$PROJECT_ROOT/core-engine/scripts/core-engine.sh"
RUN_DIR="$PROJECT_ROOT/.run"
LOG_DIR="$PROJECT_ROOT/.logs"

DEV_IP="192.168.1.40"

NODE_RED_PORT="1881"

MQTT_GATEWAY_HOST="127.0.0.1"
MQTT_GATEWAY_PORT="1883"

MQTT_APP_HOST="192.168.1.40"
MQTT_APP_PORT="1884"

CORE_URL="http://127.0.0.1:8090"

PID_FILE="$RUN_DIR/gateway.pid"
LOG_FILE="$LOG_DIR/gateway.log"

mkdir -p "$RUN_DIR" "$LOG_DIR"

green() {
    printf '\033[0;32m%s\033[0m\n' "$*"
}

yellow() {
    printf '\033[0;33m%s\033[0m\n' "$*"
}

red() {
    printf '\033[0;31m%s\033[0m\n' "$*" >&2
}

port_open() {
    local host="$1"
    local port="$2"

    timeout 2 \
      bash -c "</dev/tcp/$host/$port" \
      >/dev/null 2>&1
}

http_ok() {
    local url="$1"

    curl -fsS \
      --max-time 3 \
      "$url" \
      >/dev/null 2>&1
}

read_gateway_pid() {
    [[ -f "$PID_FILE" ]] || return 1

    local pid
    pid="$(cat "$PID_FILE" 2>/dev/null || true)"

    [[ "$pid" =~ ^[0-9]+$ ]] || return 1

    printf '%s' "$pid"
}

gateway_process_running() {
    local pid

    pid="$(read_gateway_pid)" || return 1

    kill -0 "$pid" 2>/dev/null
}

gateway_healthy() {
    http_ok \
      "http://127.0.0.1:$NODE_RED_PORT/"
}

core_health_ok() {
    http_ok \
      "$CORE_URL/health"
}

core_commands_ok() {
    http_ok \
      "$CORE_URL/api/v1/commands?limit=1"
}

check_broker() {
    if systemctl is-active --quiet mosquitto; then
        green "Mosquitto: ATTIVO"
    else
        red "Mosquitto: NON ATTIVO"
        red "Avvialo con:"
        red "sudo systemctl enable --now mosquitto"
        return 1
    fi

    if port_open \
        "$MQTT_GATEWAY_HOST" \
        "$MQTT_GATEWAY_PORT"
    then
        green \
          "MQTT Gateway disponibile su " \
          "$MQTT_GATEWAY_HOST:$MQTT_GATEWAY_PORT"
    else
        red \
          "MQTT Gateway non raggiungibile su " \
          "$MQTT_GATEWAY_HOST:$MQTT_GATEWAY_PORT"
        return 1
    fi

    if port_open \
        "$MQTT_APP_HOST" \
        "$MQTT_APP_PORT"
    then
        green \
          "MQTT App disponibile su " \
          "$MQTT_APP_HOST:$MQTT_APP_PORT"
    else
        red \
          "MQTT App non raggiungibile su " \
          "$MQTT_APP_HOST:$MQTT_APP_PORT"
        return 1
    fi
}

start_gateway() {
    if (
        gateway_process_running &&
        gateway_healthy
    ); then
        green \
          "Gateway già attivo e sano, " \
          "PID $(read_gateway_pid)."
        return
    fi

    if gateway_process_running; then
        yellow \
          "Gateway attivo ma non sano: " \
          "lo arresto."
        stop_gateway
    else
        rm -f "$PID_FILE"
    fi

    local node_red_binary
    node_red_binary="$GATEWAY_DIR/node_modules/.bin/node-red"

    if [[ ! -x "$node_red_binary" ]]; then
        yellow \
          "Dipendenze Node.js mancanti: " \
          "eseguo npm install..."

        (
            cd "$GATEWAY_DIR"
            npm install
        )
    fi

    green "Avvio Node-RED Gateway..."

    (
        cd "$GATEWAY_DIR"

        nohup "$node_red_binary" \
          --userDir "$GATEWAY_DIR" \
          --settings "$GATEWAY_DIR/settings.js" \
          "$GATEWAY_DIR/flows.json" \
          >>"$LOG_FILE" 2>&1 &

        echo $! >"$PID_FILE"
    )

    for _ in {1..30}; do
        if gateway_healthy; then
            green \
              "Gateway disponibile su " \
              "http://$DEV_IP:$NODE_RED_PORT"
            return
        fi

        sleep 1
    done

    red "Gateway non sano dopo 30 secondi."
    tail -n 80 "$LOG_FILE" || true
    return 1
}

stop_gateway() {
    local pid

    if ! pid="$(read_gateway_pid)"; then
        yellow \
          "Gateway: PID file assente " \
          "o non valido."
        rm -f "$PID_FILE"
        return
    fi

    if ! kill -0 "$pid" 2>/dev/null; then
        yellow "Gateway: PID obsoleto $pid."
        rm -f "$PID_FILE"
        return
    fi

    green "Arresto Gateway PID $pid..."

    kill "$pid" 2>/dev/null || true

    for _ in {1..15}; do
        kill -0 "$pid" 2>/dev/null || break
        sleep 1
    done

    if kill -0 "$pid" 2>/dev/null; then
        yellow \
          "Arresto forzato del Gateway..."
        kill -9 "$pid" 2>/dev/null || true
    fi

    rm -f "$PID_FILE"
}

start_core() {
    "$CORE_SCRIPT" start

    for _ in {1..20}; do
        if (
            core_health_ok &&
            core_commands_ok
        ); then
            green \
              "Core Engine: ATTIVO E SANO"
            return
        fi

        sleep 1
    done

    red \
      "Core Engine avviato ma non sano."

    tail -n 100 \
      "$LOG_DIR/core-engine.log" \
      || true

    return 1
}

stop_core() {
    "$CORE_SCRIPT" stop
}

status_stack() {
    echo \
      "=== DomoticsAI Development Stack ==="

    check_broker || true

    if gateway_process_running; then
        if gateway_healthy; then
            green \
              "Gateway: ATTIVO E SANO, " \
              "PID $(read_gateway_pid)"
        else
            red \
              "Gateway: ATTIVO MA NON RISPONDE, " \
              "PID $(read_gateway_pid)"
        fi
    elif [[ -f "$PID_FILE" ]]; then
        red "Gateway: PID OBSOLETO"
    else
        red "Gateway: NON ATTIVO"
    fi

    if core_health_ok; then
        if core_commands_ok; then
            green \
              "Core Engine: ATTIVO E SANO"
        else
            red \
              "Core Engine: ATTIVO, MA " \
              "/api/v1/commands È IN ERRORE"
        fi
    else
        red \
          "Core Engine: NON RAGGIUNGIBILE"
    fi

    "$CORE_SCRIPT" status || true
}

show_logs() {
    touch "$LOG_FILE"
    tail -f "$LOG_FILE"
}

case "${1:-start}" in
    start)
        check_broker
        start_gateway
        start_core
        status_stack
        ;;

    stop)
        stop_core
        stop_gateway
        green \
          "Mosquitto resta attivo come " \
          "servizio di sistema."
        ;;

    restart)
        stop_core
        stop_gateway
        check_broker
        start_gateway
        start_core
        status_stack
        ;;

    status)
        status_stack
        ;;

    logs)
        show_logs
        ;;

    *)
        echo \
          "Uso: $0 " \
          "{start|stop|restart|status|logs}"
        exit 2
        ;;
esac
