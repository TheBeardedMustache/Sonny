## restart_sonny_services.sh

    #!/usr/bin/env bash
    # restart_sonny_services.sh: Robust "Master Everything" reboot for Sonny unified agents

    set -e
    cd "$(dirname "$0")"   # Switch to script’s directory (project root or wherever placed)

    echo "Stopping any running FastAPI (uvicorn), Streamlit, and Sonny master services..."
    pkill -f "uvicorn" || true
    pkill -f "streamlit" || true
    pkill -f "Sonny.py"  || true

    sleep 2

    echo "Starting the Symbolic AI FastAPI backend..."
    PYTHONPATH=. nohup uvicorn services.symbolic_ai_service.backend.symbolic_service:app --host 0.0.0.0 --port 8000 --reload > symbolic_service.log 2>&1 &

    echo "Starting the Streamlit frontend UI..."
    PYTHONPATH=. nohup streamlit run services/frontend_service/frontend/app.py > frontend_service.log 2>&1 &

    # Optional: Launch Sonny orchestrator, if you have it
    if [ -f services/frontend_service/frontend/Sonny.py ]; then
        echo "Starting Sonny master orchestrator..."
        PYTHONPATH=. nohup python services/frontend_service/frontend/Sonny.py > sonny_master.log 2>&1 &
    fi

    echo "All Sonny core services are rebooted!"
    echo "----------------------------------------------------"
    echo "Symbolic FastAPI      : http://localhost:8000/"
    echo "Streamlit UI (Mercury): http://localhost:8501/"
    echo "Check *.log files for service logs."
