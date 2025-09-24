"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { History, Search, Download, Eye, Trash2, Route, Calendar, MapPin, DollarSign, FolderOpen } from "lucide-react"
import { apiClient, HistoryResponse } from "../lib/api"

interface RouteHistoryItem {
  id: number
  from: string
  to: string
  distance: number | null
  toll: number | null
  date: string
  time: string
  status: "completed" | "processing" | "error"
  type: "individual" | "batch" | "multiple"
  groupId?: string
  groupName?: string
}

export function RouteHistory() {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedFilter, setSelectedFilter] = useState<"all" | "individual" | "batch">("all")
  const [selectedGroup, setSelectedGroup] = useState<string>("all")
  const [historyData, setHistoryData] = useState<RouteHistoryItem[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      setIsLoading(true)
      const data = await apiClient.getHistory()
      
      const formattedData: RouteHistoryItem[] = data.map(item => ({
        id: item.id,
        from: item.origem,
        to: item.destino,
        distance: item.distancia ? Number(item.distancia) : null,
        toll: item.pedagios ? Number(item.pedagios) : null,
        date: new Date(item.data_consulta).toLocaleDateString('pt-BR'),
        time: new Date(item.data_consulta).toLocaleTimeString('pt-BR'),
        status: "completed",
        type: item.tipo_consulta as "individual" | "batch" | "multiple"
      }))
      
      setHistoryData(formattedData)
    } catch (error) {
      console.error('Erro ao carregar histórico:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const availableGroups = Array.from(
    new Set(historyData.filter((item) => item.groupName).map((item) => ({ id: item.groupId!, name: item.groupName! }))),
  )

  const filteredHistory = historyData.filter((item) => {
    const matchesSearch =
      item.from.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.to.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (item.distance && item.distance.toString().includes(searchTerm)) ||
      (item.toll && item.toll.toString().includes(searchTerm)) ||
      (item.groupName && item.groupName.toLowerCase().includes(searchTerm.toLowerCase()))
    const matchesFilter = selectedFilter === "all" || item.type === selectedFilter
    const matchesGroup =
      selectedGroup === "all" || (selectedGroup === "no-group" && !item.groupId) || item.groupId === selectedGroup
    return matchesSearch && matchesFilter && matchesGroup
  })

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "completed":
        return <Badge className="bg-green-500/20 text-green-400 border-green-500/30">Concluído</Badge>
      case "processing":
        return <Badge className="bg-blue-500/20 text-blue-400 border-blue-500/30">Processando</Badge>
      case "error":
        return <Badge className="bg-red-500/20 text-red-400 border-red-500/30">Erro</Badge>
      default:
        return <Badge variant="secondary">{status}</Badge>
    }
  }

  const getTypeBadge = (type: string) => {
    return type === "individual" ? <Badge variant="outline">Individual</Badge> : <Badge variant="outline">Lote</Badge>
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-8 space-y-8 gradient-bg min-h-full">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">Histórico de Rotas</h1>
        <p className="text-muted-foreground">Visualize e gerencie todas as rotas calculadas anteriormente</p>
      </div>

      {/* Filters and Search */}
      <Card className="glass-effect">
        <CardContent className="pt-6">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Buscar por origem, destino ou grupo..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-input border-border"
              />
            </div>

            <Select value={selectedGroup} onValueChange={setSelectedGroup}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filtrar por grupo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos os grupos</SelectItem>
                <SelectItem value="no-group">Sem grupo</SelectItem>
                {availableGroups.map((group) => (
                  <SelectItem key={group.id} value={group.id}>
                    <div className="flex items-center gap-2">
                      <FolderOpen className="w-4 h-4" />
                      {group.name}
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <div className="flex gap-2">
              <Button
                variant={selectedFilter === "all" ? "default" : "outline"}
                onClick={() => setSelectedFilter("all")}
                className="hover-glow"
              >
                Todas
              </Button>
              <Button
                variant={selectedFilter === "individual" ? "default" : "outline"}
                onClick={() => setSelectedFilter("individual")}
                className="hover-glow"
              >
                Individual
              </Button>
              <Button
                variant={selectedFilter === "batch" ? "default" : "outline"}
                onClick={() => setSelectedFilter("batch")}
                className="hover-glow"
              >
                Lote
              </Button>
            </div>
            <Button variant="outline" className="hover-glow bg-transparent">
              <Download className="w-4 h-4 mr-2" />
              Exportar
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* History List */}
      <Card className="glass-effect">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-card-foreground">
            <History className="w-5 h-5 text-primary" />
            Rotas Calculadas ({filteredHistory.length})
          </CardTitle>
          <CardDescription>Histórico completo de todas as rotas processadas</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="w-16 h-16 bg-muted/20 rounded-full flex items-center justify-center mb-4">
                <History className="w-8 h-8 text-muted-foreground animate-spin" />
              </div>
              <h3 className="font-medium text-card-foreground mb-2">Carregando histórico...</h3>
              <p className="text-sm text-muted-foreground">Aguarde enquanto buscamos suas rotas</p>
            </div>
          ) : filteredHistory.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="w-16 h-16 bg-muted/20 rounded-full flex items-center justify-center mb-4">
                <History className="w-8 h-8 text-muted-foreground" />
              </div>
              <h3 className="font-medium text-card-foreground mb-2">Nenhuma rota encontrada</h3>
              <p className="text-sm text-muted-foreground">
                {searchTerm ? "Tente ajustar os filtros de busca" : "Calcule sua primeira rota para ver o histórico"}
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredHistory.map((item) => (
                <div
                  key={item.id}
                  className="p-4 rounded-lg bg-muted/20 border border-border hover:bg-muted/30 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center">
                        <Route className="w-6 h-6 text-primary" />
                      </div>
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-medium text-card-foreground">
                            {item.from} → {item.to}
                          </span>
                          {getTypeBadge(item.type)}
                          {getStatusBadge(item.status)}
                          {item.groupName && (
                            <Badge variant="secondary" className="bg-primary/20 text-primary border-primary/30">
                              <FolderOpen className="w-3 h-3 mr-1" />
                              {item.groupName}
                            </Badge>
                          )}
                        </div>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <MapPin className="w-3 h-3" />
                            {item.distance ? `${Number(item.distance).toLocaleString()} km` : 'N/A'}
                          </div>
                          <div className="flex items-center gap-1">
                            <DollarSign className="w-3 h-3" />
                            {item.toll ? `R$ ${Number(item.toll).toFixed(2).replace('.', ',')}` : 'N/A'}
                          </div>
                          <div className="flex items-center gap-1">
                            <Calendar className="w-3 h-3" />
                            {item.date} às {item.time}
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button variant="ghost" size="sm" className="hover-glow">
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button variant="ghost" size="sm" className="hover-glow">
                        <Download className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="text-destructive hover:text-destructive hover:bg-destructive/10"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="glass-effect hover-glow">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total de Rotas</p>
                <p className="text-2xl font-bold text-card-foreground">{historyData.length}</p>
              </div>
              <Route className="w-8 h-8 text-primary" />
            </div>
          </CardContent>
        </Card>

        <Card className="glass-effect hover-glow">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Distância Total</p>
                <p className="text-2xl font-bold text-card-foreground">3,076 km</p>
              </div>
              <MapPin className="w-8 h-8 text-accent" />
            </div>
          </CardContent>
        </Card>

        <Card className="glass-effect hover-glow">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Pedágios Totais</p>
                <p className="text-2xl font-bold text-card-foreground">R$ 303,20</p>
              </div>
              <DollarSign className="w-8 h-8 text-green-400" />
            </div>
          </CardContent>
        </Card>
      </div>
      </div>
    </div>
  )
}
