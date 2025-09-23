"use client"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Calculator, History, Home, Route, MapPin, FolderOpen } from "lucide-react"

interface SidebarProps {
  activeSection: "dashboard" | "calculator" | "history" | "groups"
  onSectionChange: (section: "dashboard" | "calculator" | "history" | "groups") => void
}

export function Sidebar({ activeSection, onSectionChange }: SidebarProps) {
  const menuItems = [
    {
      id: "dashboard" as const,
      label: "Dashboard",
      icon: Home,
      description: "Visão geral do sistema",
    },
    {
      id: "groups" as const,
      label: "Grupos de Busca",
      icon: FolderOpen,
      description: "Gerenciar grupos de rotas",
    },
    {
      id: "calculator" as const,
      label: "Calcular Rota",
      icon: Calculator,
      description: "Calcular distância e pedágios",
    },
    {
      id: "history" as const,
      label: "Histórico",
      icon: History,
      description: "Ver rotas calculadas",
    },
  ]

  return (
    <div className="w-80 bg-sidebar border-r border-sidebar-border p-6 flex flex-col">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
            <Route className="w-6 h-6 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-sidebar-foreground">RouteCalc Pro</h1>
            <p className="text-sm text-muted-foreground">Calculadora de Rotas</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-3">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = activeSection === item.id

          return (
            <Button
              key={item.id}
              variant={isActive ? "default" : "ghost"}
              className={`w-full justify-start h-auto p-4 ${
                isActive
                  ? "bg-primary text-primary-foreground hover:bg-primary/90"
                  : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              }`}
              onClick={() => onSectionChange(item.id)}
            >
              <div className="flex items-center gap-3 w-full">
                <Icon className="w-5 h-5" />
                <div className="text-left">
                  <div className="font-medium">{item.label}</div>
                  <div className="text-xs opacity-70">{item.description}</div>
                </div>
              </div>
            </Button>
          )
        })}
      </nav>

      {/* Footer */}
      <Card className="p-4 bg-card/50 border-border">
        <div className="flex items-center gap-2 mb-2">
          <MapPin className="w-4 h-4 text-primary" />
          <span className="text-sm font-medium">Status do Sistema</span>
        </div>
        <div className="text-xs text-muted-foreground">
          <div className="flex justify-between">
            <span>API:</span>
            <span className="text-green-400">Online</span>
          </div>
          <div className="flex justify-between">
            <span>Última atualização:</span>
            <span>Agora</span>
          </div>
        </div>
      </Card>
    </div>
  )
}
