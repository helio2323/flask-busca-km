from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import pandas as pd
import io
from ..core.database import get_db
from ..schemas.grupo import GrupoCreate, GrupoResponse, GrupoList, GrupoUpdate, GrupoStats
from ..schemas.upload_error import UploadErrorResponse, UploadErrorUpdate, ReprocessErrorRequest
from ..models.grupo import Grupo
from ..models.consulta import Consulta
from ..models.upload_error import UploadError
from ..services.route_service import RouteService

def atualizar_estatisticas_grupo(db: Session, grupo_id: int):
    """Atualiza as estatísticas de um grupo baseado nas consultas"""
    try:
        print(f"🔍 Atualizando estatísticas para grupo {grupo_id}...")
        
        # Buscar estatísticas das consultas do grupo
        stats = db.query(
            func.count(Consulta.id).label('total_rotas'),
            func.coalesce(func.sum(Consulta.distancia), 0).label('total_distancia'),
            func.coalesce(func.sum(Consulta.pedagios), 0).label('total_pedagios')
        ).filter(Consulta.grupo_id == grupo_id).first()
        
        print(f"📊 Estatísticas encontradas: {stats.total_rotas} rotas, {stats.total_distancia} km, R$ {stats.total_pedagios}")
        
        # Atualizar o grupo
        grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
        if grupo:
            print(f"📝 Atualizando grupo {grupo_id}...")
            grupo.total_rotas = stats.total_rotas or 0
            grupo.total_distancia = float(stats.total_distancia or 0)
            grupo.total_pedagios = float(stats.total_pedagios or 0)
            db.commit()
            
            print(f"✅ Estatísticas atualizadas para grupo {grupo_id}: {stats.total_rotas} rotas, {stats.total_distancia} km, R$ {stats.total_pedagios}")
        else:
            print(f"❌ Grupo {grupo_id} não encontrado!")
            
    except Exception as e:
        print(f"❌ Erro ao atualizar estatísticas do grupo {grupo_id}: {str(e)}")
        db.rollback()

router = APIRouter(prefix="/groups", tags=["groups"])

