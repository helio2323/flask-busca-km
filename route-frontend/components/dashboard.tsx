import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Calculator, History, TrendingUp, MapPin, Clock, DollarSign, Route, Users, Package } from "lucide-react"
import { useState, useEffect } from "react"
import { apiClient, GrupoStats, HistoryResponse } from "@/lib/api"

export function Dashboard() {
  const [stats, setStats] = useState<GrupoStats | null>(null)
  const [recentRoutes, setRecentRoutes] = useState<HistoryResponse[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      
      // Dados mockados para quando o backend não estiver disponível
      const mockStats: GrupoStats = {
        total_grupos: 3,
        total_rotas: 15,
        total_distancia: 2500,
        total_pedagios: 450.50,
        grupos_ativos: 2
      }
      
      const mockHistory: HistoryResponse[] = [
        {
          id: 1,
          origem: "São Paulo, SP",
          destino: "Rio de Janeiro, RJ",
          distancia: 429,
          pedagios: 45.50,
          data_consulta: new Date().toISOString(),
          ip_address: "127.0.0.1",
          tipo_consulta: "individual"
        },
        {
          id: 2,
          origem: "Belo Horizonte, MG",
          destino: "Brasília, DF",
          distancia: 747,
          pedagios: 78.20,
          data_consulta: new Date(Date.now() - 3600000).toISOString(),
          ip_address: "127.0.0.1",
          tipo_consulta: "individual"
        }
      ]
      
      // Tentar carregar dados reais, mas usar mock se falhar
      try {
        const [statsData, historyData] = await Promise.all([
          apiClient.getGroupsStats(),
          apiClient.getHistory()
        ])
        
        setStats(statsData)
        setRecentRoutes(historyData.slice(0, 5))
      } catch (apiError) {
        console.warn('Backend não disponível, usando dados mockados:', apiError)
        setStats(mockStats)
        setRecentRoutes(mockHistory)
      }
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error)
      // Em caso de erro, usar dados mockados
      setStats({
        total_grupos: 0,
        total_rotas: 0,
        total_distancia: 0,
        total_pedagios: 0,
        grupos_ativos: 0
      })
      setRecentRoutes([])
    } finally {
      setLoading(false)
    }
  }

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('pt-BR').format(num)
  }

  const formatCurrency = (num: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(num)
  }

  const formatDistance = (num: number) => {
    return `${formatNumber(num)} km`
  }

  const getTimeAgo = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
    
    if (diffInHours < 1) return 'Agora mesmo'
    if (diffInHours < 24) return `${diffInHours}h atrás`
    const diffInDays = Math.floor(diffInHours / 24)
    return `${diffInDays} dia${diffInDays > 1 ? 's' : ''} atrás`
  }

  if (loading) {
    return (
      <div className="p-8 space-y-8 gradient-bg min-h-full">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground">Carregando dados...</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="glass-effect">
              <CardHeader className="animate-pulse">
                <div className="h-4 bg-muted rounded w-3/4"></div>
              </CardHeader>
              <CardContent className="animate-pulse">
                <div className="h-8 bg-muted rounded w-1/2 mb-2"></div>
                <div className="h-3 bg-muted rounded w-2/3"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  const statsCards = [
    {
      title: "Grupos Ativos",
      value: stats?.total_grupos.toString() || "0",
      icon: Users,
      color: "text-primary",
    },
    {
      title: "Rotas Calculadas",
      value: formatNumber(stats?.total_rotas || 0),
      icon: Route,
      color: "text-accent",
    },
    {
      title: "Distância Total",
      value: formatDistance(stats?.total_distancia || 0),
      icon: MapPin,
      color: "text-blue-400",
    },
    {
      title: "Pedágios Calculados",
      value: formatCurrency(stats?.total_pedagios || 0),
      icon: DollarSign,
      color: "text-green-400",
    },
  ]

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-8 space-y-8 gradient-bg min-h-full">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
        <p className="text-muted-foreground">
          Bem-vindo ao RouteCalc Pro - Sua solução completa para cálculo de rotas e pedágios
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statsCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <Card key={index} className="glass-effect hover-glow">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-card-foreground">{stat.title}</CardTitle>
                <Icon className={`h-4 w-4 ${stat.color}`} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-card-foreground">{stat.value}</div>
                <div className="flex items-center text-xs text-muted-foreground">
                  <TrendingUp className="h-3 w-3 mr-1 text-green-400" />
                  Dados em tempo real
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Quick Actions */}
      <Card className="glass-effect">
        <CardHeader>
          <CardTitle className="text-card-foreground">Ações Rápidas</CardTitle>
          <CardDescription>Acesse rapidamente as principais funcionalidades do sistema</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Button className="h-20 flex-col gap-2 hover:bg-primary/10 hover:border-primary/50 hover:shadow-lg hover:shadow-primary/20 transition-all duration-300 bg-transparent" variant="outline">
              <Calculator className="h-6 w-6" />
              <span>Calcular Nova Rota</span>
            </Button>
            <Button className="h-20 flex-col gap-2 hover:bg-primary/10 hover:border-primary/50 hover:shadow-lg hover:shadow-primary/20 transition-all duration-300 bg-transparent" variant="outline">
              <History className="h-6 w-6" />
              <span>Ver Histórico</span>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Recent Routes */}
      <Card className="glass-effect">
        <CardHeader>
          <CardTitle className="text-card-foreground">Rotas Recentes</CardTitle>
          <CardDescription>Últimas rotas calculadas no sistema</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentRoutes.length > 0 ? (
              recentRoutes.map((route, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-4 rounded-lg bg-muted/20 border border-border"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center">
                      <Route className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <div className="font-medium text-card-foreground">
                        {route.origem} → {route.destino.split(" [UPLOAD:")[0]}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {route.distancia ? `${formatDistance(route.distancia)}` : 'N/A'} • 
                        {route.pedagios ? ` ${formatCurrency(route.pedagios)}` : ' N/A'} • 
                        {getTimeAgo(route.data_consulta)}
                      </div>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm">
                    Ver Detalhes
                  </Button>
                </div>
              ))
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <Route className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Nenhuma rota calculada ainda</p>
                <p className="text-sm">Comece calculando sua primeira rota!</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
      </div>
    </div>
  )
}
