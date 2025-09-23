"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Textarea } from "@/components/ui/textarea"
import { Plus, FolderOpen, Edit, Trash2, Play, MapPin, Clock, FileSpreadsheet, Upload, Download, X, Eye, Archive } from "lucide-react"
import { apiClient, Grupo, GrupoCreate, GrupoRotas, UploadResponse, UploadStatus } from "@/lib/api"
import { useRouter } from "next/navigation"

export function GroupManager() {
  const router = useRouter()
  const [groups, setGroups] = useState<Grupo[]>([])
  const [loading, setLoading] = useState(true)
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [newGroup, setNewGroup] = useState<GrupoCreate>({ nome: "", descricao: "" })
  const [uploadingFile, setUploadingFile] = useState<File | null>(null)
  const [selectedGroupForUpload, setSelectedGroupForUpload] = useState<number | null>(null)
  const [isUploadDialogOpen, setIsUploadDialogOpen] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle')
  const [currentUploadId, setCurrentUploadId] = useState<string | null>(null)
  const [uploadStatusData, setUploadStatusData] = useState<UploadStatus | null>(null)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isArchiveDialogOpen, setIsArchiveDialogOpen] = useState(false)
  const [selectedGroupForAction, setSelectedGroupForAction] = useState<number | null>(null)
  const [deletePassword, setDeletePassword] = useState("")
  const [deleteError, setDeleteError] = useState("")

  useEffect(() => {
    loadGroups()
  }, [])

  const loadGroups = async () => {
    try {
      setLoading(true)
      const response = await apiClient.getGroups()
      setGroups(response.grupos)
    } catch (error) {
      console.error('Erro ao carregar grupos:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateGroup = async () => {
    if (newGroup.nome.trim()) {
      try {
        const createdGroup = await apiClient.createGroup(newGroup)
        setGroups([createdGroup, ...groups])
        setNewGroup({ nome: "", descricao: "" })
        setIsCreateDialogOpen(false)
      } catch (error) {
        console.error('Erro ao criar grupo:', error)
      }
    }
  }

  const handleDeleteGroup = async (groupId: number) => {
    try {
      await apiClient.deleteGroup(groupId)
      setGroups(groups.filter(g => g.id !== groupId))
    } catch (error) {
      console.error('Erro ao deletar grupo:', error)
    }
  }

  const handleArchiveGroup = async (groupId: number) => {
    try {
      // Aqui você pode implementar a lógica de arquivamento
      // Por enquanto, vou apenas mostrar um alerta
      alert('Funcionalidade de arquivamento será implementada em breve!')
      console.log('Arquivando grupo:', groupId)
    } catch (error) {
      console.error('Erro ao arquivar grupo:', error)
    }
  }

  const openDeleteDialog = (groupId: number) => {
    setSelectedGroupForAction(groupId)
    setDeletePassword("")
    setDeleteError("")
    setIsDeleteDialogOpen(true)
  }

  const openArchiveDialog = (groupId: number) => {
    setSelectedGroupForAction(groupId)
    setIsArchiveDialogOpen(true)
  }

  const confirmDelete = async () => {
    if (deletePassword !== "715423") {
      setDeleteError("Senha incorreta!")
      return
    }

    try {
      if (selectedGroupForAction) {
        await handleDeleteGroup(selectedGroupForAction)
        setIsDeleteDialogOpen(false)
        setDeletePassword("")
        setDeleteError("")
      }
    } catch (error) {
      setDeleteError("Erro ao excluir grupo. Tente novamente.")
    }
  }

  const confirmArchive = async () => {
    try {
      if (selectedGroupForAction) {
        await handleArchiveGroup(selectedGroupForAction)
        setIsArchiveDialogOpen(false)
      }
    } catch (error) {
      console.error('Erro ao arquivar grupo:', error)
    }
  }

  const handleUploadFile = async (file: File, grupoId: number) => {
    try {
      setUploadingFile(file)
      setUploadStatus('uploading')
      setUploadProgress(0)
      
      // Fazer upload
      const response = await apiClient.uploadExcelWithGroup(file, grupoId)
      setCurrentUploadId(response.upload_id)
      
      // Iniciar polling do status
      const statusInterval = setInterval(async () => {
        try {
          const status = await apiClient.getUploadStatus(response.upload_id)
          setUploadStatusData(status)
          setUploadProgress(status.progresso)
          
          if (status.status === 'completed') {
            clearInterval(statusInterval)
            setUploadStatus('success')
            await loadGroups() // Recarregar grupos
            
            // Fechar modal após 2 segundos
            setTimeout(() => {
              setIsUploadDialogOpen(false)
              setUploadingFile(null)
              setSelectedGroupForUpload(null)
              setUploadStatus('idle')
              setUploadProgress(0)
              setCurrentUploadId(null)
              setUploadStatusData(null)
            }, 2000)
          } else if (status.status === 'error') {
            clearInterval(statusInterval)
            setUploadStatus('error')
            setUploadingFile(null)
          }
        } catch (error) {
          console.error('Erro ao verificar status:', error)
        }
      }, 1000) // Verificar a cada segundo
      
    } catch (error) {
      console.error('Erro ao fazer upload:', error)
      setUploadStatus('error')
      setUploadingFile(null)
    }
  }

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file && selectedGroupForUpload) {
      handleUploadFile(file, selectedGroupForUpload)
    }
  }

  const openUploadDialog = (groupId: number) => {
    setSelectedGroupForUpload(groupId)
    setIsUploadDialogOpen(true)
  }

  const loadGroupRoutes = async (groupId: number) => {
    router.push(`/grupos/${groupId}`)
  }

  const handleDownloadGroup = async (groupId: number, groupName: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/groups/${groupId}/download`)
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `rotas_grupo_${groupName}.xlsx`
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

  const getStatusColor = (status: string) => {
    switch (status) {
      case "ativo":
        return "bg-green-500/20 text-green-400 border-green-500/30"
      case "calculando":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
      case "concluido":
        return "bg-blue-500/20 text-blue-400 border-blue-500/30"
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30"
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case "ativo":
        return "Ativo"
      case "calculando":
        return "Calculando..."
      case "concluido":
        return "Concluído"
      default:
        return "Desconhecido"
    }
  }

  const formatCurrency = (num: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(num)
  }

  const formatDistance = (num: number) => {
    return `${new Intl.NumberFormat('pt-BR').format(num)} km`
  }

  if (loading) {
    return (
      <div className="flex-1 p-8 bg-gradient-to-br from-background via-background to-muted/20">
        <div className="max-w-7xl mx-auto">
          <div className="space-y-2 mb-8">
            <h1 className="text-3xl font-bold">Grupos de Busca</h1>
            <p className="text-muted-foreground">Carregando grupos...</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(3)].map((_, i) => (
              <Card key={i} className="animate-pulse">
                <CardHeader>
                  <div className="h-4 bg-muted rounded w-3/4"></div>
                  <div className="h-3 bg-muted rounded w-1/2"></div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="h-3 bg-muted rounded w-full"></div>
                    <div className="h-3 bg-muted rounded w-2/3"></div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="flex-1 p-8 bg-gradient-to-br from-background via-background to-muted/20">
        <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">
              Grupos de Busca
            </h1>
            <p className="text-muted-foreground mt-2">
              Organize suas rotas em grupos para cálculos em massa mais eficientes
            </p>
          </div>

          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-primary hover:bg-primary/90 text-primary-foreground">
                <Plus className="w-4 h-4 mr-2" />
                Novo Grupo
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
              <DialogHeader>
                <DialogTitle>Criar Novo Grupo</DialogTitle>
                <DialogDescription>Crie um grupo para organizar suas rotas de busca</DialogDescription>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="name">Nome do Grupo</Label>
                  <Input
                    id="name"
                    placeholder="Ex: Rotas Shopee"
                    value={newGroup.nome}
                    onChange={(e) => setNewGroup({ ...newGroup, nome: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="description">Descrição</Label>
                  <Textarea
                    id="description"
                    placeholder="Descreva o propósito deste grupo..."
                    value={newGroup.descricao || ""}
                    onChange={(e) => setNewGroup({ ...newGroup, descricao: e.target.value })}
                  />
                </div>
              </div>
              <DialogFooter>
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Cancelar
                </Button>
                <Button onClick={handleCreateGroup}>Criar Grupo</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>

        {/* Groups Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {groups.map((group) => (
            <Card
              key={group.id}
              className="bg-card/50 backdrop-blur-sm border-border hover:bg-card/70 transition-all duration-300 hover:shadow-lg hover:shadow-primary/10"
            >
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <FolderOpen className="w-5 h-5 text-primary" />
                    <CardTitle className="text-lg">{group.nome}</CardTitle>
                  </div>
                  <Badge className={`text-xs ${getStatusColor(group.status)}`}>{getStatusText(group.status)}</Badge>
                </div>
                <CardDescription className="text-sm">{group.descricao || "Sem descrição"}</CardDescription>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Stats */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="flex items-center gap-2 text-sm">
                    <MapPin className="w-4 h-4 text-muted-foreground" />
                    <span className="text-muted-foreground">Rotas:</span>
                    <span className="font-medium">{group.total_rotas}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Clock className="w-4 h-4 text-muted-foreground" />
                    <span className="text-muted-foreground">Criado:</span>
                    <span className="font-medium">{new Date(group.data_criacao).toLocaleDateString("pt-BR")}</span>
                  </div>
                </div>

                {/* Distance and Tolls */}
                {group.total_distancia > 0 && (
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="flex items-center gap-2">
                      <MapPin className="w-4 h-4 text-muted-foreground" />
                      <span className="text-muted-foreground">Distância:</span>
                      <span className="font-medium">{formatDistance(group.total_distancia)}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-muted-foreground" />
                      <span className="text-muted-foreground">Pedágios:</span>
                      <span className="font-medium">{formatCurrency(group.total_pedagios)}</span>
                    </div>
                  </div>
                )}

                {/* Actions */}
                <div className="flex gap-2 pt-2">
                  <Button
                    size="sm"
                    className="flex-1"
                    onClick={() => loadGroupRoutes(group.id)}
                  >
                    <Eye className="w-4 h-4 mr-2" />
                    Ver Rotas
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => openUploadDialog(group.id)}
                    title="Upload de planilha"
                  >
                    <Upload className="w-4 h-4" />
                  </Button>
                  {group.total_rotas > 0 && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => handleDownloadGroup(group.id, group.nome)}
                      title="Baixar planilha calculada"
                    >
                      <Download className="w-4 h-4" />
                    </Button>
                  )}
                  <Button
                    size="sm"
                    variant="outline"
                    className="text-orange-500 hover:text-orange-600 hover:bg-orange-50 bg-transparent"
                    onClick={() => openArchiveDialog(group.id)}
                    title="Arquivar grupo"
                  >
                    <Archive className="w-4 h-4" />
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    className="text-destructive hover:text-destructive bg-transparent"
                    onClick={() => openDeleteDialog(group.id)}
                    title="Excluir grupo"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}

          {/* Empty State */}
          {groups.length === 0 && (
            <Card className="col-span-full bg-card/30 border-dashed border-2 border-border">
              <CardContent className="flex flex-col items-center justify-center py-12">
                <FolderOpen className="w-12 h-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-medium mb-2">Nenhum grupo criado</h3>
                <p className="text-muted-foreground text-center mb-4">
                  Crie seu primeiro grupo para organizar suas rotas de busca
                </p>
                <Button onClick={() => setIsCreateDialogOpen(true)}>
                  <Plus className="w-4 h-4 mr-2" />
                  Criar Primeiro Grupo
                </Button>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="bg-card/30 border-border">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <FileSpreadsheet className="w-8 h-8 text-primary" />
                <div>
                  <h3 className="font-medium">Upload em Massa</h3>
                  <p className="text-sm text-muted-foreground">Importe rotas via Excel para grupos</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-card/30 border-border">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <Play className="w-8 h-8 text-green-500" />
                <div>
                  <h3 className="font-medium">Calcular Todos</h3>
                  <p className="text-sm text-muted-foreground">Execute todos os grupos ativos</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-card/30 border-border">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <MapPin className="w-8 h-8 text-blue-500" />
                <div>
                  <h3 className="font-medium">Relatórios</h3>
                  <p className="text-sm text-muted-foreground">Visualize estatísticas por grupo</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Upload Dialog */}
        <Dialog open={isUploadDialogOpen} onOpenChange={setIsUploadDialogOpen}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Upload de Planilha</DialogTitle>
              <DialogDescription>
                Faça upload de uma planilha Excel para o grupo selecionado
              </DialogDescription>
            </DialogHeader>
            
            <div className="space-y-4">
              {uploadStatus === 'idle' && (
                <div className="space-y-4">
                  <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
                    <FileSpreadsheet className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                    <p className="text-sm text-muted-foreground mb-4">
                      Selecione um arquivo Excel (.xlsx ou .xls)
                    </p>
                    <input
                      type="file"
                      accept=".xlsx,.xls"
                      onChange={handleFileSelect}
                      className="hidden"
                      id="file-upload"
                    />
                    <Button asChild>
                      <label htmlFor="file-upload" className="cursor-pointer">
                        <Upload className="w-4 h-4 mr-2" />
                        Selecionar Arquivo
                      </label>
                    </Button>
                  </div>
                  
                  <div className="text-xs text-muted-foreground">
                    <p><strong>Formato esperado:</strong></p>
                    <p>• Coluna A: origem</p>
                    <p>• Coluna B: destino</p>
                    <p>• Exemplo: "São Paulo SP" → "Rio de Janeiro RJ"</p>
                  </div>
                </div>
              )}

              {uploadStatus === 'uploading' && (
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="w-16 h-16 mx-auto mb-4 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
                    <p className="text-sm text-muted-foreground">Processando planilha em background...</p>
                    <p className="text-xs text-muted-foreground">Você pode fechar este modal e continuar navegando</p>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Progresso</span>
                      <span>{uploadProgress}%</span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2">
                      <div 
                        className="bg-primary h-2 rounded-full transition-all duration-300"
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  {uploadStatusData && (
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div className="text-center">
                        <div className="text-lg font-semibold text-green-500">
                          {uploadStatusData.rotas_processadas}
                        </div>
                        <div className="text-xs text-muted-foreground">Processadas</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-red-500">
                          {uploadStatusData.rotas_com_erro}
                        </div>
                        <div className="text-xs text-muted-foreground">Com Erro</div>
                      </div>
                    </div>
                  )}
                  
                  {uploadingFile && (
                    <p className="text-xs text-muted-foreground text-center">
                      Arquivo: {uploadingFile.name}
                    </p>
                  )}
                  
                  {currentUploadId && (
                    <p className="text-xs text-muted-foreground text-center">
                      ID: {currentUploadId}
                    </p>
                  )}
                </div>
              )}

              {uploadStatus === 'success' && (
                <div className="text-center space-y-4">
                  <div className="w-16 h-16 mx-auto mb-4 bg-green-500/20 rounded-full flex items-center justify-center">
                    <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-green-500">Upload Concluído!</h3>
                    <p className="text-sm text-muted-foreground">
                      A planilha foi processada com sucesso e as rotas foram adicionadas ao grupo.
                    </p>
                  </div>
                </div>
              )}

              {uploadStatus === 'error' && (
                <div className="text-center space-y-4">
                  <div className="w-16 h-16 mx-auto mb-4 bg-red-500/20 rounded-full flex items-center justify-center">
                    <X className="w-8 h-8 text-red-500" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-red-500">Erro no Upload</h3>
                    <p className="text-sm text-muted-foreground">
                      Ocorreu um erro ao processar a planilha. Verifique o formato e tente novamente.
                    </p>
                  </div>
                  <Button 
                    onClick={() => {
                      setUploadStatus('idle')
                      setUploadProgress(0)
                    }}
                    variant="outline"
                  >
                    Tentar Novamente
                  </Button>
                </div>
              )}
            </div>

            {uploadStatus === 'idle' && (
              <DialogFooter>
                <Button variant="outline" onClick={() => setIsUploadDialogOpen(false)}>
                  Cancelar
                </Button>
              </DialogFooter>
            )}
          </DialogContent>
        </Dialog>

        {/* Dialog de Confirmação de Exclusão */}
        <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="text-destructive">Confirmar Exclusão</DialogTitle>
              <DialogDescription>
                Esta ação não pode ser desfeita. Digite a senha para confirmar a exclusão do grupo.
              </DialogDescription>
            </DialogHeader>
            
            <div className="space-y-4">
              <div>
                <Label htmlFor="delete-password">Senha de Confirmação</Label>
                <Input
                  id="delete-password"
                  type="password"
                  value={deletePassword}
                  onChange={(e) => setDeletePassword(e.target.value)}
                  placeholder="Digite a senha"
                  className="mt-1"
                />
                {deleteError && (
                  <p className="text-sm text-destructive mt-1">{deleteError}</p>
                )}
              </div>
            </div>

            <DialogFooter>
              <Button variant="outline" onClick={() => setIsDeleteDialogOpen(false)}>
                Cancelar
              </Button>
              <Button 
                variant="destructive" 
                onClick={confirmDelete}
                disabled={!deletePassword}
              >
                Excluir Grupo
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* Dialog de Confirmação de Arquivamento */}
        <Dialog open={isArchiveDialogOpen} onOpenChange={setIsArchiveDialogOpen}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="text-orange-500">Arquivar Grupo</DialogTitle>
              <DialogDescription>
                O grupo será movido para o arquivo. Você poderá restaurá-lo posteriormente se necessário.
              </DialogDescription>
            </DialogHeader>
            
            <div className="space-y-4">
              <div className="flex items-center gap-3 p-4 bg-orange-50 border border-orange-200 rounded-lg">
                <Archive className="w-5 h-5 text-orange-500" />
                <div>
                  <p className="font-medium text-orange-800">Arquivar Grupo</p>
                  <p className="text-sm text-orange-600">
                    O grupo será movido para a seção de arquivos e não aparecerá na lista principal.
                  </p>
                </div>
              </div>
            </div>

            <DialogFooter>
              <Button variant="outline" onClick={() => setIsArchiveDialogOpen(false)}>
                Cancelar
              </Button>
              <Button 
                className="bg-orange-500 hover:bg-orange-600 text-white"
                onClick={confirmArchive}
              >
                Arquivar Grupo
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        </div>
      </div>
    </div>
  )
}

