#!/bin/bash

echo "🔧 Corrigindo problemas do backend..."

# Verificar se estamos no diretório correto
if [ ! -f "backend/main.py" ]; then
    echo "❌ Arquivo backend/main.py não encontrado!"
    echo "📁 Listando arquivos no diretório backend:"
    ls -la backend/
    exit 1
fi

echo "✅ Arquivo backend/main.py encontrado!"

# Verificar se o main.py tem o conteúdo correto
echo "🔍 Verificando conteúdo do main.py..."
head -5 backend/main.py

# Verificar permissões
echo "🔐 Verificando permissões..."
ls -la backend/main.py

# Testar importação Python
echo "🐍 Testando importação Python..."
cd backend
python3 -c "from main import app; print('✅ Importação bem-sucedida!')" || {
    echo "❌ Erro na importação Python!"
    echo "🔍 Verificando estrutura de diretórios:"
    ls -la
    echo "🔍 Verificando se a pasta app existe:"
    ls -la app/
    exit 1
}

echo "✅ Backend configurado corretamente!"
