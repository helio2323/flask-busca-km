from fastapi import APIRouter, HTTPException, Depends, Request, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io
import asyncio
import uuid
from datetime import datetime

from ..core.database import get_db
from ..schemas.rota import RouteCalculate, RouteResponse, RouteMultipleCalculate, RouteBatchResponse
from ..services.route_service import RouteService
from ..models.consulta import Consulta
from ..models.upload_error import UploadError

router = APIRouter(prefix="/routes", tags=["routes"])

# Dicionário global para armazenar status dos processamentos
processing_status = {}

async def processar_rota_individual(
    index: int,
    row: pd.Series,
    upload_id: str,
    grupo_id: int,
    ip_address: str,
    route_service: 'RouteService',
    db: Session
):
    """Processa uma rota individual de forma assíncrona"""
    try:
        # Extrair ID da planilha se existir
        planilha_id = str(row.get('id', '')).strip() if 'id' in row.index and not pd.isna(row.get('id')) else None
        
        origem = str(row['origem']).strip()
        destinos_str = str(row['destino']).strip()
        
        if pd.isna(row['origem']) or pd.isna(row['destino']):
            print(f"⚠️ Linha {index + 1}: Dados inválidos (origem ou destino vazio)")
            # Salvar erro no banco
            error = UploadError(
                upload_id=upload_id,
                grupo_id=grupo_id,
                planilha_id=planilha_id,
                linha_index=index,
                origem_original=origem,
                destino_original=destinos_str,
                tipo_erro="dados_invalidos",
                mensagem_erro="Origem ou destino vazio",
                status="pendente"
            )
            db.add(error)
            return {'success': False, 'error': 'Dados inválidos', 'error_saved': True}
        
        # Separar múltiplos destinos por vírgula
        destinos = [d.strip() for d in destinos_str.split(',') if d.strip()]
        
        # Processar rota sempre via API (cache desabilitado)
        if len(destinos) == 1:
            resultado = await route_service.processar_rota(origem, destinos[0])
            resultado["fonte"] = "api"
        else:
            # Para múltiplos destinos
            resultado = await route_service.processar_rota_multipla(origem, destinos)
            resultado["fonte"] = "api"
        
        # Verificar se o resultado é válido
        distancia_valida = isinstance(resultado.get("distance"), (int, float)) and resultado.get("distance", 0) > 0
        pedagios_validos = isinstance(resultado.get("pedagios"), (int, float)) and resultado.get("pedagios", 0) >= 0
        
        if distancia_valida and pedagios_validos:
            # Salvar no histórico
            consulta = Consulta(
                planilha_id=planilha_id,
                origem=origem,
                destino=f"{destinos_str} [UPLOAD:{upload_id}]",
                distancia=resultado["distance"],
                pedagios=resultado["pedagios"],
                ip_address=ip_address,
                tipo_consulta="batch",
                grupo_id=grupo_id,
                cache_hit="false"
            )
            db.add(consulta)
            
            print(f"✅ Linha {index + 1} (ID: {planilha_id or 'N/A'}): {origem} → {destinos_str} - {resultado['distance']}km, R${resultado['pedagios']} ({resultado.get('fonte', 'api')})")
            return {'success': True, 'resultado': resultado}
        else:
            print(f"❌ Linha {index + 1} (ID: {planilha_id or 'N/A'}): Erro ao processar {origem} → {destinos_str}")
            # Salvar erro no banco
            error = UploadError(
                upload_id=upload_id,
                grupo_id=grupo_id,
                planilha_id=planilha_id,
                linha_index=index,
                origem_original=origem,
                destino_original=destinos_str,
                tipo_erro="resultado_invalido",
                mensagem_erro="Distância ou pedágios inválidos retornados pela API",
                status="pendente"
            )
            db.add(error)
            return {'success': False, 'error': 'Resultado inválido', 'error_saved': True}
            
    except Exception as e:
        print(f"❌ Erro na linha {index + 1}: {str(e)}")
        # Salvar erro no banco
        error = UploadError(
            upload_id=upload_id,
            grupo_id=grupo_id,
            planilha_id=planilha_id,
            linha_index=index,
            origem_original=origem,
            destino_original=destinos_str,
            tipo_erro="api_error",
            mensagem_erro=str(e),
            status="pendente"
        )
        db.add(error)
        return {'success': False, 'error': str(e), 'error_saved': True}

