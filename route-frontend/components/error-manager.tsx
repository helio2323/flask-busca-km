"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { RefreshCw, Edit, Trash2, CheckCircle, XCircle, AlertCircle, RotateCcw } from 'lucide-react';
import { toast } from 'sonner';

interface UploadError {
  id: number;
  upload_id: string;
  grupo_id: number;
  planilha_id?: string;
  linha_index: number;
  origem_original: string;
  destino_original: string;
  origem_corrigida?: string;
  destino_corrigido?: string;
  tipo_erro: string;
  mensagem_erro?: string;
  status: 'pendente' | 'processando' | 'sucesso' | 'erro';
  criado_em: string;
  processado_em?: string;
}

interface ErrorManagerProps {
  grupoId: number;
  grupoNome: string;
}

export function ErrorManager({ grupoId, grupoNome }: ErrorManagerProps) {
  const [errors, setErrors] = useState<UploadError[]>([]);
  const [loading, setLoading] = useState(false);
  const [editingError, setEditingError] = useState<UploadError | null>(null);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isReprocessDialogOpen, setIsReprocessDialogOpen] = useState(false);
  const [origemCorrigida, setOrigemCorrigida] = useState('');
  const [destinoCorrigido, setDestinoCorrigido] = useState('');
  const [reprocessing, setReprocessing] = useState(false);

  const loadErrors = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:50001/api/v1'}/groups/${grupoId}/errors`);
      if (response.ok) {
        const data = await response.json();
        setErrors(data);
      } else {
        toast.error('Erro ao carregar erros');
      }
    } catch (error) {
      console.error('Erro ao carregar erros:', error);
      toast.error('Erro ao carregar erros');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadErrors();
  }, [grupoId]);

  const handleEditError = (error: UploadError) => {
    setEditingError(error);
    setOrigemCorrigida(error.origem_corrigida || error.origem_original);
    setDestinoCorrigido(error.destino_corrigido || error.destino_original);
    setIsEditDialogOpen(true);
  };

  const handleReprocessError = (error: UploadError) => {
    setEditingError(error);
    setOrigemCorrigida(error.origem_corrigida || error.origem_original);
    setDestinoCorrigido(error.destino_corrigido || error.destino_original);
    setIsReprocessDialogOpen(true);
  };

  const saveErrorEdit = async () => {
    if (!editingError) return;

    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/groups/${grupoId}/errors/${editingError.id}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            origem_corrigida: origemCorrigida,
            destino_corrigido: destinoCorrigido,
          }),
        }
      );

      if (response.ok) {
        toast.success('Erro atualizado com sucesso');
        setIsEditDialogOpen(false);
        loadErrors();
      } else {
        toast.error('Erro ao atualizar');
      }
    } catch (error) {
      console.error('Erro ao atualizar:', error);
      toast.error('Erro ao atualizar');
    }
  };

  const reprocessError = async () => {
    if (!editingError) return;

    try {
      setReprocessing(true);
      const response = await fetch(
        `http://localhost:8000/api/v1/groups/${grupoId}/errors/${editingError.id}/reprocess`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            origem_corrigida: origemCorrigida,
            destino_corrigido: destinoCorrigido,
          }),
        }
      );

      const result = await response.json();
      
      if (response.ok && result.success) {
        toast.success('Erro reprocessado com sucesso!');
        setIsReprocessDialogOpen(false);
        loadErrors();
      } else {
        toast.error(result.message || 'Erro ao reprocessar');
      }
    } catch (error) {
      console.error('Erro ao reprocessar:', error);
      toast.error('Erro ao reprocessar');
    } finally {
      setReprocessing(false);
    }
  };

  const deleteError = async (errorId: number) => {
    if (!confirm('Tem certeza que deseja excluir este erro?')) return;

    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/groups/${grupoId}/errors/${errorId}`,
        {
          method: 'DELETE',
        }
      );

      if (response.ok) {
        toast.success('Erro excluído com sucesso');
        loadErrors();
      } else {
        toast.error('Erro ao excluir');
      }
    } catch (error) {
      console.error('Erro ao excluir:', error);
      toast.error('Erro ao excluir');
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'sucesso':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'erro':
        return <XCircle className="w-4 h-4 text-red-500" />;
      case 'processando':
        return <RefreshCw className="w-4 h-4 text-blue-500 animate-spin" />;
      default:
        return <AlertCircle className="w-4 h-4 text-yellow-500" />;
    }
  };

  const getStatusBadge = (status: string) => {
    const variants = {
      sucesso: 'default',
      erro: 'destructive',
      processando: 'secondary',
      pendente: 'outline',
    } as const;

    return (
      <Badge variant={variants[status as keyof typeof variants] || 'outline'}>
        {status}
      </Badge>
    );
  };

  const getTipoErroLabel = (tipo: string) => {
    const labels = {
      dados_invalidos: 'Dados Inválidos',
      api_error: 'Erro da API',
      resultado_invalido: 'Resultado Inválido',
      timeout: 'Timeout',
    };
    return labels[tipo as keyof typeof labels] || tipo;
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Gerenciar Erros de Upload</CardTitle>
          <CardDescription>Carregando erros...</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  if (errors.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Gerenciar Erros de Upload</CardTitle>
          <CardDescription>Nenhum erro encontrado para este grupo</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>Gerenciar Erros de Upload</CardTitle>
            <CardDescription>
              {errors.length} erro(s) encontrado(s) no grupo "{grupoNome}"
            </CardDescription>
          </div>
          <Button onClick={loadErrors} variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Atualizar
          </Button>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Tipo</TableHead>
                <TableHead>Origem</TableHead>
                <TableHead>Destino</TableHead>
                <TableHead>Mensagem</TableHead>
                <TableHead>Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {errors.map((error) => (
                <TableRow key={error.id}>
                  <TableCell className="font-mono text-sm">
                    {error.planilha_id || `L${error.linha_index + 1}`}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      {getStatusIcon(error.status)}
                      {getStatusBadge(error.status)}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">
                      {getTipoErroLabel(error.tipo_erro)}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="text-sm font-medium">
                        {error.origem_corrigida || error.origem_original}
                      </div>
                      {error.origem_corrigida && error.origem_corrigida !== error.origem_original && (
                        <div className="text-xs text-muted-foreground">
                          Original: {error.origem_original}
                        </div>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="text-sm font-medium">
                        {error.destino_corrigido || error.destino_original}
                      </div>
                      {error.destino_corrigido && error.destino_corrigido !== error.destino_original && (
                        <div className="text-xs text-muted-foreground">
                          Original: {error.destino_original}
                        </div>
                      )}
                    </div>
                  </TableCell>
                  <TableCell className="max-w-xs">
                    <div className="truncate text-sm text-muted-foreground">
                      {error.mensagem_erro || 'N/A'}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleEditError(error)}
                        disabled={error.status === 'processando'}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleReprocessError(error)}
                        disabled={error.status === 'processando' || error.status === 'sucesso'}
                      >
                        <RotateCcw className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => deleteError(error.id)}
                        disabled={error.status === 'processando'}
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Dialog para editar erro */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Editar Erro</DialogTitle>
            <DialogDescription>
              Corrija a origem e destino para este erro
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
              Salvar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Dialog para reprocessar erro */}
      <Dialog open={isReprocessDialogOpen} onOpenChange={setIsReprocessDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Reprocessar Erro</DialogTitle>
            <DialogDescription>
              Processe novamente este erro com origem e destino corrigidos
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                Esta ação irá processar a rota novamente e, se bem-sucedida, 
                adicionará o resultado ao histórico do grupo.
              </AlertDescription>
            </Alert>
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
                  Processando...
                </>
              ) : (
                <>
                  <RotateCcw className="w-4 h-4 mr-2" />
                  Reprocessar
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
