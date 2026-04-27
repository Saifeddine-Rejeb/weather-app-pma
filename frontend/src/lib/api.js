const BASE = import.meta.env.VITE_API_URL || "http://localhost:5000";

async function req(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({ error: "Invalid response" }));
  if (!res.ok) {
    throw new Error(data.error || data.message || `HTTP ${res.status}`);
  }
  return data;
}

// Weather
export const getWeather = (q) => req(`/weather?q=${encodeURIComponent(q)}`);
export const getForecast = (q) => req(`/forecast?q=${encodeURIComponent(q)}`);
export const getAirQuality = (q) => req(`/air-quality?q=${encodeURIComponent(q)}`);

// Extras
export const getYoutube = (q) => req(`/youtube?q=${encodeURIComponent(q)}`);
export const getMaps = (q) => req(`/maps?q=${encodeURIComponent(q)}`);

// Records CRUD
export const getRecords = () => req("/records");
export const getRecord = (id) => req(`/records/${id}`);
export const createRecord = (body) =>
  req("/records", { method: "POST", body: JSON.stringify(body) });
export const updateRecord = (id, body) =>
  req(`/records/${id}`, { method: "PUT", body: JSON.stringify(body) });
export const deleteRecord = (id) =>
  req(`/records/${id}`, { method: "DELETE" });

// Export
export const getExportUrl = (format) => `${BASE}/records/export?format=${format}`;