const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export interface RouteRequest {
  origem: string
  destino: string
}

export interface RouteMultipleRequest {
  origem: string
  destinos: string[]
}

export interface RouteResponse {
  origem: string
  destino: string
  distance: number | string
  pedagios: number | string
  tempo_estimado?: number
  combustivel_estimado?: number
}

export interface RouteBatchResponse {
  resultados: RouteResponse[]
}

export interface UploadResponse {
  upload_id: string
  status: string
  total_rotas: number
  message: string
}

export interface UploadStatus {
  status: 'processing' | 'completed' | 'error'
  total_rotas: number
  rotas_processadas: number
  rotas_com_erro: number
  progresso: number
  inicio: string
  fim?: string
  erro?: string
}

export interface HistoryResponse {
  id: number
  origem: string
  destino: string
  distancia: number | null
  pedagios: number | null
  data_consulta: string
  ip_address: string
  tipo_consulta: string
}

export interface SuggestionResponse {
  nome: string
  endereco_completo: string
  latitude: number
  longitude: number
}

export interface Grupo {
  id: number
  nome: string
  descricao?: string
  data_criacao: string
  total_rotas: number
  total_distancia: number
  total_pedagios: number
  status: string
}

export interface GrupoCreate {
  nome: string
  descricao?: string
}

export interface GrupoStats {
  total_grupos: number
  total_rotas: number
  total_distancia: number
  total_pedagios: number
  grupos_ativos: number
}

export interface GrupoRotas {
  grupo: Grupo
  rotas: Array<{
    id: number
    origem: string
    destino: string
    distancia: number
    pedagios: number
    data_consulta: string
  }>
  total_rotas: number
}

export interface UploadError {
  id: number
  upload_id: string
  grupo_id: number
  planilha_id?: string
  linha_index: number
  origem_original: string
  destino_original: string
  origem_corrigida?: string
  destino_corrigido?: string
  tipo_erro: string
  mensagem_erro?: string
  status: string
  criado_em: string
  processado_em?: string
}

export interface UploadErrorUpdate {
  origem_corrigida?: string
  destino_corrigido?: string
  status?: string
}

export interface ReprocessErrorRequest {
  origem_corrigida: string
  destino_corrigido: string
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    }

    const response = await fetch(url, { ...defaultOptions, ...options })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`API Error: ${response.status} - ${errorText}`)
    }

    return response.json()
  }

  // Calcular rota individual
  async calculateRoute(data: RouteRequest): Promise<RouteResponse> {
    return this.request<RouteResponse>('/routes/calculate', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  // Calcular rota com múltiplos destinos
  async calculateMultipleRoute(data: RouteMultipleRequest): Promise<RouteResponse> {
    return this.request<RouteResponse>('/routes/calculate-multiple', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  // Upload de planilha Excel
  async uploadExcel(file: File): Promise<UploadResponse> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${this.baseUrl}/routes/upload`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`API Error: ${response.status} - ${errorText}`)
    }

    return response.json()
  }

  // Buscar sugestões de cidades
  async getCitySuggestions(termo: string): Promise<SuggestionResponse[]> {
    return this.request<SuggestionResponse[]>(`/suggestions?termo=${encodeURIComponent(termo)}`)
  }

  // Buscar histórico de consultas
  async getHistory(): Promise<HistoryResponse[]> {
    const response = await this.request<{consultas: HistoryResponse[], total: number, page: number, size: number}>('/history')
    return response.consultas
  }

  // Buscar grupos
  async getGroups(): Promise<{ grupos: Grupo[]; total: number }> {
    return this.request<{ grupos: Grupo[]; total: number }>('/groups')
  }

  // Buscar estatísticas dos grupos
  async getGroupsStats(): Promise<GrupoStats> {
    return this.request<GrupoStats>('/groups/stats')
  }

  // Criar grupo
  async createGroup(data: GrupoCreate): Promise<Grupo> {
    return this.request<Grupo>('/groups', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  // Buscar grupo específico
  async getGroup(id: number): Promise<Grupo> {
    return this.request<Grupo>(`/groups/${id}`)
  }

  // Buscar rotas de um grupo
  async getGroupRoutes(id: number): Promise<GrupoRotas> {
    return this.request<GrupoRotas>(`/groups/${id}/rotas`)
  }

  // Atualizar grupo
  async updateGroup(id: number, data: Partial<GrupoCreate>): Promise<Grupo> {
    return this.request<Grupo>(`/groups/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  // Deletar grupo
  async deleteGroup(id: number): Promise<void> {
    return this.request<void>(`/groups/${id}`, {
      method: 'DELETE',
    })
  }

  // Upload de planilha Excel com grupo
  async uploadExcelWithGroup(file: File, grupoId?: number): Promise<UploadResponse> {
    const formData = new FormData()
    formData.append('file', file)

    // Construir URL com parâmetros de query
    let url = `${this.baseUrl}/routes/upload`
    if (grupoId) {
      url += `?grupo_id=${grupoId}`
    }

    const response = await fetch(url, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`API Error: ${response.status} - ${errorText}`)
    }

    return response.json()
  }

  // Verificar status de upload
  async getUploadStatus(uploadId: string): Promise<UploadStatus> {
    return this.request<UploadStatus>(`/routes/upload-status/${uploadId}`)
  }

  // Listar todos os uploads em processamento
  async getAllUploadStatus(): Promise<{ uploads: Record<string, UploadStatus>; total: number }> {
    return this.request<{ uploads: Record<string, UploadStatus>; total: number }>('/routes/upload-status')
  }

  // Buscar erros de um grupo
  async getGroupErrors(grupoId: number): Promise<UploadError[]> {
    return this.request<UploadError[]>(`/groups/${grupoId}/errors`)
  }

  // Atualizar erro de upload
  async updateUploadError(grupoId: number, errorId: number, data: UploadErrorUpdate): Promise<UploadError> {
    return this.request<UploadError>(`/groups/${grupoId}/errors/${errorId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  // Reprocessar erro de upload
  async reprocessUploadError(grupoId: number, errorId: number, data: ReprocessErrorRequest): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/groups/${grupoId}/errors/${errorId}/reprocess`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  // Excluir erro de upload
  async deleteUploadError(grupoId: number, errorId: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/groups/${grupoId}/errors/${errorId}`, {
      method: 'DELETE',
    })
  }
}

export const apiClient = new ApiClient()
export default apiClient
