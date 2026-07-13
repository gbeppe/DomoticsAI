#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="/home/giuseppe/AndroidStudioProjects/DomoticsAI"
CORE_DIR="$PROJECT_ROOT/core-engine"
RUN_DIR="$PROJECT_ROOT/.run"
LOG_DIR="$PROJECT_ROOT/.logs"
PID_FILE="$RUN_DIR/core-engine.pid"
LOG_FILE="$LOG_DIR/core-engine.log"
VENV_DIR="$CORE_DIR/.venv"

mkdir -p "$RUN_DIR" "$LOG_DIR"

running() {
    [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

install_dependencies() {
    [[ -x "$VENV_DIR/bin/python" ]] || python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install --upgrade pip
    "$VENV_DIR/bin/pip" install -e "$CORE_DIR"
}

start_service() {
    if running; then
        echo "Core Engine già attivo, PID $(cat "$PID_FILE")."
        return
    fi

    install_dependencies

    (
        cd "$CORE_DIR"
        nohup "$VENV_DIR/bin/python" run.py >>"$LOG_FILE" 2>&1 &
        echo $! >"$PID_FILE"
    )

    for _ in {1..30}; do
        if timeout 2 bash -c "</dev/tcp/127.0.0.1/8090" >/dev/null 2>&1; then
            echo "Core Engine disponibile su http://192.168.1.40:8090"
            return
        fi
        sleep 1
    done

    echo "Core Engine non raggiungibile."
    tail -n 100 "$LOG_FILE" || true
    exit 1
}

stop_service() {
    if running; then
        kill "$(cat "$PID_FILE")" 2>/dev/null || true
    fi
    rm -f "$PID_FILE"
}

status_service() {
    if running; then
        echo "Core Engine ATTIVO, PID $(cat "$PID_FILE")"
    else
        echo "Core Engine NON ATTIVO"
    fi
}

case "${1:-start}" in
    start) start_service ;;
    stop) stop_service ;;
    restart)
        stop_service
        start_service
        ;;
    status) status_service ;;
    logs)
        touch "$LOG_FILE"
        tail -f "$LOG_FILE"
        ;;
    *)
        echo "Uso: $0 {start|stop|restart|status|logs}"
        exit 2
        ;;
esac
