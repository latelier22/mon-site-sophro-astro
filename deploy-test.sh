#!/bin/bash
set -e

SSH_USER="yljd7979"
SSH_HOST="109.234.164.204"
REMOTE_DIR="/home/yljd7979/test"

echo "📦 Build Astro..."
npm run build

echo "📁 Création du dossier distant..."
ssh ${SSH_USER}@${SSH_HOST} "mkdir -p ${REMOTE_DIR}"

echo "🚀 Envoi vers ${REMOTE_DIR}..."
rsync -avz --delete dist/ ${SSH_USER}@${SSH_HOST}:${REMOTE_DIR}/

echo "✅ Déploiement terminé : ${REMOTE_DIR}"
