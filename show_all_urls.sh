#!/bin/bash

echo "🌐 SA Platform - All Service URLs"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Get Codespace info
CODESPACE_NAME="${CODESPACE_NAME:-unknown}"
DOMAIN="${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-githubpreview.dev}"

if [ "$CODESPACE_NAME" != "unknown" ]; then
    echo "📍 GitHub Codespaces Environment Detected"
    echo "────────────────────────────────────────────────────────────────────"
    echo ""

    echo "🎨 Main Services:"
    echo "  1. Main UI:          https://${CODESPACE_NAME}-8501.${DOMAIN}"
    echo "  2. Main API:         https://${CODESPACE_NAME}-8000.${DOMAIN}"
    echo "  3. API Docs:         https://${CODESPACE_NAME}-8000.${DOMAIN}/docs"
    echo "  4. Demo App:         https://${CODESPACE_NAME}-8502.${DOMAIN}"
    echo ""

    echo "📊 Development Tools:"
    echo "  5. Jupyter:          https://${CODESPACE_NAME}-8888.${DOMAIN}"
    echo "  6. MLflow:           https://${CODESPACE_NAME}-5000.${DOMAIN}"
    echo "  7. Documentation:    https://${CODESPACE_NAME}-8001.${DOMAIN}"
    echo "  8. System Monitor:   https://${CODESPACE_NAME}-8004.${DOMAIN}"
    echo "  9. Admin Dashboard:  https://${CODESPACE_NAME}-8012.${DOMAIN}"
    echo ""

    echo "🔧 Microservices:"
    echo " 10. Metrics API:      https://${CODESPACE_NAME}-8003.${DOMAIN}"
    echo " 11. Image Service:    https://${CODESPACE_NAME}-8005.${DOMAIN}"
    echo " 12. Video Service:    https://${CODESPACE_NAME}-8006.${DOMAIN}"
    echo " 13. Audio Service:    https://${CODESPACE_NAME}-8007.${DOMAIN}"
    echo " 14. Queue Manager:    https://${CODESPACE_NAME}-8008.${DOMAIN}"
    echo " 15. Storage Service:  https://${CODESPACE_NAME}-8009.${DOMAIN}"
    echo " 16. Analytics:        https://${CODESPACE_NAME}-8010.${DOMAIN}"
    echo " 17. Notifications:    https://${CODESPACE_NAME}-8011.${DOMAIN}"
    echo " 18. WebSocket:        https://${CODESPACE_NAME}-8013.${DOMAIN}"
    echo ""
else
    echo "💻 Local Environment"
    echo "────────────────────────────────────────────────────────────────────"
    echo ""

    echo "🎨 Main Services:"
    echo "  1. Main UI:          http://localhost:8501"
    echo "  2. Main API:         http://localhost:8000"
    echo "  3. API Docs:         http://localhost:8000/docs"
    echo "  4. Demo App:         http://localhost:8502"
    echo ""

    echo "📊 Development Tools:"
    echo "  5. Jupyter:          http://localhost:8888"
    echo "  6. MLflow:           http://localhost:5000"
    echo "  7. Documentation:    http://localhost:8001"
    echo "  8. System Monitor:   http://localhost:8004"
    echo "  9. Admin Dashboard:  http://localhost:8012"
    echo ""

    echo "🔧 Microservices:"
    echo " 10. Metrics API:      http://localhost:8003"
    echo " 11. Image Service:    http://localhost:8005"
    echo " 12. Video Service:    http://localhost:8006"
    echo " 13. Audio Service:    http://localhost:8007"
    echo " 14. Queue Manager:    http://localhost:8008"
    echo " 15. Storage Service:  http://localhost:8009"
    echo " 16. Analytics:        http://localhost:8010"
    echo " 17. Notifications:    http://localhost:8011"
    echo " 18. WebSocket:        http://localhost:8013"
    echo ""
fi

echo "════════════════════════════════════════════════════════════════════"
echo "💡 Tip: Open PORTS tab in VS Code to access all services easily"
echo "════════════════════════════════════════════════════════════════════"
echo ""
