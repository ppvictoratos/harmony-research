import { useState } from "react";
import { EvidencePage } from "./components/EvidencePage";
import { Logo } from "./components/Logo";
import { StudiesPage } from "./components/studies/StudiesPage";
import { StudyPage } from "./components/studies/StudyPage";
import { useHashRoute } from "./hooks/useHashRoute";
import { applyTheme, loadTheme, Theme } from "./theme";

function App() {
  const route = useHashRoute();
  const [theme, setTheme] = useState<Theme>(loadTheme);

  const toggleTheme = () => {
    const next = theme === "dark" ? "light" : "dark";
    applyTheme(next);
    setTheme(next);
  };

  return (
    <div className="app">
      <header>
        <div className="brand">
          <Logo size={96} />
          <div>
            <h1>Harmony Research</h1>
            <p className="subtitle">Evidence on music, rhythm and the brain, and tools to run your own study</p>
          </div>
        </div>
        <button type="button" className="theme-toggle" onClick={toggleTheme} aria-label="Toggle light and dark theme">
          {theme === "dark" ? "☀︎ Light" : "☾ Dark"}
        </button>
      </header>

      <nav className="tabs" aria-label="Sections">
        <a href="#/" aria-current={route.page === "evidence" ? "page" : undefined}>
          Evidence
        </a>
        <a href="#/studies" aria-current={route.page !== "evidence" ? "page" : undefined}>
          My studies
        </a>
      </nav>

      {route.page === "evidence" && <EvidencePage />}
      {route.page === "studies" && <StudiesPage />}
      {route.page === "study" && <StudyPage studyId={route.id} />}
    </div>
  );
}

export default App;
