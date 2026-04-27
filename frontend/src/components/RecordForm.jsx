import { useState, useEffect } from "react";
import { Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import ErrorAlert from "@/components/ErrorAlert";

export default function RecordForm({ open, onOpenChange, onSubmit, initialData, loading }) {
  const [form, setForm] = useState({ location: "", start_date: "", end_date: "" });
  const [error, setError] = useState(null);

  useEffect(() => {
    if (initialData) {
      setForm({
        location: initialData.location || "",
        start_date: initialData.start_date?.slice(0, 10) || "",
        end_date: initialData.end_date?.slice(0, 10) || "",
      });
    } else {
      setForm({ location: "", start_date: "", end_date: "" });
    }
    setError(null);
  }, [initialData, open]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await onSubmit(form);
    } catch (err) {
      setError(err.message);
    }
  };

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="bg-white">
        <DialogHeader>
          <DialogTitle>{initialData ? "Edit Record" : "New Record"}</DialogTitle>
          <DialogDescription>
            Enter a location and date range to fetch and store weather data.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4 mt-2">
          <ErrorAlert message={error} onDismiss={() => setError(null)} />
          <div className="space-y-1.5">
            <Label htmlFor="location">Location</Label>
            <Input
              id="location"
              value={form.location}
              onChange={set("location")}
              placeholder="Paris, 75001, 48.8566,2.3522…"
              required
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <Label htmlFor="start_date">Start Date</Label>
              <Input
                id="start_date"
                type="date"
                value={form.start_date}
                onChange={set("start_date")}
                required
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="end_date">End Date</Label>
              <Input
                id="end_date"
                type="date"
                value={form.end_date}
                onChange={set("end_date")}
                required
              />
            </div>
          </div>
          <div className="flex justify-end gap-2 pt-2">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)} disabled={loading}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : initialData ? "Save Changes" : "Create"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}