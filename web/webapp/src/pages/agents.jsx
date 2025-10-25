import { useEffect, useState } from "react";
import GroupsRoundedIcon from "@mui/icons-material/GroupsRounded";
import QueryStatsRoundedIcon from "@mui/icons-material/QueryStatsRounded";
import {
  Alert,
  Avatar,
  Card,
  CardContent,
  CardHeader,
  Chip,
  Divider,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import Page from "../components/Page";
import { fetchAgentsConfig, fetchMetrics } from "../api";

export default function Agents() {
  const [agents, setAgents] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const config = await fetchAgentsConfig();
        setAgents(config.agents);
        const metricResponse = await fetchMetrics([0.001, 0.002, -0.0005]);
        setMetrics(metricResponse);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    };
    load();
  }, []);

  return (
    <Page
      title="Agent Ensemble"
      subtitle="Specialised PPO baselines collaborate via shared risk telemetry in paper mode."
    >
      <Stack spacing={3}>
        {error && <Alert severity="error">{error}</Alert>}
        <Card>
          <CardHeader
            avatar={<GroupsRoundedIcon color="primary" />}
            title="Active Policies"
            subheader="Momentum, mean reversion, and volatility overlays"
            action={
              metrics && (
                <Chip
                  icon={<QueryStatsRoundedIcon />}
                  label={`Portfolio Sharpe ${metrics.sharpe.toFixed(2)}`}
                  color="secondary"
                  variant="outlined"
                />
              )
            }
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
                    <TableCell align="right">Last Sharpe</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {agents.map((agent) => (
                    <TableRow key={agent.name} hover>
                      <TableCell>
                        <Stack direction="row" spacing={1.5} alignItems="center">
                          <Avatar sx={{ bgcolor: "primary.main", color: "common.white" }}>
                            {agent.name.slice(0, 2).toUpperCase()}
                          </Avatar>
                          <Stack spacing={0.25}>
                            <Typography fontWeight={600}>{agent.name}</Typography>
                            <Typography variant="caption" color="text.secondary">
                              {agent.description || "Paper-simulated"}
                            </Typography>
                          </Stack>
                        </Stack>
                      </TableCell>
                      <TableCell>{agent.strategy}</TableCell>
                      <TableCell>
                        <Chip label={agent.regime} size="small" color="info" variant="outlined" />
                      </TableCell>
                      <TableCell>{agent.risk_target}</TableCell>
                      <TableCell align="right">
                        {metrics ? metrics.sharpe.toFixed(2) : "—"}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            <Divider sx={{ my: 3, opacity: 0.2 }} />
            <Typography variant="body2" color="text.secondary">
              Policies share feature backbones via Ray RLlib parameter exchange while decisions remain in paper
              execution mode until human promotion.
            </Typography>
          </CardContent>
        </Card>
      </Stack>
    </Page>
  );
}
