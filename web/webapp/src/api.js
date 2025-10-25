import { authFetch } from "./auth";

export async function login(username, password, role) {
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);
  params.append("grant_type", "password");
  if (role) {
    params.append("scope", role);
  }
  const response = await fetch("/api/auth/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: params,
  });
  if (!response.ok) {
    throw new Error("Authentication failed");
  }
  return response.json();
}

export async function fetchMetrics(returns = []) {
  const response = await authFetch("/api/metrics/portfolio", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ returns }),
  });
  if (!response.ok) throw new Error("Metrics request failed");
  return response.json();
}

export async function fetchRiskLimits() {
  const response = await authFetch("/api/risk/limits");
  if (!response.ok) throw new Error("Risk limits request failed");
  return response.json();
}

export async function fetchAgentsConfig() {
  const response = await authFetch("/api/agents/config");
  if (!response.ok) throw new Error("Agents config request failed");
  return response.json();
}

export async function fetchEnvConfig() {
  const response = await authFetch("/api/envs/default");
  if (!response.ok) throw new Error("Env config request failed");
  return response.json();
}

export async function fetchShap() {
  const response = await authFetch("/api/explain/shap");
  if (!response.ok) throw new Error("Explainability request failed");
  return response.json();
}

export async function fetchRegime() {
  const response = await authFetch("/api/regime/current");
  if (!response.ok) throw new Error("Regime request failed");
  return response.json();
}

export async function fetchBusStatus() {
  const response = await authFetch("/api/bus/status");
  if (!response.ok) throw new Error("Bus status request failed");
  return response.json();
}

export async function fetchWalletStatus() {
  const response = await authFetch("/api/wallet/status");
  if (!response.ok) throw new Error("Wallet status request failed");
  return response.json();
}

export async function fetchExchanges() {
  const response = await authFetch("/api/exchanges/");
  if (!response.ok) throw new Error("Exchanges request failed");
  const exchanges = await response.json();
  const statuses = await Promise.all(
    exchanges.map(async (name) => {
      const statusResponse = await authFetch(`/api/exchanges/${name}/status`);
      if (statusResponse.ok) {
        return await statusResponse.json();
      }
      return { exchange: name, status: "offline", mode: "paper" };
    })
  );
  return statuses;
}

export async function activateFailSafe(reason) {
  const response = await authFetch("/api/fail-safe/activate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ reason }),
  });
  if (!response.ok) throw new Error("Fail-safe activation failed");
  return response.json();
}

export async function fetchFailSafeStatus() {
  const response = await authFetch("/api/fail-safe/status");
  if (!response.ok) throw new Error("Fail-safe status failed");
  return response.json();
}

export async function fetchPrometheusMetrics() {
  const response = await authFetch("/metrics");
  if (!response.ok) throw new Error("Metrics endpoint failed");
  return response.text();
}

export async function fetchDocs() {
  const [agents, readme] = await Promise.all([
    fetch("/AGENTS.md").then((res) => res.text()),
    fetch("/README.md").then((res) => res.text()),
  ]);
  return { agents, readme };
}
