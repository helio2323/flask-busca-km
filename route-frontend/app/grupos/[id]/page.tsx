"use client"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, MapPin } from "lucide-react"

export default function GrupoRotasPage() {
  const params = useParams()
  const router = useRouter()
  const grupoId = parseInt(params.id as string)

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
            <p className="text-muted-foreground">Página de detalhes do grupo</p>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="w-5 h-5 text-primary" />
              Detalhes do Grupo
            </CardTitle>
            <CardDescription>
              Esta página será implementada em breve
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-center py-12">
              <MapPin className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium mb-2">Em Desenvolvimento</h3>
              <p className="text-muted-foreground">
                Esta funcionalidade está sendo desenvolvida.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
