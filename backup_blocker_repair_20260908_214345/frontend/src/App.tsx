import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import NetworkAnalyzer from "./pages/NetworkAnalyzer";
import VulnerabilityScanner from "./pages/VulnerabilityScanner";
import WebSecurity from "./pages/WebSecurity";
import ThreatIntel from "./pages/ThreatIntel";
import AIChat from "./pages/AIChat";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";
import FileIntegrity from "./pages/security/FileIntegrity";

import ProtectedRoute from "./routes/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public Routes */}
        <Route
          path="/login"
          element={<Login />}
        />

        {/* Protected Application Routes */}
        <Route element={<ProtectedRoute />}>
          <Route
            path="/dashboard"
            element={<Dashboard />}
          />
          <Route
            path="/network"
            element={<NetworkAnalyzer />}
          />
          <Route
            path="/vulnerabilities"
            element={<VulnerabilityScanner />}
          />
          <Route
            path="/web-security"
            element={<WebSecurity />}
          />
          <Route
            path="/threat-intel"
            element={<ThreatIntel />}
          />
          <Route
            path="/ai-assistant"
            element={<AIChat />}
          />
          <Route
            path="/reports"
            element={<Reports />}
          />
          <Route
            path="/settings"
            element={<Settings />}
          />
          <Route
            path="/file-integrity"
            element={<FileIntegrity />}
          />
        </Route>

        {/* Default route handling */}
        <Route
          path="/"
          element={<Navigate to="/dashboard" replace />}
        />

        <Route
          path="*"
          element={<Navigate to="/dashboard" replace />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
