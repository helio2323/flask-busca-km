"use client"

import { useState, useEffect, useRef } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { MapPin, Plus, Trash2, Calculator, Route, DollarSign, Clock, Fuel, Search, Check } from "lucide-react"
import { apiClient, RouteResponse, SuggestionResponse } from "@/lib/api"

interface RoutePoint {
  id: string
  address: string
  suggestions?: SuggestionResponse[]
  showSuggestions?: boolean
}

export function RouteCalculator() {
  const [points, setPoints] = useState<RoutePoint[]>([
    { id: "1", address: "" },
    { id: "2", address: "" },
  ])
  const [isCalculating, setIsCalculating] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(false)
  const inputRefs = useRef<{ [key: string]: HTMLInputElement | null }>({})

  const addPoint = () => {
    const newPoint: RoutePoint = {
      id: Date.now().toString(),
      address: "",
    }
    setPoints([...points, newPoint])
  }

  const removePoint = (id: string) => {
    if (points.length > 2) {
      setPoints(points.filter((point) => point.id !== id))
    }
  }

  const updatePoint = (id: string, address: string) => {
    setPoints(prevPoints => prevPoints.map((point) => (point.id === id ? { ...point, address } : point)))
  }

  // Função para buscar sugestões com debounce
  const searchSuggestions = async (termo: string, pointId: string) => {
    try {
      if (termo.length < 3) {
        setPoints(prevPoints => prevPoints.map((point) => 
          point.id === pointId 
            ? { ...point, suggestions: [], showSuggestions: false }
            : point
        ))
        return
      }

      // Debounce: aguardar 500ms antes de fazer a busca
      setTimeout(async () => {
        try {
          setIsLoadingSuggestions(true)
          const suggestions = await apiClient.getCitySuggestions(termo)
          
          setPoints(prevPoints => prevPoints.map((point) => 
            point.id === pointId 
              ? { ...point, suggestions: suggestions || [], showSuggestions: true }
              : point
          ))
        } catch (error) {
          console.error('Erro ao buscar sugestões:', error)
          setPoints(prevPoints => prevPoints.map((point) => 
            point.id === pointId 
              ? { ...point, suggestions: [], showSuggestions: false }
              : point
          ))
        } finally {
          setIsLoadingSuggestions(false)
        }
      }, 500)
    } catch (error) {
      console.error('Erro na função searchSuggestions:', error)
    }
  }

  // Função para selecionar uma sugestão
  const selectSuggestion = (pointId: string, suggestion: SuggestionResponse) => {
    setPoints(prevPoints => prevPoints.map((point) => 
      point.id === pointId 
        ? { 
            ...point, 
            address: suggestion.endereco_completo || suggestion.nome,
            suggestions: [],
            showSuggestions: false
          }
        : point
    ))
  }

  // Função para fechar sugestões
  const closeSuggestions = (pointId: string) => {
    setPoints(prevPoints => prevPoints.map((point) => 
      point.id === pointId 
        ? { ...point, showSuggestions: false }
        : point
    ))
  }

  const calculateRoute = async () => {
    if (points.length < 2) return
    
    setIsCalculating(true)
    setResult(null)
    
    try {
      const origem = points[0].address
      const destinos = points.slice(1).map(point => point.address).filter(addr => addr.trim())
      
      if (destinos.length === 0) {
        throw new Error('Pelo menos um destino é necessário')
      }
      
      let response: RouteResponse
      
      if (destinos.length === 1) {
        // Rota individual - usar o novo sistema
        response = await apiClient.calculateRoute({
          origem,
          destino: destinos[0]
        })
      } else {
        // Rota múltipla - usar o novo sistema
        response = await apiClient.calculateMultipleRoute({
          origem,
          destinos
        })
      }
      
      // Processar resposta do novo sistema
      const distance = typeof response.distance === 'number' ? response.distance : parseFloat(response.distance as string) || 0
      const pedagios = typeof response.pedagios === 'number' ? response.pedagios : parseFloat(response.pedagios as string) || 0
      
      setResult({
        totalDistance: `${distance.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} km`,
        totalTolls: `R$ ${pedagios.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
        estimatedTime: response.tempo_estimado ? `${Math.floor(response.tempo_estimado / 60)}h ${Math.floor(response.tempo_estimado % 60)}min` : "N/A",
        fuelCost: response.combustivel_estimado ? `R$ ${response.combustivel_estimado.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : "N/A",
        routes: destinos.map((destino, index) => ({
          from: index === 0 ? origem : destinos[index - 1],
          to: destino,
          distance: "Calculado",
          toll: "Calculado"
        })),
        rawResponse: response
      })
    } catch (error) {
      console.error('Erro ao calcular rota:', error)
      setResult({
        totalDistance: "Erro",
        totalTolls: "Erro",
        estimatedTime: "Erro",
        fuelCost: "Erro",
        routes: [],
        error: error instanceof Error ? error.message : 'Erro desconhecido'
      })
    } finally {
      setIsCalculating(false)
    }
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-8 space-y-8 gradient-bg min-h-full">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">Calculadora de Rotas</h1>
        <p className="text-muted-foreground">Calcule distâncias e pedágios entre múltiplos pontos</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <Card className="glass-effect">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-card-foreground">
              <MapPin className="w-5 h-5 text-primary" />
              Pontos da Rota
            </CardTitle>
            <CardDescription>Adicione os pontos de origem e destino para calcular a rota</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {points.map((point, index) => (
              <div key={point.id} className="flex items-center gap-3">
                <div className="flex items-center justify-center w-8 h-8 bg-primary/20 rounded-full text-primary font-medium text-sm">
                  {index + 1}
                </div>
                <div className="flex-1 relative">
                  <Label htmlFor={`point-${point.id}`} className="sr-only">
                    Ponto {index + 1}
                  </Label>
                  <div className="relative">
                    <Input
                      ref={(el) => (inputRefs.current[point.id] = el)}
                      id={`point-${point.id}`}
                      placeholder={
                        index === 0
                          ? "Origem (ex: São Paulo, SP)"
                          : index === points.length - 1
                            ? "Destino final"
                            : "Ponto intermediário"
                      }
                      value={point.address}
                      onChange={(e) => {
                        console.log(`Input ${point.id} mudou para: "${e.target.value}"`)
                        updatePoint(point.id, e.target.value)
                        // Temporariamente desabilitar autocomplete
                        // searchSuggestions(e.target.value, point.id)
                      }}
                      onFocus={() => {
                        if (point.suggestions && point.suggestions.length > 0) {
                          setPoints(prevPoints => prevPoints.map((p) => 
                            p.id === point.id ? { ...p, showSuggestions: true } : p
                          ))
                        }
                      }}
                      onBlur={() => {
                        // Delay para permitir clique nas sugestões
                        setTimeout(() => closeSuggestions(point.id), 200)
                      }}
                      className="bg-input border-border pr-10"
                    />
                    {isLoadingSuggestions && (
                      <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                        <div className="w-4 h-4 animate-spin rounded-full border-2 border-primary border-t-transparent" />
                      </div>
                    )}
                    {!isLoadingSuggestions && point.address.length >= 3 && (
                      <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    )}
                  </div>
                  
                  {/* Dropdown de sugestões */}
                  {point.showSuggestions && point.suggestions && point.suggestions.length > 0 && (
                    <div className="absolute z-50 w-full mt-1 bg-background border border-border rounded-md shadow-lg max-h-60 overflow-y-auto">
                      {point.suggestions.map((suggestion, idx) => (
                        <div
                          key={idx}
                          className="px-4 py-3 hover:bg-muted/50 cursor-pointer border-b border-border last:border-b-0"
                          onClick={() => selectSuggestion(point.id, suggestion)}
                        >
                          <div className="flex items-center gap-2">
                            <MapPin className="w-4 h-4 text-primary flex-shrink-0" />
                            <div className="flex-1 min-w-0">
                              <div className="font-medium text-foreground truncate">
                                {suggestion.nome}
                              </div>
                              {suggestion.endereco_completo && suggestion.endereco_completo !== suggestion.nome && (
                                <div className="text-sm text-muted-foreground truncate">
                                  {suggestion.endereco_completo}
                                </div>
                              )}
                            </div>
                            <Check className="w-4 h-4 text-primary flex-shrink-0" />
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                {points.length > 2 && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removePoint(point.id)}
                    className="text-destructive hover:text-destructive hover:bg-destructive/10"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                )}
              </div>
            ))}

            <div className="flex gap-3">
              <Button variant="outline" onClick={addPoint} className="flex-1 hover-glow bg-transparent">
                <Plus className="w-4 h-4 mr-2" />
                Adicionar Ponto
              </Button>
              <Button
                onClick={calculateRoute}
                disabled={isCalculating || points.some((p) => !p.address.trim())}
                className="flex-1 hover-glow"
              >
                {isCalculating ? (
                  <>
                    <div className="w-4 h-4 mr-2 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
                    Calculando...
                  </>
                ) : (
                  <>
                    <Calculator className="w-4 h-4 mr-2" />
                    Calcular Rota
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Results Section */}
        <Card className="glass-effect">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-card-foreground">
              <Route className="w-5 h-5 text-accent" />
              Resultado do Cálculo
            </CardTitle>
            <CardDescription>Informações detalhadas sobre a rota calculada</CardDescription>
          </CardHeader>
          <CardContent>
            {result ? (
              <div className="space-y-6">
                {result.error ? (
                  <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20">
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-4 h-4 rounded-full bg-destructive" />
                      <span className="text-sm font-medium text-destructive">Erro no Cálculo</span>
                    </div>
                    <div className="text-sm text-destructive">{result.error}</div>
                  </div>
                ) : (
                  <>
                    {/* Summary Cards */}
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-4 rounded-lg bg-primary/10 border border-primary/20">
                        <div className="flex items-center gap-2 mb-2">
                          <Route className="w-4 h-4 text-primary" />
                          <span className="text-sm font-medium">Distância Total</span>
                        </div>
                        <div className="text-2xl font-bold text-primary">{result.totalDistance}</div>
                      </div>
                      <div className="p-4 rounded-lg bg-accent/10 border border-accent/20">
                        <div className="flex items-center gap-2 mb-2">
                          <DollarSign className="w-4 h-4 text-accent" />
                          <span className="text-sm font-medium">Pedágios</span>
                        </div>
                        <div className="text-2xl font-bold text-accent">{result.totalTolls}</div>
                      </div>
                      <div className="p-4 rounded-lg bg-blue-500/10 border border-blue-500/20">
                        <div className="flex items-center gap-2 mb-2">
                          <Clock className="w-4 h-4 text-blue-400" />
                          <span className="text-sm font-medium">Tempo Estimado</span>
                        </div>
                        <div className="text-2xl font-bold text-blue-400">{result.estimatedTime}</div>
                      </div>
                      <div className="p-4 rounded-lg bg-green-500/10 border border-green-500/20">
                        <div className="flex items-center gap-2 mb-2">
                          <Fuel className="w-4 h-4 text-green-400" />
                          <span className="text-sm font-medium">Combustível</span>
                        </div>
                        <div className="text-2xl font-bold text-green-400">{result.fuelCost}</div>
                      </div>
                    </div>

                    {/* Route Details */}
                    <div className="space-y-3">
                      <h4 className="font-medium text-card-foreground">Detalhes da Rota</h4>
                      {result.routes.map((route: any, index: number) => (
                        <div
                          key={index}
                          className="flex items-center justify-between p-3 rounded-lg bg-muted/20 border border-border"
                        >
                          <div>
                            <div className="font-medium text-card-foreground">
                              {route.from} → {route.to}
                            </div>
                            <div className="text-sm text-muted-foreground">
                              {route.distance} • {route.toll}
                            </div>
                          </div>
                          <Badge variant="secondary">{index + 1}º trecho</Badge>
                        </div>
                      ))}
                    </div>

                    {/* Informações adicionais */}
                    {result.rawResponse && (
                      <div className="p-4 rounded-lg bg-muted/10 border border-border">
                        <h4 className="font-medium text-card-foreground mb-2">Informações Técnicas</h4>
                        <div className="text-sm text-muted-foreground space-y-1">
                          <div>Fonte: {result.rawResponse.fonte || 'API Rotas Brasil'}</div>
                          {result.rawResponse.origem && (
                            <div>Origem: {result.rawResponse.origem}</div>
                          )}
                          {result.rawResponse.destino && (
                            <div>Destino: {result.rawResponse.destino}</div>
                          )}
                        </div>
                      </div>
                    )}

                    <Button className="w-full hover-glow">Salvar no Histórico</Button>
                  </>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-16 h-16 bg-muted/20 rounded-full flex items-center justify-center mb-4">
                  <Calculator className="w-8 h-8 text-muted-foreground" />
                </div>
                <h3 className="font-medium text-card-foreground mb-2">Nenhuma rota calculada</h3>
                <p className="text-sm text-muted-foreground">
                  Preencha os pontos da rota e clique em "Calcular Rota" para ver os resultados
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
      </div>
    </div>
  )
}
