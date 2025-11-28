import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import App from "./App";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import LandingPage from "./pages/LandingPage";

const rootElement = document.getElementById("root") as HTMLElement;

const Root = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route path="/" element={<App />}>
        <Route index element={<LandingPage />} />
        <Route path="dashboard" element={<DashboardPage />} />
      </Route>
    </Routes>
  </BrowserRouter>
);

ReactDOM.createRoot(rootElement).render(
    <Root />
);