async def processar_upload_background(
    upload_id: str,
    df: pd.DataFrame,
    grupo_id: int,
    ip_address: str,
    db: Session
):
    """Processa upload em background com suporte a ID da planilha e cache"""
    try:
        processing_status[upload_id] = {
            "status": "processing",
            "total_rotas": len(df),
            "rotas_processadas": 0,
            "rotas_com_erro": 0,
            "progresso": 0,
            "inicio": datetime.now(),
            "fim": None,
            "erro": None
        }
        
        route_service = RouteService()
        rotas_processadas = 0
        rotas_com_erro = 0
        
        print(f"🚀 Iniciando processamento assíncrono de {len(df)} rotas")
        
        # Processar em lotes para não travar o sistema
        batch_size = 3  # Processar 3 rotas por vez para melhor performance
        total_rotas = len(df)
        
        for batch_start in range(0, total_rotas, batch_size):
            batch_end = min(batch_start + batch_size, total_rotas)
            batch_df = df.iloc[batch_start:batch_end]
            
            print(f"📦 Processando lote {batch_start//batch_size + 1}: rotas {batch_start + 1} a {batch_end}")
            
            # Processar lote atual
            batch_tasks = []
            for index, row in batch_df.iterrows():
                task = processar_rota_individual(
                    index, row, upload_id, grupo_id, ip_address, route_service, db
                )
                batch_tasks.append(task)
            
            # Aguardar conclusão do lote atual
            print(f"⏳ Aguardando processamento de {len(batch_tasks)} rotas do lote...")
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            print(f"✅ Lote {batch_start//batch_size + 1} processado!")
            
            # Contar resultados do lote
            for result in batch_results:
                if isinstance(result, Exception):
                    rotas_com_erro += 1
                    print(f"❌ Erro no processamento: {result}")
                else:
                    if result.get('success'):
                        rotas_processadas += 1
                    else:
                        rotas_com_erro += 1
            
            # Atualizar status após cada lote
            progresso = int(batch_end / total_rotas * 100)
            processing_status[upload_id].update({
                "rotas_processadas": rotas_processadas,
                "rotas_com_erro": rotas_com_erro,
                "progresso": progresso
            })
            
            # Commit intermediário para salvar dados em lotes
            try:
                db.commit()
                print(f"💾 Lote {batch_start//batch_size + 1} salvo no banco de dados")
            except Exception as e:
                print(f"⚠️ Erro ao salvar lote {batch_start//batch_size + 1}: {str(e)}")
                db.rollback()
            
            # Pequena pausa entre lotes para não sobrecarregar
            await asyncio.sleep(0.2)
        
        # Atualizar estatísticas do grupo
        if grupo_id:
            from ..api.groups import atualizar_estatisticas_grupo
            atualizar_estatisticas_grupo(db, grupo_id)
        
        # Marcar como concluído
        processing_status[upload_id].update({
            "status": "completed",
            "fim": datetime.now()
        })
        
        print(f"🎉 Processamento concluído: {rotas_processadas} processadas, {rotas_com_erro} erros")
        
    except Exception as e:
        processing_status[upload_id].update({
            "status": "error",
            "erro": str(e),
            "fim": datetime.now()
        })

def obter_ip_usuario(request: Request) -> str:
    """Obtém o IP do usuário"""
    # Verifica se há proxy/load balancer
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    
    real_ip = request.headers.get('X-Real-IP')
    if real_ip:
        return real_ip
    
    # IP direto - usar client.host do FastAPI
    return request.client.host if request.client else "127.0.0.1"

