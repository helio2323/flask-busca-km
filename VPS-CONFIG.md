# Configuração para VPS - Portas 5000 e 5001
# ===========================================

# Frontend: http://localhost:5000
# Backend: http://localhost:5001

# Para iniciar em produção:
# docker-compose up --build -d

# Para verificar status:
# docker-compose ps

# Para ver logs:
# docker-compose logs -f

# Para parar:
# docker-compose down

# URLs de acesso:
# - Frontend: http://SEU_IP:5000
# - Backend API: http://SEU_IP:5001
# - API Docs: http://SEU_IP:5001/docs
# - PostgreSQL: SEU_IP:5432

# Configurações de firewall (se necessário):
# sudo ufw allow 5000
# sudo ufw allow 5001
# sudo ufw allow 5432

# Configurações de proxy reverso (Nginx):
# location / {
#     proxy_pass http://localhost:5000;
#     proxy_set_header Host $host;
#     proxy_set_header X-Real-IP $remote_addr;
# }
#
# location /api/ {
#     proxy_pass http://localhost:5001;
#     proxy_set_header Host $host;
#     proxy_set_header X-Real-IP $remote_addr;
# }
