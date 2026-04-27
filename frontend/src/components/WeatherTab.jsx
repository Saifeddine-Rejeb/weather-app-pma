import { useState, useEffect } from "react";
import { Thermometer, Wind, Droplets, Eye, ArrowUp, ArrowDown, BookmarkPlus, Loader2 } from "lucide-react";
import { getWeather, getForecast, getAirQuality, createRecord } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import LocationSearch from "@/components/LocationSearch";
import ErrorAlert from "@/components/ErrorAlert";

const AQI_COLORS = {
  1: "bg-green-100 text-green-800",
  2: "bg-yellow-100 text-yellow-800",
  3: "bg-orange-100 text-orange-800",
  4: "bg-red-100 text-red-800",
  5: "bg-purple-100 text-purple-800",
};

function WeatherIcon({ code, size = 48 }) {
  return (
    <img
      src={`https://openweathermap.org/img/wn/${code}@2x.png`}
      alt="weather icon"
      width={size}
      height={size}
    />
  );
}

function StatItem({ icon: Icon, label, value }) {
  return (
    <div className="flex items-center gap-2 text-sm">
      <Icon className="h-4 w-4 text-muted-foreground shrink-0" />
      <span className="text-muted-foreground">{label}</span>
      <span className="font-medium ml-auto">{value}</span>
    </div>
  );
}

