import { useState, useEffect } from "react";
import { PlayCircle, Map, ExternalLink } from "lucide-react";
import { getYoutube, getMaps } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import LocationSearch from "@/components/LocationSearch";
import ErrorAlert from "@/components/ErrorAlert";

export default function ExploreTab({ initialLocation, persistedState, onPersistState }) {
  const [videos, setVideos] = useState(() => persistedState?.videos ?? []);
  const [mapData, setMapData] = useState(() => persistedState?.mapData ?? null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(() => persistedState?.error ?? null);
  const [lastSearched, setLastSearched] = useState(() => persistedState?.lastSearched ?? "");

  useEffect(() => {
    onPersistState?.({ videos, mapData, lastSearched, error });
  }, [videos, mapData, lastSearched, error, onPersistState]);

  const handleSearch = async (q) => {
    if (!q || q === lastSearched) return;
    setLastSearched(q);
    setLoading(true);
    setError(null);
    setVideos([]);
    setMapData(null);
    try {
      const [yt, maps] = await Promise.allSettled([getYoutube(q), getMaps(q)]);
      if (yt.status === "fulfilled") setVideos(yt.value.videos || []);
      if (maps.status === "fulfilled") setMapData(maps.value);
      if (yt.status === "rejected" && maps.status === "rejected") {
        throw new Error(yt.reason?.message || "Explore fetch failed");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Auto-search when coming from WeatherTab
  useEffect(() => {
    if (initialLocation && initialLocation !== lastSearched) {
      handleSearch(initialLocation);
    }
  }, [initialLocation, lastSearched]);

  return (
    <div className="space-y-6">
      <LocationSearch
        onSearch={handleSearch}
        loading={loading}
        placeholder="Search a location to explore…"
      />
      <ErrorAlert message={error} onDismiss={() => setError(null)} />

      {mapData && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base flex items-center gap-2">
              <Map className="h-4 w-4" /> Location
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            {mapData.name && (
              <p className="font-medium text-base">{mapData.name}</p>
            )}
            {mapData.address && (
              <p className="text-muted-foreground">{mapData.address}</p>
            )}
            {mapData.lat && mapData.lng && (
              <p className="text-xs text-muted-foreground">
                {mapData.lat.toFixed(4)}, {mapData.lng.toFixed(4)}
              </p>
            )}
            {/* Static map thumbnail via OpenStreetMap — no API key needed */}
            {mapData.lat && mapData.lng && (
              <div className="mt-2 rounded-lg overflow-hidden border">
                <img
                  src={`https://static-maps.yandex.ru/1.x/?lang=en_US&ll=${mapData.lng},${mapData.lat}&z=12&l=map&size=650,300`}
                  alt={`Map of ${mapData.name}`}
                  className="w-full object-cover"
                  onError={(e) => { e.target.style.display = "none"; }}
                />
              </div>
            )}
            {mapData.maps_url && (
              <Button variant="outline" size="sm" asChild>
                <a href={mapData.maps_url} target="_blank" rel="noopener noreferrer">
                  <ExternalLink className="h-3.5 w-3.5" />
                  Open in Google Maps
                </a>
              </Button>
            )}
          </CardContent>
        </Card>
      )}

      {videos.length > 0 && (
        <div>
          <h3 className="text-sm font-medium text-muted-foreground mb-3 flex items-center gap-2">
            <PlayCircle className="h-4 w-4 text-red-500" /> Related Videos
          </h3>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {videos.slice(0, 6).map((video) => {
              const id = video.video_id;
              if (!id) return null;
              return (
                <Card key={id} className="overflow-hidden group">
                  <a href={video.url} target="_blank" rel="noopener noreferrer">
                    <div className="aspect-video relative overflow-hidden">
                      <img
                        src={video.thumbnail}
                        alt={video.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                      />
                      <div className="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors flex items-center justify-center">
                        <div className="bg-red-600 rounded-full p-2 opacity-90">
                          <PlayCircle className="h-5 w-5 text-white fill-white" />
                        </div>
                      </div>
                    </div>
                    <CardContent className="p-3">
                      <p className="text-sm font-medium line-clamp-2 group-hover:text-primary transition-colors">
                        {video.title}
                      </p>
                      {video.channel && (
                        <p className="text-xs text-muted-foreground mt-1">{video.channel}</p>
                      )}
                    </CardContent>
                  </a>
                </Card>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}