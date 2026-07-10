#!/bin/bash

# Diretório absoluto onde este script está localizado
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="${REPO_DIR}/$(basename "${BASH_SOURCE[0]}")"
SERVICE_NAME="datasus-metadata"

# ==============================================================================
# MODO DE INSTALAÇÃO: Executado com './cron-update.sh install'
# ==============================================================================
if [ "$1" == "install" ]; then
    echo "⚙️  Instalando timer systemd para rodar este script..."

    SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"
    mkdir -p "$SYSTEMD_USER_DIR"

    # Cria o .service apontando para ESTE MESMO script
    cat <<EOF > "${SYSTEMD_USER_DIR}/${SERVICE_NAME}.service"
[Unit]
Description=Atualiza metadados DATASUS

[Service]
Type=oneshot
WorkingDirectory=${REPO_DIR}
ExecStart=${SCRIPT_PATH}
EOF

    # Cria o .timer para as 03:00 UTC
    cat <<EOF > "${SYSTEMD_USER_DIR}/${SERVICE_NAME}.timer"
[Unit]
Description=Roda atualizacao do DATASUS as 03:00 UTC

[Timer]
OnCalendar=*-*-* 03:00:00 UTC
Persistent=true

[Install]
WantedBy=timers.target
EOF

    # Ativa o timer
    systemctl --user daemon-reload
    systemctl --user enable --now ${SERVICE_NAME}.timer

    echo "✅ Timer instalado com sucesso!"
    echo "🕒 Agendado para: 03:00 UTC"
    echo "📌 O systemd agora vai executar este mesmo script automaticamente."
    echo ""
    echo "⚠️  IMPORTANTE:"
    echo "Para rodar em background mesmo após você deslogar, certifique-se"
    echo "de que o linger está ativo no seu usuário executando o comando:"
    echo "   sudo loginctl enable-linger \$USER"
    exit 0
fi

# ==============================================================================
# MODO DE EXECUÇÃO (Payload do cronjob): Executado automaticamente pelo timer
# ==============================================================================

# Entra na pasta do repositório
cd "$REPO_DIR" || exit 1

echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Iniciando atualização..."

# Se você estiver usando o 'uv' do ecossistema Quantilica, pode alterar para:
uv run python update-metadata.py
# python3 update-metadata.py

# Faz commit e push se houver alterações
if [[ -n $(git status -s) ]]; then
    git add .
    git commit -m "chore: atualiza metadados do DATASUS - $(date +'%Y-%m-%d')"
    git push
    echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Atualização concluída e enviada ao remote."
else
    echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Nenhuma alteração detectada nos metadados."
fi
