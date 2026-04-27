import { useState } from "react";
import { Cloud } from "lucide-react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import WeatherTab from "@/components/WeatherTab";
import ExploreTab from "@/components/ExploreTab";
import RecordsTab from "@/components/RecordsTab";
import pmaLogo from "@/assets/pma.png";

export default function App() {
  const [sharedLocation, setSharedLocation] = useState("");
  const [weatherState, setWeatherState] = useState({
    weather: null,
    forecast: null,
    airQuality: null,
    currentQuery: "",
    error: null,
  });
  const [exploreState, setExploreState] = useState({
    videos: [],
    mapData: null,
    lastSearched: "",
    error: null,
  });

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="bg-primary rounded-lg p-1.5">
              <Cloud className="h-5 w-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="font-semibold text-sm leading-none">WeatherApp</h1>
              <p className="text-xs text-muted-foreground mt-0.5">by Saifeddine Rejeb</p>
            </div>
          </div>
          <a
            href="https://www.pmaccelerator.io"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-muted-foreground hover:text-foreground transition-colors hidden sm:flex items-center gap-2"
          >
            <img
              src={pmaLogo}
              alt="PM Accelerator logo"
              className="h-6 w-auto bg-white rounded-sm p-0.5"
            />
            <span>PM Accelerator ↗</span>
          </a>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-5xl mx-auto px-4 py-6 flex-1 w-full">
        <Tabs defaultValue="weather">
          <TabsList className="mb-6">
            <TabsTrigger value="weather">🌤 Weather</TabsTrigger>
            <TabsTrigger value="explore">🗺 Explore</TabsTrigger>
            <TabsTrigger value="records">🗃 Records</TabsTrigger>
          </TabsList>

          <TabsContent value="weather">
            <WeatherTab
              onLocationChange={setSharedLocation}
              persistedState={weatherState}
              onPersistState={setWeatherState}
            />
          </TabsContent>

          <TabsContent value="explore">
            <ExploreTab
              initialLocation={sharedLocation}
              persistedState={exploreState}
              onPersistState={setExploreState}
            />
          </TabsContent>

          <TabsContent value="records">
            <RecordsTab />
          </TabsContent>
        </Tabs>
      </main>

      <section className="max-w-5xl mx-auto w-full px-4 pb-3">
        <div className="rounded-md border bg-card px-3 py-2">
          <h2 className="text-xs font-semibold">PM Accelerator</h2>
          <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
            The Product Manager Accelerator Program is designed to support PM professionals through every stage
            of their careers. From students looking for entry-level jobs to Directors looking to take on a
            leadership role, the program has helped hundreds of students fulfill their career aspirations.
            Learn more at{" "}
            <a
              href="https://www.pmaccelerator.io"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline font-medium"
            >
              pmaccelerator.io
            </a>
            .
          </p>
        </div>
      </section>

      <Separator />
      <footer className="text-center py-4 text-xs text-muted-foreground">
        Weather data from OpenWeatherMap · Built with React + Flask
      </footer>
    </div>
  );
}