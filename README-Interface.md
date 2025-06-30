# 🚛 Busca KM - Nova Interface Web

## 📋 Visão Geral

A nova interface web do Busca KM oferece uma experiência moderna e intuitiva para calcular rotas e pedágios entre cidades brasileiras, com visualização no mapa.

## 🎯 Funcionalidades

### 📍 Busca Individual
- Calcule rotas pontuais entre duas cidades
- Visualização imediata dos resultados
- Integração com mapa interativo

### 📊 Upload de Planilha
- Processe múltiplas rotas de uma vez
- Suporte para rotas sequenciais
- Download dos resultados em CSV

### 🗺️ Visualização no Mapa
- Mapa interativo com OpenStreetMap
- Visualização das rotas calculadas
- Marcadores de origem e destino
- Controles de navegação

### 💾 Downloads
- Modelo de planilha pré-formatado
- Exportação de resultados em CSV
- Compatível com Excel

## 🚀 Como Usar

### 1. Busca Individual
1. Digite a cidade de origem (ex: "São Paulo SP")
2. Digite a cidade de destino (ex: "Rio de Janeiro RJ")
3. Clique em "🔍 Calcular"
4. Veja o resultado na lista de rotas
5. Clique na rota para visualizar no mapa

### 2. Upload de Planilha
1. Clique em "📥 Modelo de Planilha" para baixar o template
2. Preencha o arquivo com suas rotas
3. Arraste o arquivo para a área de upload ou clique para selecionar
4. Clique em "📤 Processar Planilha"
5. Aguarde o processamento
6. Visualize os resultados na lista
7. Baixe o CSV com os resultados

### 3. Formato da Planilha

#### Colunas Obrigatórias:
- **origem**: Cidade de origem (ex: "São Paulo SP")
- **destino**: Cidade de destino (ex: "Rio de Janeiro RJ")

#### Rotas Sequenciais:
Para criar uma rota que passa por múltiplas cidades, separe os destinos por vírgula:
- **Exemplo**: "Rio de Janeiro RJ, Belo Horizonte MG"
- **Resultado**: São Paulo → Rio de Janeiro → Belo Horizonte

#### Exemplos:
```csv
origem,destino
"São Paulo SP","Rio de Janeiro RJ"
"Rio de Janeiro RJ","Belo Horizonte MG"
"São Paulo SP","Rio de Janeiro RJ, Belo Horizonte MG"
"Brasília DF","Goiânia GO, São Paulo SP"
```

## 🗺️ Funcionalidades do Mapa

### Controles Disponíveis:
- **🇧🇷**: Centralizar no Brasil
- **🗑️**: Limpar rotas do mapa

### Interação:
- Clique em uma rota na lista para visualizar no mapa
- Zoom automático para mostrar toda a rota
- Popups informativos nos marcadores

## 📱 Design Responsivo

A interface se adapta automaticamente a diferentes tamanhos de tela:
- **Desktop**: Layout em duas colunas (painel + mapa)
- **Mobile**: Layout empilhado (painel sobre mapa)

## 🎨 Características Visuais

### Layout:
- **Painel Lateral**: Controles e lista de rotas
- **Mapa Principal**: Visualização interativa
- **Design Moderno**: Gradientes e sombras suaves

### Cores:
- **Primária**: Azul/Roxo (#667eea → #764ba2)
- **Sucesso**: Verde (#28a745)
- **Info**: Azul (#17a2b8)
- **Erro**: Vermelho (#dc3545)

### Status das Rotas:
- 🟢 **Verde**: Rota calculada com sucesso
- 🔴 **Vermelho**: Erro no cálculo
- 🟡 **Amarelo**: Processando

## 🔧 Tecnologias Utilizadas

### Frontend:
- **HTML5 + CSS3**: Estrutura e estilização
- **JavaScript ES6+**: Interatividade
- **Leaflet.js**: Mapa interativo
- **OpenStreetMap**: Tiles do mapa

### Backend:
- **Python + Quart**: Servidor assíncrono
- **Pandas**: Processamento de planilhas
- **API Rotas Brasil**: Cálculo de rotas

## 📊 Exemplo de Uso Completo

1. **Acesse**: http://localhost:5000
2. **Teste Individual**: 
   - Origem: "São Paulo SP"
   - Destino: "Rio de Janeiro RJ"
   - Resultado: ~431 km, R$ 52,20
3. **Teste Planilha**:
   - Baixe o modelo
   - Adicione suas rotas
   - Faça upload
   - Visualize no mapa
4. **Export**: Baixe os resultados em CSV

## 🎯 Vantagens da Nova Interface

- ✅ **Visual Moderno**: Interface limpa e profissional
- ✅ **Mapa Interativo**: Visualização das rotas
- ✅ **Responsivo**: Funciona em qualquer dispositivo
- ✅ **Intuitivo**: Fácil de usar
- ✅ **Eficiente**: Cache inteligente
- ✅ **Completo**: Upload, cálculo e download

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs: `./run-local.sh logs`
2. Reinicie o servidor: `./run-local.sh restart`
3. Verifique o status: `./run-local.sh status`

---

🚛 **Busca KM** - Calculadora de Rotas e Pedágios do Brasil 