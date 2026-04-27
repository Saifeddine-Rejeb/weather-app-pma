import { useState } from "react";
import { Search, Loader2, LocateFixed } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function LocationSearch({ onSearch, loading, placeholder = "City, zip code, coordinates, or landmark…" }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) onSearch(query.trim());
  };

  const handleGeolocate = () => {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const q = `${pos.coords.latitude},${pos.coords.longitude}`;
        setQuery(q);
        onSearch(q);
      },
      () => alert("Could not get your location.")
    );
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <div className="relative flex-1">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          className="pl-9"
          disabled={loading}
        />
      </div>
      <Button type="button" variant="outline" size="icon" onClick={handleGeolocate} disabled={loading} title="Use my location">
        <LocateFixed className="h-4 w-4" />
      </Button>
      <Button type="submit" disabled={loading || !query.trim()}>
        {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Search"}
      </Button>
    </form>
  );
}