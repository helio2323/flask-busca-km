"use client"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, MapPin, Route, DollarSign, Calendar, Download, RefreshCw, AlertTriangle, Edit, Trash2, Play } from "lucide-react"
import { apiClient, GrupoRotas, UploadError } from "../../../lib/api"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

export default function GrupoRotasPage() {
  const params = useParams()
  const router = useRouter()
  const grupoId = parseInt(params.id as string)
  
  const [grupoData, setGrupoData] = useState<GrupoRotas | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [errors, setErrors] = useState<UploadError[]>([])
  const [loadingErrors, setLoadingErrors] = useState(false)
  const [editingError, setEditingError] = useState<UploadError | null>(null)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isReprocessDialogOpen, setIsReprocessDialogOpen] = useState(false)
  const [origemCorrigida, setOrigemCorrigida] = useState('')
  const [destinoCorrigido, setDestinoCorrigido] = useState('')
  const [reprocessing, setReprocessing] = useState(false)

  console.log('🔍 Componente renderizado. Grupo ID:', grupoId)

  const loadGroupData = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await apiClient.getGroupRoutes(grupoId)
      setGrupoData(data)
    } catch (err) {
      console.error('Erro ao carregar dados do grupo:', err)
      setError('Erro ao carregar dados do grupo')
    } finally {
      setLoading(false)
    }
  }

  const loadErrors = async () => {
    try {
      setLoadingErrors(true)
      console.log('🔍 Carregando erros para grupo:', grupoId)
      const errorsData = await apiClient.getGroupErrors(grupoId)
      console.log('📊 Erros carregados:', errorsData.length, errorsData)
      setErrors(errorsData)
    } catch (err) {
      console.error('❌ Erro ao carregar erros:', err)
      console.error('❌ Detalhes do erro:', err.message)
      console.error('❌ Stack trace:', err.stack)
      // Tentar carregar diretamente via fetch
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:50001/api/v1'}/groups/${grupoId}/errors`)
        if (response.ok) {
          const directErrors = await response.json()
          console.log('📊 Erros carregados via fetch direto:', directErrors.length, directErrors)
          setErrors(directErrors)
        } else {
          console.error('❌ Erro na resposta fetch:', response.status, response.statusText)
        }
      } catch (fetchErr) {
        console.error('❌ Erro no fetch direto:', fetchErr)
      }
    } finally {
      setLoadingErrors(false)
    }
  }

  useEffect(() => {
    loadGroupData()
    loadErrors()
  }, [grupoId])

  useEffect(() => {
    console.log('🔍 Estado dos erros atualizado:', errors.length, errors)
  }, [errors])

  const formatCurrency = (num: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(num)
  }

  const formatDistance = (num: number) => {
    return `${new Intl.NumberFormat('pt-BR').format(num)} km`
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const handleDownload = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:50001/api/v1'}/groups/${grupoId}/download`)
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `rotas_grupo_${grupoData?.grupo.nome || grupoId}.xlsx`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      } else {
        console.error('Erro ao baixar arquivo')
      }
    } catch (error) {
      console.error('Erro ao baixar:', error)
    }
  }

  const handleEditError = (error: UploadError) => {
    setEditingError(error)
    setOrigemCorrigida(error.origem_corrigida || error.origem_original)
    setDestinoCorrigido(error.destino_corrigido || error.destino_original)
    setIsEditDialogOpen(true)
  }

  const handleReprocessError = (error: UploadError) => {
    setEditingError(error)
    setOrigemCorrigida(error.origem_corrigida || error.origem_original)
    setDestinoCorrigido(error.destino_corrigido || error.destino_original)
    setIsReprocessDialogOpen(true)
  }

  const saveErrorEdit = async () => {
    if (!editingError) return

    try {
      await apiClient.updateUploadError(grupoId, editingError.id, {
        origem_corrigida: origemCorrigida,
        destino_corrigido: destinoCorrigido
      })
      setIsEditDialogOpen(false)
      loadErrors()
    } catch (error) {
      console.error('Erro ao salvar edição:', error)
    }
  }

  const reprocessError = async () => {
    if (!editingError) return

    try {
      setReprocessing(true)
      await apiClient.reprocessUploadError(grupoId, editingError.id, {
        origem_corrigida: origemCorrigida,
        destino_corrigido: destinoCorrigido
      })
      setIsReprocessDialogOpen(false)
      loadErrors()
      loadGroupData() // Recarregar dados do grupo para atualizar estatísticas
    } catch (error) {
      console.error('Erro ao reprocessar:', error)
    } finally {
      setReprocessing(false)
    }
  }

  const deleteError = async (errorId: number) => {
    if (!confirm('Tem certeza que deseja excluir este erro?')) return

    try {
      await apiClient.deleteUploadError(grupoId, errorId)
      loadErrors()
    } catch (error) {
      console.error('Erro ao excluir:', error)
    }
  }

  const getErrorTypeColor = (tipo: string) => {
    switch (tipo) {
      case 'api_error':
        return 'bg-red-500/20 text-red-400 border-red-500/30'
      case 'dados_invalidos':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
      case 'timeout':
        return 'bg-orange-500/20 text-orange-400 border-orange-500/30'
      case 'resultado_invalido':
        return 'bg-purple-500/20 text-purple-400 border-purple-500/30'
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    }
  }

  const getErrorTypeText = (tipo: string) => {
    switch (tipo) {
      case 'api_error':
        return 'Erro da API'
      case 'dados_invalidos':
        return 'Dados Inválidos'
      case 'timeout':
        return 'Timeout'
      case 'resultado_invalido':
        return 'Resultado Inválido'
      default:
        return 'Erro Desconhecido'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center gap-4 mb-8">
            <Button variant="outline" size="sm" onClick={() => router.back()}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Voltar
            </Button>
            <div>
              <h1 className="text-3xl font-bold">Carregando...</h1>
              <p className="text-muted-foreground">Buscando dados do grupo</p>
            </div>
          </div>
          <div className="flex items-center justify-center py-12">
            <RefreshCw className="w-8 h-8 animate-spin text-primary" />
          </div>
        </div>
      </div>
    )
  }

  if (error || !grupoData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center gap-4 mb-8">
            <Button variant="outline" size="sm" onClick={() => router.back()}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              Voltar
            </Button>
            <div>
              <h1 className="text-3xl font-bold">Grupo {grupoId}</h1>
              <p className="text-muted-foreground">Erro ao carregar dados</p>
            </div>
          </div>
          <Card>
            <CardContent className="text-center py-12">
              <p className="text-destructive mb-4">{error || 'Grupo não encontrado'}</p>
              <Button onClick={loadGroupData} variant="outline">
                <RefreshCw className="w-4 h-4 mr-2" />
                Tentar Novamente
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center gap-4 mb-8">
          <Button variant="outline" size="sm" onClick={() => router.back()}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar
          </Button>
          <div className="flex-1">
            <h1 className="text-3xl font-bold">{grupoData?.grupo.nome || `Grupo ${grupoId}`}</h1>
            <p className="text-muted-foreground">
              {grupoData?.grupo.descricao || 'Página de detalhes do grupo'}
            </p>
          </div>
          <Button onClick={handleDownload} className="hover-glow">
            <Download className="w-4 h-4 mr-2" />
            Baixar Excel
          </Button>
        </div>

        {/* Estatísticas do Grupo */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2 mb-2">
                <Route className="w-4 h-4 text-blue-400" />
                <span className="text-sm font-medium">Total de Rotas</span>
              </div>
              <div className="text-2xl font-bold text-blue-400">
                {grupoData.total_rotas}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2 mb-2">
                <MapPin className="w-4 h-4 text-green-400" />
                <span className="text-sm font-medium">Distância Total</span>
              </div>
              <div className="text-2xl font-bold text-green-400">
                {formatDistance(grupoData.rotas.reduce((sum, rota) => sum + rota.distancia, 0))}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2 mb-2">
                <DollarSign className="w-4 h-4 text-purple-400" />
                <span className="text-sm font-medium">Pedágios Total</span>
              </div>
              <div className="text-2xl font-bold text-purple-400">
                {formatCurrency(grupoData.rotas.reduce((sum, rota) => sum + rota.pedagios, 0))}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2 mb-2">
                <Calendar className="w-4 h-4 text-orange-400" />
                <span className="text-sm font-medium">Criado em</span>
              </div>
              <div className="text-sm font-bold text-orange-400">
                {formatDate(grupoData.grupo.data_criacao)}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Seção de Erros */}
        {errors.length > 0 && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-orange-400" />
                Erros de Processamento ({errors.length})
              </CardTitle>
              <CardDescription>
                Rotas que falharam no processamento e podem ser reprocessadas
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loadingErrors ? (
                <div className="flex items-center justify-center py-8">
                  <RefreshCw className="w-6 h-6 animate-spin text-primary" />
                </div>
              ) : (
                <div className="space-y-3">
                  {errors.map((error) => (
                    <div
                      key={error.id}
                      className="flex items-center justify-between p-4 rounded-lg bg-orange-500/10 border border-orange-500/20 hover:bg-orange-500/20 transition-colors"
                    >
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 bg-orange-500/20 rounded-lg flex items-center justify-center">
                          <AlertTriangle className="w-5 h-5 text-orange-400" />
                        </div>
                        <div className="space-y-1">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="font-medium text-card-foreground">
                              {error.origem_corrigida || error.origem_original} → {error.destino_corrigido || error.destino_original}
                            </span>
                            <Badge className={getErrorTypeColor(error.tipo_erro)}>
                              {getErrorTypeText(error.tipo_erro)}
                            </Badge>
                            <Badge variant="outline">
                              Linha {error.linha_index + 1}
                            </Badge>
                          </div>
                          <div className="text-sm text-muted-foreground">
                            {error.mensagem_erro && (
                              <div className="mb-1">
                                <strong>Erro:</strong> {error.mensagem_erro}
                              </div>
                            )}
                            <div className="flex items-center gap-1">
                              <Calendar className="w-3 h-3" />
                              {formatDate(error.criado_em)}
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleEditError(error)}
                        >
                          <Edit className="w-4 h-4 mr-1" />
                          Editar
                        </Button>
                        <Button
                          size="sm"
                          variant="default"
                          onClick={() => handleReprocessError(error)}
                        >
                          <Play className="w-4 h-4 mr-1" />
                          Reprocessar
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => deleteError(error.id)}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Lista de Rotas */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Route className="w-5 h-5 text-primary" />
              Rotas do Grupo ({grupoData.total_rotas})
            </CardTitle>
            <CardDescription>
              Lista detalhada de todas as rotas calculadas neste grupo
            </CardDescription>
          </CardHeader>
          <CardContent>
            {grupoData.rotas.length === 0 ? (
              <div className="text-center py-12">
                <MapPin className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">Nenhuma rota encontrada</h3>
                <p className="text-muted-foreground">
                  Este grupo ainda não possui rotas calculadas.
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {grupoData.rotas.map((rota, index) => (
                  <div
                    key={rota.id}
                    className="flex items-center justify-between p-4 rounded-lg bg-muted/20 border border-border hover:bg-muted/30 transition-colors"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center">
                        <Route className="w-5 h-5 text-primary" />
                      </div>
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-medium text-card-foreground">
                            {rota.origem} → {rota.destino}
                          </span>
                          <Badge variant="secondary">{index + 1}º</Badge>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <MapPin className="w-3 h-3" />
                            {formatDistance(rota.distancia)}
                          </div>
                          <div className="flex items-center gap-1">
                            <DollarSign className="w-3 h-3" />
                            {formatCurrency(rota.pedagios)}
                          </div>
                          <div className="flex items-center gap-1">
                            <Calendar className="w-3 h-3" />
                            {formatDate(rota.data_consulta)}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>




        {/* Diálogos */}
        <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Editar Rota com Erro</DialogTitle>
              <DialogDescription>
                Corrija a origem e destino para tentar reprocessar esta rota.
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label htmlFor="origem">Origem</Label>
                <Input
                  id="origem"
                  value={origemCorrigida}
                  onChange={(e) => setOrigemCorrigida(e.target.value)}
                  placeholder="Digite a origem corrigida"
                />
              </div>
              <div>
                <Label htmlFor="destino">Destino</Label>
                <Input
                  id="destino"
                  value={destinoCorrigido}
                  onChange={(e) => setDestinoCorrigido(e.target.value)}
                  placeholder="Digite o destino corrigido"
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsEditDialogOpen(false)}>
                Cancelar
              </Button>
              <Button onClick={saveErrorEdit}>
                Salvar Edição
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        <Dialog open={isReprocessDialogOpen} onOpenChange={setIsReprocessDialogOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Reprocessar Rota</DialogTitle>
              <DialogDescription>
                Confirme os dados corrigidos e reprocesse esta rota.
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div>
                <Label htmlFor="origem-reprocess">Origem</Label>
                <Input
                  id="origem-reprocess"
                  value={origemCorrigida}
                  onChange={(e) => setOrigemCorrigida(e.target.value)}
                  placeholder="Digite a origem corrigida"
                />
              </div>
              <div>
                <Label htmlFor="destino-reprocess">Destino</Label>
                <Input
                  id="destino-reprocess"
                  value={destinoCorrigido}
                  onChange={(e) => setDestinoCorrigido(e.target.value)}
                  placeholder="Digite o destino corrigido"
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsReprocessDialogOpen(false)}>
                Cancelar
              </Button>
              <Button onClick={reprocessError} disabled={reprocessing}>
                {reprocessing ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    Reprocessando...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 mr-2" />
                    Reprocessar
                  </>
                )}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )

}
