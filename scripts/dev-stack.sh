#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="/home/giuseppe/AndroidStudioProjects/DomoticsAI"
GATEWAY_DIR="$PROJECT_ROOT/gateway"
RUN_DIR="$PROJECT_ROOT/.run"
LOG_DIR="$PROJECT_ROOT/.logs"

DEV_IP="192.168.1.40"
MQTT_GATEWAY_PORT="1883"
MQTT_APP_PORT="1884"
NODE_RED_PORT="1881"

PID_FILE="$RUN_DIR/gateway.pid"
LOG_FILE="$LOG_DIR/gateway.log"

mkdir -p "$RUN_DIR" "$LOG_DIR"

green() { printf '\033[0;32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[0;33m%s\033[0m\n' "$*"; }
red() { printf '\033[0;31m%s\033[0m\n' "$*" >&2; }

port_open() {
    local host="$1"
    local port="$2"
    timeout 2 bash -c "</dev/tcp/$host/$port" >/dev/null 2>&1
}

gateway_running() {
    [[ -f "$PID_FILE" ]] || return 1
    local pid
    pid="$(cat "$PID_FILE")"
    kill -0 "$pid" 2>/dev/null
}

start_broker() {
    green "Avvio Mosquitto..."
    sudo systemctl start mosquitto
    sudo systemctl is-active --quiet mosquitto || {
        red "Mosquitto non è attivo."
        sudo systemctl status mosquitto --no-pager || true
        exit 1
    }

    for port in "$MQTT_GATEWAY_PORT" "$MQTT_APP_PORT"; do
        if port_open "$DEV_IP" "$port"; then
            green "MQTT disponibile su $DEV_IP:$port"
        else
            red "MQTT non raggiungibile su $DEV_IP:$port"
            exit 1
        fi
    done
}

start_gateway() {
    if gateway_running; then
        yellow "Gateway già attivo, PID $(cat "$PID_FILE")."
        return
    fi

    [[ -d "$GATEWAY_DIR" ]] || {
        red "Directory Gateway non trovata: $GATEWAY_DIR"
        exit 1
    }

    if [[ ! -d "$GATEWAY_DIR/node_modules" ]]; then
        yellow "Dipendenze Node.js mancanti: eseguo npm install..."
        (
            cd "$GATEWAY_DIR"
            npm install
        )
    fi

    green "Avvio Node-RED Gateway..."
    (
        cd "$GATEWAY_DIR"
        nohup npm start >>"$LOG_FILE" 2>&1 &
        echo $! >"$PID_FILE"
    )

    for _ in {1..30}; do
        if port_open "$DEV_IP" "$NODE_RED_PORT" || port_open "127.0.0.1" "$NODE_RED_PORT"; then
            green "Gateway disponibile su http://$DEV_IP:$NODE_RED_PORT"
            return
        fi
        sleep 1
    done

    red "Gateway non raggiungibile dopo 30 secondi."
    tail -n 80 "$LOG_FILE" || true
    exit 1
}

stop_gateway() {
    if ! gateway_running; then
        yellow "Gateway non attivo."
        rm -f "$PID_FILE"
        return
    fi

    local pid
    pid="$(cat "$PID_FILE")"
    green "Arresto Gateway PID $pid..."
    kill "$pid" 2>/dev/null || true

    for _ in {1..15}; do
        kill -0 "$pid" 2>/dev/null || break
        sleep 1
    done

    if kill -0 "$pid" 2>/dev/null; then
        yellow "Arresto forzato del Gateway..."
        kill -9 "$pid" 2>/dev/null || true
    fi

    rm -f "$PID_FILE"
}

status_stack() {
    echo "=== DomoticsAI Development Stack ==="

    if systemctl is-active --quiet mosquitto; then
        green "Mosquitto: ATTIVO"
    else
        red "Mosquitto: NON ATTIVO"
    fi

    for port in "$MQTT_GATEWAY_PORT" "$MQTT_APP_PORT"; do
        if port_open "$DEV_IP" "$port"; then
            green "MQTT $DEV_IP:$port: OK"
        else
            red "MQTT $DEV_IP:$port: NON RAGGIUNGIBILE"
        fi
    done

    if gateway_running; then
        green "Gateway: ATTIVO, PID $(cat "$PID_FILE")"
    else
        red "Gateway: NON ATTIVO"
    fi

    if port_open "$DEV_IP" "$NODE_RED_PORT" || port_open "127.0.0.1" "$NODE_RED_PORT"; then
        green "Node-RED: http://$DEV_IP:$NODE_RED_PORT"
    else
        red "Node-RED porta $NODE_RED_PORT: NON RAGGIUNGIBILE"
    fi
}

show_logs() {
    touch "$LOG_FILE"
    tail -f "$LOG_FILE"
}

case "${1:-start}" in
    start)
        start_broker
        start_gateway
        status_stack
        ;;
    stop)
        stop_gateway
        green "Mosquitto resta attivo perché è un servizio di sistema."
        ;;
    restart)
        stop_gateway
        start_broker
        start_gateway
        status_stack
        ;;
    status)
        status_stack
        ;;
    logs)
        show_logs
        ;;
    *)
        echo "Uso: $0 {start|stop|restart|status|logs}"
        exit 2
        ;;
esac
