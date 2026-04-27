import { useState, useEffect, useCallback } from "react";
import { Plus, Pencil, Trash2, Download, RefreshCw, Loader2, FileJson, FileText, FileSpreadsheet, FileCode } from "lucide-react";
import { getRecords, createRecord, updateRecord, deleteRecord, getExportUrl } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import RecordForm from "@/components/RecordForm";
import ErrorAlert from "@/components/ErrorAlert";

const EXPORT_FORMATS = [
  { value: "json", label: "JSON", icon: FileJson },
  { value: "csv", label: "CSV", icon: FileSpreadsheet },
  { value: "xml", label: "XML", icon: FileCode },
  { value: "markdown", label: "Markdown", icon: FileText },
];

function ConfirmDialog({ open, onOpenChange, onConfirm, loading }) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-sm">
        <DialogHeader>
          <DialogTitle>Delete Record</DialogTitle>
          <DialogDescription>This action cannot be undone.</DialogDescription>
        </DialogHeader>
        <div className="flex justify-end gap-2 mt-4">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={loading}>Cancel</Button>
          <Button variant="destructive" onClick={onConfirm} disabled={loading}>
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Delete"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

export default function RecordsTab() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [formLoading, setFormLoading] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formOpen, setFormOpen] = useState(false);
  const [editRecord, setEditRecord] = useState(null);
  const [deleteId, setDeleteId] = useState(null);
  const [exportFormat, setExportFormat] = useState("json");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getRecords();
      setRecords(Array.isArray(data) ? data : data.records || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleCreate = async (form) => {
    setFormLoading(true);
    try {
      await createRecord(form);
      setFormOpen(false);
      await load();
    } finally {
      setFormLoading(false);
    }
  };

  const handleUpdate = async (form) => {
    setFormLoading(true);
    try {
      await updateRecord(editRecord.id, form);
      setEditRecord(null);
      await load();
    } finally {
      setFormLoading(false);
    }
  };

  const handleDelete = async () => {
    setDeleteLoading(true);
    try {
      await deleteRecord(deleteId);
      setDeleteId(null);
      await load();
    } catch (err) {
      setError(err.message);
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleExport = () => {
    window.open(getExportUrl(exportFormat), "_blank");
  };

  return (
    <div className="space-y-4">
      <ErrorAlert message={error} onDismiss={() => setError(null)} />

      {/* Toolbar */}
      <div className="flex flex-wrap items-center gap-2">
        <Button onClick={() => setFormOpen(true)} size="sm">
          <Plus className="h-4 w-4" /> New Record
        </Button>
        <Button variant="outline" size="sm" onClick={load} disabled={loading}>
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCw className="h-4 w-4" />}
          Refresh
        </Button>
        <div className="flex items-center gap-2 ml-auto">
          <Select value={exportFormat} onValueChange={setExportFormat}>
            <SelectTrigger className="h-8 w-32 text-xs">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {EXPORT_FORMATS.map((f) => (
                <SelectItem key={f.value} value={f.value}>{f.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm" onClick={handleExport}>
            <Download className="h-4 w-4" /> Export
          </Button>
        </div>
      </div>

      {/* Table */}
      {loading && records.length === 0 ? (
        <div className="flex justify-center py-12 text-muted-foreground">
          <Loader2 className="h-6 w-6 animate-spin" />
        </div>
      ) : records.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center text-muted-foreground text-sm">
            No records yet. Create one to get started.
          </CardContent>
        </Card>
      ) : (
        <Card>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-xs text-muted-foreground">
                  <th className="px-4 py-3 font-medium">ID</th>
                  <th className="px-4 py-3 font-medium">Location</th>
                  <th className="px-4 py-3 font-medium">Start</th>
                  <th className="px-4 py-3 font-medium">End</th>
                  <th className="px-4 py-3 font-medium">Temp</th>
                  <th className="px-4 py-3 font-medium">Condition</th>
                  <th className="px-4 py-3 font-medium">Created</th>
                  <th className="px-4 py-3 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {records.map((r) => (
                  <tr key={r.id} className="border-b last:border-0 hover:bg-muted/50 transition-colors">
                    <td className="px-4 py-3 text-muted-foreground">#{r.id}</td>
                    <td className="px-4 py-3 font-medium">{r.location}</td>
                    <td className="px-4 py-3 text-muted-foreground">{r.start_date?.slice(0, 10)}</td>
                    <td className="px-4 py-3 text-muted-foreground">{r.end_date?.slice(0, 10)}</td>
                    <td className="px-4 py-3">
                      {r.temperature != null ? (
                        <span className="text-sm font-medium">{r.temperature}°C</span>
                      ) : (
                        <span className="text-xs text-muted-foreground">—</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-xs text-muted-foreground capitalize">
                      {r.description || "—"}
                    </td>
                    <td className="px-4 py-3 text-muted-foreground text-xs">
                      {r.created_at ? new Date(r.created_at).toLocaleDateString() : "—"}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex justify-end gap-1">
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-7 w-7"
                          onClick={() => setEditRecord(r)}
                        >
                          <Pencil className="h-3.5 w-3.5" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-7 w-7 text-destructive hover:text-destructive"
                          onClick={() => setDeleteId(r.id)}
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Dialogs */}
      <RecordForm
        open={formOpen}
        onOpenChange={setFormOpen}
        onSubmit={handleCreate}
        loading={formLoading}
      />
      <RecordForm
        open={!!editRecord}
        onOpenChange={(o) => !o && setEditRecord(null)}
        onSubmit={handleUpdate}
        initialData={editRecord}
        loading={formLoading}
      />
      <ConfirmDialog
        open={!!deleteId}
        onOpenChange={(o) => !o && setDeleteId(null)}
        onConfirm={handleDelete}
        loading={deleteLoading}
      />
    </div>
  );
}