@router.get("/", response_model=GrupoList)
async def get_groups(db: Session = Depends(get_db)):
    """Lista todos os grupos"""
    try:
        grupos = db.query(Grupo).filter(Grupo.status == "ativo").order_by(Grupo.data_criacao.desc()).all()
        return GrupoList(
            grupos=[GrupoResponse.model_validate(grupo) for grupo in grupos],
            total=len(grupos)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar grupos: {str(e)}")

@router.get("/stats", response_model=GrupoStats)
async def get_groups_stats(db: Session = Depends(get_db)):
    """Obtém estatísticas dos grupos"""
    try:
        total_grupos = db.query(Grupo).filter(Grupo.status == "ativo").count()
        grupos_ativos = total_grupos
        
        # Calcular totais das consultas
        stats = db.query(
            func.count(Consulta.id).label('total_rotas'),
            func.coalesce(func.sum(Consulta.distancia), 0).label('total_distancia'),
            func.coalesce(func.sum(Consulta.pedagios), 0).label('total_pedagios')
        ).join(Grupo).filter(Grupo.status == "ativo").first()
        
        return GrupoStats(
            total_grupos=total_grupos,
            total_rotas=stats.total_rotas or 0,
            total_distancia=float(stats.total_distancia or 0),
            total_pedagios=float(stats.total_pedagios or 0),
            grupos_ativos=grupos_ativos
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")

@router.post("/", response_model=GrupoResponse)
async def create_group(grupo_data: GrupoCreate, db: Session = Depends(get_db)):
    """Cria um novo grupo"""
    try:
        print(f"🔍 Dados recebidos: {grupo_data}")
        
        # Criar grupo com valores padrão explícitos
        grupo = Grupo(
            nome=grupo_data.nome,
            descricao=grupo_data.descricao,
            total_rotas=0,
            total_distancia=0.0,
            total_pedagios=0.0,
            status="ativo"
        )
        
        print(f"🔍 Grupo criado: {grupo.nome}")
        
        db.add(grupo)
        db.commit()
        db.refresh(grupo)
        
        print(f"✅ Grupo criado: {grupo.nome} (ID: {grupo.id})")
        return GrupoResponse.model_validate(grupo)
    except Exception as e:
        print(f"❌ Erro ao criar grupo: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao criar grupo: {str(e)}")

@router.get("/{grupo_id}", response_model=GrupoResponse)
async def get_group(grupo_id: int, db: Session = Depends(get_db)):
    """Obtém um grupo específico"""
    try:
        grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
        return GrupoResponse.model_validate(grupo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter grupo: {str(e)}")

@router.put("/{grupo_id}", response_model=GrupoResponse)
async def update_group(grupo_id: int, grupo_data: GrupoUpdate, db: Session = Depends(get_db)):
    """Atualiza um grupo"""
    try:
        grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
        # Atualizar apenas campos fornecidos
        update_data = grupo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(grupo, field, value)
        
        db.commit()
        db.refresh(grupo)
        
        print(f"✅ Grupo atualizado: {grupo.nome} (ID: {grupo.id})")
        return GrupoResponse.model_validate(grupo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar grupo: {str(e)}")

@router.delete("/{grupo_id}")
async def delete_group(grupo_id: int, db: Session = Depends(get_db)):
    """Arquiva um grupo (soft delete)"""
    try:
        grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
        # Soft delete - apenas marcar como excluído
        grupo.status = "excluido"
        db.commit()
        
        print(f"✅ Grupo arquivado: {grupo.nome} (ID: {grupo.id})")
        return {"message": "Grupo arquivado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao arquivar grupo: {str(e)}")

@router.get("/{grupo_id}/rotas")
async def get_group_routes(grupo_id: int, db: Session = Depends(get_db)):
    """Obtém as rotas de um grupo específico"""
    try:
        grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
        rotas = db.query(Consulta).filter(
            Consulta.grupo_id == grupo_id
        ).order_by(Consulta.data_consulta.desc()).all()
        
        return {
            "grupo": GrupoResponse.model_validate(grupo),
            "rotas": [
                {
                    "id": rota.id,
                    "origem": rota.origem,
                    "destino": rota.destino.split(" [UPLOAD:")[0] if "[UPLOAD:" in rota.destino else rota.destino,
                    "distancia": float(rota.distancia) if rota.distancia else 0,
                    "pedagios": float(rota.pedagios) if rota.pedagios else 0,
                    "data_consulta": rota.data_consulta
                }
                for rota in rotas
            ],
            "total_rotas": len(rotas)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter rotas do grupo: {str(e)}")

@router.get("/{grupo_id}/download")
async def download_grupo_rotas(grupo_id: int, db: Session = Depends(get_db)):
    """Baixa as rotas de um grupo específico em formato Excel"""
    try:
        # Verificar se o grupo existe
        grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
        # Buscar todas as rotas do grupo
        rotas = db.query(Consulta).filter(
            Consulta.grupo_id == grupo_id
        ).order_by(Consulta.data_consulta.desc()).all()
        
        if not rotas:
            raise HTTPException(status_code=404, detail="Nenhuma rota encontrada para este grupo")
        
        print(f"📊 Baixando {len(rotas)} rotas do grupo {grupo.nome} (ID: {grupo_id})")
        
        # Converter para DataFrame
        data = []
        for rota in rotas:
            # Limpar o upload_id do destino para exibição
            destino_limpo = rota.destino
            if "[UPLOAD:" in destino_limpo:
                destino_limpo = destino_limpo.split(" [UPLOAD:")[0]
            
            data.append({
                "ID": rota.planilha_id or "",
                "Origem": rota.origem,
                "UF": rota.uf_origem or "",
                "Destino": destino_limpo,
                "UF.1": rota.uf_destino or "",
                "Distância (km)": rota.distancia if rota.distancia else "Erro",
                "Pedágios (R$)": rota.pedagios if rota.pedagios is not None else 0,
                "Fonte": "Cache" if rota.cache_hit == "true" else "API",
                "Data": rota.data_consulta.strftime("%d/%m/%Y %H:%M")
            })
        
        df = pd.DataFrame(data)
        
        # Criar arquivo Excel em memória
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Rotas do Grupo', index=False)
        
        output.seek(0)
        
        print(f"✅ Arquivo Excel gerado com sucesso para grupo {grupo.nome}: {len(output.getvalue())} bytes")
        
        # Retornar arquivo para download
        return StreamingResponse(
            io.BytesIO(output.read()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=rotas_grupo_{grupo.nome.replace(' ', '_')}.xlsx"}
        )
        
    except Exception as e:
        print(f"❌ Erro ao gerar arquivo Excel do grupo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar arquivo Excel: {str(e)}")

# ===== ROTAS PARA GERENCIAR ERROS DE UPLOAD =====

@router.get("/{grupo_id}/errors", response_model=List[UploadErrorResponse])
async def listar_erros_grupo(grupo_id: int, db: Session = Depends(get_db)):
    """Lista todos os erros de upload de um grupo"""
    try:
        # Verificar se o grupo existe
        grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
        # Buscar erros do grupo
        erros = db.query(UploadError).filter(
            UploadError.grupo_id == grupo_id
        ).order_by(UploadError.criado_em.desc()).all()
        
        return erros
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao listar erros do grupo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao listar erros: {str(e)}")

@router.put("/{grupo_id}/errors/{error_id}", response_model=UploadErrorResponse)
async def atualizar_erro(
    grupo_id: int, 
    error_id: int, 
    error_update: UploadErrorUpdate, 
    db: Session = Depends(get_db)
):
    """Atualiza um erro de upload (corrige origem/destino)"""
    try:
        # Verificar se o grupo existe
        grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
        # Buscar o erro
        erro = db.query(UploadError).filter(
            UploadError.id == error_id,
            UploadError.grupo_id == grupo_id
        ).first()
        
        if not erro:
            raise HTTPException(status_code=404, detail="Erro não encontrado")
        
        # Atualizar campos fornecidos
        if error_update.origem_corrigida is not None:
            erro.origem_corrigida = error_update.origem_corrigida
        if error_update.destino_corrigido is not None:
            erro.destino_corrigido = error_update.destino_corrigido
        if error_update.status is not None:
            erro.status = error_update.status
        
        db.commit()
        db.refresh(erro)
        
        return erro
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao atualizar erro: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar erro: {str(e)}")

@router.post("/{grupo_id}/errors/{error_id}/reprocess")
async def reprocessar_erro(
    grupo_id: int,
    error_id: int,
    reprocess_request: ReprocessErrorRequest,
    db: Session = Depends(get_db)
):
    """Reprocessa um erro com origem e destino corrigidos"""
    try:
        # Verificar se o grupo existe
        grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
        # Buscar o erro
        erro = db.query(UploadError).filter(
            UploadError.id == error_id,
            UploadError.grupo_id == grupo_id
        ).first()
        
        if not erro:
            raise HTTPException(status_code=404, detail="Erro não encontrado")
        
        # Marcar como processando
        erro.status = "processando"
        erro.origem_corrigida = reprocess_request.origem_corrigida
        erro.destino_corrigido = reprocess_request.destino_corrigido
        db.commit()
        
        # Processar a rota corrigida
        route_service = RouteService()
        
        try:
            # Separar múltiplos destinos por vírgula
            destinos = [d.strip() for d in reprocess_request.destino_corrigido.split(',') if d.strip()]
            
            if len(destinos) == 1:
                resultado = await route_service.processar_rota(
                    reprocess_request.origem_corrigida, 
                    destinos[0]
                )
            else:
                resultado = await route_service.processar_rota_multipla(
                    reprocess_request.origem_corrigida, 
                    destinos
                )
            
            # Verificar se o resultado é válido
            distancia_valida = isinstance(resultado.get("distance"), (int, float)) and resultado.get("distance", 0) > 0
            pedagios_validos = isinstance(resultado.get("pedagios"), (int, float)) and resultado.get("pedagios", 0) >= 0
            
            if distancia_valida and pedagios_validos:
                # Salvar no histórico
                consulta = Consulta(
                    planilha_id=erro.planilha_id,
                    origem=reprocess_request.origem_corrigida,
                    destino=f"{reprocess_request.destino_corrigido} [REPROCESSADO:{error_id}]",
                    distancia=resultado["distance"],
                    pedagios=resultado["pedagios"],
                    ip_address="127.0.0.1",  # IP local para reprocessamento
                    tipo_consulta="reprocess",
                    grupo_id=grupo_id,
                    cache_hit="false"
                )
                db.add(consulta)
                
                # Marcar erro como sucesso
                erro.status = "sucesso"
                erro.processado_em = func.now()
                
                # Atualizar estatísticas do grupo
                atualizar_estatisticas_grupo(db, grupo_id)
                
                db.commit()
                
                return {
                    "success": True,
                    "message": "Erro reprocessado com sucesso",
                    "resultado": resultado
                }
            else:
                erro.status = "erro"
                erro.mensagem_erro = "Resultado inválido após reprocessamento"
                db.commit()
                
                return {
                    "success": False,
                    "message": "Resultado inválido após reprocessamento"
                }
                
        except Exception as e:
            erro.status = "erro"
            erro.mensagem_erro = f"Erro no reprocessamento: {str(e)}"
            db.commit()
            
            return {
                "success": False,
                "message": f"Erro no reprocessamento: {str(e)}"
            }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao reprocessar erro: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao reprocessar: {str(e)}")

@router.delete("/{grupo_id}/errors/{error_id}")
async def excluir_erro(grupo_id: int, error_id: int, db: Session = Depends(get_db)):
    """Exclui um erro de upload"""
    try:
        # Verificar se o grupo existe
        grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo não encontrado")
        
        # Buscar o erro
        erro = db.query(UploadError).filter(
            UploadError.id == error_id,
            UploadError.grupo_id == grupo_id
        ).first()
        
        if not erro:
            raise HTTPException(status_code=404, detail="Erro não encontrado")
        
        # Excluir o erro
        db.delete(erro)
        db.commit()
        
        return {"message": "Erro excluído com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao excluir erro: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao excluir erro: {str(e)}")
