import { Box } from "@mui/material";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Nav from "./components/Nav";
import Dashboard from "./pages/dashboard";
import Login from "./pages/login";
import Sandbox from "./pages/sandbox";
import XAI from "./pages/xai";
import Agents from "./pages/agents";
import Environment from "./pages/environment";
import Risk from "./pages/risk";
import Exchanges from "./pages/exchanges";
import Monitoring from "./pages/monitoring";
import Wallet from "./pages/wallet";
import Settings from "./pages/settings";
import Docs from "./pages/docs";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Box sx={{ minHeight: "100vh", bgcolor: "background.default" }}>
        <Nav />
        <Box component="main">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/sandbox" element={<Sandbox />} />
            <Route path="/xai" element={<XAI />} />
            <Route path="/agents" element={<Agents />} />
            <Route path="/environment" element={<Environment />} />
            <Route path="/risk" element={<Risk />} />
            <Route path="/exchanges" element={<Exchanges />} />
            <Route path="/monitoring" element={<Monitoring />} />
            <Route path="/wallet" element={<Wallet />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/docs" element={<Docs />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </Box>
      </Box>
    </BrowserRouter>
  );
}
