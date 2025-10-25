import { useEffect, useMemo, useState } from "react";
import AutoAwesomeRoundedIcon from "@mui/icons-material/AutoAwesomeRounded";
import TuneRoundedIcon from "@mui/icons-material/TuneRounded";
import ViewTimelineRoundedIcon from "@mui/icons-material/ViewTimelineRounded";
import {
  Alert,
  Card,
  CardContent,
  CardHeader,
  Chip,
  Divider,
  Grid,
  InputAdornment,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import Page from "../components/Page";
import { fetchAgentsConfig, fetchEnvConfig } from "../api";

export default function Sandbox() {
  const [agents, setAgents] = useState([]);
  const [envConfig, setEnvConfig] = useState(null);
  const [sandboxBalance, setSandboxBalance] = useState(100000);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [agentResponse, envResponse] = await Promise.all([
          fetchAgentsConfig(),
          fetchEnvConfig(),
        ]);
        setAgents(agentResponse.agents);
        setEnvConfig(envResponse);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    };
    load();
  }, []);

  const envDetails = useMemo(() => {
    if (!envConfig) return [];
    return [
      { label: "Data Path", value: envConfig.data_path },
      { label: "Window Size", value: envConfig.window_size },
      { label: "Assets", value: envConfig.assets.join(", ") },
      { label: "Transaction Cost", value: envConfig.transaction_cost },
    ];
  }, [envConfig]);

  return (
    <Page
      title="Paper Sandbox"
      subtitle="Adjust configuration for what-if analysis. All results stay in paper trading mode."
    >
      <Stack spacing={3}>
        {error && <Alert severity="error">{error}</Alert>}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader
                avatar={<ViewTimelineRoundedIcon color="primary" />}
                title="Environment"
                subheader="Gym-style state definition and data sources"
              />
              <CardContent>
                {envConfig ? (
                  <Stack spacing={1.5}>
                    {envDetails.map((detail) => (
                      <Stack key={detail.label} direction="row" justifyContent="space-between">
                        <Typography variant="body2" color="text.secondary">
                          {detail.label}
                        </Typography>
                        <Typography variant="subtitle2" fontWeight={600}>
                          {detail.value}
                        </Typography>
                      </Stack>
                    ))}
                  </Stack>
                ) : (
                  <Typography color="text.secondary">Loading environment…</Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader
                avatar={<TuneRoundedIcon color="secondary" />}
                title="Sandbox Controls"
                subheader="Local-only changes for simulation sensitivity"
              />
              <CardContent>
                <Stack spacing={2}>
                  <TextField
                    type="number"
                    label="Paper Balance"
                    value={sandboxBalance}
                    onChange={(event) => setSandboxBalance(Number(event.target.value))}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                    helperText="Used for local what-if analysis only"
                  />
                  <Chip
                    icon={<AutoAwesomeRoundedIcon />}
                    label="Parameter tweaks do not route live orders"
                    color="success"
                    variant="outlined"
                    sx={{ alignSelf: "flex-start" }}
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
        <Card>
          <CardHeader
            title="Participating Agents"
            subheader="All orders remain virtual until human approval for live deployment"
          />
          <CardContent>
            <TableContainer
              component={Paper}
              sx={(theme) => ({
                borderRadius: 3,
                border: `1px solid ${theme.palette.divider}`,
                boxShadow: "0 16px 36px rgba(15, 23, 42, 0.08)",
                backgroundColor: theme.palette.background.paper,
              })}
            >
              <Table
                size="small"
                sx={{
                  "& thead th": {
                    fontWeight: 600,
                    color: "text.secondary",
                    backgroundColor: "#f9fafb",
                    borderBottom: "1px solid",
                    borderColor: "divider",
                  },
                  "& tbody td": {
                    borderBottomColor: "rgba(15, 23, 42, 0.06)",
                  },
                  "& tbody tr:hover": {
                    backgroundColor: "rgba(17, 24, 39, 0.04)",
                  },
                }}
              >
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>Strategy</TableCell>
                    <TableCell>Regime</TableCell>
                    <TableCell>Risk Target</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {agents.map((agent) => (
                    <TableRow key={agent.name} hover>
                      <TableCell>{agent.name}</TableCell>
                      <TableCell>{agent.strategy}</TableCell>
                      <TableCell>
                        <Chip label={agent.regime} size="small" color="info" variant="outlined" />
                      </TableCell>
                      <TableCell>{agent.risk_target}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <Divider sx={{ mt: 3, opacity: 0.2 }} />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 3 }}>
              Tune signal horizons, balances, and reward weights safely. Updated figures sync with backend configs
              without ever touching live markets.
            </Typography>
          </CardContent>
        </Card>
      </Stack>
    </Page>
  );
}