// forecastDays: array of { date, temp_min, temp_max, description, icon, humidity }
function SaveRecordDialog({ open, onOpenChange, location, forecastDays }) {
  const [selected, setSelected] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saved, setSaved] = useState(false);

  // Reset every time the dialog opens
  useEffect(() => {
    if (open) {
      setSelected(forecastDays.map((d) => d.date));
      setError(null);
      setSaved(false);
    }
  }, [open, forecastDays]);

  const toggle = (date) =>
    setSelected((prev) =>
      prev.includes(date) ? prev.filter((d) => d !== date) : [...prev, date].sort()
    );

  const sortedSelected = [...selected].sort();
  const startDate = sortedSelected[0];
  const endDate = sortedSelected.at(-1);

  const handleSave = async () => {
    if (selected.length === 0) return;
    setError(null);
    setLoading(true);
    try {
      await createRecord({ location, start_date: startDate, end_date: endDate });
      setSaved(true);
      setTimeout(() => {
        setSaved(false);
        onOpenChange(false);
      }, 1200);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-sm bg-white">
        <DialogHeader>
          <DialogTitle>Save Weather Record</DialogTitle>
          <DialogDescription>
            Pick which forecast days to save for <strong>{location}</strong>. The backend will store daily temps for the selected range.
          </DialogDescription>
        </DialogHeader>

        {saved ? (
          <p className="text-center text-sm text-green-600 font-medium py-4">✓ Record saved!</p>
        ) : (
          <div className="space-y-4 mt-2">
            <ErrorAlert message={error} onDismiss={() => setError(null)} />

            <div className="space-y-2">
              {forecastDays.map((day) => {
                const checked = selected.includes(day.date);
                return (
                  <button
                    key={day.date}
                    type="button"
                    onClick={() => toggle(day.date)}
                    className={`w-full flex items-center justify-between rounded-lg border px-4 py-2.5 text-sm transition-colors ${
                      checked
                        ? "border-primary bg-primary/5 text-foreground"
                        : "border-border bg-background text-muted-foreground hover:bg-muted"
                    }`}
                  >
                    <span className="font-medium">
                      {new Date(day.date + "T12:00:00").toLocaleDateString("en-US", {
                        weekday: "short", month: "short", day: "numeric",
                      })}
                    </span>
                    <span className="flex items-center gap-3 text-xs">
                      <span>
                        <span className="text-red-500">{Math.round(day.temp_max)}°</span>
                        {" / "}
                        <span className="text-blue-500">{Math.round(day.temp_min)}°C</span>
                      </span>
                      <span
                        className={`h-4 w-4 rounded border flex items-center justify-center shrink-0 ${
                          checked ? "bg-primary border-primary" : "border-muted-foreground"
                        }`}
                      >
                        {checked && <span className="text-primary-foreground text-[10px] leading-none">✓</span>}
                      </span>
                    </span>
                  </button>
                );
              })}
            </div>

            {selected.length > 0 ? (
              <p className="text-xs text-muted-foreground">
                {selected.length} day{selected.length > 1 ? "s" : ""} selected — {startDate} → {endDate}
              </p>
            ) : (
              <p className="text-xs text-destructive">Select at least one day.</p>
            )}

            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={() => onOpenChange(false)} disabled={loading}>
                Cancel
              </Button>
              <Button onClick={handleSave} disabled={loading || selected.length === 0}>
                {loading
                  ? <Loader2 className="h-4 w-4 animate-spin" />
                  : `Save ${selected.length} Day${selected.length !== 1 ? "s" : ""}`}
              </Button>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}

export default function WeatherTab({ onLocationChange, persistedState, onPersistState }) {
  const [weather, setWeather] = useState(() => persistedState?.weather ?? null);
  const [forecast, setForecast] = useState(() => persistedState?.forecast ?? null);
  const [airQuality, setAirQuality] = useState(() => persistedState?.airQuality ?? null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(() => persistedState?.error ?? null);
  const [saveOpen, setSaveOpen] = useState(false);
  const [currentQuery, setCurrentQuery] = useState(() => persistedState?.currentQuery ?? "");

  useEffect(() => {
    onPersistState?.({
      weather,
      forecast,
      airQuality,
      currentQuery,
      error,
    });
  }, [weather, forecast, airQuality, currentQuery, error, onPersistState]);

  const handleSearch = async (q) => {
    setLoading(true);
    setError(null);
    setWeather(null);
    setForecast(null);
    setAirQuality(null);
    setCurrentQuery(q);
    try {
      const [w, f, a] = await Promise.allSettled([
        getWeather(q),
        getForecast(q),
        getAirQuality(q),
      ]);
      if (w.status === "fulfilled") {
        setWeather(w.value);
        onLocationChange?.(w.value.city || q);
      } else {
        throw new Error(w.reason?.message || "Weather fetch failed");
      }
      if (f.status === "fulfilled") setForecast(f.value);
      if (a.status === "fulfilled") setAirQuality(a.value);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const forecastDays = forecast?.forecast || [];

  return (
    <div className="space-y-6">
      <LocationSearch onSearch={handleSearch} loading={loading} />
      <ErrorAlert message={error} onDismiss={() => setError(null)} />

      {weather && (
        <div className="grid gap-4 md:grid-cols-2">
          {/* Current Weather */}
          <Card>
            <CardHeader className="pb-2">
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-xl">
                    {weather.city}{weather.country ? `, ${weather.country}` : ""}
                  </CardTitle>
                  <p className="text-sm text-muted-foreground capitalize mt-1">
                    {weather.description}
                  </p>
                </div>
                {weather.icon && <WeatherIcon code={weather.icon} size={56} />}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-end gap-2">
                <span className="text-5xl font-bold">{Math.round(weather.temperature)}°C</span>
                <span className="text-muted-foreground text-sm mb-2">
                  Feels like {Math.round(weather.feels_like)}°C
                </span>
              </div>
              <div className="flex gap-3 text-sm text-muted-foreground">
                <span className="flex items-center gap-1">
                  <ArrowUp className="h-3 w-3 text-red-400" />{Math.round(weather.temp_max)}°
                </span>
                <span className="flex items-center gap-1">
                  <ArrowDown className="h-3 w-3 text-blue-400" />{Math.round(weather.temp_min)}°
                </span>
              </div>
              <div className="space-y-2 pt-2 border-t">
                <StatItem icon={Droplets} label="Humidity" value={`${weather.humidity}%`} />
                <StatItem icon={Wind} label="Wind" value={`${weather.wind_speed} m/s`} />
                <StatItem icon={Eye} label="Visibility" value={`${((weather.visibility || 0) / 1000).toFixed(1)} km`} />
                <StatItem icon={Thermometer} label="Coordinates" value={`${weather.lat?.toFixed(2)}, ${weather.lon?.toFixed(2)}`} />
              </div>
              <Button
                variant="outline"
                size="sm"
                className="w-full mt-2"
                onClick={() => setSaveOpen(true)}
                disabled={forecastDays.length === 0}
              >
                <BookmarkPlus className="h-4 w-4" />
                Save as Record
              </Button>
            </CardContent>
          </Card>

          {/* Air Quality */}
          {airQuality && (
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Air Quality</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${AQI_COLORS[airQuality.aqi] || "bg-muted text-muted-foreground"}`}>
                    {airQuality.aqi_label}
                  </span>
                  <span className="text-muted-foreground text-sm">AQI {airQuality.aqi}/5</span>
                </div>
                {airQuality.components && (
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    {Object.entries(airQuality.components).map(([key, val]) => (
                      <div key={key} className="flex justify-between rounded-md bg-muted px-3 py-1.5">
                        <span className="text-muted-foreground uppercase text-xs">{key}</span>
                        <span className="font-medium">{Number(val).toFixed(1)}</span>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* 5-Day Forecast */}
      {forecastDays.length > 0 && (
        <div>
          <h3 className="text-sm font-medium text-muted-foreground mb-3">5-Day Forecast</h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
            {forecastDays.map((day) => (
              <Card key={day.date} className="text-center">
                <CardContent className="p-3 space-y-1">
                  <p className="text-xs font-medium">
                    {new Date(day.date + "T12:00:00").toLocaleDateString("en-US", {
                      weekday: "short", month: "short", day: "numeric",
                    })}
                  </p>
                  {day.icon && <WeatherIcon code={day.icon} size={36} />}
                  <p className="text-xs text-muted-foreground capitalize">{day.description}</p>
                  <div className="flex justify-center gap-2 text-sm">
                    <span className="font-semibold text-red-500">{Math.round(day.temp_max)}°</span>
                    <span className="text-muted-foreground">{Math.round(day.temp_min)}°</span>
                  </div>
                  <p className="text-xs text-muted-foreground">{day.humidity}% hum.</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      <SaveRecordDialog
        open={saveOpen}
        onOpenChange={setSaveOpen}
        location={weather?.city || currentQuery}
        forecastDays={forecastDays}
      />
    </div>
  );
}