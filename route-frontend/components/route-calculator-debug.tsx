"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { MapPin, Plus, Trash2, Calculator } from "lucide-react"

interface RoutePoint {
  id: string
  address: string
}

export function RouteCalculatorDebug() {
  const [points, setPoints] = useState<RoutePoint[]>([
    { id: "1", address: "" },
    { id: "2", address: "" },
  ])

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
    console.log(`Atualizando ponto ${id} com: "${address}"`)
    setPoints(points.map((point) => (point.id === id ? { ...point, address } : point)))
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-8 space-y-8 gradient-bg min-h-full">
        {/* Header */}
        <div className="space-y-2">
          <h1 className="text-3xl font-bold text-foreground">Calculadora de Rotas - DEBUG</h1>
          <p className="text-muted-foreground">Versão simplificada para debug</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <Card className="glass-effect">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <MapPin className="w-5 h-5 text-primary" />
                Pontos da Rota
              </CardTitle>
              <CardDescription>Teste de inputs sem autocomplete</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {points.map((point, index) => (
                <div key={point.id} className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-8 h-8 bg-primary/20 rounded-full text-primary font-medium text-sm">
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <Label htmlFor={`point-${point.id}`} className="sr-only">
                      Ponto {index + 1}
                    </Label>
                    <Input
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
                      }}
                      className="bg-input border-border"
                      autoComplete="off"
                    />
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
                  onClick={() => console.log("Pontos atuais:", points)}
                  className="flex-1 hover-glow"
                >
                  <Calculator className="w-4 h-4 mr-2" />
                  Debug Estado
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Debug Section */}
          <Card className="glass-effect">
            <CardHeader>
              <CardTitle className="text-card-foreground">Debug do Estado</CardTitle>
              <CardDescription>Estado atual dos pontos</CardDescription>
            </CardHeader>
            <CardContent>
              <pre className="bg-muted p-4 rounded-lg text-sm overflow-auto">
                {JSON.stringify(points, null, 2)}
              </pre>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