@router.post("/calculate", response_model=RouteResponse)
async def calculate_route(
    route_data: RouteCalculate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Calcula uma rota individual"""
    try:
        route_service = RouteService()
        
        # Processar a rota
        resultado = await route_service.processar_rota(
            route_data.origem, 
            route_data.destino
        )
        
        # Salvar no histórico
        ip_address = obter_ip_usuario(request)
        consulta = Consulta(
            origem=route_data.origem,
            destino=route_data.destino,
            distancia=resultado.get("distance") if isinstance(resultado.get("distance"), (int, float)) else None,
            pedagios=resultado.get("pedagios") if isinstance(resultado.get("pedagios"), (int, float)) else None,
            ip_address=ip_address,
            tipo_consulta="individual"
        )
        db.add(consulta)
        db.commit()
        
        return RouteResponse(**resultado)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular rota: {str(e)}")

@router.post("/calculate-multiple", response_model=RouteResponse)
async def calculate_multiple_route(
    route_data: RouteMultipleCalculate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Calcula uma rota com múltiplos destinos"""
    try:
        route_service = RouteService()
        
        # Processar a rota múltipla
        resultado = await route_service.processar_rota_multipla(
            route_data.origem, 
            route_data.destinos
        )
        
        # Salvar no histórico
        ip_address = obter_ip_usuario(request)
        destinos_str = ", ".join(route_data.destinos)
        consulta = Consulta(
            origem=route_data.origem,
            destino=destinos_str,
            distancia=resultado.get("distance") if isinstance(resultado.get("distance"), (int, float)) else None,
            pedagios=resultado.get("pedagios") if isinstance(resultado.get("pedagios"), (int, float)) else None,
            ip_address=ip_address,
            tipo_consulta="multiple"
        )
        db.add(consulta)
        db.commit()
        
        return RouteResponse(**resultado)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular rota múltipla: {str(e)}")

@router.post("/upload")
async def upload_excel(
    request: Request,
    file: UploadFile = File(...),
    grupo_id: int = None,
    db: Session = Depends(get_db)
):
    """Upload e processamento de planilha Excel em background"""
    try:
        # Verificar se é um arquivo Excel
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Arquivo deve ser Excel (.xlsx ou .xls)")
        
        # Lê o arquivo Excel
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Verifica se as colunas necessárias existem
        required_columns = ['origem', 'destino']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail="Planilha deve conter colunas: origem, destino")
        
        # Gerar ID único para este upload
        upload_id = str(uuid.uuid4())[:8]
        ip_address = obter_ip_usuario(request)
        
        print(f"📋 Upload iniciado: {file.filename} (ID: {upload_id})")
        print(f"📊 Total de linhas: {len(df)}")
        print(f"👥 Grupo: {grupo_id if grupo_id else 'Nenhum'}")
        
        # Iniciar processamento em background
        asyncio.create_task(processar_upload_background(upload_id, df, grupo_id, ip_address, db))
        
        return {
            "upload_id": upload_id,
            "status": "processing",
            "total_rotas": len(df),
            "message": "Upload iniciado. Use o upload_id para verificar o progresso."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")

@router.get("/upload-status/{upload_id}")
async def get_upload_status(upload_id: str):
    """Verifica o status de um upload em processamento"""
    if upload_id not in processing_status:
        raise HTTPException(status_code=404, detail="Upload não encontrado")
    
    return processing_status[upload_id]

@router.get("/upload-status")
async def get_all_upload_status():
    """Lista todos os uploads em processamento"""
    return {
        "uploads": processing_status,
        "total": len(processing_status)
    }

@router.get("/download-results/{filename}")
async def download_results(filename: str, db: Session = Depends(get_db)):
    """Baixa os resultados processados em formato Excel"""
    try:
        print(f"🔍 Buscando resultados para arquivo: {filename}")
        
        # Buscar apenas as consultas mais recentes (últimas 2 minutos) para pegar só o que foi processado agora
        from datetime import datetime, timedelta
        agora = datetime.now()
        dois_minutos_atras = agora - timedelta(minutes=2)
        
        consultas = db.query(Consulta).filter(
            Consulta.data_consulta >= dois_minutos_atras,
            Consulta.tipo_consulta == "batch",
            Consulta.destino.like("%[UPLOAD:%")  # Buscar apenas consultas com upload_id
        ).order_by(Consulta.data_consulta.desc()).all()
        
        print(f"📊 Consultas dos últimos 2 minutos com upload_id encontradas: {len(consultas)}")
        
        # Se não encontrou consultas recentes, buscar as 3 mais recentes do tipo batch
        if not consultas:
            consultas = db.query(Consulta).filter(
                Consulta.tipo_consulta == "batch"
            ).order_by(Consulta.data_consulta.desc()).limit(3).all()
            print(f"📊 Últimas 3 consultas batch encontradas: {len(consultas)}")
        
        # Remover duplicatas baseado na combinação origem + destino (sem upload_id)
        consultas_unicas = []
        rotas_vistas = set()
        
        for consulta in consultas:
            # Extrair destino limpo (sem upload_id)
            destino_limpo = consulta.destino
            if "[UPLOAD:" in destino_limpo:
                destino_limpo = destino_limpo.split(" [UPLOAD:")[0]
            
            chave_rota = f"{consulta.origem}|{destino_limpo}"
            if chave_rota not in rotas_vistas:
                rotas_vistas.add(chave_rota)
                consultas_unicas.append(consulta)
        
        consultas = consultas_unicas
        print(f"📊 Consultas únicas após remoção de duplicatas: {len(consultas)}")
        
        if not consultas:
            print("❌ Nenhuma consulta encontrada")
            raise HTTPException(status_code=404, detail="Nenhum resultado encontrado para este arquivo")
        
        print(f"📊 Total de consultas encontradas: {len(consultas)}")
        
        # Mostrar todas as consultas encontradas para debug
        print(f"🔍 Consultas encontradas:")
        for i, consulta in enumerate(consultas):
            print(f"  {i+1}. {consulta.origem} → {consulta.destino} ({consulta.data_consulta})")
        
        # Se encontrou mais de 3 consultas, pegar apenas as 3 mais recentes
        if len(consultas) > 3:
            consultas = consultas[:3]
            print(f"📊 Limitando para as 3 consultas mais recentes: {len(consultas)}")
        
        # Converter resultados para DataFrame
        data = []
        for consulta in consultas:
            # Limpar o upload_id do destino para exibição
            destino_limpo = consulta.destino
            if "[UPLOAD:" in destino_limpo:
                destino_limpo = destino_limpo.split(" [UPLOAD:")[0]
            
            data.append({
                "Origem": consulta.origem,
                "Destino": destino_limpo,
                "Distância (km)": consulta.distancia if consulta.distancia else "Erro",
                "Pedágios (R$)": consulta.pedagios if consulta.pedagios else "Erro",
                "Data": consulta.data_consulta.strftime("%d/%m/%Y %H:%M")
            })
        
        print(f"📋 Dados preparados: {len(data)} registros")
        
        df = pd.DataFrame(data)
        
        # Criar arquivo Excel em memória
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Resultados', index=False)
        
        output.seek(0)
        
        print(f"✅ Arquivo Excel gerado com sucesso: {len(output.getvalue())} bytes")
        
        # Retornar arquivo para download
        return StreamingResponse(
            io.BytesIO(output.read()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=resultados_{filename}.xlsx"}
        )
        
    except Exception as e:
        print(f"❌ Erro ao gerar arquivo Excel: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar arquivo Excel: {str(e)}")

@router.get("/km/{origem}/{destino}", response_model=RouteResponse)
async def get_route_km(
    origem: str,
    destino: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Endpoint compatível com a API original para cálculo de KM"""
    try:
        route_service = RouteService()
        resultado = await route_service.processar_rota(origem, destino)
        
        # Salvar no histórico
        ip_address = obter_ip_usuario(request)
        consulta = Consulta(
            origem=origem,
            destino=destino,
            distancia=resultado.get("distance") if isinstance(resultado.get("distance"), (int, float)) else None,
            pedagios=resultado.get("pedagios") if isinstance(resultado.get("pedagios"), (int, float)) else None,
            ip_address=ip_address,
            tipo_consulta="individual"
        )
        db.add(consulta)
        db.commit()
        
        return RouteResponse(**resultado)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular rota: {str(e)}")
