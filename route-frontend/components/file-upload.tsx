"use client"

import type React from "react"

import { useState, useCallback } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import { Upload, FileSpreadsheet, Download, CheckCircle, AlertCircle, X, FolderOpen } from "lucide-react"
import { apiClient, RouteBatchResponse } from "@/lib/api"

interface UploadedFile {
  name: string
  size: string
  status: "uploading" | "processing" | "completed" | "error"
  progress: number
  routes?: number
  groupId?: string
}

interface RouteGroup {
  id: string
  name: string
}

export function FileUpload() {
  const [files, setFiles] = useState<UploadedFile[]>([])
  const [isDragOver, setIsDragOver] = useState(false)
  const [selectedGroup, setSelectedGroup] = useState<string>("")

  const availableGroups: RouteGroup[] = [
    { id: "1", name: "Rotas Shopee" },
    { id: "2", name: "Rotas Mercado Livre" },
    { id: "3", name: "Rotas Magazine Luiza" },
  ]

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)

    const droppedFiles = Array.from(e.dataTransfer.files)
    processFiles(droppedFiles)
  }, [])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || [])
    processFiles(selectedFiles)
  }

  const processFiles = async (fileList: File[]) => {
    const newFiles: UploadedFile[] = fileList.map((file) => ({
      name: file.name,
      size: formatFileSize(file.size),
      status: "uploading",
      progress: 0,
      groupId: selectedGroup || undefined,
    }))

    setFiles((prev) => [...prev, ...newFiles])

    // Processar cada arquivo
    for (const file of fileList) {
      await processFile(file)
    }
  }

  const processFile = async (file: File) => {
    try {
      // Atualizar status para processando
      setFiles((prev) =>
        prev.map((f) =>
          f.name === file.name
            ? { ...f, status: "processing", progress: 50 }
            : f
        )
      )

      // Fazer upload para a API
      const response = await apiClient.uploadExcel(file)
      
      // Atualizar status para concluído
      setFiles((prev) =>
        prev.map((f) =>
          f.name === file.name
            ? { 
                ...f, 
                status: "completed", 
                progress: 100,
                routes: response.total_rotas
              }
            : f
        )
      )
    } catch (error) {
      console.error('Erro ao processar arquivo:', error)
      // Atualizar status para erro
      setFiles((prev) =>
        prev.map((f) =>
          f.name === file.name
            ? { ...f, status: "error", progress: 0 }
            : f
        )
      )
    }
  }

  const removeFile = (fileName: string) => {
    setFiles((prev) => prev.filter((file) => file.name !== fileName))
  }

  const downloadResults = async (fileName: string) => {
    try {
      // Buscar os resultados do arquivo processado
      const file = files.find(f => f.name === fileName)
      if (!file || !file.routes) {
        alert('Nenhum resultado encontrado para este arquivo.')
        return
      }

      // Fazer download dos resultados da API
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/routes/download-results/${encodeURIComponent(fileName)}`)
      
      if (!response.ok) {
        if (response.status === 404) {
          alert('Nenhum resultado encontrado para este arquivo.')
          return
        }
        throw new Error('Erro ao baixar resultados')
      }

      // Criar blob e fazer download
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `resultados_${fileName.replace('.xlsx', '')}.xlsx`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Erro ao baixar resultados:', error)
      alert('Erro ao baixar os resultados. Tente novamente.')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle className="w-4 h-4 text-green-400" />
      case "error":
        return <AlertCircle className="w-4 h-4 text-destructive" />
      default:
        return <div className="w-4 h-4 animate-spin rounded-full border-2 border-primary border-t-transparent" />
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case "uploading":
        return "Enviando..."
      case "processing":
        return "Processando..."
      case "completed":
        return "Concluído"
      case "error":
        return "Erro"
      default:
        return status
    }
  }

  const getGroupName = (groupId?: string) => {
    if (!groupId) return "Sem grupo"
    const group = availableGroups.find((g) => g.id === groupId)
    return group?.name || "Grupo desconhecido"
  }

  return (
    <div className="p-8 space-y-8 gradient-bg min-h-full">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">Upload de Planilhas</h1>
        <p className="text-muted-foreground">
          Importe planilhas Excel com pontos de origem e destino para cálculo em lote
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Upload Section */}
        <div className="space-y-6">
          <Card className="glass-effect">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <Upload className="w-5 h-5 text-primary" />
                Enviar Arquivo
              </CardTitle>
              <CardDescription>Arraste e solte ou clique para selecionar arquivos Excel (.xlsx, .xls)</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="group-select">Grupo de Destino</Label>
                <Select value={selectedGroup} onValueChange={setSelectedGroup}>
                  <SelectTrigger id="group-select">
                    <SelectValue placeholder="Selecione um grupo (opcional)" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="none">Sem grupo</SelectItem>
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
                <p className="text-xs text-muted-foreground">Selecione um grupo para organizar as rotas importadas</p>
              </div>

              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  isDragOver ? "border-primary bg-primary/5" : "border-border hover:border-primary/50"
                }`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FileSpreadsheet className="w-8 h-8 text-primary" />
                </div>
                <h3 className="font-medium text-card-foreground mb-2">Arraste arquivos aqui</h3>
                <p className="text-sm text-muted-foreground mb-4">ou clique para selecionar do seu computador</p>
                <input
                  type="file"
                  multiple
                  accept=".xlsx,.xls"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload">
                  <Button variant="outline" className="hover-glow bg-transparent" asChild>
                    <span>Selecionar Arquivos</span>
                  </Button>
                </label>
              </div>
            </CardContent>
          </Card>

          {/* Template Download */}
          <Card className="glass-effect">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <Download className="w-5 h-5 text-accent" />
                Modelo de Planilha
              </CardTitle>
              <CardDescription>Baixe o modelo para organizar seus dados corretamente</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 rounded-lg bg-muted/20 border border-border">
                  <h4 className="font-medium text-card-foreground mb-2">Formato Esperado:</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Coluna A: Origem (ex: São Paulo, SP)</li>
                    <li>• Coluna B: Destino (ex: Rio de Janeiro, RJ)</li>
                    <li>• Primeira linha deve conter os cabeçalhos</li>
                  </ul>
                </div>
                <Button variant="outline" className="w-full hover-glow bg-transparent">
                  <Download className="w-4 h-4 mr-2" />
                  Baixar Modelo Excel
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Files List */}
        <Card className="glass-effect">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-card-foreground">
              <FileSpreadsheet className="w-5 h-5 text-accent" />
              Arquivos Enviados
            </CardTitle>
            <CardDescription>Acompanhe o progresso do processamento dos seus arquivos</CardDescription>
          </CardHeader>
          <CardContent>
            {files.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-16 h-16 bg-muted/20 rounded-full flex items-center justify-center mb-4">
                  <FileSpreadsheet className="w-8 h-8 text-muted-foreground" />
                </div>
                <h3 className="font-medium text-card-foreground mb-2">Nenhum arquivo enviado</h3>
                <p className="text-sm text-muted-foreground">Envie arquivos Excel para começar o processamento</p>
              </div>
            ) : (
              <div className="space-y-4">
                {files.map((file, index) => (
                  <div key={index} className="p-4 rounded-lg bg-muted/20 border border-border">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        {getStatusIcon(file.status)}
                        <div>
                          <div className="font-medium text-card-foreground">{file.name}</div>
                          <div className="text-sm text-muted-foreground">
                            {file.size} • {getStatusText(file.status)}
                            {file.routes && ` • ${file.routes} rotas encontradas`}
                          </div>
                          <div className="flex items-center gap-1 mt-1">
                            <FolderOpen className="w-3 h-3 text-muted-foreground" />
                            <span className="text-xs text-muted-foreground">{getGroupName(file.groupId)}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant={file.status === "completed" ? "default" : "secondary"}>
                          {file.status === "completed" ? "Concluído" : "Processando"}
                        </Badge>
                        {file.status === "completed" && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => downloadResults(file.name)}
                            className="hover-glow"
                          >
                            <Download className="w-4 h-4 mr-1" />
                            Baixar
                          </Button>
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeFile(file.name)}
                          className="text-muted-foreground hover:text-destructive"
                        >
                          <X className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                    {file.status !== "completed" && <Progress value={file.progress} className="h-2" />}
                  </div>
                ))}

                {files.some((f) => f.status === "completed") && (
                  <Button className="w-full hover-glow">Processar Todas as Rotas</Button>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
